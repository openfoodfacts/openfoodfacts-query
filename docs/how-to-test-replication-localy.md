# How to test replication locally

## Initial setup

Let's assume you have already cloned this repository once
with working configuration to run openfoodfacts-query (refer to the README).

Clone the repository a second time to have a replica.

Eg.
```bash
git clone git@github.com:openfoodfacts/openfoodfacts-query.git off-query-replica
```

In the following I will call your original openfoodfacts-query clone **primary**,
and the clone created for replication **replica**.

## Modify primary configuration

Go to the primary repository.

We will:
* change postgres configuration to allow replication
* allow for connections from the replica
* recreate postgres
* add a replication user

We will first create the configuration files:
```bash
# start from the dev files
cp confs/postgresql/dev.conf confs/postgresql/dev_primary.conf
cp confs/postgresql/dev_hba.conf confs/postgresql/dev_primary_hba.conf

# Edit config to add replication settings
echo "# Add replication settings for main postgres" >> confs/postgresql/dev_primary.conf
echo "wal_level=replica" >> confs/postgresql/dev_primary.conf
echo "max_wal_senders=3" >> confs/postgresql/dev_primary.conf
echo "# We don't set a large wal_keep_size because we will use slots" >> confs/postgresql/dev_primary.conf
echo "max_slot_wal_keep_size=20GB" >> confs/postgresql/dev_primary.conf
echo "max_slot_wal_keep_size=30GB" >> confs/postgresql/dev_primary.conf

# Edit hba file to enable connection of replica
echo "# Replica connects through docker network" >> confs/postgresql/dev_primary_hba.conf
echo "# so they are viewed as in local network" >> confs/postgresql/dev_primary_hba.conf
echo "host    replication     all             10.0.0.0/8                 scram-sha-256" >> confs/postgresql/dev_primary_hba.conf
echo "host    replication     all             192.168.0.0/16                 scram-sha-256" >> confs/postgresql/dev_primary_hba.conf
echo "host    replication     all             172.16.0.0/12                 scram-sha-256" >> confs/postgresql/dev_primary_hba.conf
```

Now we activate those configuration files in our primary docker.
We also need to publish POSTGRES to every interface of the host,
because the replica will be in another network.
Edit your .envrc to add:
```bash
export POSTGRES_CONFIG_FILE=./confs/postgresql/dev_primary.conf
export POSTGRES_HBA_FILE=./confs/postgresql/dev_primary_hba.conf
export POSTGRES_EXPOSE=0.0.0.0:5512
```
(don't forget to run `direnv allow` if you use direnv)

Then we relaunch the docker forcing creation of a new container,
to ensure our new environment variables are taken into account.
If you use direnv, you can launch:
```bash
docker compose up --force-recreate
```
otherwise use:
```bash
docker compose rm -sf query_postgres
make up
```

Finally we add a replication user:
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

This time go to the replication repository.

We will:
* change postgres configuration to be in replication mode as a client
* recreate postgres

We will first create the configuration files:
```bash
# start from the dev files
cp confs/postgresql/dev.conf confs/postgresql/dev_replica.conf
cp confs/postgresql/dev_hba.conf confs/postgresql/dev_replica_hba.conf

# add replication settings
echo "# replication settings for replicate" >> confs/postgresql/dev_replica.conf
echo "# We use localhost to connect to the primary postgres" >> confs/postgresql/dev_replica.conf
echo "primary_conninfo='host=host.docker.internal port=5512 user=replication password=test'" >> confs/postgresql/dev_replica.conf
echo "# use a simple slot name" >> confs/postgresql/dev_replica.conf
echo "primary_slot_name=dev_replica" >> confs/postgresql/dev_replica.conf
echo "# we need hot standby if we want to run requests" >> confs/postgresql/dev_replica.conf
echo "hot_standby=on" >> confs/postgresql/dev_replica.conf
```

We now need to activate those configuration files in our replica docker,
change the PROFILE to avoid launching the app,
but we also need to change the COMPOSE_PROJECT_NAME so that our instance
is not the same as the primary one,
we will also change network to avoid app reaching the replica instead of the primary.
Finally we also must use a different expose port for the replica,
to avoid conflicts with primary postgres (as we run on same host).
We will also remove POSTGRES_PASSWORD to avoid database initialization,
by init_db.

Edit your .envrc (if you use the Makefile or direnv) to add:
```bash
export POSTGRES_CONFIG_FILE=./confs/postgresql/dev_replica.conf
export POSTGRES_HBA_FILE=./confs/postgresql/dev_replica_hba.conf

export COMPOSE_PROJECT_NAME=off-query-replica
# Note that the replica profile does not exists, but just exclude the app
export COMPOSE_PROFILES=replica

export POSTGRES_EXPOSE=127.0.0.1:5612
export COMMON_NET_NAME=off_query_replica

export POSTGRES_REPLICATION_SOURCE_HOST=host.docker.internal
export POSTGRES_REPLICATION_SOURCE_PORT=5512

export POSTGRES_PASSWORD=

```
(don't forget to run `direnv allow` if you use direnv)

Create the network:
```bash
docker network create off_query_replica
```

We don't start the container yet,
we need to initialize the data first.

## Initialize data on replica

Now that we have our primary and replica,
we can initialize data.

Go to the replica repository.
Activate the env variables (either through direnv or with a `source .envrc`)

We will get the data from the primary to initiate the database.
This is done thanks to the [pg_basebackup](https://www.postgresql.org/docs/current/app-pgbasebackup.html) command:
```
docker compose run --entry-point bash query_postgres

/usr/local/bin/pg_basebackup --host host.docker.internal --port 5512 --username replication --password --pgdata /var/lib/postgresql/data --progress --wal-method=stream --write-recovery-conf --create-slot --slot dev_replica -v
...
exit
```

Now we can start the database:
```bash
make up
```
(or `docker compose up`)

## Verify it's working

You can now go to the replica project and see if the database is here,
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
