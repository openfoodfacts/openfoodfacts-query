"""These manage database schema updates. Note in most cases the SQL itself is in the relevant `tables` module.
The migration history is stored in a table called `mikro_orm_migrations` for backward compatibility with the
previous NestJS / Mikro-ORM implementation of this project"""