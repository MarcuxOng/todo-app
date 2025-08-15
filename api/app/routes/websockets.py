from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User
from app.utils.dep import get_current_websocket_user
from app.workspace.endpoints import handle_websocket_connection

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user: User = Depends(get_current_websocket_user),
    db: Session = Depends(get_db),
):
    await handle_websocket_connection(websocket, user, db)
