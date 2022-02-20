from logging import getLogger

from fastapi import FastAPI
from src.api import health_check, reorder
from src.configurations import Configurations

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
    health_check.router,
    prefix=f"{base_prefix}/health-check",
    tags=["health_check"],
)

app.include_router(
    reorder.router,
    prefix=f"{base_prefix}/reorder",
    tags=["reorder"],
)
