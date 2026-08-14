from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    coins: float

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class RoomCreate(BaseModel):
    title: str
    room_type: str = "voice"
    max_users: int = 20

class RoomOut(BaseModel):
    id: int
    title: str
    room_type: str
    host_id: int
    is_live: bool
    max_users: int
    created_at: datetime

    class Config:
        from_attributes = True

class GiftSend(BaseModel):
    gift_id: int
    receiver_id: int
    room_id: Optional[int] = None
