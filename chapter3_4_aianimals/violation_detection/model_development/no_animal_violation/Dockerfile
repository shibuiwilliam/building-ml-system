ARG FROM_IMAGE=python:3.9.7-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=violation_detection/model_development/no_animal_violation

ENV PROJECT_DIR opt
WORKDIR /${PROJECT_DIR}
COPY ${LOCAL_DIR}/requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY ${LOCAL_DIR}/src/ /${PROJECT_DIR}/src/
COPY ${LOCAL_DIR}/hydra/ /${PROJECT_DIR}/hydra/
