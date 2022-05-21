ARG FROM_IMAGE=google/tf-serving-scann:2.8.0

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=search/similar_image_search/serving
ENV PROJECT_DIR similar_image_search
ENV MODEL_NAME similar_image_search

COPY ${LOCAL_DIR}/model/saved_model/ /models/similar_image_search/
