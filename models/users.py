from pydantic import BaseModel, Field
from typing import Optional


import uuid

class User(BaseModel):
    user_id: Optional[str] = None
    name: str
    email: str
    bio: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: str 
    password: str 