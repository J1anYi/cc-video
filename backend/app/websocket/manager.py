from fastapi import WebSocket
from typing import Dict, List, Set, Optional
from collections import defaultdict
import asyncio
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # user_id -> set of websocket connections
        self.user_connections: Dict[int, Set[WebSocket]] = defaultdict(set)
        # room_id -> set of user_ids
        self.rooms: Dict[str, Set[int]] = defaultdict(set)
        # websocket -> user_id mapping
        self.connection_user: Dict[WebSocket, int] = {}
        # Heartbeat tracking
        self.heartbeat_interval = 30
        self.heartbeat_timeout = 60

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.user_connections[user_id].add(websocket)
        self.connection_user[websocket] = user_id
        logger.info(f"User {user_id} connected. Total connections: {len(self.connection_user)}")
        await self._send_connection_ack(websocket)

    async def disconnect(self, websocket: WebSocket):
        user_id = self.connection_user.pop(websocket, None)
        if user_id:
            self.user_connections[user_id].discard(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
            logger.info(f"User {user_id} disconnected. Total connections: {len(self.connection_user)}")

    async def _send_connection_ack(self, websocket: WebSocket):
        await self.send_personal(websocket, {
            "type": "connection_ack",
            "timestamp": datetime.utcnow().isoformat(),
        })

    async def send_personal(self, websocket: WebSocket, message: dict):
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            await self.disconnect(websocket)

    async def send_to_user(self, user_id: int, message: dict):
        connections = self.user_connections.get(user_id, set())
        disconnected = []
        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        for conn in disconnected:
            await self.disconnect(conn)

    async def broadcast(self, message: dict, exclude_user: Optional[int] = None):
        for user_id, connections in list(self.user_connections.items()):
            if exclude_user and user_id == exclude_user:
                continue
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

    async def broadcast_to_room(self, room_id: str, message: dict, exclude_user: Optional[int] = None):
        user_ids = self.rooms.get(room_id, set())
        for user_id in user_ids:
            if exclude_user and user_id == exclude_user:
                continue
            await self.send_to_user(user_id, message)

    async def join_room(self, user_id: int, room_id: str):
        self.rooms[room_id].add(user_id)
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "room_id": room_id,
            "user_id": user_id,
        }, exclude_user=user_id)

    async def leave_room(self, user_id: int, room_id: str):
        self.rooms[room_id].discard(user_id)
        if not self.rooms[room_id]:
            del self.rooms[room_id]
        await self.broadcast_to_room(room_id, {
            "type": "user_left",
            "room_id": room_id,
            "user_id": user_id,
        })

    def get_room_users(self, room_id: str) -> Set[int]:
        return self.rooms.get(room_id, set())

    def get_user_connection_count(self, user_id: int) -> int:
        return len(self.user_connections.get(user_id, set()))

    def get_total_connections(self) -> int:
        return len(self.connection_user)

    async def handle_heartbeat(self, websocket: WebSocket):
        await self.send_personal(websocket, {
            "type": "heartbeat",
            "timestamp": datetime.utcnow().isoformat(),
        })


manager = ConnectionManager()
