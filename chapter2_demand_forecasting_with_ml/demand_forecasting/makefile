ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker_compose.yml
VERSION := 0.0.0
DOCKER_TEST_TAG := test

DOCKER_REPOSITORY := shibui/building-ml-system

DEMAND_FORECASTING_DIR := $(ABSOLUTE_PATH)
DEMAND_FORECASTING_TRAIN_DIR := $(DEMAND_FORECASTING_DIR)/train
DEMAND_FORECASTING_EVALUATE_DIR := $(DEMAND_FORECASTING_DIR)/evaluate
DEMAND_FORECASTING_PREDICT_DIR := $(DEMAND_FORECASTING_DIR)/predict
DEMAND_FORECASTING_DATA_MANAGER_DIR := $(DEMAND_FORECASTING_DIR)/data_manager


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
	


############ DEMAND FORECASTING TRAIN COMMANDS ############
DOCKERFILE_DEMAND_FORECASTING_TRAIN = $(DEMAND_FORECASTING_TRAIN_DIR)/$(DOCKERFILE)
DOCKER_DEMAND_FORECASTING_TRAIN_TAG = demand_forecasting_train
DOCKER_DEMAND_FORECASTING_TRAIN_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_TRAIN_TAG)_$(VERSION)
DOCKER_DEMAND_FORECASTING_TRAIN_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_TRAIN_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_demand_forecasting_train
patch_demand_forecasting_train:
	cd $(DEMAND_FORECASTING_TRAIN_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_demand_forecasting_train
minor_upgrade_demand_forecasting_train:
	cd $(DEMAND_FORECASTING_TRAIN_DIR) && \
	poetry version minor

.PHONY: major_upgrade_demand_forecasting_train
major_upgrade_demand_forecasting_train:
	cd $(DEMAND_FORECASTING_TRAIN_DIR) && \
	poetry version major

.PHONY: req_demand_forecasting_train
req_demand_forecasting_train:
	cd $(DEMAND_FORECASTING_TRAIN_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: req_demand_forecasting_train_test
req_demand_forecasting_test_train:
	cd $(DEMAND_FORECASTING_TRAIN_DIR) && \
	poetry export \
		--dev \
		--without-hashes \
		-f requirements.txt \
		--output requirements_test.txt

.PHONY: build_demand_forecasting_train
build_demand_forecasting_train: 
	docker build \
		-t $(DOCKER_DEMAND_FORECASTING_TRAIN_IMAGE_NAME) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_TRAIN) \
		.
	 
.PHONY: push_demand_forecasting_train
push_demand_forecasting_train: 
	docker push $(DOCKER_DEMAND_FORECASTING_TRAIN_IMAGE_NAME)

.PHONY: build_demand_forecasting_train_test
build_demand_forecasting_train_test: build_demand_forecasting_train
	docker build \
		--build-arg FROM_IMAGE=$(DOCKER_DEMAND_FORECASTING_TRAIN_IMAGE_NAME) \
		-t $(DOCKER_DEMAND_FORECASTING_TRAIN_IMAGE_NAME_TEST) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_TRAIN_TEST) \
		.

.PHONY: test_demand_forecasting_train
test_demand_forecasting_train: build_demand_forecasting_train_test
	docker run \
		--rm \
		--name test \
		$(DOCKER_DEMAND_FORECASTING_TRAIN_IMAGE_NAME_TEST)


############ DEMAND FORECASTING EVALUATE COMMANDS ############
DOCKERFILE_DEMAND_FORECASTING_EVALUATE = $(DEMAND_FORECASTING_EVALUATE_DIR)/$(DOCKERFILE)
DOCKER_DEMAND_FORECASTING_EVALUATE_TAG = demand_forecasting_evaluate
DOCKER_DEMAND_FORECASTING_EVALUATE_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_EVALUATE_TAG)_$(VERSION)
DOCKER_DEMAND_FORECASTING_EVALUATE_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_EVALUATE_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_demand_forecasting_evaluate
patch_demand_forecasting_evaluate:
	cd $(DEMAND_FORECASTING_EVALUATE_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_demand_forecasting_evaluate
minor_upgrade_demand_forecasting_evaluate:
	cd $(DEMAND_FORECASTING_EVALUATE_DIR) && \
	poetry version minor

.PHONY: major_upgrade_demand_forecasting_evaluate
major_upgrade_demand_forecasting_evaluate:
	cd $(DEMAND_FORECASTING_EVALUATE_DIR) && \
	poetry version major

.PHONY: req_demand_forecasting_evaluate
req_demand_forecasting_evaluate:
	cd $(DEMAND_FORECASTING_EVALUATE_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: req_demand_forecasting_evaluate_test
req_demand_forecasting_test_evaluate:
	cd $(DEMAND_FORECASTING_EVALUATE_DIR) && \
	poetry export \
		--dev \
		--without-hashes \
		-f requirements.txt \
		--output requirements_test.txt

.PHONY: build_demand_forecasting_evaluate
build_demand_forecasting_evaluate: 
	docker build \
		-t $(DOCKER_DEMAND_FORECASTING_EVALUATE_IMAGE_NAME) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_EVALUATE) \
		.
	 
.PHONY: push_demand_forecasting_evaluate
push_demand_forecasting_evaluate: 
	docker push $(DOCKER_DEMAND_FORECASTING_EVALUATE_IMAGE_NAME)

.PHONY: build_demand_forecasting_evaluate_test
build_demand_forecasting_evaluate_test: build_demand_forecasting_evaluate
	docker build \
		--build-arg FROM_IMAGE=$(DOCKER_DEMAND_FORECASTING_EVALUATE_IMAGE_NAME) \
		-t $(DOCKER_DEMAND_FORECASTING_EVALUATE_IMAGE_NAME_TEST) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_EVALUATE_TEST) \
		.

