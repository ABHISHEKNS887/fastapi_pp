from pydantic import BaseModel, Field
from datetime import datetime

class TweetCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=280, description="This is a sample tweet content.")
    image_url: str | None = Field(None, description="https://example.com/image.jpg")

    class Config:
        from_attributes = True

class ShowTweet(BaseModel):
    id: int
    content: str
    email: str
    created_at: datetime
    updated_at: datetime
    image_url: str | None