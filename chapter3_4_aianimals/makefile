ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 0.0.0

DOCKER_REPOSITORY := shibui/building-ml-system

DIR := $(ABSOLUTE_PATH)
TAG = ai_animals


############ DATA MANAGER COMMANDS ############
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
		--platform linux/amd64 \
		-t $(DOCKER_DATA_MANAGER_IMAGE_NAME) \
		-f $(DOCKERFILE_DATA_MANAGER) \
		.
	 
.PHONY: push_data_manager
push_data_manager: 
	docker push $(DOCKER_DATA_MANAGER_IMAGE_NAME)


############ BACKEND COMMANDS ############
BACKEND_DIR := $(DIR)/backend
DOCKERFILE_BACKEND = $(BACKEND_DIR)/$(DOCKERFILE)
DOCKER_BACKEND_TAG = $(TAG)_backend
DOCKER_BACKEND_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_BACKEND_TAG)_$(VERSION)
DOCKER_BACKEND_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_BACKEND_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_backend
patch_backend:
	cd $(BACKEND_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_backend
minor_upgrade_backend:
	cd $(BACKEND_DIR) && \
	poetry version minor

.PHONY: major_upgrade_backend
major_upgrade_backend:
	cd $(BACKEND_DIR) && \
	poetry version major

.PHONY: req_backend
req_backend:
	cd $(BACKEND_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_backend
build_backend: 
	docker build \
		--platform linux/amd64 \
		-t $(DOCKER_BACKEND_IMAGE_NAME) \
		-f $(DOCKERFILE_BACKEND) \
		.
	 
.PHONY: push_backend
push_backend: 
	docker push $(DOCKER_BACKEND_IMAGE_NAME)


############ KUBERNETES COMMANDS ############
K8S_DIR := $(ABSOLUTE_PATH)/infrastructure
K8S_SECRET_DIR := $(K8S_DIR)/secrets

.PHONY: admin_clusterrole
admin_clusterrole:
	@cd $(K8S_SECRET_DIR) && \
		./admin_clusterrole.sh


############ ARGO COMMANDS ############
ARGO_DIR := $(K8S_DIR)/manifests/argo

.PHONY: argo_registry
argo_registry:
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=argo ./private_registry_secret.sh

.PHONY: argo_deploy
argo_deploy:
	kubectl apply -f $(ARGO_DIR)/namespace.yaml && \
	kubectl apply -f $(ARGO_DIR)/quick_argo.yaml


############ ELASTICSEARCH COMMANDS ############
ES_DIR := $(K8S_DIR)/manifests/elasticsearch

.PHONY: es_registry
es_registry:
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=argo ./private_registry_secret.sh

.PHONY: es_deploy
es_deploy:
	kubectl apply -f $(ES_DIR)/crds.yaml && \
	kubectl apply -f $(ES_DIR)/operator.yaml && \
	kubectl apply -f $(ES_DIR)/deployment.yaml

.PHONY: es_password
es_password:
	kubectl -n elastic-search \
		get secret elastic-search-es-elastic-user \
		-o go-template='{{.data.elastic | base64decode}}'


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


############ ALL COMMANDS ############
.PHONY: req_all
req_all: req_data_manager req_backend
build_all: build_data_manager build_backend
push_all: push_backend push_data_manager
