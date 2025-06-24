from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.tweet.utils.database import get_db
from src.tweet.schemas import user as schemas
from src.tweet.repositories import user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    return user.create(request, db)

@router.get("/{user_id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user details by user ID.
    """
    return user.get_user_by_id(user_id, db)