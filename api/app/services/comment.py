from sqlalchemy.orm import Session

from app.database.schemas import CommentCreate
from app.database.models import Comment


def create_comment(db: Session, comment: CommentCreate, task_id: int, author_id: int):
    db_comment = Comment(
        text=comment.text,
        task_id=task_id,
        author_id=author_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_task_comments(db: Session, task_id: int):
    return db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at).all()
