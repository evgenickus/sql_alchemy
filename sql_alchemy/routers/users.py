from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from .dependencies import get_db


router = APIRouter()

@router.get("/{username}", response_model=schemas.UserBase)
def search_user_by_username(username: str, db: Session = Depends(get_db)):
  user = crud.get_user_by_username(db, username)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  print(user.hashed_password)
  return user

@router.get("/", response_model=List[schemas.UserBase])
def read_users(db: Session = Depends(get_db)):
  users = crud.get_users(db)
  if not users:
    raise HTTPException(status_code=404, detail="There is not any users in database")
  return users

@router.post("/", response_model=schemas.UserBase)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_username(db, user.username)
  if db_user:
    raise HTTPException(status_code=409, detail=f"User with username: '{user.username}' already exists")
  db_user = crud.get_user_by_email(db, user.email)
  if db_user:
    raise HTTPException(status_code=409, detail=f"User with email: '{user.email}' already exists")
  return crud.create_user(db, user)