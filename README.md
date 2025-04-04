# Open Food Facts Query Engine

This project extracts key product data from MongoDB into a Postgres database in order to support faster aggregate calculations

# Development

## Running locally

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

This is mainly an SQL-based project so the Python application framework is kept to a minimum. The main folders (inside the `query` folder) are as follows:

 - Root folder: API routes (in `main.py`), schedule definition and other core dependencies, i.e. PostgreSQL, MongoDB and Redis
 - `tables`: Each table, or set of very similar tables (like tags) has a module. This contains all of the SQL for modifying the data and structure of the table, so even `migrations` call out to functions in these modules. The `tables` modules will contain limited business logic, mostly where this would be the equivalent of a database trigger
 - `migrations`: These manage database schema updates. Note in most cases the SQL itself is in the relevant `tables` module. The migration history is stored in a table called `mikro_orm_migrations` for backward compatibility with the previous NestJS / Mikro-ORM implementation of this project
 - `services`: This is where most of the complex business logic lives, where interactions between multiple tables are coordinated
 - `models`: These are the [Pydantic](https://docs.pydantic.dev/) classes used to validate API requests and generate OpenAPI documentation.
 - `views`: The SQL definition for any views that are created in the database during migrations
 - `assets`: Non-python resources

The entrypoint is main.py which runs database migrations and starts the service and scheduler.

## Design Philosophy

Most of the logic in this project is in the actual SQL used to update and query data. There has therefore been conscious decision to avoid using any kind of ORM to hade the SQL from the code.

Pydantic models are only used for outward-facing models to ensure we get good API documentation and validation. Internally, data is mainly passed around using dictionaries or the [asyncpg Record](https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.Record) structure (which behaves like a dictionary).

## Testing

The unit tests use testcontainers to create a temporary Postgres database and Redis instance in Docker, which lasts for the duration of the test run. The tests share the same database while running, so ensure that tests are independent from one another by using randomized product codes / tags.

Tests are mingled in with the project structure to make it easier to find them. A TDD approach to development is recommended.

## Calling from Product Opener

By default, product opener is configured to call the "query" host on the `COMMON_NET_NAME` network. To configure Product Opener to use a locally running instance update the following line in the Product Opener .env file:

```
QUERY_URL=http://host.docker.internal:5510
```

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

The `dev.yml` override simply adds the Docker build instruction.

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
# selection
curl -d '{"categories_tags": "en:teas"}' -H "Content-Type: application/json" http://localhost:5510/select
# aggergation
curl -d '[{"$match": {"countries_tags": "en:france"}},{"$group":{"_id":"$brands_tags"}}]' -H "Content-Type: application/json" http://localhost:5510/aggregate
```


