from urllib.parse import urlparse

from fastapi import FastAPI
from uvicorn import run

from easy_notes_api.config import get_settings
from easy_notes_api.endpoints import list_of_routes


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    settings = get_settings()
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
        {
            "name": "Notes",
            "description": "Create notes from text fragments and annotate them.",
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

if __name__ == "__main__":
    settings = get_settings()
    run(
        "easy_notes_api.__main__:app",
        host=urlparse(settings.APP_HOST).netloc,
        port=settings.APP_PORT,
        reload=True,
        reload_dirs=["easy_notes_api"],
        log_level="debug",
    )
