from logging import getLogger

from src.configurations import Configurations
from src.registry.container import AbstractContainer
from src.registry.container_builder import build_container, build_empty_container

logger = getLogger(__name__)

if Configurations.empty_run:
    logger.info("empty container...")
    container: AbstractContainer = build_empty_container()
else:
    logger.info("plain container...")
    container = build_container()
