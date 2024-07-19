from .notes import api_router as notes_router
from .user import api_router as user_router

list_of_routes = [
    user_router,
    notes_router,
]


__all__ = [
    "list_of_routes",
]
