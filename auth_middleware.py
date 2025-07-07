
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from utils import decode_jwt_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # List of endpoints that do NOT require authentication
        open_endpoints = [
            "/api/v1/users/login",
            "/api/v1/users/sign-up",
            "/openapi.json",
            "/docs",
            "/docs/oauth2-redirect",
            "/redoc"
        ]
        if request.url.path not in open_endpoints and request.url.path.startswith("/api/v1/users/"):
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Authorization header missing")
            token = token.strip()
            decoded = decode_jwt_token(token)
            if isinstance(decoded, dict) and decoded.get("error"):
                raise HTTPException(status_code=401, detail=decoded["error"])
        response = await call_next(request)
        return response
