from .user import api_router as user_router


list_of_routes = [
    user_router,
]


__all__ = [
    "list_of_routes",
]
