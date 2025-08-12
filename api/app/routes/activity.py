from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Task, User
from app.database.schemas import ActivityLog
from app.services import activity_log as activity_service
from app.utils.dep import get_current_user

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("/me", response_model=list[ActivityLog])
def get_my_activity(
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return activity_service.get_user_activity(db, current_user.id, limit)


@router.get("/{entity_type}/{entity_id}", response_model=list[ActivityLog])
def get_entity_history(
        entity_type: str,
        entity_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Verify access rights first
    if entity_type == "task":
        task = db.query(Task).filter(
            Task.id == entity_id,
            Task.owner_id == current_user.id
        ).first()
        if not task:
            raise HTTPException(404, "Task not found or access denied")

    return activity_service.get_entity_activity(db, entity_type, entity_id)