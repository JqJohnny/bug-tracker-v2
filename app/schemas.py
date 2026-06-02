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


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: UUID


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BugCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.low
    author_id: UUID
    assignee_id: Optional[UUID] = None
    project_id: UUID


class BugUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    assignee_id: Optional[UUID] = None


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
    project_id: UUID

    class Config:
        from_attributes = True
