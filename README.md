# Open Food Facts Query Engine
This project extracts key product data from MongoDB into a Postgres database in order to support faster aggregate calculations

# Development
Use docker compose to start:

```
docker-compose up -d
```

By default, this project expects Product Opener (openfoodfacts-server) to be available to supply the source (Mongo) database, with a local Postgres database to store the results.

To use a local version of MongoDB comment the PO_MONGO line in the .env file. To share the Postgres (Minion) instance with Product Opener uncomment the PO_POSTGRES line.
