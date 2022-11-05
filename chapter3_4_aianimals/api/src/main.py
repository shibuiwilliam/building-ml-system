from logging import getLogger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api import access_log, animal, animal_category, health_check, like, metadata, user, violation
from src.configurations import Configurations
from src.exceptions.custom_exceptions import APINotAllowedException, DatabaseException, StorageClientException

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


@app.exception_handler(DatabaseException)
async def database_exception_handler(
    request: Request,
    e: DatabaseException,
):
    logger.error(e)
    return JSONResponse(
        status_code=400,
        content={"message": e.message},
    )


@app.exception_handler(StorageClientException)
async def storage_client_exception_handler(
    request: Request,
    e: StorageClientException,
):
    logger.error(e)
    return JSONResponse(
        status_code=500,
        content={"message": e.message},
    )


@app.exception_handler(APINotAllowedException)
async def api_not_allowed_exception_handler(
    request: Request,
    e: APINotAllowedException,
):
    logger.error(e)
    return JSONResponse(
        status_code=403,
        content={"message": e.message},
    )


app.include_router(
    health_check.router,
    prefix=f"{base_prefix}/health-check",
    tags=["health_check"],
)

app.include_router(
    animal_category.router,
    prefix=f"{base_prefix}/animal_category",
    tags=["animal_category"],
)

app.include_router(
    user.router,
    prefix=f"{base_prefix}/user",
    tags=["user"],
)

app.include_router(
    animal.router,
    prefix=f"{base_prefix}/animal",
    tags=["animal"],
)

app.include_router(
    like.router,
    prefix=f"{base_prefix}/like",
    tags=["like"],
)

app.include_router(
    violation.router,
    prefix=f"{base_prefix}/violation",
    tags=["violation"],
)

app.include_router(
    access_log.router,
    prefix=f"{base_prefix}/access_log",
    tags=["access_log"],
)

app.include_router(
    metadata.router,
    prefix=f"{base_prefix}/metadata",
    tags=["metadata"],
)
