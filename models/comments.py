from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Creator(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Comment(BaseModel):
    comment_id: Optional[str] = None
    post_id : str
    content : str
    created_by : Optional[Creator] = None
    created_at : datetime | None =None
