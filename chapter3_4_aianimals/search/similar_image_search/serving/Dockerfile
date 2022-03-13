ARG FROM_IMAGE=google/tf-serving-scann:2.7.0

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=search/similar_image_search/serving
ARG SERVER_DIR=similar_image_search
ENV PROJECT_DIR similar_image_search
ENV MODEL_NAME similar_image_search
ENV MODEL_BASE_PATH /${PROJECT_DIR}/saved_model/

COPY ${LOCAL_DIR}/model/saved_model/ ${MODEL_BASE_PATH}
COPY ${LOCAL_DIR}/tf_serving_entrypoint.sh /usr/bin/tf_serving_entrypoint.sh
RUN chmod +x /usr/bin/tf_serving_entrypoint.sh
EXPOSE 8500
EXPOSE 8501
ENTRYPOINT ["/usr/bin/tf_serving_entrypoint.sh"]
