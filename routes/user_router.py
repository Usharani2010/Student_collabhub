from models.users import *
from fastapi import APIRouter, HTTPException, Path, Header
from db import db  
from utils import get_hashed_password, check_password, create_jwt_token, decode_jwt_token
from uuid import uuid4

import jwt
from typing import Dict


router= APIRouter()

@router.post("/sign-up", response_model=dict)
async def create_user(user: User):
    user_exists = await db.users.find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=400, detail="User with this email already exists")
   
    user.password = get_hashed_password(user.password)
    user_dict = user.dict()
    user_dict["user_id"] = uuid4().hex
    result = await db.users.insert_one(user_dict)
    if result.acknowledged:
        return {
            "status": "success",
            "message": "User created successfully",
            "data": {
                "user_id": user_dict["user_id"],
                "email": user.email,
            }
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
@router.post("/login", response_model=dict)
async def user_login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found! sign-up first")
    if not check_password(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Invalid password")
    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "id": str(db_user['_id']),
            "email": db_user['email'],
            "token": create_jwt_token({"email": db_user['email']})
        }
    }
           
@router.get("/", response_model=dict)
async def get_users():
    users = await db.users.find({}, {"_id": 0}).to_list(length=100)
    return {
        "status": "success",
        "message": "Users retrieved successfully",
        "data": users
    }
    


   
