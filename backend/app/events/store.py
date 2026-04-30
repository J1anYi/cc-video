from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class StoredEvent:
    sequence: int
    event_id: str
    event_type: str
    aggregate_id: str
    aggregate_type: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: datetime
    version: int


class EventStore:
    def __init__(self):
        self.events: List[StoredEvent] = []
        self.sequence = 0
        self.snapshots: Dict[str, Dict[str, Any]] = {}

    async def append(self, event) -> int:
        self.sequence += 1
        stored = StoredEvent(
            sequence=self.sequence,
            event_id=event.id,
            event_type=event.type,
            aggregate_id=event.aggregate_id,
            aggregate_type=event.aggregate_type,
            data=event.data,
            metadata=event.metadata,
            timestamp=event.timestamp,
            version=event.version,
        )
        self.events.append(stored)
        logger.info(f"Stored event: {event.type} - sequence {self.sequence}")
        return self.sequence

    async def get_events(
        self,
        aggregate_id: Optional[str] = None,
        event_type: Optional[str] = None,
        from_sequence: int = 0,
    ) -> List[StoredEvent]:
        events = self.events
        if aggregate_id:
            events = [e for e in events if e.aggregate_id == aggregate_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        events = [e for e in events if e.sequence > from_sequence]
        return events

    async def get_aggregate_events(self, aggregate_id: str) -> List[StoredEvent]:
        return [e for e in self.events if e.aggregate_id == aggregate_id]

    async def save_snapshot(self, aggregate_id: str, state: Dict[str, Any]):
        self.snapshots[aggregate_id] = {
            "state": state,
            "sequence": self.sequence,
            "timestamp": datetime.utcnow().isoformat(),
        }
        logger.info(f"Saved snapshot for aggregate: {aggregate_id}")

    async def get_snapshot(self, aggregate_id: str) -> Optional[Dict[str, Any]]:
        return self.snapshots.get(aggregate_id)

    async def replay_events(
        self,
        aggregate_id: str,
        from_sequence: int = 0,
    ) -> List[StoredEvent]:
        events = await self.get_aggregate_events(aggregate_id)
        return [e for e in events if e.sequence > from_sequence]

    def get_all_events(self) -> List[StoredEvent]:
        return self.events

    def get_event_count(self) -> int:
        return len(self.events)


# Global event store instance
event_store = EventStore()
