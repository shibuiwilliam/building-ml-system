ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 0.0.0
DOCKER_TEST_TAG := test

DOCKER_REPOSITORY := shibui/building-ml-system

DEMAND_FORECASTING_DIR := $(ABSOLUTE_PATH)
DEMAND_FORECASTING_ML_DIR := $(DEMAND_FORECASTING_DIR)/ml
DEMAND_FORECASTING_DATA_MANAGER_DIR := $(DEMAND_FORECASTING_DIR)/data_manager
DEMAND_FORECASTING_BI_DIR := $(DEMAND_FORECASTING_DIR)/bi


############ COMMON COMMANDS ############
.PHONY: download_kaggle
download_kaggle:
	cd $(DEMAND_FORECASTING_DIR)/data && \
	kaggle competitions download -c demand-forecasting-kernels-only && \
	unzip demand-forecasting-kernels-only.zip

.PHONY: dvc_init
dvc_init:
	cd $(DEMAND_FORECASTING_DIR) && \
	dvc init --subdir
	

############ DEMAND FORECASTING ML COMMANDS ############
DOCKERFILE_DEMAND_FORECASTING_ML = $(DEMAND_FORECASTING_ML_DIR)/$(DOCKERFILE)
DOCKER_DEMAND_FORECASTING_ML_TAG = demand_forecasting_ml
DOCKER_DEMAND_FORECASTING_ML_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_ML_TAG)_$(VERSION)
DOCKER_DEMAND_FORECASTING_ML_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_ML_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_demand_forecasting_ml
patch_demand_forecasting_ml:
	cd $(DEMAND_FORECASTING_ML_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_demand_forecasting_ml
minor_upgrade_demand_forecasting_ml:
	cd $(DEMAND_FORECASTING_ML_DIR) && \
	poetry version minor

.PHONY: major_upgrade_demand_forecasting_ml
major_upgrade_demand_forecasting_ml:
	cd $(DEMAND_FORECASTING_ML_DIR) && \
	poetry version major

.PHONY: req_demand_forecasting_ml
req_demand_forecasting_ml:
	cd $(DEMAND_FORECASTING_ML_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: req_demand_forecasting_ml_test
req_demand_forecasting_test_ml:
	cd $(DEMAND_FORECASTING_ML_DIR) && \
	poetry export \
		--dev \
		--without-hashes \
		-f requirements.txt \
		--output requirements_test.txt

.PHONY: build_demand_forecasting_ml
build_demand_forecasting_ml: 
	docker build \
		-t $(DOCKER_DEMAND_FORECASTING_ML_IMAGE_NAME) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_ML) \
		.
	 
.PHONY: push_demand_forecasting_ml
push_demand_forecasting_ml: 
	docker push $(DOCKER_DEMAND_FORECASTING_ML_IMAGE_NAME)

.PHONY: build_demand_forecasting_ml_test
build_demand_forecasting_ml_test: build_demand_forecasting_ml
	docker build \
		--build-arg FROM_IMAGE=$(DOCKER_DEMAND_FORECASTING_ML_IMAGE_NAME) \
		-t $(DOCKER_DEMAND_FORECASTING_ML_IMAGE_NAME_TEST) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_ML_TEST) \
		.

.PHONY: test_demand_forecasting_ml
test_demand_forecasting_ml: build_demand_forecasting_ml_test
	docker run \
		--rm \
		--name test \
		$(DOCKER_DEMAND_FORECASTING_ML_IMAGE_NAME_TEST)


.PHONY: run_ml
run_ml: build_demand_forecasting_ml
	docker run \
		-it \
		-d \
		--name ml_test \
		-v $(DEMAND_FORECASTING_DIR)/data:/opt/data \
		$(DOCKER_DEMAND_FORECASTING_ML_IMAGE_NAME) \
		python \
			-m src.main \
			--data_file_path /opt/data/item_sale_records_2017_2019.csv \
			--model_name light_gbm_regression \
			--save_file_directory /opt/data \
			--train_start_date 2017-01-01 \
			--train_end_date 2019-12-15 \
			--test_start_date 2019-12-23 \
			--test_end_date 2019-12-29 \
			--experiment_param_file_path /opt/data/light_gbm_regression_experiment_params.json \
			--train_param_file_path /opt/data/light_gbm_regression_train_params.json \
			--run_experiment \
			--run_train

