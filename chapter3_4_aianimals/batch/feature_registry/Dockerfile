ARG FROM_IMAGE=python:3.10.6-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=batch/feature_registry

ENV PROJECT_DIR opt
WORKDIR /${PROJECT_DIR}
COPY ${LOCAL_DIR}/requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc \
    curl \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY ${LOCAL_DIR}/src/ /${PROJECT_DIR}/src/
COPY ${LOCAL_DIR}/hydra/ /${PROJECT_DIR}/hydra/
