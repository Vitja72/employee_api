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
        raise HTTPException(status_code=400, details=str(e))




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8000)