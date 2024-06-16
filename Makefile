#!/usr/bin/make

# use bash everywhere !
SHELL := /bin/bash
# some vars
ENV_FILE ?= .env

# load env variables to be able to use them in this file
# also takes into account envrc (direnv file)
ifneq (,$(wildcard ./${ENV_FILE}))
    -include ${ENV_FILE}
    -include .envrc
    export
endif

create_folders:
	mkdir -p ${QUERY_DATA_DIR}

# Use this to start both the query service and associated database in Docker
up: create_folders
	docker compose up -d --build

# This task starts a Postgres database in Docker and then prepares the local environment for development
dev: create_folders
	docker compose up -d query_postgres
	npm install
	npm run migration:up

tests:
	npm test

lint:
	npm run lint

# PRODUCTION
create_external_volumes:
	@echo "🎣 No external volumes (it's all cache !)"

create_external_networks:
	@echo "🎣 Creating external networks (production only) …"
	docker network create --driver=bridge --subnet="172.30.0.0/16" ${COMMON_NET_NAME} \
	|| echo "network already exists"
