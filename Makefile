dev:
	docker-compose up -d --build
	npm install
	npm run migration:up