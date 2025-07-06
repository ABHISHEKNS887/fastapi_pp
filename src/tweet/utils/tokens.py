import os
import jwt

from datetime import datetime, timedelta, timezone
from tweet.schemas import tokens as schemas
from jwt import InvalidTokenError
from dotenv import load_dotenv

load_dotenv()  # Load .env file

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), 
                             algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def verify_tocken(token, credentials_exception):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"),
                             algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return schemas.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception