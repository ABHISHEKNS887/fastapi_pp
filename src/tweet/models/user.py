from tweet.utils.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # Added nullable constraint
    email = Column(String(length=50), unique=True, nullable=False)  # RFC max email length
    password = Column(String(250))  # Longer for hashed passwords
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tweets = relationship("Tweet", back_populates="user", cascade="all, delete-orphan")