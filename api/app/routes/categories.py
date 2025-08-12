from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.database import schemas, models
from app.services import category as category_service

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=schemas.Category)
def create_category(
        category: schemas.CategoryCreate,
        db: Session = Depends(get_db)
):
    db_category = models.Category(name=category.name)
    return category_service.create_category(db, db_category)


@router.get("/", response_model=List[schemas.Category])
def read_categories(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return category_service.get_categories(db, skip=skip, limit=limit)


@router.post("/{task_id}/add/{category_id}", response_model=schemas.Task)
def add_category_to_task(
        task_id: int,
        category_id: int,
        db: Session = Depends(get_db),
):
    return category_service.add_category_to_task(db, task_id, category_id)
