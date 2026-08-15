from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

class AddCoinsRequest(BaseModel):
    user_id: int
    amount: float

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.post("/add-coins")
def add_coins(
    data: AddCoinsRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Temporary: jasko token cha tyaslai allow (testing ko lagi)
    # Production ma is_admin check enable garnu
    # if not getattr(current_user, "is_admin", False):
    #     raise HTTPException(status_code=403, detail="Admin only")

    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    user.coins += data.amount
    db.commit()
    db.refresh(user)

    return {
        "message": "Coins added successfully",
        "user_id": user.id,
        "username": user.username,
        "new_balance": user.coins
    }
