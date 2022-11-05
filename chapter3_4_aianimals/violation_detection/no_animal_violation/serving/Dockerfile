ARG FROM_IMAGE=tensorflow/serving:2.9.1

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=violation_detection/no_animal_violation/serving
ENV PROJECT_DIR no_animal_violation
ENV MODEL_NAME no_animal_violation
ENV MODEL_BASE_PATH /${PROJECT_DIR}/saved_model/

COPY ${LOCAL_DIR}/model/saved_model/ ${MODEL_BASE_PATH}
COPY ${LOCAL_DIR}/tf_serving_entrypoint.sh /usr/bin/tf_serving_entrypoint.sh
RUN chmod +x /usr/bin/tf_serving_entrypoint.sh
EXPOSE 8500
EXPOSE 8501
ENTRYPOINT ["/usr/bin/tf_serving_entrypoint.sh"]
