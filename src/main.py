from fastapi import FastAPI, Request
from tweet.routers import authentication, user, tweet
from tweet import  models
from tweet.utils.database import engine
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from redis.asyncio import Redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize async Redis client
    redis = Redis.from_url("redis://localhost:6379/0")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # Cleanup
    await FastAPICache.clear()
    await redis.close()  # Proper async close

app = FastAPI(lifespan=lifespan)

# Initialize rate limiter (default: 5 requests/minute)
limiter = Limiter(
    key_func=get_remote_address
)
app.state.limiter = limiter

# Error handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(
        status_code=429,
        detail={"error": "Rate limit exceeded. Please try again later.", "retry_after": f"{exc.detail}"}
    )

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(tweet.router)