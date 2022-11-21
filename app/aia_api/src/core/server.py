from typing import Sequence

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from aia_api.src.v1.router import api_router
from aia_api.src.core.app_container import AppContainer


def get_application(project_name: str, api_prefix: str, cors_allowed_origins: Sequence[str]) -> FastAPI:
    """Initialize and configure App"""
    # Create AppContainer instance
    container = AppContainer()
    # Init container resources
    container.init_resources()
    app = FastAPI(title=project_name, openapi_url=f"{api_prefix}/openapi.json")
    app.container = container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=api_prefix)
    return app
