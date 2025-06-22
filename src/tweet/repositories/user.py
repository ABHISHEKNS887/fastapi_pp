from sqlalchemy.orm import Session
from src.tweet.utils.hashing import HashPassword
from src.tweet.models import user as models
from src.tweet.schemas import user as schemas
from fastapi import HTTPException

def create(request: schemas.User, db: Session):
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail=f"User with this email {request.email} already exists")
    new_user = models.User(
                name=request.name,
                email=request.email,
                password=HashPassword.bcrypt(request.password)
                )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user

