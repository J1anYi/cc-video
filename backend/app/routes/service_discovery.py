from fastapi import APIRouter
from app.services.service_registry import service_registry
from app.services.service_registry import ServiceInstance

router = APIRouter(prefix="/services", tags=["service-discovery"])


@router.get("/")
async def list_services():
    """List all registered services."""
    return service_registry.get_all_services()


@router.post("/register")
async def register_service(
    name: str,
    url: str,
    health_check_url: str,
    metadata: dict = None,
):
    """Register a service instance."""
    instance = ServiceInstance(
        name=name,
        url=url,
        health_check_url=health_check_url,
        metadata=metadata or {},
    )
    service_registry.register(instance)
    return {"status": "registered", "name": name, "url": url}


@router.delete("/deregister")
async def deregister_service(name: str, url: str):
    """Deregister a service instance."""
    service_registry.deregister(name, url)
    return {"status": "deregistered"}


@router.get("/{name}")
async def get_service(name: str):
    """Get instances of a specific service."""
    instances = service_registry.get_instances(name)
    return {
        "name": name,
        "instances": [
            {
                "url": inst.url,
                "status": inst.status,
                "metadata": inst.metadata,
            }
            for inst in instances
        ],
    }


@router.get("/{name}/health")
async def service_health(name: str):
    """Check health of service instances."""
    instances = service_registry.get_instances(name)
    healthy = sum(1 for inst in instances if inst.is_healthy())
    return {
        "name": name,
        "total_instances": len(instances),
        "healthy_instances": healthy,
        "status": "healthy" if healthy > 0 else "unhealthy",
    }
