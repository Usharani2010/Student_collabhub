from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Comment(BaseModel):
    comment_id: Optional[str] = None
    post_id : str
    content : str
    created_by : str | None = None
    created_at : datetime | None =None