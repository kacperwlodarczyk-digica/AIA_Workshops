import socket

import uvicorn
from starlette.responses import RedirectResponse

from api.src.core.server import get_application
from api.src.core.settings import load_settings


#  Load application settings
settings = load_settings()


# Get FastAPI application
app = get_application(
    project_name=settings.PROJECT_NAME,
    api_prefix=settings.API_VERSION_PREFIX,
)


# Redirect API user to the docs
@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    addr = s.getsockname()
    port = addr[1]
    s.close()

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, debug=True, workers=1)
