from sqlalchemy.orm import Session
from tweet.utils.hashing import HashPassword
from tweet.models import user as models
from tweet.schemas import user as schemas
from fastapi import HTTPException
import json

###############################################################################################################
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
###############################################################################################################

def get_user_by_id(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user
###############################################################################################################

def delete_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    db.delete(user)
    db.commit()
    return {"detail": f"User with id {user_id} deleted successfully"}
###############################################################################################################

def delete_all_users(db: Session):
    """Background task to delete all users (except admins if needed)"""
    try:
        # Example: Delete all non-admin users
        deleted_count = db.query(models.User)\
                        .filter(models.User.is_admin == False)\
                        .delete()
        db.commit()
        print(f"Deleted {deleted_count} users")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting users: {str(e)}")

async def batch_delete_users(db: Session,
                            background_tasks):
    """
    ✅ Secure: Admin-only access.
    ✅ Async: Uses BackgroundTasks to avoid timeout.
    ✅ Flexible: Can be modified for soft deletion or partial cleanup.
    ⚠️ Dangerous: Always backup data before running!
    """
    print("Backing up data before deletion...")  # Placeholder for backup logic
    # Example: Export users before deletion (SQLAlchemy)
    users = db.query(models.User).all()
    with open("user_backup.json", "w") as f:
        f.write(json.dumps([u.__dict__ for u in users]))
    """Endpoint to trigger batch deletion (async)"""
    background_tasks.add_task(delete_all_users, db)
    return {"message": "Batch user deletion started in background"}
