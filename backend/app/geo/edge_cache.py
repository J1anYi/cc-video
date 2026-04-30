"""Edge Caching Infrastructure"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class EdgeCacheManager:
    """Manages edge caching"""
    
    def __init__(self):
        self._edge_nodes: Dict[str, Dict[str, Any]] = {}
        self._cache_entries: Dict[str, Dict[str, Any]] = {}
    
    async def register_edge_node(self, node_id: str, location: str) -> Dict[str, Any]:
        node = {"id": node_id, "location": location, "status": "active"}
        self._edge_nodes[node_id] = node
        return node
    
    async def cache_content(self, content_id: str, data: Any, ttl: int = 3600) -> Dict[str, Any]:
        entry = {
            "content_id": content_id,
            "data": data,
            "expires_at": (datetime.utcnow() + timedelta(seconds=ttl)).isoformat()
        }
        self._cache_entries[content_id] = entry
        return {"cached": True, "content_id": content_id}
    
    async def get_cached_content(self, content_id: str) -> Optional[Dict[str, Any]]:
        if content_id not in self._cache_entries:
            return None
        entry = self._cache_entries[content_id]
        expires = datetime.fromisoformat(entry["expires_at"])
        if datetime.utcnow() > expires:
            del self._cache_entries[content_id]
            return None
        return entry
    
    async def invalidate_cache(self, content_id: str) -> bool:
        if content_id in self._cache_entries:
            del self._cache_entries[content_id]
            return True
        return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        return {"entries": len(self._cache_entries), "nodes": len(self._edge_nodes)}
