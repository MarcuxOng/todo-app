from typing import Type
from sqlalchemy.orm import Session

from app.database.models import ActivityLog


def log_activity(
        db: Session,
        user_id: int,
        action: str,
        entity_type: str,
        entity_id: int,
        details: dict | None = None
) -> ActivityLog:
    activity = ActivityLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )
    db.add(activity)
    db.commit()
    return activity


def get_user_activity(db: Session, user_id: int, limit: int = 100) -> list[Type[ActivityLog]]:
    return db.query(ActivityLog).filter(
        ActivityLog.user_id == user_id
    ).order_by(
        ActivityLog.created_at.desc()
    ).limit(limit).all()


def get_entity_activity(db: Session, entity_type: str, entity_id: int) -> list[Type[ActivityLog]]:
    return db.query(ActivityLog).filter(
        ActivityLog.entity_type == entity_type,
        ActivityLog.entity_id == entity_id
    ).order_by(
        ActivityLog.created_at.desc()
    ).all()
