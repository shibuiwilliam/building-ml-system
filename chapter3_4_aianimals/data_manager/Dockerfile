ARG FROM_IMAGE=python:3.9.7-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=backend

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
COPY ./dataset/animal_category.json /${PROJECT_DIR}/dataset/animal_category.json
COPY ./dataset/animal_subcategory.json /${PROJECT_DIR}/dataset/animal_subcategory.json
COPY ./dataset/animal.json /${PROJECT_DIR}/dataset/animal.json
COPY ./dataset/user.json /${PROJECT_DIR}/dataset/user.json

COPY ${LOCAL_DIR}/run.sh /${PROJECT_DIR}/run.sh
RUN chmod +x /${PROJECT_DIR}/run.sh
CMD [ "./run.sh" ]
