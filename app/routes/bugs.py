from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..auth import get_current_user
from ..database import get_db
from ..models import Bug, User, StatusEnum, PriorityEnum
from ..schemas import BugCreate, BugUpdate, BugResponse

router = APIRouter(prefix="/api/bugs", tags=["bugs"])


@router.get("/", response_model=List[BugResponse])
def get_bugs(
    db: Session = Depends(get_db),
    status: StatusEnum | None = None,
    priority: PriorityEnum | None = None,
    author_id: str | None = None,
    assignee_id: str | None = None,
):
    query = db.query(Bug)

    if status:
        query = query.filter(Bug.status == status)
    if priority:
        query = query.filter(Bug.priority == priority)
    if author_id:
        query = query.filter(Bug.author_id == author_id)
    if assignee_id:
        query = query.filter(Bug.assignee_id == assignee_id)

    return query.all()


@router.post("/", response_model=BugResponse, status_code=201)
def create_bug(
    bug: BugCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_bug = Bug(**bug.model_dump(), author_id=current_user.id)
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
def update_bug(
    bug_id: str,
    updates: BugUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    if bug.author_id != current_user.id and bug.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this bug")
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(bug, key, value)
    db.commit()
    db.refresh(bug)
    return bug


@router.delete("/{bug_id}", status_code=204)
def delete_bug(
    bug_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    if bug.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this bug")
    db.delete(bug)
    db.commit()
