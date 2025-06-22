from fastapi import APIRouter, Depends, HTTPException, status
from src.tweet.schemas import tokens as token_schemas
from src.tweet.utils.database import get_db
from src.tweet.models import user as models
from src.tweet.utils.hashing import HashPassword
from sqlalchemy.orm import Session
from src.tweet.utils import tokens
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    """
    Authenticate a user and return a token.
    """
    email = db.query(models.User).filter(models.User.email == request.username).first()
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not HashPassword.verify(request.password, email.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    access_token = tokens.create_access_token(
        data={"sub": email.email}
    )
    
    return token_schemas.Token(
        access_token=access_token,
        token_type="bearer"
    )