############ DEMAND FORECASTING DATA_MANAGER COMMANDS ############
DOCKERFILE_DEMAND_FORECASTING_DATA_MANAGER = $(DEMAND_FORECASTING_DATA_MANAGER_DIR)/$(DOCKERFILE)
DOCKER_DEMAND_FORECASTING_DATA_MANAGER_TAG = demand_forecasting_data_manager
DOCKER_DEMAND_FORECASTING_DATA_MANAGER_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_DATA_MANAGER_TAG)_$(VERSION)
DOCKER_DEMAND_FORECASTING_DATA_MANAGER_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_DATA_MANAGER_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_demand_forecasting_data_manager
patch_demand_forecasting_data_manager:
	cd $(DEMAND_FORECASTING_DATA_MANAGER_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_demand_forecasting_data_manager
minor_upgrade_demand_forecasting_data_manager:
	cd $(DEMAND_FORECASTING_DATA_MANAGER_DIR) && \
	poetry version minor

.PHONY: major_upgrade_demand_forecasting_data_manager
major_upgrade_demand_forecasting_data_manager:
	cd $(DEMAND_FORECASTING_DATA_MANAGER_DIR) && \
	poetry version major

.PHONY: req_demand_forecasting_data_manager
req_demand_forecasting_data_manager:
	cd $(DEMAND_FORECASTING_DATA_MANAGER_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: req_demand_forecasting_data_manager_test
req_demand_forecasting_test_data_manager:
	cd $(DEMAND_FORECASTING_DATA_MANAGER_DIR) && \
	poetry export \
		--dev \
		--without-hashes \
		-f requirements.txt \
		--output requirements_test.txt

.PHONY: build_demand_forecasting_data_manager
build_demand_forecasting_data_manager: 
	docker build \
		-t $(DOCKER_DEMAND_FORECASTING_DATA_MANAGER_IMAGE_NAME) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_DATA_MANAGER) \
		.
	 
.PHONY: push_demand_forecasting_data_manager
push_demand_forecasting_data_manager: 
	docker push $(DOCKER_DEMAND_FORECASTING_DATA_MANAGER_IMAGE_NAME)

.PHONY: build_demand_forecasting_data_manager_test
build_demand_forecasting_data_manager_test: build_demand_forecasting_data_manager
	docker build \
		--build-arg FROM_IMAGE=$(DOCKER_DEMAND_FORECASTING_DATA_MANAGER_IMAGE_NAME) \
		-t $(DOCKER_DEMAND_FORECASTING_DATA_MANAGER_IMAGE_NAME_TEST) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_DATA_MANAGER_TEST) \
		.

.PHONY: test_demand_forecasting_data_manager
test_demand_forecasting_data_manager: build_demand_forecasting_data_manager_test
	docker run \
		--rm \
		--name test \
		$(DOCKER_DEMAND_FORECASTING_DATA_MANAGER_IMAGE_NAME_TEST)


