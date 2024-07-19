from fastapi import FastAPI
from .endpoints import list_of_routes
from .config import DefaultSettings


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    settings = DefaultSettings()
    for route in list_of_routes:
        application.include_router(route, prefix=settings.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates a microservice
    """
    description = "A microservice that allows you to save text notes."

    tags_metadata = [
        {
            "name": "User",
            "description": "Registration and authorization before further actions.",
        },
    ]

    application = FastAPI(
        title="EasyNotes",
        description=description,
        openapi_tags=tags_metadata,
    )
    bind_routes(application)
    return application


app = get_app()
