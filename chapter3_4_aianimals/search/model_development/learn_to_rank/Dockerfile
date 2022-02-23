ARG FROM_IMAGE=python:3.9.7-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=search/model_development/learn_to_rank

ENV PROJECT_DIR opt
WORKDIR /${PROJECT_DIR}
COPY ${LOCAL_DIR}/requirements.txt /${PROJECT_DIR}/
RUN pip install --no-cache-dir -r requirements.txt

COPY ${LOCAL_DIR}/src/ /${PROJECT_DIR}/src/
COPY ${LOCAL_DIR}/hydra/ /${PROJECT_DIR}/hydra/
