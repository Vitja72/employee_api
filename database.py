from sqlalchemy import create_engine, Column, Integer, String, Float, Datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DATABASE_URL = "postgresql://api_user:secure_password_123@localhost:5432/employees_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EmployeeDB[Base]:
    __tablename__ = "emlpoyees"

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String(100), nullable=False)
    email= Column(String(255), unique=True, nullable=False, index=True)
    postition= Column(String(100), nullable=True)
    start_date= Column(Datetime,nullable=True)
    salery= Column(Float, nullable=True)
    created_at= Column(Datetime, default=datetime.utcnow)
    updated_at= Column(Datetime, nullable=True)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

