# emp/models/salary_slip.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from emp.database import Base

class SalarySlip(Base):
    __tablename__ = "salary_slips"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    month = Column(String, nullable=False)
    basic_salary = Column(Float, nullable=False)
    bonus = Column(Float, default=0.0)
    deductions = Column(Float, default=0.0)
    net_salary = Column(Float, nullable=False)
    issued_date = Column(Date, nullable=False)
