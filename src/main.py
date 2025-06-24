from fastapi import FastAPI
from src.tweet.routers import authentication, user, tweet
from src.tweet import  models
from src.tweet.utils.database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(tweet.router)