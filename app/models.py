from sqlalchemy import Column, String, Text, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
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
    created_at = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )  # Check to ensure correctly working
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )
