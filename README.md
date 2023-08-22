# Open Food Facts Query Engine

This project extracts key product data from MongoDB into a Postgres database in order to support faster aggregate calculations

# Development

## Running locally

When running locally the project expects a Postgres database to be available on port 5432 and a Mongo database on port 27017, both on localhost.

The service is exposed on port 5510, to avoid clashing with Robotoff.

## Running in Docker

The project joins the Product Opener "po_default" network.

The project still uses its own Postgres database but will connect to product opener's Mongo database using the mongodb host.

The service is exposed to localhost on 5511

Use docker compose to start:

```
docker-compose up -d --build
```

## Calling from Product Opener

By default, product opener is configured to call the "query" host on the "po_default" network. To configure Product Opener to use a locally running instance update the following line in the Product Opener .env file:

`QUERY_URL=http://host.docker.internal:5510`
