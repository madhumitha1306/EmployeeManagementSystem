# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from emp.database import Base, engine
from emp.routes import user, auth, dashboard, attendance, audit_log, department
from emp.routes import leave_request, salary_slip, performance_review, notification

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System",
    description="Manage employees, attendance, departments, and more.",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Routers
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(department.router)
app.include_router(attendance.router)
app.include_router(leave_request.router)
app.include_router(salary_slip.router)
app.include_router(performance_review.router)
app.include_router(notification.router)
app.include_router(audit_log.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Employee Management System API"}
