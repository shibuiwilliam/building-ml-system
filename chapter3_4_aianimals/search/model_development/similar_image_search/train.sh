#!/bin/sh

set -eu

docker run \
    -it \
    --rm \
    --name test \
    --network aianimals \
    -v $(pwd)/outputs:/opt/outputs/ \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_PORT=5432 \
    -e POSTGRES_DBNAME=aianimals \
    -e POSTGRES_HOST=postgres \
    shibui/building-ml-system:ai_animals_search_similar_image_search_train_0.0.0 \
    python -m src.main
