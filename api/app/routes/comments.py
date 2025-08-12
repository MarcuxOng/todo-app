from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, schemas, models
from app.services import comment as comment_service
from app.utils.dep import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/tasks/{task_id}", response_model=schemas.Comment)
def create_comment(
        task_id: int,
        comment: schemas.CommentCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    return comment_service.create_comment(
        db,
        comment=comment,
        task_id=task_id,
        author_id=current_user.id
    )


@router.get("/tasks/{task_id}", response_model=List[schemas.Comment])
def get_comments(
        task_id: int,
        db: Session = Depends(get_db)
):
    return comment_service.get_task_comments(db, task_id)
