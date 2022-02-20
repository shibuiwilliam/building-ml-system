#!/bin/sh

set -eu

docker run \
    -it \
    --rm \
    --name test \
    --network aianimals \
    -v $(pwd)/outputs:/opt/outputs/ \
    shibui/building-ml-system:ai_animals_violation_detection_no_animal_violation_train_0.0.0 \
    python -m src.main
