from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import models, schemas
from app.database.database import get_db
from app.services import task as task_service
from app.utils.dep import get_current_user
from app.utils.logging import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=schemas.Task)
async def create_task(
        task: schemas.TaskCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    try:
        return await task_service.create_task(db, task, current_user.id)
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[schemas.Task])
def read_tasks(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    return task_service.get_user_tasks(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_task = task_service.get_user_task(db, task_id=task_id, user_id=current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(
        task_id: int,
        task: schemas.TaskUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_task = await task_service.update_user_task(db, task_id=task_id, user_id=current_user.id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    try:
        await task_service.delete_user_task(db, task_id=task_id, user_id=current_user.id)
        return {"message": "Task deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
