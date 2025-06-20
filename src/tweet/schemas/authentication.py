from pydantic import BaseModel

class LogIn(BaseModel):
    email: str
    password: str