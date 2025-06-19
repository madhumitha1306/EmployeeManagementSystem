from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from emp import schemas
from emp.database import get_db
from emp.models import leave_request as models

router = APIRouter(
    prefix="/leave_requests",
    tags=["Leave Requests"]
)

# Get all leave requests
@router.get("/", response_model=List[schemas.LeaveRequestOut])
def get_all_leave_requests(db: Session = Depends(get_db)):
    return db.query(models.LeaveRequest).all()


# Get a specific leave request by ID
@router.get("/{leave_id}", response_model=schemas.LeaveRequestOut)
def get_leave_request(leave_id: str, db: Session = Depends(get_db)):
    leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave


# Create a new leave request
@router.post("/", response_model=schemas.LeaveRequestOut, status_code=status.HTTP_201_CREATED)
def create_leave_request(request: schemas.LeaveRequestCreate, db: Session = Depends(get_db)):
    new_leave = models.LeaveRequest(**request.dict())
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave


# Update an existing leave request
@router.put("/{leave_id}", response_model=schemas.LeaveRequestOut)
def update_leave_request(leave_id: str, request: schemas.LeaveRequestUpdate, db: Session = Depends(get_db)):
    leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    for key, value in request.dict(exclude_unset=True).items():
        setattr(leave, key, value)
    db.commit()
    db.refresh(leave)
    return leave


# Delete a leave request
@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave_request(leave_id: str, db: Session = Depends(get_db)):
    leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    db.delete(leave)
    db.commit()
    return
