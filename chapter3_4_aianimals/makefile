ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml

DOCKER_REPOSITORY := shibui/building-ml-system
TAG = ai_animals

DIR := $(ABSOLUTE_PATH)
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
	kubectl apply -f $(DATA_MANIFEST_DIR)/postgres.yaml && \
	kubectl apply -f $(DATA_MANIFEST_DIR)/redis.yaml && \
	kubectl apply -f $(DATA_MANIFEST_DIR)/rabbitmq.yaml

.PHONY: connect_postgres
connect_postgres:
	kubectl -n default \
		run postgresql-client \
		--rm --tty -i \
		--restart="Never" \
		--image bitnami/postgresql \
		--env="PGPASSWORD=password" \
		--command -- psql --host postgres.data.svc.cluster.local -U postgres


############ MLFLOW COMMANDS ############
MLFLOW_DIR := $(DIR)/mlflow
MLFLOW_VERSION := 0.0.0
MLFLOW_MANIFEST_DIR := $(K8S_DIR)/manifests/mlflow
DOCKERFILE_MLFLOW = $(MLFLOW_DIR)/$(DOCKERFILE)
DOCKER_MLFLOW_TAG = $(TAG)_mlflow
DOCKER_MLFLOW_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_MLFLOW_TAG)_$(MLFLOW_VERSION)

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

.PHONY: port_forward_mlflow
port_forward_mlflow:
	kubectl -n mlflow port-forward service/mlflow 5000:5000 &


############ BASE_TEXT_PROCESSING COMMANDS ############
BASE_TEXT_PROCESSING_DIR := $(DIR)/base_text_processing
BASE_TEXT_PROCESSING_VERSION := $(shell cd ${BASE_TEXT_PROCESSING_DIR} && poetry version -s)
DOCKERFILE_BASE_TEXT_PROCESSING = $(BASE_TEXT_PROCESSING_DIR)/$(DOCKERFILE)
DOCKER_BASE_TEXT_PROCESSING_TAG = $(TAG)_base_text_processing
DOCKER_BASE_TEXT_PROCESSING_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_BASE_TEXT_PROCESSING_TAG)_$(BASE_TEXT_PROCESSING_VERSION)

.PHONY: req_base_text_processing
req_base_text_processing:
	cd $(BASE_TEXT_PROCESSING_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_base_text_processing
build_base_text_processing: 
	docker build \
		--platform x86_64 \
		-t $(DOCKER_BASE_TEXT_PROCESSING_IMAGE_NAME) \
		-f $(DOCKERFILE_BASE_TEXT_PROCESSING) \
		.

.PHONY: push_base_text_processing
push_base_text_processing: 
	docker push $(DOCKER_BASE_TEXT_PROCESSING_IMAGE_NAME)


############ DATA REGISTRY COMMANDS ############
DATA_REGISTRY_DIR := $(DIR)/batch/data_registry
DATA_REGISTRY_VERSION := $(shell cd ${DATA_REGISTRY_DIR} && poetry version -s)
DOCKERFILE_DATA_REGISTRY = $(DATA_REGISTRY_DIR)/$(DOCKERFILE)
DOCKER_DATA_REGISTRY_TAG = $(TAG)_data_registry
DOCKER_DATA_REGISTRY_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DATA_REGISTRY_TAG)_$(DATA_REGISTRY_VERSION)

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
		--platform x86_64 \
		--build-arg FROM_IMAGE=$(DOCKER_BASE_TEXT_PROCESSING_IMAGE_NAME) \
		-t $(DOCKER_DATA_REGISTRY_IMAGE_NAME) \
		-f $(DOCKERFILE_DATA_REGISTRY) \
		.
	 
.PHONY: push_data_registry
push_data_registry: 
	docker push $(DOCKER_DATA_REGISTRY_IMAGE_NAME)


############ API COMMANDS ############
API_DIR := $(DIR)/api
API_VERSION := $(shell cd ${API_DIR} && poetry version -s)
API_MANIFEST_DIR := $(K8S_DIR)/manifests/aianimals
DOCKERFILE_API = $(API_DIR)/$(DOCKERFILE)
DOCKER_API_TAG = $(TAG)_api
DOCKER_API_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_API_TAG)_$(API_VERSION)

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
		--platform x86_64 \
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

.PHONY: secret_api
secret_api:
	kubectl -n aianimals \
		create secret generic auth-secret \
		--from-file=infrastructure/secrets/secret.key

