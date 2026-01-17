#!/usr/bin/make

# use bash everywhere !
SHELL := /bin/bash

# load env variables to be able to use them in this file
# also takes into account envrc (direnv file)
include .env
-include .envrc
export

# Set the DEPS_DIR if it hasn't been set already
ifeq (${DEPS_DIR},)
	export DEPS_DIR=${PWD}/deps
endif

install:
	poetry install

build:
	docker compose build

# Use this to start both the query service and associated database in Docker
up: run_deps build
	docker compose up --wait

_up: run_deps
	docker compose up --wait

# Called by other projects to start this project as a dependency
run: run_deps
	COMPOSE_FILE=${COMPOSE_FILE_RUN} docker compose up -d

start_postgres:
	docker compose up --wait query_postgres

# This task starts a Postgres database in Docker and then prepares the local environment for development
dev: run_deps install migrate_database_local

migrate_database_local: start_postgres
	poetry run python -m query.migrator

migrate_database_docker:
	docker compose run --rm query python -m query.migrator

# used for deployment
create_external_networks:
		@echo "🔍 Creating external networks (production only) …"
		docker network create ${COMMON_NET_NAME} \
		|| echo "network already exists"

# in staging/prod, volumes might be on virtiofs,
# so we prefer to create them manually
create_external_volumes:
		@echo  "🔍 Creating external volumes (production only) …"
		docker volume create ${COMPOSE_PROJECT_NAME}_dbdata \
		|| echo "volume already exists"

create_replication_user:
	@echo  "🔍 Creating replication user (production only) …"
# user @ to avoid exposing password
	@docker compose exec query_postgres \
	  bash -c "PGPASSWORD=${POSTGRES_PASSWORD} psql -h 127.0.0.1 -U ${POSTGRES_USER} ${POSTGRES_DB} -c \"create role replication with replication login password '${POSTGRES_REPLICATION_PASSWORD}'\" || true "

create_superset_user:
	@docker compose exec query_postgres \
	  bash -c "PGPASSWORD=${POSTGRES_PASSWORD} psql -h 127.0.0.1 -U ${POSTGRES_USER} ${POSTGRES_DB} -c \
	  \" \
	  create role superset login password '${POSTGRES_SUPERSET_PASSWORD}'; \
	  grant pg_read_all_data to superset; \
	  \" \
	  || true "

watch: migrate_database_local
	poetry run python -m query.main watch

tests:
	poetry run pytest ${args}

lint:
	poetry run autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables query scripts
	poetry run isort --profile black query scripts
	poetry run black query scripts

# Refresh the countries.json file from the ProductOwner taxonomy
refresh_countries:
	python scripts/refresh_countries.py

build_asyncapi:
	npm list -g @asyncapi/cli || npm install -g @asyncapi/cli
	cd docs/events && asyncapi generate fromTemplate openfoodfacts-query.yaml @asyncapi/html-template@3.0.0 --use-new-generator --param singleFile=true outFilename=openfoodfacts-query.html --force-write --output=.

# Run dependent projects
run_deps: clone_deps
	@for dep in ${DEPS} ; do \
		cd ${DEPS_DIR}/$$dep && $(MAKE) run; \
	done

# Clone dependent projects without running them
clone_deps:
	@mkdir -p ${DEPS_DIR}; \
	for dep in ${DEPS} ; do \
		echo $$dep; \
		if [ ! -d ${DEPS_DIR}/$$dep ]; then \
			git clone --filter=blob:none --sparse \
				https://github.com/openfoodfacts/$$dep.git ${DEPS_DIR}/$$dep; \
		else \
			cd ${DEPS_DIR}/$$dep && git pull; \
		fi; \
	done

# Stop dependent projects
stop_deps:
	@for dep in ${DEPS} ; do \
		cd ${DEPS_DIR}/$$dep && $(MAKE) stop; \
	done

# Called from other projects to stop this project
stop:
	COMPOSE_FILE=${COMPOSE_FILE_RUN} docker compose stop
	$(MAKE) stop_deps