############ DEMAND FORECASTING BI COMMANDS ############
DOCKERFILE_DEMAND_FORECASTING_BI = $(DEMAND_FORECASTING_BI_DIR)/$(DOCKERFILE)
DOCKER_DEMAND_FORECASTING_BI_TAG = demand_forecasting_bi
DOCKER_DEMAND_FORECASTING_BI_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_BI_TAG)_$(VERSION)
DOCKER_DEMAND_FORECASTING_BI_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_BI_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_demand_forecasting_bi
patch_demand_forecasting_bi:
	cd $(DEMAND_FORECASTING_BI_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_demand_forecasting_bi
minor_upgrade_demand_forecasting_bi:
	cd $(DEMAND_FORECASTING_BI_DIR) && \
	poetry version minor

.PHONY: major_upgrade_demand_forecasting_bi
major_upgrade_demand_forecasting_bi:
	cd $(DEMAND_FORECASTING_BI_DIR) && \
	poetry version major

.PHONY: req_demand_forecasting_bi
req_demand_forecasting_bi:
	cd $(DEMAND_FORECASTING_BI_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: req_demand_forecasting_bi_test
req_demand_forecasting_test_bi:
	cd $(DEMAND_FORECASTING_BI_DIR) && \
	poetry export \
		--dev \
		--without-hashes \
		-f requirements.txt \
		--output requirements_test.txt

.PHONY: build_demand_forecasting_bi
build_demand_forecasting_bi: 
	docker build \
		-t $(DOCKER_DEMAND_FORECASTING_BI_IMAGE_NAME) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_BI) \
		.
	 
.PHONY: push_demand_forecasting_bi
push_demand_forecasting_bi: 
	docker push $(DOCKER_DEMAND_FORECASTING_BI_IMAGE_NAME)

.PHONY: build_demand_forecasting_bi_test
build_demand_forecasting_bi_test: build_demand_forecasting_bi
	docker build \
		--build-arg FROM_IMAGE=$(DOCKER_DEMAND_FORECASTING_BI_IMAGE_NAME) \
		-t $(DOCKER_DEMAND_FORECASTING_BI_IMAGE_NAME_TEST) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_BI_TEST) \
		.

.PHONY: test_demand_forecasting_bi
test_demand_forecasting_bi: build_demand_forecasting_bi_test
	docker run \
		--rm \
		--name test \
		$(DOCKER_DEMAND_FORECASTING_BI_IMAGE_NAME_TEST)


############ ALL COMMANDS ############
.PHONY: patch_demand_forecasting_all
patch_demand_forecasting_all: patch_demand_forecasting_ml \
	patch_demand_forecasting_data_manager \
	patch_demand_forecasting_bi

.PHONY: minor_upgrade_demand_forecasting_all
minor_upgrade_demand_forecasting_all: minor_upgrade_demand_forecasting_ml \
	minor_upgrade_demand_forecasting_data_manager \
	minor_upgrade_demand_forecasting_bi

.PHONY: major_upgrade_demand_forecasting_all
major_upgrade_demand_forecasting_all: major_upgrade_demand_forecasting_ml \
	major_upgrade_demand_forecasting_data_manager \
	major_upgrade_demand_forecasting_bi

.PHONY: req_demand_forecasting_all
req_demand_forecasting_all: req_demand_forecasting_ml \
	req_demand_forecasting_data_manager \
	req_demand_forecasting_bi

.PHONY: req_demand_forecasting_all_test
req_demand_forecasting_test_all: req_demand_forecasting_ml_test \
	req_demand_forecasting_data_manager_test \
	req_demand_forecasting_bi_test

.PHONY: build_demand_forecasting_all
build_demand_forecasting_all: build_demand_forecasting_ml \
	build_demand_forecasting_data_manager \
	build_demand_forecasting_bi
	 
.PHONY: push_demand_forecasting_all
push_demand_forecasting_all: push_demand_forecasting_ml \
	push_demand_forecasting_data_manager \
	push_demand_forecasting_bi

.PHONY: build_demand_forecasting_all_test
build_demand_forecasting_all_test: build_demand_forecasting_all \
	build_demand_forecasting_ml_test \
	build_demand_forecasting_data_manager_test \
	build_demand_forecasting_bi_test

.PHONY: test_demand_forecasting_all
test_demand_forecasting_all: build_demand_forecasting_all_test \
	test_demand_forecasting_ml \
	test_demand_forecasting_data_manager \
	test_demand_forecasting_bi


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
