from fastapi import FastAPI, Path
import uvicorn
import os
from models.users import User
from models.post import Post
from routes.post_router import router as post_router
from routes.user_router import router as user_router
from routes.comment_router import router as comment_router
from fastapi.middleware.cors import CORSMiddleware
from auth_middleware import AuthMiddleware

app=FastAPI(
    title="Student Collaboration Hub",
    description="A platform for students to collaborate on projects, share resources, and connect with peers.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(post_router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(comment_router, prefix="/api/v1/comments", tags=["comments"])



if __name__ == "__main__":
     port = int(os.environ.get("PORT", 8000))
     uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)