import jwt 
from datetime import datetime, timedelta, UTC
from typing import Dict

def create_jwt_token(data: dict) -> str:
    payload={
        "email" : data.get("email"),
        "exp" : datetime.now(UTC) + timedelta(hours=1),  # Token valid for 1 day
    }
    token = jwt.encode(payload, "MY_SECRET_KEY", algorithm="HS256")
    return token

def decode_jwt_token(token: str) -> Dict[str, str]:
    try:
        decoded = jwt.decode(token, "MY_SECRET_KEY", algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


print(create_jwt_token({"email": "usha123@gmail.com"}))