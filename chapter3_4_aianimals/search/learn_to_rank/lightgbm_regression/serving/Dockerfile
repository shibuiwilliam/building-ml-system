FROM mcr.microsoft.com/onnxruntime/server:latest

ARG SERVER_DIR=search/learn_to_rank/lightgbm_regression/serving
ENV PROJECT_DIR lightgbm_regression
ENV MODEL_BASE_PATH=${PROJECT_DIR}/model

WORKDIR /${PROJECT_DIR}

COPY /${SERVER_DIR}/model/learning_to_rank_lightgbm_regression.onnx /${MODEL_BASE_PATH}/learning_to_rank_lightgbm_regression.onnx

ENV MODEL_PATH /${MODEL_BASE_PATH}/learning_to_rank_lightgbm_regression.onnx

WORKDIR /onnxruntime/server/
COPY ./${SERVER_DIR}/onnx_runtime_server_entrypoint.sh ./onnx_runtime_server_entrypoint.sh
RUN chmod +x onnx_runtime_server_entrypoint.sh
ENTRYPOINT ["./onnx_runtime_server_entrypoint.sh"]