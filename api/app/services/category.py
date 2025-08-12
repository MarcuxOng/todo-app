from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.database.models import Category, Task


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def add_category_to_task(db: Session, task_id: int, category_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    category = get_category(db, category_id)

    if not task or not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or category not found"
        )

    if category not in task.categories:
        task.categories.append(category)
        db.commit()

    return task
