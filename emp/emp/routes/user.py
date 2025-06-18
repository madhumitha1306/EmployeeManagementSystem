from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from emp.models import user as user_model
from emp.models import employee as employee_model
from emp import schemas, database
from emp.hashing import Hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    request: schemas.UserCreate,
    db: Session = Depends(database.get_db)
):
    # ✅ Check if email already exists
    if db.query(user_model.User).filter(user_model.User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Create and add user
    new_user = user_model.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ✅ Generate custom_id
    new_user.custom_id = f"DTG{new_user.id:03d}"
    db.commit()

    # ✅ Create linked employee
    emp = request.employee
    new_employee = employee_model.Employee(
        user_id=new_user.id,
        team=emp.team,
        positions=emp.positions,
        hire_date=emp.hire_date,
        place=emp.place,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "code": 201,
        "message": "User and Employee registered successfully",
        "user": {
            "id": new_user.custom_id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role,
        },
        "employee": {
            "team": new_employee.team,
            "positions": new_employee.positions,
            "hire_date": str(new_employee.hire_date),
            "place": new_employee.place,
        }
    }
