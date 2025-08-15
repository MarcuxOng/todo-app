from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.utils.logging import logger

from app.database.models import Workspace, WorkspaceMember


def create_workspace(db: Session, workspace_data: dict, owner_id: int):
    try:
        workspace = Workspace(**workspace_data, owner_id=owner_id)
        db.add(workspace)
        db.flush()  # Use flush to get the workspace ID before the final commit

        member = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=owner_id,
            role="admin"
        )
        db.add(member)
        db.commit()
        db.refresh(workspace)
        return workspace
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating workspace: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create workspace"
        )


def get_workspace(db: Session, workspace_id: int, user_id: int):
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.members.any(user_id=user_id)
    ).first()

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found or access denied"
        )
    return workspace


def get_workspaces(db: Session, user_id: int):
    workspaces = db.query(Workspace).filter(
        Workspace.members.any(user_id=user_id)
    ).all()
    return workspaces


def add_member(db: Session, workspace_id: int, user_id: int, adder_id: int, role: str):
    try:
        adder_membership = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == adder_id,
            WorkspaceMember.role == "admin"
        ).first()

        if not adder_membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can add members"
            )

        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role
        )
        db.add(member)
        db.commit()
        db.refresh(member)
        return member
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding member to workspace: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add member"
        )


def update_workspace(db: Session, workspace_id: int, workspace_data: dict, user_id: int):
    try:
        membership = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
            WorkspaceMember.role == "admin"
        ).first()

        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can update the workspace"
            )

        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )

        for key, value in workspace_data.items():
            setattr(workspace, key, value)

        db.commit()
        db.refresh(workspace)
        return workspace
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating workspace: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update workspace"
        )
