from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class SLIType(Enum):
    AVAILABILITY = "availability"
    LATENCY = "latency"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"


@dataclass
class SLI:
    name: str
    sli_type: SLIType
    description: str
    query: str  # How to calculate
    unit: str = ""


@dataclass
class SLO:
    name: str
    sli: SLI
    target: float  # e.g., 99.9 for 99.9%
    time_window_days: int = 30
    error_budget_percentage: float = 0.1  # 100 - target

    @property
    def error_budget(self) -> float:
        return 100.0 - self.target


@dataclass
class SLOStatus:
    slo_name: str
    current_value: float
    target: float
    error_budget_remaining: float
    error_budget_consumed: float
    burn_rate: float  # How fast we're consuming error budget
    status: str  # healthy, at_risk, breached


class SLOTracker:
    def __init__(self):
        self.slos: Dict[str, SLO] = {}
        self.sli_values: Dict[str, List[tuple]] = defaultdict(list)  # (timestamp, value)
        self._setup_default_slos()

    def _setup_default_slos(self):
        # Availability SLO
        availability_sli = SLI(
            name="availability",
            sli_type=SLIType.AVAILABILITY,
            description="Percentage of successful requests",
            query="successful_requests / total_requests * 100",
            unit="%",
        )
        self.slos["availability"] = SLO(
            name="availability",
            sli=availability_sli,
            target=99.9,
            time_window_days=30,
        )

        # Latency SLO
        latency_sli = SLI(
            name="latency_p99",
            sli_type=SLIType.LATENCY,
            description="P99 latency under 500ms",
            query="percentile(latency, 99)",
            unit="ms",
        )
        self.slos["latency_p99"] = SLO(
            name="latency_p99",
            sli=latency_sli,
            target=500,
            time_window_days=30,
        )

        # Error Rate SLO
        error_sli = SLI(
            name="error_rate",
            sli_type=SLIType.ERROR_RATE,
            description="Error rate below 1%",
            query="error_requests / total_requests * 100",
            unit="%",
        )
        self.slos["error_rate"] = SLO(
            name="error_rate",
            sli=error_sli,
            target=1.0,
            time_window_days=30,
        )

    def add_slo(self, slo: SLO):
        self.slos[slo.name] = slo

    def record_sli_value(self, sli_name: str, value: float, timestamp: datetime = None):
        timestamp = timestamp or datetime.utcnow()
        self.sli_values[sli_name].append((timestamp, value))

    def get_slo_status(self, slo_name: str) -> Optional[SLOStatus]:
        slo = self.slos.get(slo_name)
        if not slo:
            return None

        values = self.sli_values.get(slo.sli.name, [])
        if not values:
            return SLOStatus(
                slo_name=slo_name,
                current_value=0,
                target=slo.target,
                error_budget_remaining=slo.error_budget,
                error_budget_consumed=0,
                burn_rate=0,
                status="no_data",
            )

        # Calculate current value (average over time window)
        cutoff = datetime.utcnow() - timedelta(days=slo.time_window_days)
        recent_values = [(ts, v) for ts, v in values if ts > cutoff]
        
        if not recent_values:
            current_value = 0
        else:
            current_value = sum(v for _, v in recent_values) / len(recent_values)

        # Calculate error budget
        if slo.sli.sli_type == SLIType.AVAILABILITY:
            error_budget_consumed = slo.target - current_value
        elif slo.sli.sli_type == SLIType.ERROR_RATE:
            error_budget_consumed = current_value
        else:
            error_budget_consumed = max(0, current_value - slo.target)

        error_budget_remaining = slo.error_budget - error_budget_consumed
        burn_rate = error_budget_consumed / slo.error_budget if slo.error_budget > 0 else 0

        # Determine status
        if error_budget_remaining <= 0:
            status = "breached"
        elif burn_rate > 0.5:
            status = "at_risk"
        else:
            status = "healthy"

        return SLOStatus(
            slo_name=slo_name,
            current_value=current_value,
            target=slo.target,
            error_budget_remaining=error_budget_remaining,
            error_budget_consumed=error_budget_consumed,
            burn_rate=burn_rate,
            status=status,
        )

    def get_all_slo_statuses(self) -> List[SLOStatus]:
        return [self.get_slo_status(name) for name in self.slos]

    def get_error_budget_report(self) -> Dict[str, Any]:
        statuses = self.get_all_slo_statuses()
        return {
            "slos": [
                {
                    "name": s.slo_name,
                    "current": s.current_value,
                    "target": s.target,
                    "budget_remaining": s.error_budget_remaining,
                    "budget_consumed": s.error_budget_consumed,
                    "burn_rate": s.burn_rate,
                    "status": s.status,
                }
                for s in statuses
            ],
            "overall_status": "healthy" if all(s.status == "healthy" for s in statuses) else "at_risk",
        }


# Global SLO tracker
slo_tracker = SLOTracker()
