ARG FROM_IMAGE=python:3.9-slim

FROM ${FROM_IMAGE}

ENV PROJECT_DIR opt
WORKDIR /${PROJECT_DIR}
RUN pip install mlflow sqlalchemy psycopg2-binary

CMD [ "mlflow", "server", "--backend-store-uri", "/opt/outputs", "--default-artifact-root", "/opt/outputs", "--host", "0.0.0.0" ]
