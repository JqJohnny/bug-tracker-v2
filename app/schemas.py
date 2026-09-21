from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator
from zxcvbn import zxcvbn

from .models import PriorityEnum, StatusEnum


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if v != v.strip():
            raise ValueError("Password cannot have leading or trailing whitespace")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        result = zxcvbn(v)
        if result["score"] < 2:
            raise ValueError("Password is too weak")
        return v


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


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

    class ConfigDict:
        from_attributes = True


class BugCreate(BaseModel):
    title: str
    description: str | None = None
    priority: PriorityEnum = PriorityEnum.low
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

    class ConfigDict:
        from_attributes = True