.PHONY: deploy_api
deploy_api: registry_api
	kubectl apply -f $(API_MANIFEST_DIR)/api.yaml

.PHONY: port_forward_api
port_forward_api:
	kubectl -n aianimals port-forward service/api 8000:8000 &


############ BATCH COMMANDS ############
BATCH_MANIFEST_DIR := $(K8S_DIR)/manifests/aianimals

.PHONY: deploy_batch_config
deploy_batch_config: registry_api
	kubectl apply \
		-f $(BATCH_MANIFEST_DIR)/data_configmap.yaml

.PHONY: deploy_initial_data_registry
deploy_initial_data_registry: deploy_batch_config
	kubectl apply \
		-f $(BATCH_MANIFEST_DIR)/initial_data_registry.yaml

.PHONY: deploy_search_registry
deploy_search_registry:
	kubectl apply \
		-f $(BATCH_MANIFEST_DIR)/search_registry.yaml


.PHONY: deploy_animal_feature_registry
deploy_animal_feature_registry:
	kubectl apply \
		-f $(BATCH_MANIFEST_DIR)/animal_feature_registry.yaml

############ AB_TEST_PROXY COMMANDS ############
AB_TEST_PROXY_DIR := $(DIR)/ab_test_proxy
AB_TEST_PROXY_VERSION := $(shell cd ${AB_TEST_PROXY_DIR} && poetry version -s)
DOCKERFILE_AB_TEST_PROXY = $(AB_TEST_PROXY_DIR)/$(DOCKERFILE)
DOCKER_AB_TEST_PROXY_TAG = $(TAG)_ab_test_proxy
DOCKER_AB_TEST_PROXY_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_AB_TEST_PROXY_TAG)_$(AB_TEST_PROXY_VERSION)

.PHONY: req_ab_test_proxy
req_ab_test_proxy:
	cd $(AB_TEST_PROXY_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_ab_test_proxy
build_ab_test_proxy: 
	docker build \
		--platform x86_64 \
		-t $(DOCKER_AB_TEST_PROXY_IMAGE_NAME) \
		-f $(DOCKERFILE_AB_TEST_PROXY) \
		.

.PHONY: push_ab_test_proxy
push_ab_test_proxy: 
	docker push $(DOCKER_AB_TEST_PROXY_IMAGE_NAME)


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
	kubectl -n argo apply -f $(ARGO_MANIFEST_DIR)/argo_clusterrolebinding.yaml
	kubectl -n argo apply -f $(ARGO_MANIFEST_DIR)/quick_argo.yaml

.PHONY: port_forward_argo
port_forward_argo:
	kubectl -n argo port-forward service/argo-server 2746:2746 &
	echo "Open https://127.0.0.1:2746"

.PHONY: create_argo_similar_image_search_train_cron
create_argo_similar_image_search_train_cron:
	argo cron create infrastructure/manifests/argo/workflow/search_similar_image_search_train.yaml

.PHONY: submit_argo_no_animal_violation_train
submit_argo_no_animal_violation_train:
	argo submit infrastructure/manifests/argo/workflow/no_animal_violation_train.yaml


############ ELASTICSEARCH COMMANDS ############
ES_DIR := $(DIR)/elasticsearch
ES_VERSION := 0.0.0
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
deploy_es: registry_es
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


############ SEARCH COMMANDS ############
SEARCH_MANIFEST_DIR := $(K8S_DIR)/manifests/search

.PHONY: deploy_search_ns
deploy_search_ns:
	kubectl apply \
		-f $(SEARCH_MANIFEST_DIR)/namespace.yaml

.PHONY: registry_search
registry_search: deploy_search_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=search ./private_registry_secret.sh


############ SEARCH_LEARN_TO_RANK_TRAIN COMMANDS ############
SEARCH_LEARN_TO_RANK_TRAIN_DIR := $(DIR)/search/model_development/learn_to_rank
SEARCH_LEARN_TO_RANK_TRAIN_VERSION := $(shell cd ${SEARCH_LEARN_TO_RANK_TRAIN_DIR} && poetry version -s)
SEARCH_LEARN_TO_RANK_TRAIN_MANIFEST_DIR := $(K8S_DIR)/manifests/search/learn_to_rank_train
DOCKERFILE_SEARCH_LEARN_TO_RANK_TRAIN = $(SEARCH_LEARN_TO_RANK_TRAIN_DIR)/$(DOCKERFILE)
DOCKER_SEARCH_LEARN_TO_RANK_TRAIN_TAG = $(TAG)_search_learn_to_rank_train
DOCKER_SEARCH_LEARN_TO_RANK_TRAIN_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_SEARCH_LEARN_TO_RANK_TRAIN_TAG)_$(SEARCH_LEARN_TO_RANK_TRAIN_VERSION)

