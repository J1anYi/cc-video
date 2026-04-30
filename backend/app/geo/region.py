"""Multi-Region Management"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RegionStatus(Enum):
    ACTIVE = "active"
    STANDBY = "standby"
    DRAINING = "draining"
    OFFLINE = "offline"


@dataclass
class RegionConfig:
    region_id: str
    name: str
    provider: str
    endpoint: str
    priority: int = 1
    capacity: int = 100
    latency_target_ms: int = 100


@dataclass
class Region:
    id: str
    name: str
    config: RegionConfig
    status: RegionStatus = RegionStatus.ACTIVE
    health_score: float = 1.0
    current_load: int = 0
    last_health_check: Optional[datetime] = None


class RegionManager:
    """Manages multi-region deployment"""
    
    def __init__(self):
        self._regions: Dict[str, Region] = {}
        self._primary_region: Optional[str] = None
    
    async def register_region(
        self,
        config: RegionConfig,
        is_primary: bool = False
    ) -> Region:
        region = Region(
            id=config.region_id,
            name=config.name,
            config=config
        )
        
        self._regions[config.region_id] = region
        
        if is_primary or not self._primary_region:
            self._primary_region = config.region_id
        
        logger.info(f"Region registered: {config.region_id}")
        return region
    
    async def get_region(self, region_id: str) -> Optional[Region]:
        return self._regions.get(region_id)
    
    async def list_regions(
        self,
        status: Optional[RegionStatus] = None
    ) -> List[Region]:
        regions = list(self._regions.values())
        if status:
            regions = [r for r in regions if r.status == status]
        return regions
    
    async def set_region_status(
        self,
        region_id: str,
        status: RegionStatus
    ) -> bool:
        if region_id not in self._regions:
            return False
        
        region = self._regions[region_id]
        region.status = status
        logger.info(f"Region {region_id} status set to {status.value}")
        return True
    
    def get_primary_region(self) -> Optional[Region]:
        if self._primary_region:
            return self._regions.get(self._primary_region)
        return None
    
    async def health_check(self, region_id: str) -> Dict[str, Any]:
        if region_id not in self._regions:
            return {"error": "Region not found"}
        
        region = self._regions[region_id]
        region.last_health_check = datetime.utcnow()
        
        return {
            "region_id": region_id,
            "status": region.status.value,
            "health_score": region.health_score,
            "current_load": region.current_load,
            "capacity": region.config.capacity,
            "checked_at": region.last_health_check.isoformat()
        }
