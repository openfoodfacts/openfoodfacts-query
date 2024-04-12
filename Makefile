# Use this to start both the query service and associated database in Docker
up:
	docker compose up -d --build

# This task starts a Postgres database in Docker and then prepares the local environment for development
dev:
	docker compose up -d query_postgres
	npm install
	npm run migration:up

tests:
	npm test

lint:
	npm run lint
