from starlette.responses import RedirectResponse

from aia_api.src.core.server import get_application
from aia_api.src.core.settings import load_settings

#  Load application settings
settings = load_settings()

# Get FastAPI application
app = get_application(
    project_name=settings.PROJECT_NAME,
    api_prefix=settings.API_PREFIX,
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
)

# Redirect API user to the docs
@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
