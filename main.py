from fastapi import FastAPI, Depends, HTTPException, ststus
from sqlalchemy.orm import Session
from database import get_db
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status":"all good and dandy"}
