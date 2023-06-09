#!make
include .env
SHELL := /bin/bash

# Constants
TAIL_LOGS = 50
PYTEST_WORKERS = 8

# Local develop
dev: complete-build sh

up:
	docker compose up --force-recreate -d

down:
	docker compose down

down-up: down up

start-registry:
	docker run -d -p ${REGISTRY_PORT}:5000 --restart=always --name "${REGISTRY_NAME}" registry:2

build:
	docker buildx build --platform linux/amd64 \
						--build-arg GIT_EMAIL="${GIT_EMAIL}" \
 						--build-arg GIT_NAME="${GIT_NAME}" \
						--output type=docker \
						-t ${DOCKER_CONTAINER_NAME}_image .
	docker tag ${DOCKER_CONTAINER_NAME}_image ${REGISTRY}:${REGISTRY_PORT}/${DOCKER_CONTAINER_NAME}_image

complete-build: build up activate-hooks

activate-hooks:
	docker exec -it ${DOCKER_CONTAINER_NAME} poetry run autohooks activate --mode poetry --force

sh:
	docker exec -it ${DOCKER_CONTAINER_NAME} bash

build-package:
	docker exec ${DOCKER_CONTAINER_NAME} poetry build

clean-dist:
	docker exec ${DOCKER_CONTAINER_NAME} rm -r dist
