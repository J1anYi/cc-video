from .manager import manager
from typing import Dict, Set, Optional
from datetime import datetime
from collections import defaultdict
import asyncio
import logging

logger = logging.getLogger(__name__)


class CollaborationManager:
    def __init__(self):
        # document/room -> {user_id: last_activity}
        self.presence: Dict[str, Dict[int, datetime]] = defaultdict(dict)
        # user_id -> {room_id: typing_status}
        self.typing_status: Dict[int, Dict[str, bool]] = defaultdict(dict)
        # Presence timeout in seconds
        self.presence_timeout = 300

    async def update_presence(self, room_id: str, user_id: int):
        self.presence[room_id][user_id] = datetime.utcnow()
        await self._broadcast_presence(room_id)

    async def remove_presence(self, room_id: str, user_id: int):
        if room_id in self.presence and user_id in self.presence[room_id]:
            del self.presence[room_id][user_id]
            if not self.presence[room_id]:
                del self.presence[room_id]
        await self._broadcast_presence(room_id)

    async def _broadcast_presence(self, room_id: str):
        present_users = list(self.presence.get(room_id, {}).keys())
        await manager.broadcast_to_room(room_id, {
            "type": "presence_update",
            "room_id": room_id,
            "users": present_users,
            "timestamp": datetime.utcnow().isoformat(),
        })

    async def set_typing(self, room_id: str, user_id: int, is_typing: bool):
        self.typing_status[user_id][room_id] = is_typing
        
        if is_typing:
            await manager.broadcast_to_room(room_id, {
                "type": "typing_start",
                "room_id": room_id,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
            }, exclude_user=user_id)
        else:
            await manager.broadcast_to_room(room_id, {
                "type": "typing_stop",
                "room_id": room_id,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
            }, exclude_user=user_id)

    async def get_typing_users(self, room_id: str) -> Set[int]:
        typing_users = set()
        for user_id, rooms in self.typing_status.items():
            if rooms.get(room_id, False):
                typing_users.add(user_id)
        return typing_users

    async def watch_party_sync(self, room_id: str, action: str, timestamp: float, user_id: int):
        await manager.broadcast_to_room(room_id, {
            "type": "watch_party_sync",
            "room_id": room_id,
            "action": action,  # play, pause, seek
            "timestamp_video": timestamp,
            "initiator": user_id,
            "server_time": datetime.utcnow().isoformat(),
        }, exclude_user=user_id)

    async def cleanup_inactive(self):
        now = datetime.utcnow()
        for room_id in list(self.presence.keys()):
            for user_id in list(self.presence[room_id].keys()):
                last_activity = self.presence[room_id][user_id]
                delta = (now - last_activity).total_seconds()
                if delta > self.presence_timeout:
                    await self.remove_presence(room_id, user_id)


collaboration_manager = CollaborationManager()
