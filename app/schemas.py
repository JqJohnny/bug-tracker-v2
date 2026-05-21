from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
import enum


class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class StatusEnum(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"


class BugCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.low
    status: StatusEnum = StatusEnum.new


class BugUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None


class BugResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    priority: PriorityEnum
    status: StatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
