from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from emp.database import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date)
    status = Column(String)
    check_in_time = Column(Time, nullable=True)
    check_out_time = Column(Time, nullable=True)
    created_at = Column(DateTime)

    employee = relationship("Employee", back_populates="attendances")
