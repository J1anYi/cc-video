from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, Request
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.database import get_db
from app.config import settings
from app.models.user import User
from app.websocket.manager import manager
from app.websocket.collaboration import collaboration_manager
from app.websocket.notification_handler import notification_handler

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])


async def get_user_from_token(token: str, db: AsyncSession) -> int | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except (JWTError, ValueError, TypeError):
        return None


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    user_id = await get_user_from_token(token, db)
    if not user_id:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            await handle_message(websocket, user_id, data, db)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await manager.disconnect(websocket)


async def handle_message(websocket: WebSocket, user_id: int, data: dict, db: AsyncSession):
    message_type = data.get("type")
    
    if message_type == "heartbeat":
        await manager.handle_heartbeat(websocket)
    
    elif message_type == "join_room":
        room_id = data.get("room_id")
        if room_id:
            await manager.join_room(user_id, room_id)
            await collaboration_manager.update_presence(room_id, user_id)
    
    elif message_type == "leave_room":
        room_id = data.get("room_id")
        if room_id:
            await manager.leave_room(user_id, room_id)
            await collaboration_manager.remove_presence(room_id, user_id)
    
    elif message_type == "typing":
        room_id = data.get("room_id")
        is_typing = data.get("is_typing", False)
        if room_id:
            await collaboration_manager.set_typing(room_id, user_id, is_typing)
    
    elif message_type == "watch_party_sync":
        room_id = data.get("room_id")
        action = data.get("action")
        timestamp = data.get("timestamp", 0)
        if room_id and action:
            await collaboration_manager.watch_party_sync(room_id, action, timestamp, user_id)
    
    else:
        logger.warning(f"Unknown message type: {message_type}")


@router.get("/ws/stats")
async def websocket_stats():
    return {
        "total_connections": manager.get_total_connections(),
        "rooms": len(manager.rooms),
    }


@router.get("/ws/room/{room_id}/users")
async def room_users(room_id: str):
    users = manager.get_room_users(room_id)
    return {"room_id": room_id, "users": list(users)}


# Polling fallback endpoints

@router.get("/poll/notifications")
async def poll_notifications(request: Request, last_id: int = 0):
    """Long-polling fallback for notifications."""
    user = request.state.user if hasattr(request.state, "user") else None
    if not user:
        return {"error": "Unauthorized"}
    
    # Return pending notifications since last_id
    # In production, this would query the notification table
    return {
        "notifications": [],
        "last_id": last_id,
    }


@router.get("/poll/presence/{room_id}")
async def poll_presence(room_id: str):
    """Polling fallback for presence."""
    from app.websocket.collaboration import collaboration_manager
    
    present_users = list(collaboration_manager.presence.get(room_id, {}).keys())
    typing_users = await collaboration_manager.get_typing_users(room_id)
    
    return {
        "room_id": room_id,
        "present_users": present_users,
        "typing_users": list(typing_users),
    }