.PHONY: req_search_learn_to_rank_train
req_search_learn_to_rank_train:
	cd $(SEARCH_LEARN_TO_RANK_TRAIN_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_search_learn_to_rank_train
build_search_learn_to_rank_train: 
	docker build \
		--platform x86_64 \
		--build-arg FROM_IMAGE=$(DOCKER_BASE_TEXT_PROCESSING_IMAGE_NAME) \
		-t $(DOCKER_SEARCH_LEARN_TO_RANK_TRAIN_IMAGE_NAME) \
		-f $(DOCKERFILE_SEARCH_LEARN_TO_RANK_TRAIN) \
		.

.PHONY: push_search_learn_to_rank_train
push_search_learn_to_rank_train: 
	docker push $(DOCKER_SEARCH_LEARN_TO_RANK_TRAIN_IMAGE_NAME)


############ SEARCH_LEARN_TO_RANK_LGBM_API COMMANDS ############
SEARCH_LEARN_TO_RANK_LGBM_API_DIR := $(DIR)/search/learn_to_rank/api
SEARCH_LEARN_TO_RANK_LGBM_API_VERSION := $(shell cd ${SEARCH_LEARN_TO_RANK_LGBM_API_DIR} && poetry version -s)
SEARCH_LEARN_TO_RANK_LGBM_API_MANIFEST_DIR := $(K8S_DIR)/manifests/search_learn_to_rank_lgbm_api
DOCKERFILE_SEARCH_LEARN_TO_RANK_LGBM_API = $(SEARCH_LEARN_TO_RANK_LGBM_API_DIR)/$(DOCKERFILE)
DOCKER_SEARCH_LEARN_TO_RANK_LGBM_API_TAG = $(TAG)_search_learn_to_rank_lgbm_api
DOCKER_SEARCH_LEARN_TO_RANK_LGBM_API_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_SEARCH_LEARN_TO_RANK_LGBM_API_TAG)_$(SEARCH_LEARN_TO_RANK_LGBM_API_VERSION)

.PHONY: req_search_learn_to_rank_lgbm_api
req_search_learn_to_rank_lgbm_api:
	cd $(SEARCH_LEARN_TO_RANK_LGBM_API_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_search_learn_to_rank_lgbm_api
build_search_learn_to_rank_lgbm_api: 
	docker build \
		--platform x86_64 \
		--build-arg FROM_IMAGE=$(DOCKER_BASE_TEXT_PROCESSING_IMAGE_NAME) \
		-t $(DOCKER_SEARCH_LEARN_TO_RANK_LGBM_API_IMAGE_NAME) \
		-f $(DOCKERFILE_SEARCH_LEARN_TO_RANK_LGBM_API) \
		.

.PHONY: push_search_learn_to_rank_lgbm_api
push_search_learn_to_rank_lgbm_api: 
	docker push $(DOCKER_SEARCH_LEARN_TO_RANK_LGBM_API_IMAGE_NAME)

.PHONY: deploy_search_learn_to_rank_lgbm_api
deploy_search_learn_to_rank_lgbm_api: 
	kubectl apply \
		-f $(SEARCH_MANIFEST_DIR)/search_learn_to_rank_lgbm_api.yaml


############ SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN COMMANDS ############
SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_DIR := $(DIR)/search/model_development/similar_image_search
SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_VERSION := $(shell cd ${SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_DIR} && poetry version -s)
SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_MANIFEST_DIR := $(K8S_DIR)/manifests/search/similar_image_search
DOCKERFILE_SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN = $(SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_DIR)/$(DOCKERFILE)
DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_TAG = $(TAG)_search_similar_image_search_train
DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_TAG)_$(SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_VERSION)

