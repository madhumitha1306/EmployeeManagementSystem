from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import date, time, datetime
import re

# ----------------------------
# EMPLOYEE SCHEMAS
# ----------------------------

class EmployeeCreate(BaseModel):
    team: str
    positions: str
    hire_date: date
    place: str

class EmployeeUpdate(BaseModel):
    team: Optional[str] = None
    positions: Optional[str] = None
    hire_date: Optional[date] = None
    place: Optional[str] = None

class EmployeeOut(BaseModel):
    id: int
    user_id: int
    team: Optional[str] = None
    hire_date: Optional[date] = None
    positions: Optional[str] = None
    place: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


# ----------------------------
# USER SCHEMAS
# ----------------------------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    employee: EmployeeCreate  

    @field_validator("password")
    def password_strength(cls, v):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must include at least one special character")
        return v

    model_config = {
        "from_attributes": True
    }

class UserOut(BaseModel):
    id: int
    custom_id: Optional[str] = None
    name: str
    email: EmailStr
    role: str

    model_config = {
        "from_attributes": True
    }

# ----------------------------
# DASHBOARD SCHEMA
# ----------------------------

class DashboardOut(BaseModel):
    user: UserOut
    employee: Optional[EmployeeOut]  

    model_config = {
        "from_attributes": True
    }

# ----------------------------
# LOGIN SCHEMA
# ----------------------------

class Login(BaseModel):
    email: EmailStr
    password: str
    role: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    otp: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    def password_strength(cls, v):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must include at least one special character")
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirm password do not match")
        return self

# ----------------------------
# ADDITIONAL MODULE SCHEMAS
# ----------------------------

class DepartmentBase(BaseModel):
    name: str
class DepartmentCreate(DepartmentBase):
    name: str
    description: str
    
class DepartmentOut(DepartmentBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    check_in_time: time
    check_out_time: time
    status: str
class AttendanceCreate(BaseModel):
    employee_id: int
    date: date 
    status: str

    
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None

class AttendanceOut(AttendanceBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class LeaveRequestBase(BaseModel):
    employee_id: int
    from_date: date
    to_date: date
    leave_type: str
    reason: Optional[str]
    status: Optional[str] = "Pending"

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequestUpdate(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    reason: Optional[str]
    status: Optional[str]
class LeaveRequestOut(LeaveRequestBase):
    id: int
    applied_on: datetime

    model_config = {
        "from_attributes": True
    }

class SalarySlipBase(BaseModel):
    employee_id: int
    month: str  # Format: YYYY-MM
    basic_salary: float
    bonus: Optional[float] = 0.0
    deductions: Optional[float] = 0.0
    net_salary: float

class SalarySlipOut(SalarySlipBase):
    id: int
    issued_date: date

    model_config = {
        "from_attributes": True
    }

class PerformanceReviewBase(BaseModel):
    employee_id: int
    reviewer_id: int
    review_date: date
    rating: int
    comments: Optional[str] = None
    goals_set: Optional[str] = None

class PerformanceReviewOut(PerformanceReviewBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    is_read: bool = False

class NotificationOut(NotificationBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class AuditLogBase(BaseModel):
    user_id: int
    action: str
    table_name: str
    record_id: Optional[int] = None
class AuditLogCreate(AuditLogBase):
    pass

class AuditLogOut(AuditLogBase):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

class empdetails(BaseModel):

    
    
    team:Optional[str]
    positions: Optional[str]
    hire_date: Optional[date]
    place: Optional[str]

    model_config = {
        "from_attributes" : True
    }

class UserCreateWithEmployee(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    employee: empdetails

    model_config = {
        "from_attributes": True
    }