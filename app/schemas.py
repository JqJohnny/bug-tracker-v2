from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from .models import PriorityEnum, StatusEnum


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    owner_id: UUID


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BugCreate(BaseModel):
    title: str
    description: str | None = None
    priority: PriorityEnum = PriorityEnum.low
    author_id: UUID
    assignee_id: UUID | None = None
    project_id: UUID


class BugUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: PriorityEnum | None = None
    status: StatusEnum | None = None
    assignee_id: UUID | None = None


class BugResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    priority: PriorityEnum
    status: StatusEnum
    created_at: datetime
    updated_at: datetime
    author_id: UUID
    assignee_id: UUID | None = None
    project_id: UUID

    class Config:
        from_attributes = True
