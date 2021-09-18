ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker_compose.yml

DEMAND_FORECASTING_DIR := $(ABSOLUTE_PATH)/demand_forecasting

DOCKER_REPOSITORY := shibui/building-ml-system

############ DEMAND FORECASTING COMMANDS ############
VERSION := 0.0.0
DOCKERFILE_DEMAND_FORECASTING = $(DEMAND_FORECASTING_DIR)/$(DOCKERFILE)
DOCKER_DEMAND_FORECASTING_TAG = demand_forecasting
DOCKER_DEMAND_FORECASTING_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_TAG)_$(VERSION)
DOCKER_DEMAND_FORECASTING_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DEMAND_FORECASTING_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: download_kaggle
download_kaggle:
	cd $(DEMAND_FORECASTING_DIR)/dataset && \
	kaggle competitions download -c demand-forecasting-kernels-only && \
	unzip demand-forecasting-kernels-only.zip

.PHONY: dvc_init
dvc_init:
	cd $(DEMAND_FORECASTING_DIR) && \
	dvc init --subdir
	
.PHONY: patch_demand_forecasting
patch_demand_forecasting:
	cd $(DEMAND_FORECASTING_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_demand_forecasting
minor_upgrade_demand_forecasting:
	cd $(DEMAND_FORECASTING_DIR) && \
	poetry version minor

.PHONY: major_upgrade_demand_forecasting
major_upgrade_demand_forecasting:
	cd $(DEMAND_FORECASTING_DIR) && \
	poetry version major

.PHONY: req_demand_forecasting
req_demand_forecasting:
	cd $(DEMAND_FORECASTING_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: req_demand_forecasting_test
req_demand_forecasting_test:
	cd $(DEMAND_FORECASTING_DIR) && \
	poetry export \
		--dev \
		--without-hashes \
		-f requirements.txt \
		--output requirements_test.txt

.PHONY: build_demand_forecasting
build_demand_forecasting: 
	docker build \
		-t $(DOCKER_DEMAND_FORECASTING_IMAGE_NAME) \
		-f $(DOCKERFILE_DEMAND_FORECASTING) \
		.
	 
.PHONY: push_demand_forecasting
push_demand_forecasting: 
	docker push $(DOCKER_DEMAND_FORECASTING_IMAGE_NAME)

.PHONY: build_demand_forecasting_test
build_demand_forecasting_test: build_demand_forecasting
	docker build \
		--build-arg FROM_IMAGE=$(DOCKER_DEMAND_FORECASTING_IMAGE_NAME) \
		-t $(DOCKER_DEMAND_FORECASTING_IMAGE_NAME_TEST) \
		-f $(DOCKERFILE_DEMAND_FORECASTING_TEST) \
		.

.PHONY: test_demand_forecasting
test_demand_forecasting: build_demand_forecasting_test
	docker run \
		--rm \
		--name test \
		$(DOCKER_DEMAND_FORECASTING_IMAGE_NAME_TEST)
