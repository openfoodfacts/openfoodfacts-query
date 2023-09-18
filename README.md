# Open Food Facts Query Engine

This project extracts key product data from MongoDB into a Postgres database in order to support faster aggregate calculations

# Development

## Running locally

When running locally the project expects a Postgres database to be available on port 5512 and a Mongo database on port 27017, both on localhost. Running docker-compose will create a suitable Postgres database if needed. The database name can be set in the environment, but the schema name is always "query".

To get started...

### Create a Postgres database in Docker

Run the following:

```
docker-compose up -d --build
```

### Use an existing Postgres database

Update the POSTGRES_HOST (and other necessary) environment variables to reference your existing database. Please don't commit any changes to the .env file if this is edited.

### Prepare for development

Run the following:

```
npm install
npm run migration:up
```

You can then start in watch mode with:

```
npm run start:dev
```

The service is exposed on port 5510, to avoid clashing with Robotoff.

## Testing

The unit tests use testcontainers to create a temporary Postgres database in Docker, which lasts for the duration of the test run. The tests share the same database while running, so ensure that tests are independant from one another by using randmoised product codes / tags.

## Calling from Product Opener

By default, product opener is configured to call the "query" host on the "po_default" network. To configure Product Opener to use a locally running instance update the following line in the Product Opener .env file:

```
QUERY_URL=http://host.docker.internal:5510
```

## Running in Docker

The project joins the Product Opener "po_default" network.

The project still uses its own Postgres database but will connect to product opener's Mongo database using the "mongodb" host.

The service is exposed to localhost on 5511 to avoid clashing with any locally running instance.

Use docker compose to start:

```
docker-compose up -d --build
```

# Deployment vs Development

The main docker-compose.yml creates the openfoodfacts-query service and associated Postres database and expects MongoDB to already exist.

The dev.yml Docker Compose joins the services to the po_default network to ease communication with Product Opener and MongoDB. The prod.yml uses the po_webnet network.

# Use

## Import from Mongo

The `make refresh_product_tags` command from Product Opener will refresh the Query Postgres database with the current tags from MongoDB. This can also be invoked from a browser with:

```
http://localhost:5510/importfrommongo?from
```

The "from" option ensures that an incremental import is performed. If no date is supplied then the query service will look at the latest modified time for products it already has and only fetch products from MongoDB that have been modified since then. An explicit date can also be specified in the from parameter, e.g. "from=2023-02-23". If no from parameter is applied then all data in the Postgres database will be deleted and a full import will be performed.

## Import from File

There is also an importfromfile endpoint which will import from a file called openfoodfacts-products.jsonl in the data directory. This local folder is mapped to the container in dev.yml.

## Performing queries

The "count" and "aggregate" POST endpoints accept a MongoDB style filter and aggregate pipeline respectively. Syntax support is only basic and is limted to what Product Opener currently uses. See the tests for some examples of what is supported.

# TODO

- Run tests on PR
- Add branch protection
- Configure production deployment
