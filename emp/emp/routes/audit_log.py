from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from emp.database import get_db
from emp.models.audit_log import AuditLog
from emp.schemas import AuditLogCreate, AuditLogOut
import uuid
from datetime import datetime

router = APIRouter(prefix="/logs", tags=["Audit Logs"])

@router.post("/", response_model=AuditLogOut)
def create_log(request: AuditLogCreate, db: Session = Depends(get_db)):
    log = AuditLog(
        user_id=request.user_id,
        action=request.action,
        table_name=request.table_name,
        record_id=request.record_id,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/{user_id}", response_model=list[AuditLogOut])
def get_logs(user_id: str, db: Session = Depends(get_db)):
    return db.query(AuditLog).filter(AuditLog.user_id == user_id).order_by(AuditLog.timestamp.desc()).all()
