from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List 
from database import get_db
from models import Employee, EmployeeCreate, EmployeeUpdate
import crud

app = FastAPI(
    title = "Employee Management API",
    description = "Adding, reading, updating and deleting employees from Postgres DB.",
    version = "1.0"
)

@app.get("/health")
def health_check():
    return {"status":"all good and dandy"}

@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
def created_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        db_employee = crud.create_employee(db = db, employee = employee)
        return db_employee 
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/employees", response_model=List[Employee])

def get_employees_endpoint(skip: int= 0, limit: int=100, db:Session = Depends(get_db)):
    return crud.get_employees(db, skip = skip, limit = limit)

@app.get("/employees/{employee_id}", response_model=Employee)

def get_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id)

    if not db_employee:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} was not found.")
    return db_employee

@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee_endpoint(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        db_employee = crud.update_employee(db, employee_id, employee)
        if not db_employee:
            raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} was not found.")
        return db_employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.delete("/employees/{employee_id}")
def delete_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    success = crud.delete_employee(db, employee_id)

    if not success:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} was not found.")
    return {"message": f"Employee with ID {employee_id} was successfuly deleted."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8000)