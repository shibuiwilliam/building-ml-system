ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 0.0.0

DOCKER_REPOSITORY := shibui/building-ml-system

DIR := $(ABSOLUTE_PATH)
TAG = beverage_sales_forecasting


############ DEMAND FORECASTING DATA_REGISTRATION COMMANDS ############
DATA_REGISTRATION_DIR := $(DIR)/data_registration
DOCKERFILE_DATA_REGISTRATION = $(DATA_REGISTRATION_DIR)/$(DOCKERFILE)
DOCKER_DATA_REGISTRATION_TAG = $(TAG)_data_registration
DOCKER_DATA_REGISTRATION_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DATA_REGISTRATION_TAG)_$(VERSION)
DOCKER_DATA_REGISTRATION_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DATA_REGISTRATION_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_data_registration
patch_data_registration:
	cd $(DATA_REGISTRATION_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_data_registration
minor_upgrade_data_registration:
	cd $(DATA_REGISTRATION_DIR) && \
	poetry version minor

.PHONY: major_upgrade_data_registration
major_upgrade_data_registration:
	cd $(DATA_REGISTRATION_DIR) && \
	poetry version major

.PHONY: req_data_registration
req_data_registration:
	cd $(DATA_REGISTRATION_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_data_registration
build_data_registration: 
	docker build \
		-t $(DOCKER_DATA_REGISTRATION_IMAGE_NAME) \
		-f $(DOCKERFILE_DATA_REGISTRATION) \
		.
	 
.PHONY: push_data_registration
push_data_registration: 
	docker push $(DOCKER_DATA_REGISTRATION_IMAGE_NAME)


############ DEMAND FORECASTING ML COMMANDS ############
ML_DIR := $(DIR)/ml
DOCKERFILE_ML = $(ML_DIR)/$(DOCKERFILE)
DOCKER_ML_TAG = $(TAG)_ml
DOCKER_ML_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_ML_TAG)_$(VERSION)
DOCKER_ML_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_ML_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

DOCKERFILE_MLFLOW = $(ML_DIR)/$(DOCKERFILE).mlflow
DOCKER_MLFLOW_TAG = $(TAG)_mlflow
DOCKER_MLFLOW_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_MLFLOW_TAG)_$(VERSION)

.PHONY: patch_ml
patch_ml:
	cd $(ML_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_ml
minor_upgrade_ml:
	cd $(ML_DIR) && \
	poetry version minor

.PHONY: major_upgrade_ml
major_upgrade_ml:
	cd $(ML_DIR) && \
	poetry version major

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
		-t $(DOCKER_ML_IMAGE_NAME) \
		-f $(DOCKERFILE_ML) \
		.
	 
.PHONY: push_ml
push_ml: 
	docker push $(DOCKER_ML_IMAGE_NAME)

.PHONY: build_mlflow
build_mlflow: 
	docker build \
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

.PHONY: patch_bi
patch_bi:
	cd $(BI_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_bi
minor_upgrade_bi:
	cd $(BI_DIR) && \
	poetry version minor

.PHONY: major_upgrade_bi
major_upgrade_bi:
	cd $(BI_DIR) && \
	poetry version major

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
		-t $(DOCKER_BI_IMAGE_NAME) \
		-f $(DOCKERFILE_BI) \
		.
	 
.PHONY: push_bi
push_bi: 
	docker push $(DOCKER_BI_IMAGE_NAME)


############ ALL COMMANDS ############
.PHONY: patch_all
patch_all: patch_data_registration \
	patch_ml \
	patch_bi

.PHONY: minor_upgrade_all
minor_upgrade_all: minor_upgrade_data_registration \
	minor_upgrade_ml \
	minor_upgrade_bi

.PHONY: major_upgrade_all
major_upgrade_all: major_upgrade_data_registration \
	major_upgrade_ml \
	major_upgrade_bi

.PHONY: req_all
req_all: req_data_registration \
	req_ml \
	req_bi

.PHONY: build_all
build_all: build_data_registration \
	build_ml \
	build_mlflow \
	build_bi
	 
.PHONY: push_all
push_all: push_data_registration \
	push_ml \
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
