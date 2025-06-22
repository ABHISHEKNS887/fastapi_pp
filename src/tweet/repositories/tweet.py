from sqlalchemy.orm import Session
from src.tweet.models import tweet as models
from src.tweet.schemas import tweet as schemas
from fastapi import HTTPException

def create(request: schemas.TweetCreate, db: Session, current_user):
    """
    Create a new tweet.
    """
    try:
        print(current_user)
        new_tweet = models.Tweet(**request.model_dump(), email=current_user.email)
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
        return new_tweet
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating tweet: {str(e)}")