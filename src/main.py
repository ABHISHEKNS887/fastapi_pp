from fastapi import FastAPI
from tweet.routers import authentication

app = FastAPI()

app.include_router(authentication.router)