.PHONY: test_demand_forecasting_evaluate
test_demand_forecasting_evaluate: build_demand_forecasting_evaluate_test
	docker run \
		--rm \
		--name test \
		$(DOCKER_DEMAND_FORECASTING_EVALUATE_IMAGE_NAME_TEST)


############ DEMAND FORECASTING PREDICT COMMANDS ############
DOCKERFILE_DEMAND_FORECASTING_PREDICT = $(DEMAND_FORECASTING_PREDICT_DIR)/$(DOCKERFILE)
DOCKER_DEMAND_FORECASTING_PREDICT_TAG = demand_forecasting_predict
DOCKER_DEMAND_FORECASTING_PREDICT_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_PREDICT_TAG)_$(VERSION)
DOCKER_DEMAND_FORECASTING_PREDICT_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_PREDICT_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_demand_forecasting_predict
patch_demand_forecasting_predict:
	cd $(DEMAND_FORECASTING_PREDICT_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_demand_forecasting_predict
minor_upgrade_demand_forecasting_predict:
	cd $(DEMAND_FORECASTING_PREDICT_DIR) && \
	poetry version minor

.PHONY: major_upgrade_demand_forecasting_predict
major_upgrade_demand_forecasting_predict:
	cd $(DEMAND_FORECASTING_PREDICT_DIR) && \
	poetry version major

.PHONY: req_demand_forecasting_predict
req_demand_forecasting_predict:
	cd $(DEMAND_FORECASTING_PREDICT_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: req_demand_forecasting_predict_test
req_demand_forecasting_test_predict:
	cd $(DEMAND_FORECASTING_PREDICT_DIR) && \
	poetry export \
		--dev \
		--without-hashes \
		-f requirements.txt \
		--output requirements_test.txt

.PHONY: build_demand_forecasting_predict
build_demand_forecasting_predict: 
	docker build \
		-t $(DOCKER_DEMAND_FORECASTING_PREDICT_IMAGE_NAME) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_PREDICT) \
		.
	 
.PHONY: push_demand_forecasting_predict
push_demand_forecasting_predict: 
	docker push $(DOCKER_DEMAND_FORECASTING_PREDICT_IMAGE_NAME)

.PHONY: build_demand_forecasting_predict_test
build_demand_forecasting_predict_test: build_demand_forecasting_predict
	docker build \
		--build-arg FROM_IMAGE=$(DOCKER_DEMAND_FORECASTING_PREDICT_IMAGE_NAME) \
		-t $(DOCKER_DEMAND_FORECASTING_PREDICT_IMAGE_NAME_TEST) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_PREDICT_TEST) \
		.

.PHONY: test_demand_forecasting_predict
test_demand_forecasting_predict: build_demand_forecasting_predict_test
	docker run \
		--rm \
		--name test \
		$(DOCKER_DEMAND_FORECASTING_PREDICT_IMAGE_NAME_TEST)


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


############ ALL COMMANDS ############
.PHONY: patch_demand_forecasting_all
patch_demand_forecasting_all: patch_demand_forecasting_train \
	patch_demand_forecasting_evaluate \
	patch_demand_forecasting_predict \
	patch_demand_forecasting_data_manager

.PHONY: minor_upgrade_demand_forecasting_all
minor_upgrade_demand_forecasting_all: minor_upgrade_demand_forecasting_train \
	minor_upgrade_demand_forecasting_evaluate \
	minor_upgrade_demand_forecasting_predict \
	minor_upgrade_demand_forecasting_data_manager

.PHONY: major_upgrade_demand_forecasting_all
major_upgrade_demand_forecasting_all: major_upgrade_demand_forecasting_train \
	major_upgrade_demand_forecasting_evaluate \
	major_upgrade_demand_forecasting_predict \
	major_upgrade_demand_forecasting_data_manager

.PHONY: req_demand_forecasting_all
req_demand_forecasting_all: req_demand_forecasting_train \
	req_demand_forecasting_evaluate \
	req_demand_forecasting_predict \
	req_demand_forecasting_data_manager

.PHONY: req_demand_forecasting_all_test
req_demand_forecasting_test_all: req_demand_forecasting_train_test \
	req_demand_forecasting_evaluate_test \
	req_demand_forecasting_predict_test \
	req_demand_forecasting_data_manager_test

.PHONY: build_demand_forecasting_all
build_demand_forecasting_all: build_demand_forecasting_train \
	build_demand_forecasting_evaluate \
	build_demand_forecasting_predict \
	build_demand_forecasting_data_manager
	 
.PHONY: push_demand_forecasting_all
push_demand_forecasting_all: push_demand_forecasting_train \
	push_demand_forecasting_evaluate \
	push_demand_forecasting_predict \
	push_demand_forecasting_data_manager

.PHONY: build_demand_forecasting_all_test
build_demand_forecasting_all_test: build_demand_forecasting_all \
	build_demand_forecasting_train_test \
	build_demand_forecasting_evaluate_test \
	build_demand_forecasting_predict_test \
	build_demand_forecasting_data_manager_test

.PHONY: test_demand_forecasting_all
test_demand_forecasting_all: build_demand_forecasting_all_test \
	test_demand_forecasting_train \
	test_demand_forecasting_evaluate \
	test_demand_forecasting_predict \
	test_demand_forecasting_data_manager

