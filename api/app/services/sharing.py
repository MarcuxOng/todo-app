from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.database.models import Task, SharedTask


def share_task(db: Session, task_id: int, user_id: int, permission: str):
    if permission not in ["view", "edit"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission must be 'view' or 'edit'"
        )

    shared_task = SharedTask(
        task_id=task_id,
        user_id=user_id,
        permission_level=permission
    )

    db.add(shared_task)
    db.commit()
    db.refresh(shared_task)
    return shared_task


def get_shared_tasks(db: Session, user_id: int):
    return db.query(Task).join(SharedTask).filter(SharedTask.user_id == user_id).all()
