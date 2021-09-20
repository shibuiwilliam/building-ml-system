from logging import getLogger

from fastapi import FastAPI
from src.api import health, items, stores
from src.configurations import Configurations
from src.initialize import initialize_data, initialize_tables
from src.middleware.database import engine

logger = getLogger(__name__)

if Configurations.initialize_tables:
    initialize_tables(
        engine=engine,
        checkfirst=True,
    )
if Configurations.initialize_data:
    initialize_data()

base_prefix = f"/v{Configurations.api_version}"


app = FastAPI(
    title=Configurations.api_title,
    description=Configurations.api_description,
    version=Configurations.api_version,
)

app.include_router(
    health.router,
    prefix=f"{base_prefix}/health",
    tags=["health"],
)

app.include_router(
    stores.router,
    prefix=f"{base_prefix}/stores",
    tags=["stores"],
)

app.include_router(
    items.router,
    prefix=f"{base_prefix}/items",
    tags=["items"],
)
