from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Bug
from ..schemas import BugCreate, BugUpdate, BugResponse
from typing import List

router = APIRouter(prefix="/api/bugs", tags=["bugs"])


@router.get("/", response_model=List[BugResponse])
def get_bugs(db: Session = Depends(get_db)):
    bugs = db.query(Bug).all()
    return bugs


@router.post("/", response_model=BugResponse, status_code=201)
def create_bug(bug: BugCreate, db: Session = Depends(get_db)):
    new_bug = Bug(**bug.model_dump())
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)
    return new_bug


@router.get("/{bug_id}", response_model=BugResponse)
def get_bug(bug_id: str, db: Session = Depends(get_db)):
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    return bug


@router.patch("/{bug_id}", response_model=BugResponse)
def update_bug(bug_id: str, updates: BugUpdate, db: Session = Depends(get_db)):
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(bug, key, value)
    db.commit()
    db.refresh(bug)
    return bug


@router.delete("/{bug_id}", status_code=204)
def delete_bug(bug_id: str, db: Session = Depends(get_db)):
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    db.delete(bug)
    db.commit()
