ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 0.0.0

DOCKER_REPOSITORY := shibui/building-ml-system

DIR := $(ABSOLUTE_PATH)
TAG = ai_gazos


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


