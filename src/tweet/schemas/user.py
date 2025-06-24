from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    id: int
    name: str
    email: str

    # Config class to enable ORM mode for compatibility with SQLAlchemy models
    class Config:
        from_attributes = True