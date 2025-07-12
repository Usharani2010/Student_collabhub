from fastapi import APIRouter, HTTPException, Path, Header
from db import get_database 
from datetime import datetime, UTC
from models.comments import Comment
from utils import decode_jwt_token
from uuid import UUID, uuid4

router= APIRouter()
db = get_database()

@router.post("/create", response_model=dict)
async def create_comment(comment: Comment, Authorization: str = Header(None)):
    user = decode_jwt_token(Authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    post_exists = await db.posts.find_one({"post_id": comment.post_id})
    user_exists = await db.users.find_one({"email": user["email"]})
    if not post_exists:
        raise HTTPException(status_code=404, detail="Post not found")
    user_data = decode_jwt_token(Authorization)
    comment_data = comment.dict()
    comment_data["comment_id"] = uuid4().hex
    if not comment_data.get("created_by"):
        comment_data["created_by"] = {
            "name": user_exists.get("name"),
            "email": user_exists.get("email")
        }
    if not comment_data.get("created_at"):
        comment_data["created_at"] = datetime.utcnow()
    result = await db.comments.insert_one(comment_data)
    if result.acknowledged:
        return {
            "status" : "success",
            "message": "Comment created successfully",
            "data":{
            "id": str(result.inserted_id),
            "comment_id":  comment_data["comment_id"],
            "content": comment_data["content"],
            "created_by": comment_data["created_by"],
            "created_at": comment_data["created_at"]
            }
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to create comment")  
    

