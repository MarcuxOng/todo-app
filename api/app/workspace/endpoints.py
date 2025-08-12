from fastapi import WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database import get_db
from app.database.models import User
from app.workspace.manager import manager
import json


async def handle_websocket_connection(
        websocket: WebSocket,
        user: User,
        db: Session = Depends(get_db)
):
    await manager.connect(user.id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "complete_task":
                task_id = data.get("task_id")
                await manager.broadcast_task_update(
                    task_id=task_id,
                    action="updated",
                    data={"is_completed": True}
                )

    except WebSocketDisconnect:
        await manager.disconnect(user.id, websocket)
    except json.JSONDecodeError:
        await websocket.close(code=1003)
    except Exception as e:
        await websocket.close(code=1011)
