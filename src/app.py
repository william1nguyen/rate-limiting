from fastapi import FastAPI, Request, HTTPException

from rate_limiter.middleware import RateLimit
from rate_limiter.strategies.token_bucket import TokenBucket
from rate_limiter.decorator import rate_limit
from rate_limiter.keys import by_ip_and_route

app = FastAPI()

limiter = RateLimit(factory=lambda key: TokenBucket(10, 2, 10.0))


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    key = request.client.host

    if not limiter.allow_request(key):
        raise HTTPException(status_code=429, detail="Too many requests")

    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(limiter.get_remaining(key))
    response.headers["X-RateLimit-Reset"] = str(limiter.get_reset_time(key))
    return response


@app.get("/api/search")
@rate_limit(limiter, key_extractor=by_ip_and_route)
async def root(request: Request):
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)
