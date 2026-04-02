from functools import wraps
from fastapi import Request, HTTPException
from rate_limiter.middleware import RateLimit
from rate_limiter.keys import KeyExtractor


def rate_limit(limiter: RateLimit, key_extractor: KeyExtractor):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            key = key_extractor(request)

            if not limiter.allow_request(key):
                HTTPException(status_code=429, detail="Too many requests")
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
