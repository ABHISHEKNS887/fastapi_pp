from fastapi import APIRouter, Depends, status, Query
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

@router.get("/{id}", response_model=schemas.ShowTweet, status_code=status.HTTP_200_OK)
async def get_tweet(id: int,
                    db: Session = Depends(get_db),
                    current_user: schemas_user.User = Depends(oauth2.get_current_user)):
    """Get a tweet by ID."""
    return tweet.get_tweet_by_id(id, db)

@router.get("/", response_model=list[schemas.ShowTweet], status_code=status.HTTP_200_OK)
async def get_all_tweets(db: Session = Depends(get_db),
                        skip: int = Query(0, ge=0),
                        limit: int = Query(10, le=100),
                        sort_by: str = Query("created_at", example="created_at"),
                        sort_order: str = Query("desc", regex="^(asc|desc)$"),
                        email: str | None = None):
    """Get all tweets."""
    return tweet.get_all_tweets(db, skip, limit, sort_by, sort_order, email)

@router.put("/{id}", response_model=schemas.ShowTweet, status_code=status.HTTP_200_OK)
async def update_tweet(id: int,
                       request: schemas.TweetCreate,
                       db: Session = Depends(get_db),
                       current_user: schemas_user.User = Depends(oauth2.get_current_user)):
    """Update a tweet by ID."""
    return tweet.update_tweet(id, request, db, current_user)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_tweet(id: int, 
                       db: Session = Depends(get_db),
                       current_user: schemas_user.User = Depends(oauth2.get_current_user)):
    """Delete a tweet by ID."""
    return tweet.delete_tweet(id, db, current_user)