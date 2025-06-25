from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from emp.database import get_db
from emp.models.audit_log import AuditLog
from emp.schemas import AuditLogCreate, AuditLogOut
import uuid
from datetime import datetime
from emp import schemas,database
from typing import List

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

# GET - Fetch all audit logs (admin-level access assumed)
@router.get("/", response_model=List[schemas.AuditLogOut])
def get_all_audit_logs(
    db: Session = Depends(database.get_db)
):
    logs = db.query(AuditLog.audit_logs).order_by(AuditLog.audit_logs.timestamp.desc()).all()
    return logs

@router.get("/{user_id}", response_model=list[AuditLogOut])
def get_logs(user_id: str, db: Session = Depends(get_db)):
    return db.query(AuditLog).filter(AuditLog.user_id == user_id).order_by(AuditLog.timestamp.desc()).all()
