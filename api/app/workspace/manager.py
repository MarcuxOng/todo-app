import asyncio

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = []
            self.active_connections[user_id].append(websocket)

    async def disconnect(self, user_id: int, websocket: WebSocket):
        async with self.lock:
            if user_id in self.active_connections:
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]

    async def send_personal_message(self, user_id: int, message: dict):
        async with self.lock:
            if user_id in self.active_connections:
                for connection in self.active_connections[user_id]:
                    try:
                        await connection.send_json(message)
                    except WebSocketDisconnect:
                        await self.disconnect(user_id, connection)

    async def broadcast_task_update(self, task_id: int, action: str, data: dict):
        async with self.lock:
            for user_id, connections in self.active_connections.items():
                message = {
                    "event": f"task_{action}",
                    "data": {**data, "task_id": task_id}
                }
                for connection in connections:
                    try:
                        await connection.send_json(message)
                    except WebSocketDisconnect:
                        await self.disconnect(user_id, connection)


manager = ConnectionManager()
