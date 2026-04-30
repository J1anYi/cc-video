from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import asyncio
import logging

logger = logging.getLogger(__name__)


@dataclass
class ServiceInstance:
    name: str
    url: str
    health_check_url: str
    last_heartbeat: datetime = field(default_factory=datetime.utcnow)
    status: str = "healthy"
    metadata: Dict[str, str] = field(default_factory=dict)

    def is_healthy(self, timeout_seconds: int = 30) -> bool:
        elapsed = (datetime.utcnow() - self.last_heartbeat).total_seconds()
        return elapsed < timeout_seconds and self.status == "healthy"


class ServiceRegistry:
    def __init__(self, heartbeat_interval: int = 10):
        self.services: Dict[str, List[ServiceInstance]] = {}
        self.heartbeat_interval = heartbeat_interval
        self._running = False

    def register(self, instance: ServiceInstance):
        if instance.name not in self.services:
            self.services[instance.name] = []
        
        # Check if instance already exists
        for existing in self.services[instance.name]:
            if existing.url == instance.url:
                existing.last_heartbeat = datetime.utcnow()
                existing.status = "healthy"
                logger.info(f"Service {instance.name} at {instance.url} heartbeat updated")
                return
        
        self.services[instance.name].append(instance)
        logger.info(f"Service {instance.name} registered at {instance.url}")

    def deregister(self, name: str, url: str):
        if name in self.services:
            self.services[name] = [
                inst for inst in self.services[name] if inst.url != url
            ]
            if not self.services[name]:
                del self.services[name]
            logger.info(f"Service {name} at {url} deregistered")

    def get_instances(self, name: str) -> List[ServiceInstance]:
        instances = self.services.get(name, [])
        return [inst for inst in instances if inst.is_healthy()]

    def get_instance(self, name: str) -> Optional[ServiceInstance]:
        instances = self.get_instances(name)
        if not instances:
            return None
        # Simple round-robin (could implement more sophisticated LB)
        return instances[0]

    def get_all_services(self) -> Dict[str, List[Dict]]:
        result = {}
        for name, instances in self.services.items():
            result[name] = [
                {
                    "url": inst.url,
                    "status": inst.status,
                    "last_heartbeat": inst.last_heartbeat.isoformat(),
                    "metadata": inst.metadata,
                }
                for inst in instances
            ]
        return result

    async def start_health_checks(self):
        self._running = True
        while self._running:
            await self._check_health()
            await asyncio.sleep(self.heartbeat_interval)

    async def _check_health(self):
        for name, instances in list(self.services.items()):
            for instance in instances:
                if not instance.is_healthy():
                    instance.status = "unhealthy"
                    logger.warning(f"Service {name} at {instance.url} is unhealthy")

    def stop(self):
        self._running = False


# Global registry instance
service_registry = ServiceRegistry()
