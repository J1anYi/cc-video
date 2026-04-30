from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import json
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class Event:
    id: str
    type: str
    aggregate_id: str
    aggregate_type: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "data": self.data,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
        }


EventHandler = Callable[[Event], Any]


class EventBus:
    def __init__(self):
        self.handlers: Dict[str, List[EventHandler]] = defaultdict(list)
        self.middleware: List[Callable] = []
        self.dead_letter_queue: List[Event] = []

    def subscribe(self, event_type: str, handler: EventHandler):
        self.handlers[event_type].append(handler)
        logger.info(f"Subscribed handler to event type: {event_type}")

    def unsubscribe(self, event_type: str, handler: EventHandler):
        if event_type in self.handlers:
            self.handlers[event_type] = [
                h for h in self.handlers[event_type] if h != handler
            ]

    def add_middleware(self, middleware: Callable):
        self.middleware.append(middleware)

    async def publish(self, event: Event):
        logger.info(f"Publishing event: {event.type} - {event.id}")

        # Run middleware
        for middleware in self.middleware:
            try:
                await middleware(event)
            except Exception as e:
                logger.error(f"Middleware error: {e}")

        # Get handlers for event type
        handlers = self.handlers.get(event.type, [])
        handlers.extend(self.handlers.get("*", []))  # Wildcard handlers

        # Execute handlers
        for handler in handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(f"Handler error for event {event.type}: {e}")
                self.dead_letter_queue.append(event)

    async def publish_batch(self, events: List[Event]):
        for event in events:
            await self.publish(event)

    def get_dead_letter_queue(self) -> List[Event]:
        return self.dead_letter_queue

    def clear_dead_letter_queue(self):
        self.dead_letter_queue.clear()


# Global event bus instance
event_bus = EventBus()
