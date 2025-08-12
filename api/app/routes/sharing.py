from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, schemas, models
from app.services import sharing as sharing_service
from app.utils.dep import get_current_user

router = APIRouter(prefix="/sharing", tags=["sharing"])


@router.post("/tasks/{task_id}/share", response_model=schemas.SharedTask)
def share_task(
        task_id: int,
        shared_task: schemas.SharedTaskCreate,
        db: Session = Depends(get_db)
):
    return sharing_service.share_task(
        db,
        task_id=task_id,
        user_id=shared_task.user_id,
        permission=shared_task.permission_level
    )


@router.get("/tasks", response_model=List[schemas.Task])
def get_shared_tasks(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    return sharing_service.get_shared_tasks(db, current_user.id)
