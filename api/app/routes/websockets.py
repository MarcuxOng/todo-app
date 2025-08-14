from fastapi import APIRouter, WebSocket, status
from app.utils.security import verify_token

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token or not verify_token(token):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast or process messages here
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
