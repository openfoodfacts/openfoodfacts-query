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

# Called by other projects to start this project as a dependency
run: run_deps
	COMPOSE_FILE=${COMPOSE_FILE_RUN} docker compose up -d

start_postgres:
	docker compose up --wait query_postgres

# This task starts a Postgres database in Docker and then prepares the local environment for development
dev: run_deps install migrate_database_local

migrate_database_local: start_postgres
	poetry run python query/migrator.py

migrate_database_docker:
	docker compose run --rm -e PYTHONPATH=/code query python query/migrator.py

watch: migrate_database_local
	poetry run python query/main.py watch

tests:
	poetry run pytest ${args}

lint:
	poetry run autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables query
	poetry run isort --profile black query
	poetry run black query

# Refresh the countries.json file from the ProductOwner taxonomy
refresh_countries:
	python scripts/refresh_countries.py

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
