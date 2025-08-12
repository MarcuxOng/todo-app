from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.database.models import User
from app.utils.dep import get_current_user
from app.workspace.endpoints import handle_websocket_connection

router = APIRouter()


@router.websocket("/ws/tasks")
async def tasks_websocket(
        websocket: WebSocket,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    await handle_websocket_connection(websocket, current_user, db)
