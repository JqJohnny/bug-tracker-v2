from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey, Table
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
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"


project_contributors = Table(
    "projects_contributors",
    Base.metadata,
    Column(
        "project_id", UUID(as_uuid=True), ForeignKey("projects.id"), primary_key=True
    ),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    assigned_bugs = relationship(
        "Bug", foreign_keys="Bug.assignee_id", back_populates="assignee"
    )
    authored_bugs = relationship(
        "Bug", foreign_keys="Bug.author_id", back_populates="author"
    )
    owned_projects = relationship("Project", back_populates="owner")
    contributed_projects = relationship(
        "Project", secondary=project_contributors, back_populates="contributors"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="owned_projects")
    contributors = relationship(
        "User", secondary=project_contributors, back_populates="contributed_projects"
    )
    bugs = relationship("Bug", back_populates="project")


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
    status = Column(Enum(StatusEnum), default=StatusEnum.open)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )

    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    assignee = relationship(
        "User", foreign_keys=[assignee_id], back_populates="assigned_bugs"
    )
    author = relationship(
        "User", foreign_keys=[author_id], back_populates="authored_bugs"
    )
    project = relationship("Project", back_populates="bugs")
