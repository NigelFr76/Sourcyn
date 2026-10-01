from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ProcurementRequest

router = APIRouter()

@router.get("/")
def get_all_requests(db: Session = Depends(get_db)):
    return db.query(ProcurementRequest).all()

@router.get("/{id}")
def get_request(id: int, db: Session = Depends(get_db)):
    req = db.query(ProcurementRequest).filter(ProcurementRequest.id == id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@router.post("/")
def create_request(title: str, natural_language: str, db: Session = Depends(get_db)):
    # In reality we'd use a Pydantic schema for input
    req = ProcurementRequest(
        title=title,
        natural_language_request=natural_language
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req
