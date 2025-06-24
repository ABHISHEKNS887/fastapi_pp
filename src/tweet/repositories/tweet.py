from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from src.tweet.models import tweet as models
from src.tweet.schemas import tweet as schemas
from fastapi import HTTPException

def create(request: schemas.TweetCreate, db: Session, current_user):
    """
    Create a new tweet.
    """
    try:
        new_tweet = models.Tweet(**request.model_dump(), email=current_user.email)
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
        return new_tweet
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating tweet: {str(e)}")
    
def get_tweet_by_id(id: int, db: Session):
    """
    Get a tweet by ID.
    """
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet

def get_all_tweets(db: Session, skip: int = 0, 
                   limit: int = 100, 
                   sort_by: str = "created_at", 
                   sort_order: str = "desc", 
                   email: str | None = None):
    """
    Get all tweets.
    """
    # Base query
    query = db.query(models.Tweet)

    # Filtering
    if email:
        query = query.filter(models.Tweet.email == email)

    # Sorting
    try:
        sort_column = getattr(models.Tweet, sort_by)
    except AttributeError:
        raise HTTPException(status_code=400, detail=f"Invalid sort column: {sort_by}")

    sort_func = asc if sort_order == "asc" else desc
    query = query.order_by(sort_func(sort_column))

    # Pagination
    tweets = query.offset(skip).limit(limit).all()
    return tweets

def update_tweet(id: int, request: schemas.TweetCreate, db: Session, current_user):
    """
    Update a tweet by ID.
    """
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    if tweet.email != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to update this tweet")

    try:
        for key, value in request.model_dump().items():
            setattr(tweet, key, value)
        db.commit()
        db.refresh(tweet)
        return tweet
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating tweet: {str(e)}")
    
def delete_tweet(id: int, db: Session, current_user):
    """
    Delete a tweet by ID.
    """
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    if tweet.email != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to delete this tweet")

    try:
        db.delete(tweet)
        db.commit()
        return {"detail": "Tweet deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting tweet: {str(e)}")