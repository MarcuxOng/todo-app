from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator
from typing import Optional, List


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50, pattern=r"^[a-zA-Z0-9\-_ ]+$")


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: bool = False
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None


class TaskCreate(TaskBase):
    category_ids: Optional[List[int]] = Field(None)
    workspace_ids: Optional[List[int]] = Field(None)

    @validator('workspace_ids', 'category_ids', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        if isinstance(v, list):
            # Filter out empty strings from the list
            return [item for item in v if item != ""]
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    category_ids: Optional[List[int]] = None
    workspace_ids: Optional[List[int]] = None


class Task(TaskBase):
    id: int
    owner_id: int
    categories: List[Category] = Field(default_factory=list)
    workspaces: List["Workspace"] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class TaskWithOwner(Task):
    owner: User
    model_config = ConfigDict(from_attributes=True)


class SharedTaskBase(BaseModel):
    permission_level: str = Field(..., pattern="^(view|edit)$")


class SharedTaskCreate(SharedTaskBase):
    user_id: int


class SharedTask(SharedTaskBase):
    task_id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    text: str = Field(..., max_length=1000)


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class WorkspaceBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=500)


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class Workspace(WorkspaceBase):
    id: int
    owner_id: int
    created_at: datetime
    member_count: int
    model_config = ConfigDict(from_attributes=True)


class WorkspaceWithMembers(Workspace):
    members: List["WorkspaceMember"] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class WorkspaceMemberBase(BaseModel):
    role: str = Field(..., pattern="^(admin|editor|viewer)$")


class WorkspaceMemberCreate(WorkspaceMemberBase):
    user_id: int


class WorkspaceMember(WorkspaceMemberBase):
    workspace_id: int
    user_id: int
    joined_at: datetime
    user: User
    model_config = ConfigDict(from_attributes=True)


class ActivityLogBase(BaseModel):
    action: str = Field(..., max_length=50)
    entity_type: str = Field(..., max_length=50)
    entity_id: int
    details: dict | None = None


class ActivityLog(ActivityLogBase):
    id: int
    user_id: int
    created_at: datetime
    description: str

    model_config = ConfigDict(from_attributes=True)
