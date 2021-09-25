ARG FROM_IMAGE=python:3.9.5-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=data_client

ENV PROJECT_DIR opt
WORKDIR /${PROJECT_DIR}
RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ${LOCAL_DIR}/data_client/ /${PROJECT_DIR}/data_client/
COPY ${LOCAL_DIR}/setup.py /${PROJECT_DIR}/setup.py
COPY ${LOCAL_DIR}/setup.cfg /${PROJECT_DIR}/setup.cfg
COPY ${LOCAL_DIR}/README.md /${PROJECT_DIR}/README.md
COPY ${LOCAL_DIR}/requirements.txt /${PROJECT_DIR}/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && \
    python setup.py install

