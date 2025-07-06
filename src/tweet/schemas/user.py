from pydantic import BaseModel
from typing import List
from tweet.schemas.tweet import ShowTweet

class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    tweets: List[ShowTweet] = []

    # Config class to enable ORM mode for compatibility with SQLAlchemy models
    class Config:
        from_attributes = True