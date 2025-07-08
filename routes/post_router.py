
from models.post import *
from fastapi import APIRouter, HTTPException, Path, Header, File, UploadFile, Form
from db import db  
from typing import Dict
from utils import decode_jwt_token
import cloudinary
import cloudinary.uploader
import os
from datetime import datetime
import json
from cloudinary_util import upload_file_to_cloudinary
from uuid import UUID, uuid4

router= APIRouter()



@router.post("/create", response_model=dict)
async def create_post(
    type: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    tags: str = Form(None),
    file: UploadFile = File(None),
    Authorization: str = Header(None)
):
    user_data = decode_jwt_token(Authorization)
    tags_list = []
    if tags:
        try:
            tags_list = json.loads(tags)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid tags format. Please provide a valid JSON array.")


    file_url = None
    if file:
        file_url = upload_file_to_cloudinary(file.file)
        if not file_url:
            raise HTTPException(status_code=500, detail="File upload to Cloudinary failed")


   
    post_dict = {
        "post_id": uuid4().hex,
        "type": type,
        "title": title,
        "content": content,
        "tags": tags_list,
        "file_url": file_url,
        "created_by": user_data.get("email"),
        "created_at": datetime.utcnow()
    }

    result = await db.posts.insert_one(post_dict)

    if result.acknowledged:
        post_dict["_id"] = str(result.inserted_id)
        return {
            "status": "success",
            "message": "Post created successfully",
            "data": post_dict
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to create post")
  

@router.get("/by-user", response_model=dict)
async def get_posts_by_user(Authorization: str = Header(None)):
    user_data = decode_jwt_token(Authorization)
    user_email = user_data.get("email")
    
    if not user_email:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    user_posts = await db.posts.find({"created_by": user_email}, {"_id": 0}).to_list(length=100)

    return {
        "status": "success",
        "data": user_posts
    }


@router.get("/", response_model=dict)
async def get_posts():
    all_posts = await db.posts.find({}, {"_id": 0}).to_list(length=100)
    return {
        "status": "success",
        "message": "Posts retrieved successfully",
        "data": all_posts
    }

@router.get("/{post_id}/comments", response_model=dict)
async def get_comments_by_post(post_id : str ):
    post_exists = await db.posts.find_one({"post_id": post_id})
    if not post_exists:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = await db.comments.find({"post_id": post_id }, 
                                      {"_id": 0}).sort({"created_at" : -1}).to_list(length=None)
    return {
        "status": "success",
        "message": "Comments retrieved successfully",
        "data": comments
    }

@router.put("/update/{post_id}", response_model=dict)
async def update_post(
    post_id: str,
    type: str = Form(None),
    title: str = Form(None),
    content: str = Form(None),
    tags: str = Form(None),
    file: UploadFile = File(None),
    Authorization: str = Header(None)
):
    user_data = decode_jwt_token(Authorization)
    user_email = user_data.get("email")

    existing_post = await db.posts.find_one({"post_id": post_id})
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if existing_post["created_by"] != user_email:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    update_fields = {}

    if type is not None:
        update_fields["type"] = type
    if title is not None:
        update_fields["title"] = title
    if content is not None:
        update_fields["content"] = content
    if tags is not None:
        try:
            update_fields["tags"] = json.loads(tags)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid tags format. Please provide a valid JSON array.")
    if file is not None:
        file_url = upload_file_to_cloudinary(file.file)
        if not file_url:
            raise HTTPException(status_code=500, detail="File upload to Cloudinary failed")
        update_fields["file_url"] = file_url

    update_fields["updated_at"] = datetime.utcnow()

    result = await db.posts.update_one({"post_id": post_id}, {"$set": update_fields})

    if result.modified_count == 1:
        updated_post = await db.posts.find_one({"post_id": post_id}, {"_id": 0})
        return {
            "status": "success",
            "message": "Post updated successfully",
            "data": updated_post
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to update post or no changes made")
