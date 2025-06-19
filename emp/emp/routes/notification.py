from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from emp.database import get_db
from emp.models.notification import Notification
from emp.schemas import NotificationBase, NotificationOut
from datetime import datetime
import uuid

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=NotificationOut)
def create_notification(request: NotificationBase, db: Session = Depends(get_db)):
    notification = Notification(
        user_id=request.user_id,
        title=request.title,
        message=request.message,
        is_read=request.is_read,
        created_at=datetime.utcnow()
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

@router.get("/{user_id}", response_model=list[NotificationOut])
def get_notifications_for_user(user_id: str, db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == user_id).all()
