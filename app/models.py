from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(255), default="")
    coins = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    rooms = relationship("Room", back_populates="host")
    gifts_sent = relationship("GiftTransaction", foreign_keys="GiftTransaction.sender_id")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    room_type = Column(String(20), default="voice")  # voice / video
    host_id = Column(Integer, ForeignKey("users.id"))
    is_live = Column(Boolean, default=True)
    max_users = Column(Integer, default=20)
    created_at = Column(DateTime, default=datetime.utcnow)

    host = relationship("User", back_populates="rooms")

class Gift(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String(255), default="")

class GiftTransaction(Base):
    __tablename__ = "gift_transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    gift_id = Column(Integer, ForeignKey("gifts.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
