from datetime import timedelta

from app.database.models import User
from app.services.user import get_user_by_username
from app.utils.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


def authenticate_user(username: str, password: str, db):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_user_token(user: User):
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