.PHONY: req_search_similar_image_search_train
req_search_similar_image_search_train:
	cd $(SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_search_similar_image_search_train
build_search_similar_image_search_train:
	docker build \
		--platform x86_64 \
		-t $(DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_IMAGE_NAME) \
		-f $(DOCKERFILE_SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN) \
		.

.PHONY: push_search_similar_image_search_train
push_search_similar_image_search_train: 
	docker push $(DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_TRAIN_IMAGE_NAME)


############ SIMILAR_IMAGE_SEARCH_PROXY COMMANDS ############
SIMILAR_IMAGE_SEARCH_PROXY_DIR := $(DIR)/search/similar_image_search/proxy
SIMILAR_IMAGE_SEARCH_PROXY_VERSION := $(shell cd ${SIMILAR_IMAGE_SEARCH_PROXY_DIR} && poetry version -s)
DOCKERFILE_SIMILAR_IMAGE_SEARCH_PROXY = $(SIMILAR_IMAGE_SEARCH_PROXY_DIR)/$(DOCKERFILE)
DOCKER_SIMILAR_IMAGE_SEARCH_PROXY_TAG = $(TAG)_search_similar_image_search_proxy
DOCKER_SIMILAR_IMAGE_SEARCH_PROXY_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_SIMILAR_IMAGE_SEARCH_PROXY_TAG)_$(SIMILAR_IMAGE_SEARCH_PROXY_VERSION)

.PHONY: req_search_similar_image_search_proxy
req_search_similar_image_search_proxy:
	cd $(SIMILAR_IMAGE_SEARCH_PROXY_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_search_similar_image_search_proxy
build_search_similar_image_search_proxy: 
	docker build \
		--platform x86_64 \
		-t $(DOCKER_SIMILAR_IMAGE_SEARCH_PROXY_IMAGE_NAME) \
		-f $(DOCKERFILE_SIMILAR_IMAGE_SEARCH_PROXY) \
		.

.PHONY: push_search_similar_image_search_proxy
push_search_similar_image_search_proxy: 
	docker push $(DOCKER_SIMILAR_IMAGE_SEARCH_PROXY_IMAGE_NAME)

.PHONY: deploy_similar_image_search_proxy
deploy_similar_image_search_proxy: registry_search
	kubectl apply \
		-f $(SEARCH_MANIFEST_DIR)/similar_image_search_proxy.yaml


############ SEARCH_SIMILAR_IMAGE_SEARCH_SERVING COMMANDS ############
SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_DIR := $(DIR)/search/similar_image_search/serving
SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_VERSION := 0.0.0
DOCKERFILE_SEARCH_SIMILAR_IMAGE_SEARCH_SERVING = $(SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_DIR)/$(DOCKERFILE)
DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_TAG = $(TAG)_search_similar_image_search_serving
DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_TAG)_$(SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_VERSION)

.PHONY: build_search_similar_image_search_serving
build_search_similar_image_search_serving: 
	docker build \
		--platform x86_64 \
		-t $(DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_IMAGE_NAME) \
		-f $(DOCKERFILE_SEARCH_SIMILAR_IMAGE_SEARCH_SERVING) \
		.

.PHONY: push_search_similar_image_search_serving
push_search_similar_image_search_serving: 
	docker push $(DOCKER_SEARCH_SIMILAR_IMAGE_SEARCH_SERVING_IMAGE_NAME)

.PHONY: deploy_similar_image_search_serving
deploy_similar_image_search_serving: registry_search
	kubectl apply \
		-f $(SEARCH_MANIFEST_DIR)/similar_image_search_serving.yaml


############ VIOLATION_DETECTION COMMANDS ############
VIOLATION_DETECTION_MANIFEST_DIR := $(K8S_DIR)/manifests/violation_detection

.PHONY: deploy_violation_detection_ns
deploy_violation_detection_ns:
	kubectl apply \
		-f $(VIOLATION_DETECTION_MANIFEST_DIR)/namespace.yaml

.PHONY: registry_violation_detection
registry_violation_detection: deploy_violation_detection_ns
	@cd $(K8S_SECRET_DIR) && \
		NAMESPACE=violation-detection ./private_registry_secret.sh


############ VIOLATION_DETECTION_REGISTRY COMMANDS ############
VIOLATION_DETECTION_REGISTRY_DIR := $(DIR)/violation_detection/registry
VIOLATION_DETECTION_REGISTRY_VERSION := $(shell cd ${VIOLATION_DETECTION_REGISTRY_DIR} && poetry version -s)
DOCKERFILE_VIOLATION_DETECTION_REGISTRY = $(VIOLATION_DETECTION_REGISTRY_DIR)/$(DOCKERFILE)
DOCKER_VIOLATION_DETECTION_REGISTRY_TAG = $(TAG)_violation_detection_registry
DOCKER_VIOLATION_DETECTION_REGISTRY_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_VIOLATION_DETECTION_REGISTRY_TAG)_$(VIOLATION_DETECTION_REGISTRY_VERSION)

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
		--platform x86_64 \
		-t $(DOCKER_VIOLATION_DETECTION_REGISTRY_IMAGE_NAME) \
		-f $(DOCKERFILE_VIOLATION_DETECTION_REGISTRY) \
		.

