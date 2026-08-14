from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, users, rooms, gifts
from .websocket import manager
import json

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BoloUp API",
    description="Live Streaming & Voice Room API (BoloUp style)",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(gifts.router)

@app.get("/")
def root():
    return {"message": "BoloUp API is running 🚀"}

@app.websocket("/ws/rooms/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            # Broadcast to everyone in the room
            await manager.broadcast(room_id, {
                "type": message.get("type", "chat"),
                "data": message.get("data"),
                "room_id": room_id
            })
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
