from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User
from app.database.schemas import (
    Workspace,
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceMember,
    WorkspaceMemberCreate
)
from app.services import workspace as workspace_service
from app.utils.dep import get_current_user

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.post("", response_model=Workspace)
async def create_workspace(
        workspace: WorkspaceCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return workspace_service.create_workspace(db, workspace.model_dump(), current_user.id)


@router.get("/{workspace_id}", response_model=Workspace)
async def get_workspace(
        workspace_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return workspace_service.get_workspace(db, workspace_id, current_user.id)


@router.post("/{workspace_id}/members", response_model=WorkspaceMember)
async def add_workspace_member(
        workspace_id: int,
        member: WorkspaceMemberCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return workspace_service.add_member(
        db,
        workspace_id,
        member.user_id,
        current_user.id,
        member.role
    )


@router.put("/{workspace_id}", response_model=Workspace)
async def update_workspace(
        workspace_id: int,
        workspace: WorkspaceUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return workspace_service.update_workspace(db, workspace_id, workspace.model_dump(exclude_unset=True), current_user.id)
