from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Old user route - Keeping just in case needed for now
# @router.post("/", response_model=UserResponse, status_code=201)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     existing = db.query(User).filter(User.email == user.email).first()
#     if existing:
#         raise HTTPException(status_code=409, detail="Email already registered")
#     new_user = User(**user.model_dump())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
