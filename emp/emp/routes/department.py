from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from emp.database import get_db
from emp.models.department import Department
from emp.schemas import DepartmentCreate, DepartmentOut
import uuid
from datetime import datetime

router = APIRouter(prefix="/departments", tags=["Departments"])

# ✅ Create a department
@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(request: DepartmentCreate, db: Session = Depends(get_db)):
    existing = db.query(Department).filter(Department.name == request.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department with this name already exists")

    dept = Department(
        
        name=request.name,
        description=request.description,
        created_at=datetime.utcnow()
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

# ✅ List all departments
@router.get("/", response_model=list[DepartmentOut])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

# ✅ Get department by ID
@router.get("/{dept_id}", response_model=DepartmentOut)
def get_department(dept_id: str, db: Session = Depends(get_db)):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

# ✅ Delete department by ID
@router.delete("/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(dept_id: str, db: Session = Depends(get_db)):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    db.delete(dept)
    db.commit()
    return
