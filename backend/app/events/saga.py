from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import logging
import uuid

logger = logging.getLogger(__name__)


class SagaState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"


@dataclass
class SagaStep:
    name: str
    action: Callable
    compensate: Callable
    status: str = "pending"
    result: Any = None


@dataclass
class SagaInstance:
    id: str
    name: str
    steps: List[SagaStep] = field(default_factory=list)
    current_step: int = 0
    state: SagaState = SagaState.PENDING
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class SagaOrchestrator:
    def __init__(self):
        self.sagas: Dict[str, SagaInstance] = {}
        self.step_timeout = 30

    def create_saga(self, name: str, steps: List[SagaStep]) -> SagaInstance:
        saga_id = str(uuid.uuid4())
        saga = SagaInstance(
            id=saga_id,
            name=name,
            steps=steps,
        )
        self.sagas[saga_id] = saga
        logger.info(f"Created saga: {name} - {saga_id}")
        return saga

    async def execute_saga(self, saga_id: str) -> SagaInstance:
        saga = self.sagas.get(saga_id)
        if not saga:
            raise ValueError(f"Saga not found: {saga_id}")

        saga.state = SagaState.RUNNING
        logger.info(f"Executing saga: {saga.name}")

        # Execute steps forward
        for i, step in enumerate(saga.steps):
            saga.current_step = i
            try:
                logger.info(f"Executing step: {step.name}")
                result = step.action()
                if asyncio.iscoroutine(result):
                    result = await asyncio.wait_for(result, timeout=self.step_timeout)
                step.status = "completed"
                step.result = result
            except Exception as e:
                logger.error(f"Step failed: {step.name} - {e}")
                step.status = "failed"
                saga.error = str(e)
                await self._compensate(saga, i)
                return saga

        saga.state = SagaState.COMPLETED
        saga.completed_at = datetime.utcnow()
        logger.info(f"Saga completed: {saga.name}")
        return saga

    async def _compensate(self, saga: SagaInstance, failed_step: int):
        saga.state = SagaState.COMPENSATING
        logger.info(f"Compensating saga: {saga.name}")

        # Run compensating actions in reverse
        for i in range(failed_step - 1, -1, -1):
            step = saga.steps[i]
            if step.status == "completed":
                try:
                    logger.info(f"Compensating step: {step.name}")
                    result = step.compensate()
                    if asyncio.iscoroutine(result):
                        await result
                    step.status = "compensated"
                except Exception as e:
                    logger.error(f"Compensation failed: {step.name} - {e}")
                    step.status = "compensation_failed"

        saga.state = SagaState.FAILED
        saga.completed_at = datetime.utcnow()

    def get_saga(self, saga_id: str) -> Optional[SagaInstance]:
        return self.sagas.get(saga_id)

    def get_sagas_by_state(self, state: SagaState) -> List[SagaInstance]:
        return [s for s in self.sagas.values() if s.state == state]


# Global saga orchestrator instance
saga_orchestrator = SagaOrchestrator()