.PHONY: push_violation_detection_registry
push_violation_detection_registry: 
	docker push $(DOCKER_VIOLATION_DETECTION_REGISTRY_IMAGE_NAME)

.PHONY: deploy_violation_detection_registry
deploy_violation_detection_registry: registry_violation_detection
	kubectl apply \
		-f $(VIOLATION_DETECTION_MANIFEST_DIR)/registry.yaml


############ NO_ANIMAL_VIOLATION_TRAIN COMMANDS ############
NO_ANIMAL_VIOLATION_TRAIN_DIR := $(DIR)/violation_detection/model_development/no_animal_violation
NO_ANIMAL_VIOLATION_TRAIN_VERSION := $(shell cd ${NO_ANIMAL_VIOLATION_TRAIN_DIR} && poetry version -s)
NO_ANIMAL_VIOLATION_TRAIN_MANIFEST_DIR := $(K8S_DIR)/manifests/violation_detection/no_animal_violation_train
DOCKERFILE_NO_ANIMAL_VIOLATION_TRAIN = $(NO_ANIMAL_VIOLATION_TRAIN_DIR)/$(DOCKERFILE)
DOCKER_NO_ANIMAL_VIOLATION_TRAIN_TAG = $(TAG)_violation_detection_no_animal_violation_train
DOCKER_NO_ANIMAL_VIOLATION_TRAIN_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_NO_ANIMAL_VIOLATION_TRAIN_TAG)_$(NO_ANIMAL_VIOLATION_TRAIN_VERSION)

.PHONY: req_violation_detection_no_animal_violation_train
req_violation_detection_no_animal_violation_train:
	cd $(NO_ANIMAL_VIOLATION_TRAIN_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_violation_detection_no_animal_violation_train
build_violation_detection_no_animal_violation_train: 
	docker build \
		--platform x86_64 \
		-t $(DOCKER_NO_ANIMAL_VIOLATION_TRAIN_IMAGE_NAME) \
		-f $(DOCKERFILE_NO_ANIMAL_VIOLATION_TRAIN) \
		.

.PHONY: push_violation_detection_no_animal_violation_train
push_violation_detection_no_animal_violation_train: 
	docker push $(DOCKER_NO_ANIMAL_VIOLATION_TRAIN_IMAGE_NAME)


############ NO_ANIMAL_VIOLATION_PROXY COMMANDS ############
NO_ANIMAL_VIOLATION_PROXY_DIR := $(DIR)/violation_detection/no_animal_violation/proxy
NO_ANIMAL_VIOLATION_PROXY_VERSION := $(shell cd ${NO_ANIMAL_VIOLATION_PROXY_DIR} && poetry version -s)
DOCKERFILE_NO_ANIMAL_VIOLATION_PROXY = $(NO_ANIMAL_VIOLATION_PROXY_DIR)/$(DOCKERFILE)
DOCKER_NO_ANIMAL_VIOLATION_PROXY_TAG = $(TAG)_violation_detection_no_animal_violation_proxy
DOCKER_NO_ANIMAL_VIOLATION_PROXY_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_NO_ANIMAL_VIOLATION_PROXY_TAG)_$(NO_ANIMAL_VIOLATION_PROXY_VERSION)

