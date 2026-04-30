from fastapi import APIRouter
from typing import Dict, Any, List
from app.events.bus import event_bus, Event
from app.events.store import event_store
from app.events.saga import saga_orchestrator, SagaStep
import uuid

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/publish")
async def publish_event(
    event_type: str,
    aggregate_id: str,
    aggregate_type: str,
    data: Dict[str, Any],
    metadata: Dict[str, Any] = None,
):
    """Publish an event to the event bus."""
    event = Event(
        id=str(uuid.uuid4()),
        type=event_type,
        aggregate_id=aggregate_id,
        aggregate_type=aggregate_type,
        data=data,
        metadata=metadata or {},
    )
    await event_bus.publish(event)
    await event_store.append(event)
    return {"status": "published", "event_id": event.id}


@router.get("/store")
async def list_events(
    aggregate_id: str = None,
    event_type: str = None,
    from_sequence: int = 0,
):
    """List stored events."""
    events = await event_store.get_events(
        aggregate_id=aggregate_id,
        event_type=event_type,
        from_sequence=from_sequence,
    )
    return {
        "events": [
            {
                "sequence": e.sequence,
                "event_id": e.event_id,
                "event_type": e.event_type,
                "aggregate_id": e.aggregate_id,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in events
        ],
        "count": len(events),
    }


@router.get("/store/{aggregate_id}")
async def get_aggregate_events(aggregate_id: str):
    """Get all events for an aggregate."""
    events = await event_store.get_aggregate_events(aggregate_id)
    return {
        "aggregate_id": aggregate_id,
        "events": [
            {
                "sequence": e.sequence,
                "event_type": e.event_type,
                "data": e.data,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in events
        ],
    }


@router.get("/dead-letter")
async def get_dead_letter_queue():
    """Get events in dead letter queue."""
    events = event_bus.get_dead_letter_queue()
    return {
        "count": len(events),
        "events": [e.to_dict() for e in events],
    }


@router.delete("/dead-letter")
async def clear_dead_letter_queue():
    """Clear the dead letter queue."""
    event_bus.clear_dead_letter_queue()
    return {"status": "cleared"}


@router.get("/sagas")
async def list_sagas():
    """List all sagas instances."""
    return {
        "sagas": [
            {
                "id": s.id,
                "name": s.name,
                "state": s.state.value,
                "current_step": s.current_step,
                "started_at": s.started_at.isoformat(),
            }
            for s in saga_orchestrator.sagas.values()
        ]
    }


@router.get("/sagas/{saga_id}")
async def get_saga(saga_id: str):
    """Get saga details."""
    saga = saga_orchestrator.get_saga(saga_id)
    if not saga:
        return {"error": "Saga not found"}
    return {
        "id": saga.id,
        "name": saga.name,
        "state": saga.state.value,
        "current_step": saga.current_step,
        "steps": [
            {"name": s.name, "status": s.status}
            for s in saga.steps
        ],
        "started_at": saga.started_at.isoformat(),
        "completed_at": saga.completed_at.isoformat() if saga.completed_at else None,
        "error": saga.error,
    }
