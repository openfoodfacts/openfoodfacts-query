# Open Food Facts Query Engine

This project extracts key product data from MongoDB into a Postgres database in order to support faster aggregate calculations

# Contributing

In this project we are attempting to use discussions to explore ideas and only converting these to issues when development is imminent or if it is a reproducible bug. See [here](https://github.com/openfoodfacts/openfoodfacts-query/discussions?discussions_q=is%3Aopen+label%3A%22good+first+issue%22) for "good first issues".

# Development

## Running locally

Make sure you use the same version of python that is mentioned in the `Dockerfile`. I used [pyenv](https://github.com/pyenv/pyenv) to install it. This also required installing the build dependencies mentioned in the pyenv [wiki](https://github.com/pyenv/pyenv/wiki#suggested-build-environment). If you switch to a different version of python you may need to run `poetry env use <version>` and also update the interpreter path in your IDE.

When running locally the project expects a Postgres database to be available on port 5512 and a Mongo database on port 27017, both on localhost. Running docker-compose will create a suitable Postgres database if needed. The database name can be set in the environment, but the schema name is always "query".

To get started...

### Create a Postgres database in Docker

Run the following:

```
docker compose up -d query_postgres
```

### Use an existing Postgres database

Update the POSTGRES_HOST (and other necessary) environment variables to reference your existing database.

Please use the `.envrc` file to override settings so that edits are not committed to the repo.

When connecting to a PostgreSQL database running on a Windows host from a WSL2 instance you will need to enable the PostgreSQL port (5432) in Windows Firewall.

### Prepare for development

Run the following:

```
make dev
```

You can then start in watch mode with:

```
make watch
```

The service is exposed on port 5510, to avoid clashing with Robotoff. You can check the service is running by viewing the [health check](http://localhost:5510/health) endpoint.

## Frameworks and libraries

[FastAPI](https://fastapi.tiangolo.com/) is used to support the REST APIs. Non-blocking I/O is achieved using [asyncio](https://docs.python.org/3/library/asyncio.html) and this influences the PostgreSQL. MongoDB and Redis clients used.

[Pydantic](https://docs.pydantic.dev/) is used to model externally visible schemas. The generated OpenAPI documentation can be found [here](http://localhost:5510/docs). There is also a [redoc](http://localhost:5510/redoc) version.

Other than that the reliance on external code is kept to a minimum so that the project is easy for someone new to understand what's going on.

## Project Structure

This is mainly an SQL-based project so the Python application framework is kept to a minimum. The docstring in the `__init__.py` in each of the folders describes its purpose.

The entrypoint is main.py which runs database migrations and starts the service and scheduler.

## Design Philosophy

Most of the logic in this project is in the actual SQL used to update and query data. There has therefore been conscious decision to avoid using any kind of ORM to hide the SQL from the code.

Pydantic models are only used for outward-facing models to ensure we get good API documentation and validation. Internally, data is mainly passed around using dictionaries or the [asyncpg Record](https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.Record) structure (which behaves like a dictionary).

## Testing

The unit tests use testcontainers to create a temporary Postgres database and Redis instance in Docker, which lasts for the duration of the test run. The tests share the same database while running, so ensure that tests are independent from one another by using randomized product codes / tags.

Tests are mingled in with the project structure to make it easier to find them. A TDD approach to development is recommended.

Note that all tests are classified as "unit" tests as no external dependencies are needed. However, we use testcontainers to provide transient instances of PostgreSQL and Redis so that these do not need to be mocked all of the time.

## Calling from Product Opener

By default, product opener is configured to call the "query" host on the `COMMON_NET_NAME` network. To configure Product Opener to use a locally running instance update the following line in the Product Opener .env file:

```
QUERY_URL=http://host.docker.internal:5510
```
Note that when uploading scans the off-query PostgreSQL database username and password must be passed in using basic auth. This can be done by including them in the off-query URL, e.g.
```
QUERY_URL=http://DATABASE_USER:DATABASE_PASSWORD@query:5510
```

## Product Refresh Process

The service subscribes to `product_updates` events, as documented [here](./docs/events/openfoodfacts-query.html). Data for changed products is fetched directly from MongoDB.

An incremental refresh is also performed every night.

## Running in Docker

The project joins the Product Opener `COMMON_NET_NAME` network.

The project still uses its own Postgres database but will connect to shared-services Mongo database using the "mongodb" host.

The service is exposed to localhost on 5511 to avoid clashing with any locally running instance.

Use docker compose to start:

```
make up
```

## Adding new tags

Support for new tags can be done by simply adding a further entity definition in the product_tags.py file. Extra migration logic will be needed to create the table.

The tag won't be picked up for queries until a full import is done (when it will be added to the loaded_tag table).

## Deployment vs Development

The main `docker-compose.yml` creates the openfoodfacts-query service and associated Postgres database and expects MongoDB to already exist.

The `docker-compose-run.yml` override explicitly sets the `MONGO_URI` and `REDIS_URL` variables to access those services within Docker.

The `compose-dev.yml` override simply adds the Docker build instruction.

# Use

## Import from Mongo

To refresh the Query Postgres database with the current tags from MongoDB you can invoked a browser with:

```
http://localhost:5510/importfrommongo?from
```

The "from" option ensures that an incremental import is performed. If no date is supplied then the query service will look at the latest updated time for products it has already processed and only fetch products from MongoDB that have been updated since then. An explicit date can also be specified in the from parameter, e.g. "from=2023-02-23". If no from parameter is applied then all data in the Postgres database will be deleted and a full import will be performed.

## Performing queries

The "count", "aggregate" and "find" POST endpoints accept a MongoDB style filter and aggregate pipeline respectively. Syntax support is only basic and is limited to what Product Opener currently uses. See the tests for some examples of what is supported.

You can test with curl with something like:
```bash
# find. Note that this fetches the actual product data from MongoDB
curl -d '{"filter":{"categories_tags": "en:teas"},"projection":{"_id":0,"product_name":1},"limit":10}' -H "Content-Type: application/json" http://localhost:5510/find
# aggergation
curl -d '[{"$match": {"countries_tags": "en:france"}},{"$group":{"_id":"$brands_tags"}}]' -H "Content-Type: application/json" http://localhost:5510/aggregate
```


