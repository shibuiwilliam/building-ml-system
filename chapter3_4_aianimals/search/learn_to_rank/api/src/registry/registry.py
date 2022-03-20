from src.configurations import Configurations
from src.registry.container import AbstractContainer
from src.registry.container_builder import build_container, build_empty_container

if Configurations.empty_run:
    container: AbstractContainer = build_empty_container()
else:
    container = build_container()
