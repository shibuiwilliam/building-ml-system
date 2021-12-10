ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 0.0.0

DOCKER_REPOSITORY := shibui/building-ml-system
TAG = ai_animals

DIR := $(ABSOLUTE_PATH)
K8S_DIR := $(ABSOLUTE_PATH)/infrastructure
K8S_SECRET_DIR := $(K8S_DIR)/secrets


############ DATA REGISTRY COMMANDS ############
DATA_REGISTRY_DIR := $(DIR)/data_registry
DOCKERFILE_DATA_REGISTRY = $(DATA_REGISTRY_DIR)/$(DOCKERFILE)
DOCKER_DATA_REGISTRY_TAG = $(TAG)_data_registry
DOCKER_DATA_REGISTRY_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DATA_REGISTRY_TAG)_$(VERSION)
DOCKER_DATA_REGISTRY_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DATA_REGISTRY_TAG)_$(VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_data_registry
patch_data_registry:
	cd $(DATA_REGISTRY_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_data_registry
minor_upgrade_data_registry:
	cd $(DATA_REGISTRY_DIR) && \
	poetry version minor

.PHONY: major_upgrade_data_registry
major_upgrade_data_registry:
	cd $(DATA_REGISTRY_DIR) && \
	poetry version major

.PHONY: req_data_registry
req_data_registry:
	cd $(DATA_REGISTRY_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_data_registry
build_data_registry: 
	docker build \
		-t $(DOCKER_DATA_REGISTRY_IMAGE_NAME) \
		-f $(DOCKERFILE_DATA_REGISTRY) \
		.
	 
.PHONY: push_data_registry
push_data_registry: 
	docker push $(DOCKER_DATA_REGISTRY_IMAGE_NAME)


############ BACKEND COMMANDS ############
BACKEND_DIR := $(DIR)/backend
BACKEND_MANIFEST_DIR := $(K8S_DIR)/manifests/backend
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
		-t $(DOCKER_BACKEND_IMAGE_NAME) \
		-f $(DOCKERFILE_BACKEND) \
		.

.PHONY: push_backend
push_backend: 
	docker push $(DOCKER_BACKEND_IMAGE_NAME)

.PHONY: deploy_backend_ns
deploy_backend_ns:
	kubectl apply -f $(BACKEND_MANIFEST_DIR)/namespace.yaml 

.PHONY: registry_backend
registry_backend: deploy_backend_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=aianimals ./private_registry_secret.sh

.PHONY: deploy_backend
deploy_backend: deploy_backend_ns
	kubectl apply -f $(BACKEND_MANIFEST_DIR)/postgres.yaml && \
	kubectl apply -f $(BACKEND_MANIFEST_DIR)/backend.yaml


############ ARGO COMMANDS ############
ARGO_MANIFEST_DIR := $(K8S_DIR)/manifests/argo

.PHONY: deploy_argo_ns
deploy_argo_ns:
	kubectl apply -f $(ARGO_MANIFEST_DIR)/namespace.yaml

.PHONY: registry_argo
registry_argo: deploy_argo_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=argo ./private_registry_secret.sh

.PHONY: deploy_argo
deploy_argo: deploy_argo_ns
	kubectl apply -f $(ARGO_MANIFEST_DIR)/quick_argo.yaml

.PHONY: port_forward_argo
port_forward_argo:
	kubectl -n argo port-forward service/argo-server 2746:2746 &

############ ELASTICSEARCH COMMANDS ############
ES_DIR := $(DIR)/elasticsearch
ES_MANIFEST_DIR := $(K8S_DIR)/manifests/elasticsearch
DOCKERFILE_ES = $(ES_DIR)/$(DOCKERFILE)
DOCKER_ES_TAG = $(TAG)_elasticsearch
DOCKER_ES_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_ES_TAG)_$(VERSION)

.PHONY: build_es
build_es: 
	docker build \
		-t $(DOCKER_ES_IMAGE_NAME) \
		-f $(DOCKERFILE_ES) \
		.

.PHONY: push_es
push_es:
	docker push $(DOCKER_ES_IMAGE_NAME)

.PHONY: deploy_es_ns
deploy_es_ns:
	kubectl apply -f $(ES_MANIFEST_DIR)/namespace.yaml

.PHONY: registry_es
registry_es: deploy_es_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=elastic-search ./private_registry_secret.sh

.PHONY: deploy_es
deploy_es: deploy_es_ns
	kubectl apply -f $(ES_MANIFEST_DIR)/crds.yaml && \
	kubectl apply -f $(ES_MANIFEST_DIR)/operator.yaml && \
	kubectl apply -f $(ES_MANIFEST_DIR)/deployment.yaml

.PHONY: es_password
es_password:
	kubectl -n elastic-search \
		get secret elastic-search-es-elastic-user \
		-o go-template='{{.data.elastic | base64decode}}'

.PHONY: port_forward_es
port_forward_es:
	kubectl -n elastic-search port-forward service/elastic-search-es-http 9200:9200 &

.PHONY: port_forward_kibana
port_forward_kibana:
	kubectl -n elastic-search port-forward service/kibana-kb-http 5601:5601 &


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


############ DEPLOYMENT COMMANDS ############
.PHONY: registry_default
registry_default:
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=default ./private_registry_secret.sh

.PHONY: admin_clusterrole
admin_clusterrole:
	@cd $(K8S_SECRET_DIR) && \
		./admin_clusterrole.sh

.PHONY: deploy_all
deploy_all: registry_default admin_clusterrole \
	registry_backend deploy_backend \
	registry_argo deploy_argo \
	registry_es deploy_es


############ ALL COMMANDS ############
.PHONY: req_all
req_all: req_data_registry req_backend
build_all: build_data_registry build_backend build_es
push_all: push_backend push_data_registry push_es
