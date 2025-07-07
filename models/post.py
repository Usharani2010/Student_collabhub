
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid

class Post(BaseModel):
    post_id: Optional[str] = None
    type: str
    title: str
    content: str
    file_url: Optional[str] = None
    tags: Optional[List[str]] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    