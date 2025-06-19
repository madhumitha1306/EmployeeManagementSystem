from sqlalchemy import Column, Integer, ForeignKey, Date, String
from emp.database import Base

class PerformanceReview(Base):
    __tablename__ = "performance_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    review_date = Column(Date)
    rating = Column(Integer)
    comments = Column(String)
    goals_set = Column(String)
