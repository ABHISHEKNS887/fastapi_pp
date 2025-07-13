from fastapi import File, UploadFile, Form
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Union

class TweetCreate(BaseModel):
    content: str = Form(...)
    image: Union[UploadFile, str, None] = None


class ShowTweet(BaseModel):
    id: int
    content: str
    email: str
    created_at: datetime
    updated_at: datetime
    image_url: str | None

    class Config:
        from_attributes = True