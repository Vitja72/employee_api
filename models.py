from pydantic import BaseModel, EmailStr, Field 
from typing import Optional
from datetime import datetime 

class EmployeeBase(BaseModel):
    name: str = Field(min_length=2, max_length=100, description="Vollständiger Name")
    email: EmailStr = Field(description="Gültige Email-Adressse")
    position: Optional[str] = Field(None, max_length=100, description="Position/Rolle")
    start_date: Optional[datetime] = Field(None, description="Startdatum")


class EmployeeCreate(EmployeeBase):
    salary: Optional[float] = Field(None, ge=0, description="Gehalt (optional)")


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100 )
    email: Optional[EmailStr] = None 
    position: Optional[str] = Field(None, max_length=100)
    salary: Optional[float] = Field(None, ge=0)

class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = True 

