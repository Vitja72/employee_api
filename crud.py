from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import EmployeeDB
from models import EmployeeCreate, EmployeeUpdate
from datetime import datetime


def create_employee(db: Session, employee: EmployeeCreate):
    existing = db.query(EmployeeDB).filter(EmployeeDB.email == employee.email).first()
    if existing:
        raise ValueError("Email bereits vergeben")


    db_employee = EmployeeDB(
        
        name= employee.name,
        email= employee.email,
        position= employee.position,
        start_date= employee.start_date,
        salary= employee.salary,
        created_at= datetime.utcnow()
    )
    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError:
        db.rollback()
        raise ValueError("Fehler beim speicher")
    
def get_employee(db: Session, employee_id: int):
    return db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()

def get_employees(db: Session, skip: 0, limit: int=100):
    return db.query(EmployeeDB).offset(skip).limit(limit).all()

def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate):
    db_employee = db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()

    if not db_employee:
        return None
    
    if employee_update.email and employee_update.email != db_employee.email:
        existing = db.query(EmployeeDB).filter(EmployeeDB.email == employee_update.email).first()

        if existing:
            raise ValueError("Email bereits vergeben")
    update_data = employee_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_employee, key, value)

    db_employee.updated_at = datetime.utcnow()

    try: 
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError:
        db.rollback()
        raise ValueError("Fehler beim aktualisieren") 


def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()

    if db_employee:
        db.delete(db_employee)
        db.commit()

        return True
    return False 


