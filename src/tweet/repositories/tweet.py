from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from tweet.models import tweet as models
from tweet.schemas import tweet as schemas
from fastapi import HTTPException, status

###############################################################################################################
def create(content: str, db: Session, current_user, image_url: str | None = None):
    """
    Create a new tweet.
    """
    try:
        new_tweet = models.Tweet(content=content,
                                 email=current_user.email,
                                 image_url=image_url)
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
        return new_tweet
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating tweet: {str(e)}")
###############################################################################################################

def get_tweet_by_id(id: int, db: Session):
    """
    Get a tweet by ID.
    """
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")
    return tweet
###############################################################################################################

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid sort column: {sort_by}")

    sort_func = asc if sort_order == "asc" else desc
    query = query.order_by(sort_func(sort_column))

    if not query.count():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tweets found")

    # Pagination
    tweets = query.offset(skip).limit(limit).all()
    return tweets
###############################################################################################################

def update_tweet(id: int, tweet_data: schemas.TweetCreate, db: Session, current_user, image_url):
    """
    Update a tweet by ID.
    """
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")

    if tweet.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this tweet")

    try:
        if tweet_data.content is not None:
            tweet.content = tweet_data.content
        if image_url is not None:
            tweet.image_url = image_url
        db.commit()
        db.refresh(tweet)
        return tweet
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating tweet: {str(e)}")
###############################################################################################################
    
def delete_tweet(id: int, db: Session, current_user):
    """
    Delete a tweet by ID.
    """
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")

    if tweet.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this tweet")

    try:
        db.delete(tweet)
        db.commit()
        return {"detail": "Tweet deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error deleting tweet: {str(e)}")
###############################################################################################################