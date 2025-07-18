from fastapi import APIRouter, Depends, status, Query, Request
from tweet.schemas import tweet as schemas, user as schemas_user
from tweet.utils.database import get_db
from tweet.utils import oauth2
from sqlalchemy.orm import Session
from tweet.repositories import tweet
from tweet.utils.cloudinary import upload_to_cloudinary
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/tweet",
    tags=["Tweet"]
)

# Get the limiter instance (no re-initialization)
limiter = Limiter(key_func=get_remote_address)

###############################################################################################################
@router.post("/", response_model=schemas.ShowTweet, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")  # Stricter limit for tweet creation
async def create_tweet(request: Request,  # Renamed to avoid conflict
                       tweet_data: schemas.TweetCreate = Depends(),  # Renamed from 'request'
                       db: Session = Depends(get_db), 
                       current_user: schemas_user.User = Depends(oauth2.get_current_user)):
    """
    Create a new tweet.
    """
    if tweet_data.image:
        # Upload image to Cloudinary and get the URL
        image_url = await upload_to_cloudinary(tweet_data.image)
    else:
        image_url = None
    return tweet.create(tweet_data.content, db, current_user, image_url)

###############################################################################################################

@router.get("/{id}", response_model=schemas.ShowTweet, status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")  # Stricter limit for tweet creation
@cache(expire=120)  # Cache for 60 seconds
async def get_tweet(request: Request, id: int,
                    db: Session = Depends(get_db)):
    """Get a tweet by ID."""
    return tweet.get_tweet_by_id(id, db)

###############################################################################################################

@router.get("/", response_model=list[schemas.ShowTweet], status_code=status.HTTP_200_OK)
async def get_all_tweets(db: Session = Depends(get_db),
                        skip: int = Query(0, ge=0),
                        limit: int = Query(10, le=100),
                        sort_by: str = Query("created_at", example="created_at"),
                        sort_order: str = Query("desc", regex="^(asc|desc)$"),
                        email: str | None = None):
    """Get all tweets."""
    return tweet.get_all_tweets(db, skip, limit, sort_by, sort_order, email)

###############################################################################################################

@router.put("/{id}", response_model=schemas.ShowTweet, status_code=status.HTTP_200_OK)
async def update_tweet(id: int,
                       tweet_data: schemas.TweetCreate = Depends(),
                       db: Session = Depends(get_db),
                       current_user: schemas_user.User = Depends(oauth2.get_current_user)):
    """Update a tweet by ID."""
    if tweet_data.image:
        # Upload image to Cloudinary and get the URL
        image_url = await upload_to_cloudinary(tweet_data.image)
    else:
        image_url = None
    return tweet.update_tweet(id, tweet_data, db, current_user, image_url)

###############################################################################################################

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_tweet(id: int, 
                       db: Session = Depends(get_db),
                       current_user: schemas_user.User = Depends(oauth2.get_current_user)):
    """Delete a tweet by ID."""
    return tweet.delete_tweet(id, db, current_user)

###############################################################################################################