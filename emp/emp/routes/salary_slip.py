from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from emp.database import get_db
from emp.models.salary_slip import SalarySlip
from emp.schemas import SalarySlipBase, SalarySlipOut
from datetime import date
import uuid

router = APIRouter(prefix="/salary-slips", tags=["Salary Slips"])

@router.post("/", response_model=SalarySlipOut)
def create_salary_slip(request: SalarySlipBase, db: Session = Depends(get_db)):
    slip = SalarySlip(
        employee_id=request.employee_id,
        month=request.month,
        basic_salary=request.basic_salary,
        bonus=request.bonus,
        deductions=request.deductions,
        net_salary=request.net_salary,
        issued_date=date.today()
    )
    db.add(slip)
    db.commit()
    db.refresh(slip)
    return slip

@router.get("/{employee_id}", response_model=list[SalarySlipOut])
def get_salary_slips(employee_id: str, db: Session = Depends(get_db)):
    return db.query(SalarySlip).filter(SalarySlip.employee_id == employee_id).all()
