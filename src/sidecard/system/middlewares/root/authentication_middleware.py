# !/usr/bin/python3
# type: ignore

# ** info: python imports
from typing import Callable
import contextvars
import logging

# ** info: typing imports
from typing import Self
from typing import Dict

# ** info: starlette imports
from starlette.responses import StreamingResponse
from starlette.requests import Request

# ** info: fastapi imports
from fastapi.responses import JSONResponse
from fastapi import status

# ** info: sidecards.system.artifacts imports
from src.sidecard.system.artifacts.env_provider import EnvProvider

# ** info: sidecards.system.middlewares.inheritables imports
from src.sidecard.system.middlewares.inheritables.base_middleware import BaseMiddleware

__all__: list[str] = ["AuthenticationMiddleware"]


class AuthenticationMiddleware(BaseMiddleware):
    def __init__(self: Self) -> None:
        self._env_provider: EnvProvider = EnvProvider()

    async def __call__(self: Self, request: Request, call_next: Callable) -> StreamingResponse:
        logging.debug("authentication middleware started")

        loguru_context: Dict = await self._set_values_from_request_context_to_dict(context=contextvars.copy_context(), context_key=r"loguru_context")
        internal_id: str = loguru_context[r"internalId"]
        is_authenticated: bool = False

        if is_authenticated:
            logging.info(f"the request with id {internal_id} was successfully authorized")
            response: StreamingResponse = await call_next(request)
            logging.debug("authentication middleware ended")
            return response
        else:
            logging.error(f"the request with id {internal_id} was not successfully authorized")
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={r"detail": r"Internal Server Error"})
