from fastapi import APIRouter
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass, field
import uuid

router = APIRouter(prefix="/incidents", tags=["incidents"])

@dataclass
class Incident:
    id: str
    title: str
    severity: str
    status: str = "open"
    created_at: datetime = field(default_factory=datetime.utcnow)
    timeline: List[Dict] = field(default_factory=list)

incidents_db: Dict[str, Incident] = {}

@router.post("/")
async def create_incident(title: str, severity: str):
    incident = Incident(id=str(uuid.uuid4()), title=title, severity=severity)
    incidents_db[incident.id] = incident
    return {"id": incident.id, "status": "created"}

@router.get("/")
async def list_incidents(): return {"incidents": [{"id": i.id, "title": i.title, "severity": i.severity, "status": i.status} for i in incidents_db.values()]}

@router.get("/{incident_id}")
async def get_incident(incident_id: str): return incidents_db.get(incident_id, {"error": "not found"})

@router.post("/{incident_id}/timeline")
async def add_timeline_event(incident_id: str, event: str):
    if incident_id in incidents_db:
        incidents_db[incident_id].timeline.append({"time": datetime.utcnow().isoformat(), "event": event})
    return {"status": "added"}
