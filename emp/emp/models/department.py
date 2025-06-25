from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from emp.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ensure autoincrement is set
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
