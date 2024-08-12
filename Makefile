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

# Use this to start both the query service and associated database in Docker
up: run_deps
	docker compose up --build --wait

# Called by other projects to start this project as a dependency
run: run_deps
	COMPOSE_FILE=${COMPOSE_FILE_RUN} docker compose up -d

# This task starts a Postgres database in Docker and then prepares the local environment for development
dev: run_deps
	docker compose up --wait query_postgres
	npm install
	npm run migration:up

tests:
	npm test

lint:
	npm run lint

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
