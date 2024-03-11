# DEPENENCIES
## Third-Party
from fastapi import APIRouter
## Local
from .chat.routes import router as _chat_router
from .pages.routes import router as _pages_router
from .user.routes import router as _user_router


# CONSTANTS
ROUTERS: tuple[APIRouter, ...] = (
    _chat_router,
    _pages_router,
    _user_router
)