from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
Base = declarative_base()
# Replace this with your actual DB URL if needed (e.g., PostgreSQL URI)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Manjula@localhost:5432/emp_db"


# For SQLite, we need this connect_args
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()