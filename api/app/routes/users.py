from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.models import User
from app.database.schemas import User, UserCreate
from app.database.database import get_db
from app.services import user as user_service
from app.utils.dep import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.get("/me", response_model=User)
def read_current_user(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return current_user
