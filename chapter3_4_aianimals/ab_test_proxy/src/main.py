from logging import getLogger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.configurations import Configurations
from src.proxy import proxy

logger = getLogger(__name__)


base_prefix = f"/v{Configurations.version.split('.')[0]}"

app = FastAPI(
    title=Configurations.api_title,
    description=Configurations.api_description,
    version=Configurations.version,
    openapi_url=f"{base_prefix}/openapi.json",
    docs_url=f"{base_prefix}/docs",
    redoc_url=f"{base_prefix}/redoc",
)

app.include_router(
    proxy.router,
    prefix=f"{base_prefix}/proxy",
    tags=["proxy"],
)
