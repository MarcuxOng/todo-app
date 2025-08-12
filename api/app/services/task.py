from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Type

from app.database.models import Category, Task, Workspace, WorkspaceMember
from app.database.schemas import TaskCreate, TaskUpdate
from app.services import activity_log
from app.utils.logging import logger
from app.workspace.manager import manager


def _validate_workspace_access(db: Session, user_id: int, workspace_ids: List[int]) -> List[Workspace]:
    if not workspace_ids:
        return []

    workspaces = db.query(Workspace).filter(
        Workspace.id.in_(workspace_ids)
    ).all()
    if len(workspaces) != len(workspace_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more workspaces not found"
        )

    for ws in workspaces:
        membership = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == ws.id,
            WorkspaceMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not a member of workspace {ws.id}"
            )
    return workspaces


async def create_task(db: Session, task: TaskCreate, owner_id: int) -> Task:
    try:
        task_data = task.model_dump(exclude={"category_ids", "workspace_ids"})
        db_task = Task(**task_data, owner_id=owner_id)

        if task.workspace_ids:
            workspaces = _validate_workspace_access(db, owner_id, task.workspace_ids)
            db_task.workspaces = workspaces

        if task.category_ids:
            categories = db.query(Category).filter(
                Category.id.in_(task.category_ids)
            ).all()
            if len(categories) != len(task.category_ids):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more categories not found"
                )
            db_task.categories = categories

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        activity_log.log_activity(
            db,
            user_id=owner_id,
            action="task_create",
            entity_type="task",
            entity_id=db_task.id,
            details={
                "title": db_task.title,
                "status": "created",
                "workspace_ids": task.workspace_ids
            }
        )

        await manager.broadcast_task_update(
            task_id=db_task.id,
            action="created",
            data={
                "title": db_task.title,
                "owner_id": owner_id,
                "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                "workspace_ids": task.workspace_ids
            }
        )
        logger.info(f"Task created: {db_task.id} by user {owner_id}")
        return db_task

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating task: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )


def get_user_tasks(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        include_completed: bool = True,
        due_after: datetime = None,
        search: Optional[str] = None,
        category_ids: Optional[List[int]] = None
) -> list[Type[Task]]:
    query = db.query(Task).filter(Task.owner_id == user_id)
    if not include_completed:
        query = query.filter(Task.is_completed == False)

    if due_after:
        query = query.filter(Task.due_date >= due_after)

    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )

    if category_ids:
        query = query.join(Task.categories).filter(
            Category.id.in_(category_ids)
        )

    return query.order_by(Task.due_date.asc()).offset(skip).limit(limit).all()


def get_user_task(db: Session, task_id: int, user_id: int) -> Type[Task]:
    task = db.query(Task).filter(
        and_(
            Task.id == task_id,
            Task.owner_id == user_id
        )
    ).first()

    if not task:
        logger.warning(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


async def update_user_task(db: Session, task_id: int, user_id: int, task: TaskUpdate) -> Type[Task]:
    try:
        db_task = get_user_task(db, task_id, user_id)
        changes = {}
        update_data = task.model_dump(
            exclude_unset=True,
            exclude={"category_ids", "workspace_ids"}
        )

        if task.workspace_ids is not None:
            workspaces = _validate_workspace_access(db, user_id, task.workspace_ids)
            db_task.workspaces = workspaces
            changes["workspace_ids"] = [w.id for w in workspaces]

        for key, value in update_data.items():
            if getattr(db_task, key) != value:
                changes[key] = value
            setattr(db_task, key, value)

        if task.category_ids is not None:
            categories = db.query(Category).filter(
                Category.id.in_(task.category_ids)
            ).all()
            if len(categories) != len(task.category_ids):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more categories not found"
                )
            db_task.categories = categories
            changes["categories"] = [c.id for c in categories]

        db.commit()
        db.refresh(db_task)

        if changes:
            await manager.broadcast_task_update(
                task_id=task_id,
                action="updated",
                data=changes
            )
            logger.info(f"Task updated: {task_id} by user {user_id}")

        return db_task

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating task {task_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )


async def delete_user_task(db: Session, task_id: int, user_id: int) -> None:
    try:
        db_task = get_user_task(db, task_id, user_id)
        db.delete(db_task)
        db.commit()

        await manager.broadcast_task_update(
            task_id=task_id,
            action="deleted",
            data={"deleted_by": user_id}
        )
        logger.info(f"Task deleted: {task_id} by user {user_id}")

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting task {task_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )


def get_upcoming_tasks(db: Session, user_id: int, days: int = 7, include_completed: bool = False) -> list[Type[Task]]:
    now = datetime.now()
    end_date = now + timedelta(days=days)
    query = db.query(Task).filter(
        Task.owner_id == user_id,
        Task.due_date >= now,
        Task.due_date <= end_date
    )

    if not include_completed:
        query = query.filter(Task.is_completed == False)

    return query.order_by(Task.due_date.asc()).all()
