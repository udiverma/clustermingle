from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    industry: str
    topics: str
    fun_fact: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    n_clusters: int = 7

class GroupRotate(BaseModel):
    previous_groups: List[List[int]]
    n_clusters: int = 7

class GroupAssignment(BaseModel):
    groups: List[List[int]]