from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid

class Creator(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Post(BaseModel):
    post_id: Optional[str] = None
    type: str
    title: str
    content: str
    file_url: Optional[str] = None
    tags: Optional[List[str]] = None
    created_by: Optional[Creator] = None
    created_at: Optional[datetime] = None
