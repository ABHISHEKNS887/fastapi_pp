from fastapi import APIRouter, Depends, status
from src.tweet.schemas import tweet as schemas, user as schemas_user
from src.tweet.utils.database import get_db
from src.tweet.utils import oauth2
from sqlalchemy.orm import Session
from src.tweet.repositories import tweet

router = APIRouter(
    prefix="/tweet",
    tags=["Tweet"]
)

@router.post("/", response_model=schemas.ShowTweet, status_code=status.HTTP_201_CREATED)
async def create_tweet(request: schemas.TweetCreate, 
                       db: Session = Depends(get_db), 
                       current_user: schemas_user.User = Depends(oauth2.get_current_user)):
    """
    Create a new tweet.
    """
    return tweet.create(request, db, current_user)