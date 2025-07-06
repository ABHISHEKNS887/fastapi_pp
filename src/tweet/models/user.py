from tweet.utils.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(50))
    email       = Column(String(100), unique=True)
    password    = Column(String(100))
    tweets      = relationship("Tweet", back_populates="user", cascade="all, delete-orphan")