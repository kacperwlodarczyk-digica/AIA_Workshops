from typing import Sequence

from fastapi import FastAPI

from api.src.v1.router import api_router
from api.src.core.app_container import AppContainer


def get_application(project_name: str, api_prefix: str) -> FastAPI:
    """Initialize and configure App"""
    # Create AppContainer instance (it contains app dependencies)
    container = AppContainer()
    # Init container resources
    container.init_resources()
    app = FastAPI(title=project_name, openapi_url=f"{api_prefix}/openapi.json")
    app.container = container

    app.include_router(api_router, prefix=api_prefix)
    return app
