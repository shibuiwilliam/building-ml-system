ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 0.0.0

DOCKER_REPOSITORY := shibui/building-ml-system

DIR := $(ABSOLUTE_PATH)
TAG = beverage_sales_forecasting


############ DEMAND FORECASTING ML COMMANDS ############
ML_DIR := $(DIR)/ml
DOCKERFILE_ML = $(ML_DIR)/$(DOCKERFILE)
DOCKER_ML_TAG = $(TAG)_ml
DOCKER_ML_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_ML_TAG)_$(VERSION)
DOCKER_ML_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_ML_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

DOCKERFILE_MLFLOW = $(ML_DIR)/$(DOCKERFILE).mlflow
DOCKER_MLFLOW_TAG = $(TAG)_mlflow
DOCKER_MLFLOW_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_MLFLOW_TAG)_$(VERSION)

.PHONY: req_ml
req_ml:
	cd $(ML_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_ml
build_ml:
	docker build \
		--platform x86_64 \
		-t $(DOCKER_ML_IMAGE_NAME) \
		-f $(DOCKERFILE_ML) \
		.

.PHONY: push_ml
push_ml:
	docker push $(DOCKER_ML_IMAGE_NAME)

.PHONY: build_mlflow
build_mlflow:
	docker build \
		--platform x86_64 \
		-t $(DOCKER_MLFLOW_IMAGE_NAME) \
		-f $(DOCKERFILE_MLFLOW) \
		.

.PHONY: push_mlflow
push_mlflow:
	docker push $(DOCKER_MLFLOW_IMAGE_NAME)

.PHONY: run_ml
run_ml: build_ml
	docker run \
		-it \
		-d \
		--name ml_test \
		-v $(DIR)/data:/opt/data \
		-v $(ML_DIR)/hydra/:/opt/hydra \
		-v $(ML_DIR)/outputs/:/opt/outputs \
		$(DOCKER_ML_IMAGE_NAME) \
		python \
			-m src.main

.PHONY: rm_ml
rm_ml:
	docker rm -f ml_test

.PHONY: mlflow_ui
mlflow_ui:
	docker run \
		-it \
		-d \
		--name mlflow \
		-v $(ML_DIR)/outputs/mlruns:/opt/outputs/mlruns \
		-p 15000:5000 \
		$(DOCKER_MLFLOW_IMAGE_NAME) \
		mlflow server \
			--backend-store-uri /opt/outputs/mlruns \
			--default-artifact-root /opt/outputs/mlruns \
			--host 0.0.0.0

.PHONY: rm_mlflow
rm_mlflow:
	docker rm -f mlflow

############ DEMAND FORECASTING BI COMMANDS ############
BI_DIR := $(DIR)/bi
DOCKERFILE_BI = $(BI_DIR)/$(DOCKERFILE)
DOCKER_BI_TAG = $(TAG)_bi
DOCKER_BI_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_BI_TAG)_$(VERSION)
DOCKER_BI_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_BI_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: req_bi
req_bi:
	cd $(BI_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_bi
build_bi:
	docker build \
		--platform x86_64 \
		-t $(DOCKER_BI_IMAGE_NAME) \
		-f $(DOCKERFILE_BI) \
		.

.PHONY: push_bi
push_bi:
	docker push $(DOCKER_BI_IMAGE_NAME)

.PHONY: run_bi
run_bi: build_bi
	docker run \
		-it \
		-d \
		--name bi \
		-p 8501:8501 \
		-v $(DIR)/data:/opt/data \
		-e ITEM_SALES_RECORD_FILE=/opt/data/data/item_sales_records_train_2021_04.csv \
		-e ITEM_SALES_PREDICTION_DIR=/opt/data/prediction \
		$(DOCKER_BI_IMAGE_NAME) \
		streamlit run src/main.py

.PHONY: rm_bi
rm_bi:
	docker rm -f bi

############ ALL COMMANDS ############
.PHONY: req_all
req_all: req_ml \
	req_bi

.PHONY: build_all
build_all: build_ml \
	build_mlflow \
	build_bi

.PHONY: push_all
push_all: push_ml \
	push_mlflow \
	push_bi


############ DOCKER COMPOSE COMMANDS ############
.PHONY: up
up:
	docker-compose \
		-f $(DOCKER_COMPOSE) \
		up -d

.PHONY: down
down:
	docker-compose \
		-f $(DOCKER_COMPOSE) \
		down
