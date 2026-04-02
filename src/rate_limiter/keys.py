from fastapi import Request
from typing import Callable

type KeyExtractor = Callable[[Request], str]


def by_ip(request: Request) -> str:
    return request.client.host


def by_ip_and_route(request: Request) -> str:
    return f"{request.client.host}:{request.url.path}"
