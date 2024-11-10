from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db import models
from ..schemas import schemas
from ..services import clustering

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.post("/groups/create", response_model=schemas.GroupAssignment)
def create_groups(params: schemas.GroupCreate, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=400, detail="No users available for grouping")
    groups = clustering.create_initial_groups(users, params.n_clusters)
    return {"groups": groups}

@router.post("/groups/rotate", response_model=schemas.GroupAssignment)
def rotate_groups(rotation: schemas.GroupRotate, db: Session = Depends(get_db)):
    new_groups = clustering.rotate_groups(
        previous_groups=rotation.previous_groups,
        n_clusters=rotation.n_clusters,
        db=db
    )
    return {"groups": new_groups}