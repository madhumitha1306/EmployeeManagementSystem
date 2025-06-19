from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from emp.database import get_db
from emp.models.performance_review import PerformanceReview
from emp.schemas import PerformanceReviewBase, PerformanceReviewOut
import uuid

router = APIRouter(prefix="/performance-reviews", tags=["Performance Reviews"])

@router.post("/", response_model=PerformanceReviewOut)
def create_performance_review(request: PerformanceReviewBase, db: Session = Depends(get_db)):
    review = PerformanceReview(
        
        employee_id=request.employee_id,
        reviewer_id=request.reviewer_id,
        review_date=request.review_date,
        rating=request.rating,
        comments=request.comments,
        goals_set=request.goals_set
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/{employee_id}", response_model=list[PerformanceReviewOut])
def get_reviews_for_employee(employee_id: str, db: Session = Depends(get_db)):
    return db.query(PerformanceReview).filter(PerformanceReview.employee_id == employee_id).all()
