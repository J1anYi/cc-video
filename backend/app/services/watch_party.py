from typing import Dict, Any

class WatchPartyService:
    async def create_room(self, host_id: str) -> Dict[str, Any]:
        return {"room_id": "room_123", "host_id": host_id}
    
    async def add_participant(self, room_id: str, user_id: str) -> Dict[str, Any]:
        return {"room_id": room_id, "user_id": user_id}
    
    async def sync_playback(self, room_id: str, position: int) -> Dict[str, Any]:
        return {"room_id": room_id, "position": position}
    
    async def send_reaction(self, room_id: str, user_id: str, reaction: str) -> Dict[str, Any]:
        return {"room_id": room_id, "reaction": reaction}
    
    async def schedule_party(self, room_id: str, scheduled_time: str) -> Dict[str, Any]:
        return {"room_id": room_id, "scheduled": scheduled_time}

watch_party_service = WatchPartyService()
