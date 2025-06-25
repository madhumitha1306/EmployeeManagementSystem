from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from emp.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    custom_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime)

    # 👇 One-to-one relationship
    employee = relationship("Employee", back_populates="user", uselist=False)
