ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 0.0.0

DOCKER_REPOSITORY := shibui/building-ml-system

DIR := $(ABSOLUTE_PATH)
TAG = demand_forecasting

############ COMMON COMMANDS ############
.PHONY: download_kaggle
download_kaggle:
	cd $(DIR)/data && \
	kaggle competitions download -c demand-forecasting-kernels-only && \
	unzip demand-forecasting-kernels-only.zip

.PHONY: dvc_init
dvc_init:
	cd $(DIR) && \
	dvc init --subdir
	

############ DEMAND FORECASTING DATA_MANAGER COMMANDS ############
DATA_MANAGER_DIR := $(DIR)/data_manager
DOCKERFILE_DATA_MANAGER = $(DATA_MANAGER_DIR)/$(DOCKERFILE)
DOCKER_DATA_MANAGER_TAG = $(TAG)_data_manager
DOCKER_DATA_MANAGER_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DATA_MANAGER_TAG)_$(VERSION)
DOCKER_DATA_MANAGER_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DATA_MANAGER_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_data_manager
patch_data_manager:
	cd $(DATA_MANAGER_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_data_manager
minor_upgrade_data_manager:
	cd $(DATA_MANAGER_DIR) && \
	poetry version minor

.PHONY: major_upgrade_data_manager
major_upgrade_data_manager:
	cd $(DATA_MANAGER_DIR) && \
	poetry version major

.PHONY: req_data_manager
req_data_manager:
	cd $(DATA_MANAGER_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_data_manager
build_data_manager: 
	docker build \
		-t $(DOCKER_DATA_MANAGER_IMAGE_NAME) \
		-f $(DOCKERFILE_DATA_MANAGER) \
		.
	 
.PHONY: push_data_manager
push_data_manager: 
	docker push $(DOCKER_DATA_MANAGER_IMAGE_NAME)


############ DEMAND FORECASTING DATA_CLIENT COMMANDS ############
DATA_CLIENT_DIR := $(DIR)/data_client
DOCKERFILE_DATA_CLIENT = $(DATA_CLIENT_DIR)/$(DOCKERFILE)
DOCKER_DATA_CLIENT_TAG = $(TAG)_data_client
DOCKER_DATA_CLIENT_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DATA_CLIENT_TAG)_$(VERSION)
DOCKER_DATA_CLIENT_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DATA_CLIENT_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_data_client
patch_data_client:
	cd $(DATA_CLIENT_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_data_client
minor_upgrade_data_client:
	cd $(DATA_CLIENT_DIR) && \
	poetry version minor

.PHONY: major_upgrade_data_client
major_upgrade_data_client:
	cd $(DATA_CLIENT_DIR) && \
	poetry version major

.PHONY: req_data_client
req_data_client:
	cd $(DATA_CLIENT_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_data_client
build_data_client: 
	docker build \
		-t $(DOCKER_DATA_CLIENT_IMAGE_NAME) \
		-f $(DOCKERFILE_DATA_CLIENT) \
		.
	 
.PHONY: push_data_client
push_data_client: 
	docker push $(DOCKER_DATA_CLIENT_IMAGE_NAME)


############ DEMAND FORECASTING ML COMMANDS ############
ML_DIR := $(DIR)/ml
DOCKERFILE_ML = $(ML_DIR)/$(DOCKERFILE)
DOCKER_ML_TAG = $(TAG)_ml
DOCKER_ML_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_ML_TAG)_$(VERSION)
DOCKER_ML_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_ML_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

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
		--build-arg FROM_IMAGE=$(DOCKER_DATA_CLIENT_IMAGE_NAME) \
		-t $(DOCKER_ML_IMAGE_NAME) \
		-f $(DOCKERFILE_ML) \
		.
	 
.PHONY: push_ml
push_ml: 
	docker push $(DOCKER_ML_IMAGE_NAME)


.PHONY: run_ml
run_ml: build_ml
	docker run \
		-it \
		-d \
		--name ml_test \
		-v $(DIR)/data:/opt/data \
		--network ml \
		$(DOCKER_ML_IMAGE_NAME) \
		python \
			-m src.main \
			--data_file_path /opt/data/item_sale_records_2017_2019.csv \
			--prediction_file_path /opt/data/item_target_20191223_20191229.csv \
			--model_name light_gbm_regression \
			--save_file_directory /opt/data \
			--train_start_date 2017-01-01 \
			--train_end_date 2019-12-08 \
			--test_start_date 2019-12-16 \
			--test_end_date 2019-12-22 \
			--predict_start_date 2019-12-23 \
			--predict_end_date 2019-12-29 \
			--experiment_param_file_path /opt/data/light_gbm_regression_experiment_params.json \
			--train_param_file_path /opt/data/light_gbm_regression_train_params.json \
			--run_experiment \
			--run_train \
			--run_prediction


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
		--build-arg FROM_IMAGE=$(DOCKER_DATA_CLIENT_IMAGE_NAME) \
		-t $(DOCKER_BI_IMAGE_NAME) \
		-f $(DOCKERFILE_BI) \
		.
	 
.PHONY: push_bi
push_bi: 
	docker push $(DOCKER_BI_IMAGE_NAME)


############ ALL COMMANDS ############
.PHONY: patch_all
patch_all: patch_data_manager \
	patch_data_client \
	patch_ml \
	patch_bi

.PHONY: minor_upgrade_all
minor_upgrade_all: minor_upgrade_data_manager \
	minor_upgrade_data_client \
	minor_upgrade_ml \
	minor_upgrade_bi

.PHONY: major_upgrade_all
major_upgrade_all: major_upgrade_data_manager \
	major_upgrade_data_client \
	major_upgrade_ml \
	major_upgrade_bi

.PHONY: req_all
req_all: req_data_manager \
	req_data_client \
	req_ml \
	req_bi

.PHONY: build_all
build_all: build_data_manager \
	build_data_client \
	build_ml \
	build_bi
	 
.PHONY: push_all
push_all: push_data_manager \
	push_data_client \
	push_ml \
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
