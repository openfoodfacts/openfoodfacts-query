# How to test replication locally

## How it works

In a development setup the primary database is already configured to support replication based on the settings in the `dev_primary.conf` and `dev_primary_hba.conf` files.

The replica database uses the `dev_replica.conf` file to set up the connection back to the primary database, and uses the default `base_hba.conf`. The replica database is exposed on port 5513 by default.

The following procedure sets up a separate docker compose project with just the replica database, configured to connect to the primary using its alias (defined in `DOCKER_POSTGRES_ALIAS`)

## Initial setup

Let's assume you have already cloned this repository once
with working configuration to run openfoodfacts-query (refer to the README).

Open one terminal window to interact with the primary database and start a second terminal to interact with the replica.

In the replica terminal run the following to set up the environment to just create a replica database:

```bash
. env/setenv.sh replica
```

## Modify primary configuration

The only additional step required for the primary database is to add a replication user. Run the following from the primary terminal:

```bash
make create_replication_user -e POSTGRES_REPLICATION_PASSWORD=test
```

Note: In case it was already there with a password you don't know,
you may run:
```bash
docker compose exec query_postgres psql -h localhost -U productopener -W query -c 'drop role replication;'
```
and run creation command again.

At this point postgres should be up and accepting connections.

## Modify replica configuration

This time go to the replica terminal.

We don't start the container yet,
we need to initialize the data first.

### Initialize data on replica

Now that we have our primary and replica,
we can initialize data.

We will get the data from the primary to initiate the database.
This is done thanks to the [pg_basebackup](https://www.postgresql.org/docs/current/app-pgbasebackup.html) command. From the replica terminal run:
```
docker compose run --rm --entrypoint bash query_postgres

/usr/local/bin/pg_basebackup --host query_postgres_primary --port 5432 --username replication --password --pgdata /var/lib/postgresql/data --progress --wal-method=stream --write-recovery-conf --create-slot --slot dev_replica -v
...
exit
```
If you are re-initialising replication when it has already been used before on the primary database then remove the `--create-slot` option.

Now we can start the database:
```bash
make up
```
(or `docker compose up`)

## Verify it's working

You can now go to the replica terminal and see if the database is here,
as well as the user and the tables.

```
docker compose exec query_postgres psql -h localhost -U productopener -W query
Password:
psql (16.9)
Type "help" for help.

query=# \d
```

You can also change data on product opener, if you have it deployed,
and see if, for example, product_update_event table is updated.
