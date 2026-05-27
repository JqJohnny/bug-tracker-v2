from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base
import uuid
import datetime
import enum


class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class StatusEnum(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    assigned_bugs = relationship(
        "Bug", foreign_keys="Bug.assignee_id", back_populates="assignee"
    )
    authored_bugs = relationship(
        "Bug", foreign_keys="Bug.author_id", back_populates="author"
    )


class Bug(Base):
    """
    Represents a bug report in the system.
    Uses UUID4 for primary key.
    Consider UUID7 for better index performance at scale when full native support is available.
    """

    __tablename__ = "bugs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)  # Default - nullable = True
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.low)
    status = Column(Enum(StatusEnum), default=StatusEnum.new)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )

    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    assignee = relationship(
        "User", foreign_keys=[assignee_id], back_populates="assigned_bugs"
    )
    author = relationship(
        "User", foreign_keys=[author_id], back_populates="authored_bugs"
    )
