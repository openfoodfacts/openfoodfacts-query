# Python off-query Project

## Folders

- migrations: Database migrations. These generally run SQL from the table or view modules so that all SQL is "owned" by the relevant module
- models: Pydantic class models
- services: Business logic that operates on the models
- tables: Repositories for database table storage
- views: View SQL definitions (only called from migrations)
