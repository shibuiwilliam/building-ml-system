#!/bin/sh

set -eu

docker run \
    -it \
    --rm \
    --name test \
    --network aianimals \
    -v $(pwd)/outputs:/opt/outputs/ \
    -e POSTGRESQL_USER=postgres \
    -e POSTGRESQL_PASSWORD=password \
    -e POSTGRESQL_PORT=5432 \
    -e POSTGRESQL_DBNAME=aianimals \
    -e POSTGRESQL_HOST=postgres \
    shibui/building-ml-system:ai_animals_search_similar_image_search_train_0.0.0 \
    python -m src.main