.PHONY: req_violation_detection_no_animal_violation_proxy
req_violation_detection_no_animal_violation_proxy:
	cd $(NO_ANIMAL_VIOLATION_PROXY_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_violation_detection_no_animal_violation_proxy
build_violation_detection_no_animal_violation_proxy: 
	docker build \
		--platform x86_64 \
		-t $(DOCKER_NO_ANIMAL_VIOLATION_PROXY_IMAGE_NAME) \
		-f $(DOCKERFILE_NO_ANIMAL_VIOLATION_PROXY) \
		.

.PHONY: push_violation_detection_no_animal_violation_proxy
push_violation_detection_no_animal_violation_proxy: 
	docker push $(DOCKER_NO_ANIMAL_VIOLATION_PROXY_IMAGE_NAME)

.PHONY: deploy_no_animal_violation_proxy
deploy_no_animal_violation_proxy: registry_violation_detection
	kubectl apply \
		-f $(VIOLATION_DETECTION_MANIFEST_DIR)/no_animal_violation_proxy.yaml


############ NO_ANIMAL_VIOLATION_SERVING COMMANDS ############
NO_ANIMAL_VIOLATION_SERVING_DIR := $(DIR)/violation_detection/no_animal_violation/serving
NO_ANIMAL_VIOLATION_SERVING_VERSION := 0.0.0
DOCKERFILE_NO_ANIMAL_VIOLATION_SERVING = $(NO_ANIMAL_VIOLATION_SERVING_DIR)/$(DOCKERFILE)
DOCKER_NO_ANIMAL_VIOLATION_SERVING_TAG = $(TAG)_violation_detection_no_animal_violation_serving
DOCKER_NO_ANIMAL_VIOLATION_SERVING_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_NO_ANIMAL_VIOLATION_SERVING_TAG)_$(NO_ANIMAL_VIOLATION_SERVING_VERSION)

.PHONY: build_violation_detection_no_animal_violation_serving
build_violation_detection_no_animal_violation_serving: 
	docker build \
		--platform x86_64 \
		-t $(DOCKER_NO_ANIMAL_VIOLATION_SERVING_IMAGE_NAME) \
		-f $(DOCKERFILE_NO_ANIMAL_VIOLATION_SERVING) \
		.

.PHONY: push_violation_detection_no_animal_violation_serving
push_violation_detection_no_animal_violation_serving: 
	docker push $(DOCKER_NO_ANIMAL_VIOLATION_SERVING_IMAGE_NAME)

.PHONY: deploy_no_animal_violation_serving
deploy_no_animal_violation_serving: registry_violation_detection
	kubectl apply \
		-f $(VIOLATION_DETECTION_MANIFEST_DIR)/no_animal_violation_serving.yaml


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
	registry_api \
	registry_violation_detection \
	registry_es \
	registry_mlflow \
	registry_argo \
	registry_search \
	secret_api

.PHONY: deploy_all
deploy_all: deploy_data \
	deploy_es \
	deploy_argo \
	deploy_mlflow \
	deploy_initial_data_registry \
	deploy_api \
	deploy_violation_detection_registry \
	deploy_no_animal_violation_serving \
	deploy_no_animal_violation_proxy \
	deploy_search_registry \
	deploy_animal_feature_registry \
	deploy_similar_image_search_serving

.PHONY: delete_namespaces
delete_namespaces:
	kubectl delete ns aianimals & \
	kubectl delete ns argo & \
	kubectl delete ns data & \
	kubectl delete ns elastic-search & \
	kubectl delete ns elastic-system & \
	kubectl delete ns mlflow & \
	kubectl delete ns violation-detection

############ ALL COMMANDS ############
.PHONY: req_all
req_all: \
	req_base_text_processing \
	req_data_registry \
	req_api \
	req_ab_test_proxy \
	req_violation_detection_no_animal_violation_proxy \
	req_violation_detection_registry \
	req_violation_detection_no_animal_violation_train \
	req_search_learn_to_rank_train \
	req_search_similar_image_search_train \
	req_search_similar_image_search_proxy \
	req_search_learn_to_rank_lgbm_api

.PHONY: build_all
build_all: \
	build_mlflow \
	build_base_text_processing \
	build_data_registry \
	build_api \
	build_ab_test_proxy \
	build_es \
	build_violation_detection_no_animal_violation_proxy \
	build_violation_detection_no_animal_violation_serving \
	build_violation_detection_registry \
	build_violation_detection_no_animal_violation_train \
	build_search_learn_to_rank_train \
	build_search_similar_image_search_train \
	build_search_similar_image_search_proxy \
	build_search_learn_to_rank_lgbm_api
	
.PHONY: push_all
push_all: \
	push_mlflow \
	push_base_text_processing \
	push_api \
	push_ab_test_proxy \
	push_data_registry \
	push_es \
	push_violation_detection_no_animal_violation_proxy \
	push_violation_detection_no_animal_violation_serving \
	push_violation_detection_registry \
	push_violation_detection_no_animal_violation_train \
	push_search_learn_to_rank_train \
	push_search_similar_image_search_train \
	push_search_similar_image_search_proxy \
	push_search_learn_to_rank_lgbm_api
	