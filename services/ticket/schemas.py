from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class TicketStatus(str, Enum):
    reported = "reported"
    assigned = "assigned"
    in_progress = "in_progress"
    repaired = "repaired"
    closed = "closed"

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class TicketCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    water_point_id: str = Field(min_length=2, max_length=60)
    reported_by: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=1000)
    priority: Priority = Priority.medium

class TechnicianAssignment(BaseModel):
    technician_id: str = Field(min_length=2, max_length=60)

class TicketStatusUpdate(BaseModel):
    status: TicketStatus

class TicketOut(BaseModel):
    id: UUID
    water_point_id: str
    reported_by: str
    description: str
    priority: Priority
    assigned_to: str | None = None
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None = None

class TicketList(BaseModel):
    tickets: list[TicketOut]
