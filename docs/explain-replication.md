# Explain replication of postgres database

Postgres has the capability to replicate a primary instance,
into multiple secondary instances.
Those secondary instances cannot be used for writing but can be use for requests.
In normal condition, the replication is very fast,
in degraded conditions, it will catch up as soon as it can without loosing data.

You can find a lot of documentation on internet, official doc includes:
- the [official chapter on High Availability, Load Balancing, and Replication](https://www.postgresql.org/docs/current/high-availability.html)
- the [postgres reference config is here](https://www.postgresql.org/docs/current/runtime-config-replication.html)

In our case we want to have a replica so that we can make it available to our community,
to create dashboards and so on using superset.

## How it is implemented

On the primary server, we have to add some configurations,
in order for it to accept replication connections,
and keep write ahead logs for enough time that in case of network loss
the replicas can catch up.
This is possible by mounting a different configuration file for postgres.

We also have to create a user for replication, which is done by `make create_replication_user`.

On the secondary servers, we use the same docker compose,
but we disable the app by using a different docker compose profile,
and there we tweak the configuration to connect to the primary
in replication mode.

Most of the things are configured at deployment time,
see the `container-deploy.yml` workflow.

## Bootstraping replication

The replication must be boostrapped.
This is the step where the replica asks for all data to primary instance,
before starting to look at the stream of events.

For this we need to avoid starting the replica container,
because the docker image will immediately create a new database,
according to environment (if that happens we must remove data from the postgres volume).
Note that in development we set the POSTGRES_PASSWORD to empty on the replica
which prevents a database from being created.

Instead we run the container using `pg_basebackup`.

Something like:
```bash
docker compose run --rm --entrypoint bash query_postgres

/usr/local/bin/pg_basebackup --host <remote_host> --port <remote_port> --username replication --password --pgdata /var/lib/postgresql/data --progress --wal-method=stream --write-recovery-conf --create-slot --slot <slot_name> -v
...
exit
```
The slot name must be a unique value to this replica.

If it happens that we want to restart the process,
we need first to remove the slot on the primary host,
using `select pg_drop_replication_slot('<slot_name>');`. Or alternatively you can run the `pg_basebackup` command with the `--create-slot` option removed.


## Testing it on your own

See [How to test replication locally](./how-to-test-replication-localy.md)

See also [How we setup replication on hetzner for superset](https://openfoodfacts.github.io/openfoodfacts-infrastructure/reports/2025-12-16-setting-up-query-postgres-replication/)