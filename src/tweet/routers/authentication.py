from fastapi import APIRouter, Depends, HTTPException, status
from tweet.schemas import tokens as token_schemas, authentication as auth_schemas
from tweet.utils.database import get_db
from tweet.models import user as models
from tweet.utils.hashing import HashPassword
from sqlalchemy.orm import Session
from tweet.utils import tokens
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(
          form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    """
    Authenticate a user and return a token.
    """
    email = db.query(models.User).filter(models.User.email == form_data.username).first()
    print(email)
    if not email or not HashPassword.verify(form_data.password, email.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password"
        )
    access_token = tokens.create_access_token(
        data={"sub": email.email}
    )
    
    return token_schemas.Token(
        access_token=access_token,
        token_type="bearer"
    )