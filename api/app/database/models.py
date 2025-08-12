from datetime import datetime
from sqlalchemy import ForeignKey, String, Boolean, Text, DateTime, Table, Column, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base

task_categories = Table(
    "task_categories",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True)
)


task_workspace = Table(
    "task_workspace",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("workspace_id", ForeignKey("workspaces.id"), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tasks: Mapped[list["Task"]] = relationship(back_populates="owner")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    shared_tasks: Mapped[list["SharedTask"]] = relationship(back_populates="user")
    owned_workspaces: Mapped[list["Workspace"]] = relationship(back_populates="owner")
    workspace_memberships: Mapped[list["WorkspaceMember"]] = relationship(back_populates="user")
    activity_logs: Mapped[list["ActivityLog"]] = relationship(back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    tasks: Mapped[list["Task"]] = relationship(secondary="task_categories", back_populates="categories")


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    reminder_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="tasks")
    categories: Mapped[list["Category"]] = relationship(secondary="task_categories", back_populates="tasks")
    shared_with: Mapped[list["SharedTask"]] = relationship(back_populates="task")
    comments: Mapped[list["Comment"]] = relationship(back_populates="task")
    workspaces: Mapped[list["Workspace"]] = relationship(secondary="task_workspace", back_populates="tasks")


class SharedTask(Base):
    __tablename__ = "shared_tasks"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    permission_level: Mapped[str] = mapped_column(String(10))  # "view", "edit"

    task: Mapped["Task"] = relationship(back_populates="shared_with")
    user: Mapped["User"] = relationship(back_populates="shared_tasks")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    task: Mapped["Task"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")


class Workspace(Base):
    __tablename__ = "workspaces"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="owned_workspaces")
    members: Mapped[list["WorkspaceMember"]] = relationship(back_populates="workspace")
    tasks: Mapped[list["Task"]] = relationship(secondary="task_workspace", back_populates="workspaces")

    @hybrid_property
    def member_count(self) -> int:
        """Count of workspace members including the owner"""
        return len(self.members) if self.members else 0


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role: Mapped[str] = mapped_column(String(20))  # admin, editor, viewer
    joined_at: Mapped[datetime] = mapped_column(server_default=func.now())

    workspace: Mapped["Workspace"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="workspace_memberships")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(50))  # e.g., "task_create", "workspace_update"
    entity_type: Mapped[str] = mapped_column(String(50))  # "task", "workspace", etc.
    entity_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    details: Mapped[dict] = mapped_column(JSON, nullable=True)

    user: Mapped["User"] = relationship(back_populates="activity_logs")

