from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from emp.database import get_db
from emp.models.attendance import Attendance
from emp.schemas import AttendanceCreate, AttendanceOut
import uuid
from datetime import datetime

router = APIRouter(prefix="/attendance", tags=["Attendance"])



@router.post("/", response_model=AttendanceOut)
def mark_attendance(request: AttendanceCreate, db: Session = Depends(get_db)):
    record = Attendance(
        employee_id=request.employee_id,
        date=request.date,
        status=request.status,
        check_in_time=request.check_in_time,
        check_out_time=request.check_out_time,
        created_at=datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=list[AttendanceOut])
def list_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()
