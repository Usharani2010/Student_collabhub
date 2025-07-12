import jwt
from datetime import datetime, timedelta
import bcrypt

KEY = "STUDENT_COLLABORATION_APP_KEY"

def create_jwt_token(data: dict) -> str:
    payload = {
        "email": data.get("email"),
        "name": data.get("name"),
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, KEY, algorithm="HS256")
    return token


def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    
def validate_jwt_token(token: str) -> bool:
    try:
        jwt.decode(token, KEY, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def get_hashed_password(password: str) -> str:
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    return hashed_password.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))