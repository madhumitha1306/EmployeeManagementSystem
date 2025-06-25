from sqlalchemy import Column, ForeignKey, Date, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from emp.database import Base

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True ,index=True, autoincrement=True)
    employee_id = Column(String, ForeignKey("employees.id"))
    from_date = Column(Date)
    to_date = Column(Date)
    leave_type = Column(String)
    reason = Column(String)
    status = Column(String, default="Pending")
    applied_on = Column(DateTime, default=datetime.utcnow)
