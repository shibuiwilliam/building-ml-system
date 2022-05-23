ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 1.0.0

DOCKER_REPOSITORY := shibui/building-ml-system

DIR := $(ABSOLUTE_PATH)
TAG = beverage_sales_forecasting

K8S_DIR := $(ABSOLUTE_PATH)/infrastructure
K8S_SECRET_DIR := $(K8S_DIR)/secrets


############ DATA COMMANDS ############
DATA_MANIFEST_DIR := $(K8S_DIR)/manifests/data

.PHONY: deploy_data_ns
deploy_data_ns:
	kubectl apply -f $(DATA_MANIFEST_DIR)/namespace.yaml 

.PHONY: registry_data
registry_data: deploy_data_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=data ./private_registry_secret.sh

.PHONY: deploy_data
deploy_data: registry_data
	kubectl apply -f $(DATA_MANIFEST_DIR)/postgres.yaml

.PHONY: connect_postgres
connect_postgres:
	kubectl -n default \
		run postgresql-client \
		--rm --tty -i \
		--restart="Never" \
		--image bitnami/postgresql \
		--env="PGPASSWORD=password" \
		--command -- psql --host postgres.data.svc.cluster.local -U postgres


############ DEMAND FORECASTING DATA_REGISTRATION COMMANDS ############
DATA_REGISTRATION_DIR := $(DIR)/data_registration
DATA_REGISTRATION_MANIFEST_DIR := $(K8S_DIR)/manifests/beverage_sales_forecasting
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

.PHONY: deploy_data_registration_ns
deploy_data_registration_ns:
	kubectl apply -f $(DATA_REGISTRATION_MANIFEST_DIR)/namespace.yaml 

.PHONY: registry_data_registration
registry_data_registration: deploy_data_registration_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=beverage-sales-forecasting ./private_registry_secret.sh

.PHONY: deploy_initial_data_registration
deploy_initial_data_registration: registry_data_registration
	kubectl apply -f $(DATA_REGISTRATION_MANIFEST_DIR)/initial_data_registration.yaml


############ DEMAND FORECASTING MLFLOW COMMANDS ############
MLFLOW_DIR := $(DIR)/mlflow
MLFLOW_MANIFEST_DIR := $(K8S_DIR)/manifests/mlflow
DOCKERFILE_MLFLOW = $(MLFLOW_DIR)/$(DOCKERFILE)
DOCKER_MLFLOW_TAG = $(TAG)_mlflow
DOCKER_MLFLOW_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_MLFLOW_TAG)_$(VERSION)

.PHONY: build_mlflow
build_mlflow: 
	docker build \
		-t $(DOCKER_MLFLOW_IMAGE_NAME) \
		-f $(DOCKERFILE_MLFLOW) \
		.
	 
.PHONY: push_mlflow
push_mlflow: 
	docker push $(DOCKER_MLFLOW_IMAGE_NAME)

.PHONY: deploy_mlflow_ns
deploy_mlflow_ns:
	kubectl apply -f $(MLFLOW_MANIFEST_DIR)/namespace.yaml 

.PHONY: registry_mlflow
registry_mlflow: deploy_mlflow_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=mlflow ./private_registry_secret.sh

.PHONY: deploy_mlflow
deploy_mlflow: registry_mlflow
	kubectl apply -f $(MLFLOW_MANIFEST_DIR)/mlflow.yaml


############ DEMAND FORECASTING ML COMMANDS ############
ML_DIR := $(DIR)/ml
DOCKERFILE_ML = $(ML_DIR)/$(DOCKERFILE)
DOCKER_ML_TAG = $(TAG)_ml
DOCKER_ML_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_ML_TAG)_$(VERSION)

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


############ DEMAND FORECASTING BI COMMANDS ############
BI_DIR := $(DIR)/bi
BI_MANIFEST_DIR := $(K8S_DIR)/manifests/beverage_sales_forecasting
DOCKERFILE_BI = $(BI_DIR)/$(DOCKERFILE)
DOCKER_BI_TAG = $(TAG)_bi
DOCKER_BI_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_BI_TAG)_$(VERSION)

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

.PHONY: deploy_bi_ns
deploy_bi_ns:
	kubectl apply -f $(BI_MANIFEST_DIR)/namespace.yaml 

.PHONY: registry_bi
registry_bi: deploy_bi_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=beverage-sales-forecasting ./private_registry_secret.sh

.PHONY: deploy_bi
deploy_bi: registry_bi
	kubectl apply -f $(BI_MANIFEST_DIR)/bi.yaml


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
deploy_argo: registry_argo
	kubectl \
		-n argo apply \
		-f $(ARGO_MANIFEST_DIR)/argo_clusterrolebinding.yaml && \
	kubectl \
		-n argo apply \
		-f https://github.com/argoproj/argo-workflows/releases/download/v3.3.1/quick-start-postgres.yaml

.PHONY: create_argo_data_registration
create_argo_data_registration:
	argo cron create infrastructure/manifests/argo/workflow/data_registration.yaml


############ DEPLOYMENT COMMANDS ############
KUBE_SYSTEM_MANIFEST_DIR := $(K8S_DIR)/manifests/kube_system

.PHONY: deploy_kube_system
deploy_kube_system:
	kubectl apply -f $(KUBE_SYSTEM_MANIFEST_DIR)/pdb.yaml

.PHONY: registry_default
registry_default:
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=default ./private_registry_secret.sh

.PHONY: initialize_deployment
initialize_deployment: deploy_kube_system \
	registry_default \
	registry_data \
	registry_argo \
	registry_mlflow \
	registry_bi \
	registry_data_registration

.PHONY: deploy_base
deploy_base: deploy_argo \
	deploy_data \
	deploy_bi \
	deploy_mlflow

.PHONY: deploy_job
deploy_job: deploy_initial_data_registration

.PHONY: delete_namespaces
delete_namespaces:
	kubectl delete ns argo & \
	kubectl delete ns data & \
	kubectl delete ns mlflow & \
	kubectl delete ns beverage-sales-forecasting


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
