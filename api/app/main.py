from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    activity,
    auth, 
    categories, 
    comments, 
    sharing, 
    tasks, 
    users, 
    websockets, 
    workspaces
)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(categories.router)
app.include_router(sharing.router)
app.include_router(comments.router)
app.include_router(websockets.router)
app.include_router(workspaces.router)
app.include_router(activity.router)


@app.get("/")
def read_root():
    return {"message": "Todo API is running"}
