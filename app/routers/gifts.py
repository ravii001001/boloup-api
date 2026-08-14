from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/gifts", tags=["Gifts"])

@router.post("/send")
def send_gift(
    gift_data: schemas.GiftSend,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    gift = db.query(models.Gift).filter(models.Gift.id == gift_data.gift_id).first()
    if not gift:
        raise HTTPException(status_code=404, detail="Gift not found")

    if current_user.coins < gift.price:
        raise HTTPException(status_code=400, detail="Not enough coins")

    receiver = db.query(models.User).filter(models.User.id == gift_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    # Deduct & credit
    current_user.coins -= gift.price
    receiver.coins += gift.price * 0.7  # 30% platform fee example

    transaction = models.GiftTransaction(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        gift_id=gift.id,
        room_id=gift_data.room_id
    )
    db.add(transaction)
    db.commit()

    return {"message": "Gift sent successfully", "remaining_coins": current_user.coins}
