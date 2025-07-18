from fastapi import APIRouter, status, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from tweet.utils.database import get_db
from tweet.schemas import user as schemas
from tweet.repositories import user
from tweet.utils import oauth2

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

###############################################################################################################

@router.post("", response_model=schemas.UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    return user.create(request, db)
###############################################################################################################

@router.get("/{user_id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user details by user ID.
    """
    return user.get_user_by_id(user_id, db)
###############################################################################################################

@router.delete("/delete_all", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_users(background_tasks: BackgroundTasks,
                 db: Session = Depends(get_db),
                ):
    """
    Delete all users.
    """
    # This function is not implemented in the repository, but you can add it if needed.
    return user.batch_delete_users(db, background_tasks)
###############################################################################################################

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by user ID.
    """
    return user.delete_user(user_id, db)
###############################################################################################################