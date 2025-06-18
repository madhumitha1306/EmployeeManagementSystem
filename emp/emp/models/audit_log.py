from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from emp.database import Base
import uuid
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    table_name = Column(String, nullable=True)
    record_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
