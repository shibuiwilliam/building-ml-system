ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml

DOCKER_REPOSITORY := shibui/building-ml-system
TAG = ai_animals

DIR := $(ABSOLUTE_PATH)
K8S_DIR := $(ABSOLUTE_PATH)/infrastructure
K8S_SECRET_DIR := $(K8S_DIR)/secrets


############ DATA REGISTRY COMMANDS ############
DATA_REGISTRY_DIR := $(DIR)/batch/data_registry
DATA_REGISTRY_VERSION := $(shell cd ${DATA_REGISTRY_DIR} && poetry version -s)
DOCKERFILE_DATA_REGISTRY = $(DATA_REGISTRY_DIR)/$(DOCKERFILE)
DOCKER_DATA_REGISTRY_TAG = $(TAG)_data_registry
DOCKER_DATA_REGISTRY_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DATA_REGISTRY_TAG)_$(DATA_REGISTRY_VERSION)
DOCKER_DATA_REGISTRY_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_DATA_REGISTRY_TAG)_$(DATA_REGISTRY_VERSION)_$(DOCKER_TEST_TAG)

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


############ API COMMANDS ############
API_DIR := $(DIR)/api
API_VERSION := $(shell cd ${API_DIR} && poetry version -s)
API_MANIFEST_DIR := $(K8S_DIR)/manifests/api
DOCKERFILE_API = $(API_DIR)/$(DOCKERFILE)
DOCKER_API_TAG = $(TAG)_api
DOCKER_API_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_API_TAG)_$(API_VERSION)
DOCKER_API_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_API_TAG)_$(API_VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_api
patch_api:
	cd $(API_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_api
minor_upgrade_api:
	cd $(API_DIR) && \
	poetry version minor

.PHONY: major_upgrade_api
major_upgrade_api:
	cd $(API_DIR) && \
	poetry version major

.PHONY: req_api
req_api:
	cd $(API_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_api
build_api: 
	docker build \
		-t $(DOCKER_API_IMAGE_NAME) \
		-f $(DOCKERFILE_API) \
		.

.PHONY: push_api
push_api: 
	docker push $(DOCKER_API_IMAGE_NAME)

.PHONY: deploy_api_ns
deploy_api_ns:
	kubectl apply -f $(API_MANIFEST_DIR)/namespace.yaml 

.PHONY: registry_api
registry_api: deploy_api_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=aianimals ./private_registry_secret.sh

.PHONY: deploy_api
deploy_api: deploy_api_ns
	kubectl apply -f $(API_MANIFEST_DIR)/postgres.yaml && \
	kubectl apply -f $(API_MANIFEST_DIR)/api.yaml


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
ES_VERSION := $(shell cd ${ES_DIR} && poetry version -s)
ES_MANIFEST_DIR := $(K8S_DIR)/manifests/elasticsearch
DOCKERFILE_ES = $(ES_DIR)/$(DOCKERFILE)
DOCKER_ES_TAG = $(TAG)_elasticsearch
DOCKER_ES_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_ES_TAG)_$(ES_VERSION)

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


############ VIOLATION_DETECTION_REGISTRY COMMANDS ############
VIOLATION_DETECTION_REGISTRY_DIR := $(DIR)/violation_detection/registry
VIOLATION_DETECTION_REGISTRY_VERSION := $(shell cd ${VIOLATION_DETECTION_REGISTRY_DIR} && poetry version -s)
VIOLATION_DETECTION_REGISTRY_MANIFEST_DIR := $(K8S_DIR)/manifests/violation_detection/registry
DOCKERFILE_VIOLATION_DETECTION_REGISTRY = $(VIOLATION_DETECTION_REGISTRY_DIR)/$(DOCKERFILE)
DOCKER_VIOLATION_DETECTION_REGISTRY_TAG = $(TAG)_violation_detection_registry
DOCKER_VIOLATION_DETECTION_REGISTRY_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_VIOLATION_DETECTION_REGISTRY_TAG)_$(VIOLATION_DETECTION_REGISTRY_VERSION)
DOCKER_VIOLATION_DETECTION_REGISTRY_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_VIOLATION_DETECTION_REGISTRY_TAG)_$(VIOLATION_DETECTION_REGISTRY_VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_violation_detection_registry
patch_violation_detection_registry:
	cd $(VIOLATION_DETECTION_REGISTRY_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_violation_detection_registry
minor_upgrade_violation_detection_registry:
	cd $(VIOLATION_DETECTION_REGISTRY_DIR) && \
	poetry version minor

.PHONY: major_upgrade_violation_detection_registry
major_upgrade_violation_detection_registry:
	cd $(VIOLATION_DETECTION_REGISTRY_DIR) && \
	poetry version major

.PHONY: req_violation_detection_registry
req_violation_detection_registry:
	cd $(VIOLATION_DETECTION_REGISTRY_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_violation_detection_registry
build_violation_detection_registry: 
	docker build \
		-t $(DOCKER_VIOLATION_DETECTION_REGISTRY_IMAGE_NAME) \
		-f $(DOCKERFILE_VIOLATION_DETECTION_REGISTRY) \
		.

.PHONY: push_violation_detection_registry
push_violation_detection_registry: 
	docker push $(DOCKER_VIOLATION_DETECTION_REGISTRY_IMAGE_NAME)


############ NO_ANIMAL_VIOLATION COMMANDS ############
NO_ANIMAL_VIOLATION_DIR := $(DIR)/violation_detection/no_animal_violation/proxy
NO_ANIMAL_VIOLATION_VERSION := $(shell cd ${NO_ANIMAL_VIOLATION_DIR} && poetry version -s)
NO_ANIMAL_VIOLATION_MANIFEST_DIR := $(K8S_DIR)/manifests/violation_detection/no_animal_violation
DOCKERFILE_NO_ANIMAL_VIOLATION = $(NO_ANIMAL_VIOLATION_DIR)/$(DOCKERFILE)
DOCKER_NO_ANIMAL_VIOLATION_TAG = $(TAG)_violation_detection_no_animal_violation
DOCKER_NO_ANIMAL_VIOLATION_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_NO_ANIMAL_VIOLATION_TAG)_$(NO_ANIMAL_VIOLATION_VERSION)
DOCKER_NO_ANIMAL_VIOLATION_IMAGE_NAME_TEST = $(DOCKER_REPOSITORY):$(DOCKER_NO_ANIMAL_VIOLATION_TAG)_$(NO_ANIMAL_VIOLATION_VERSION)_$(DOCKER_TEST_TAG)

.PHONY: patch_violation_detection_no_animal_violation
patch_violation_detection_no_animal_violation:
	cd $(NO_ANIMAL_VIOLATION_DIR) && \
	poetry version patch

.PHONY: minor_upgrade_violation_detection_no_animal_violation
minor_upgrade_violation_detection_no_animal_violation:
	cd $(NO_ANIMAL_VIOLATION_DIR) && \
	poetry version minor

.PHONY: major_upgrade_violation_detection_no_animal_violation
major_upgrade_violation_detection_no_animal_violation:
	cd $(NO_ANIMAL_VIOLATION_DIR) && \
	poetry version major

.PHONY: req_violation_detection_no_animal_violation
req_violation_detection_no_animal_violation:
	cd $(NO_ANIMAL_VIOLATION_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_violation_detection_no_animal_violation
build_violation_detection_no_animal_violation: 
	docker build \
		-t $(DOCKER_NO_ANIMAL_VIOLATION_IMAGE_NAME) \
		-f $(DOCKERFILE_NO_ANIMAL_VIOLATION) \
		.

.PHONY: push_violation_detection_no_animal_violation
push_violation_detection_no_animal_violation: 
	docker push $(DOCKER_NO_ANIMAL_VIOLATION_IMAGE_NAME)


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
	registry_api deploy_api \
	registry_argo deploy_argo \
	registry_es deploy_es


############ ALL COMMANDS ############
.PHONY: req_all
req_all: \
	req_data_registry \
	req_api \
	req_violation_detection_no_animal_violation \
	req_violation_detection_registry

.PHONY: build_all
build_all: \
	build_data_registry \
	build_api \
	build_es \
	build_violation_detection_no_animal_violation \
	build_violation_detection_registry

.PHONY: push_all
push_all: \
	push_api \
	push_data_registry \
	push_es \
	push_violation_detection_no_animal_violation \
	push_violation_detection_registry