from fastapi import File, UploadFile, Form
from pydantic import BaseModel
from datetime import datetime

class TweetCreate(BaseModel):
    content: str = Form(...)
    image: UploadFile = File(None)


class ShowTweet(BaseModel):
    id: int
    content: str
    email: str
    created_at: datetime
    updated_at: datetime
    image_url: str | None

    class Config:
        from_attributes = True