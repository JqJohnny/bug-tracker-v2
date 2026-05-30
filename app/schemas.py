from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from .models import PriorityEnum, StatusEnum


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class BugCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.low
    status: StatusEnum = StatusEnum.new
    author_id: UUID
    assignee_id: Optional[UUID] = None


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
    author_id: UUID
    assignee_id: Optional[UUID] = None

    class Config:
        from_attributes = True
