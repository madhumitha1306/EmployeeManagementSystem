from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from emp.models import user as user_model
from emp.models import employee as employee_model
from emp import schemas
from emp import database
from emp.jwt_token import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# ✅ GET - Fetch ALL users + employee info (Admins/HR only)
@router.get("/all", response_model=list[schemas.DashboardOut])
def get_all_dashboards(
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    if current_user.role.lower() not in ["admin", "hr"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or HR can view all users")

    users = db.query(user_model.User).options(joinedload(user_model.User.employee)).all()

    return [
        {
            "user": schemas.UserOut.model_validate(user),
            "employee": schemas.EmployeeOut.model_validate(user.employee) if user.employee else None
        }
        for user in users
    ]




# ✅ GET - Fetch user and employee info by custom_id
@router.get("/{custom_id}", response_model=schemas.DashboardOut)
def get_dashboard(
    custom_id: str,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    user = (
        db.query(user_model.User)
        .options(joinedload(user_model.User.employee))
        .filter(user_model.User.custom_id == custom_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Restrict employee from accessing others' data
    if current_user.role.lower() not in ["admin", "hr"] and current_user.custom_id != custom_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

    return {
        "user": schemas.UserOut.model_validate(user),
        "employee": schemas.EmployeeOut.model_validate(user.employee) if user.employee else None
    }

# ✅ POST - Create employee profile (Employee only for their account)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    if current_user.employee:
        raise HTTPException(status_code=400, detail="Employee profile already exists")

    new_employee = employee_model.Employee(**employee.dict(), user_id=current_user.id)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "message": "Employee created successfully",
        "employee": schemas.EmployeeOut.model_validate(new_employee)
    }

# ✅ PUT - Update employee profile (Employee updates self only)
@router.put("/", status_code=status.HTTP_200_OK)
def update_employee(
    update_data: schemas.EmployeeUpdate,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    if not current_user.employee:
        raise HTTPException(status_code=404, detail="Employee record not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(current_user.employee, key, value)

    db.commit()
    db.refresh(current_user.employee)

    return {"message": "Employee updated successfully"}

# ✅ DELETE - Delete user and employee (Admins/HR can delete anyone, others can delete themselves only)
@router.delete("/{custom_id}")
def delete_dashboard(
    custom_id: str,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    user = db.query(user_model.User).filter(user_model.User.custom_id == custom_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user.role.lower() not in ["admin", "hr"] and current_user.custom_id != custom_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

    # Delete employee first (if any), then user
    if user.employee:
        db.delete(user.employee)
    db.delete(user)
    db.commit()

    return {"detail": "User and employee record deleted successfully"}
