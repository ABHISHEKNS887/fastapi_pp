from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import HTTPException

# Initialize rate limiter (default: 5 requests/minute)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5/minute"]
)
app.state.limiter = limiter

# Error handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return HTTPException(
        status_code=429,
        detail={"error": "Rate limit exceeded. Please try again later.", "retry_after": exc.detail}
    )