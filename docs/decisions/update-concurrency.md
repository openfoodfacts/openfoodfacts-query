# Dealing with concurrency during updates and migrations

## Context and Problem Statement

We don't want Redis updates to run at the same time as incremental sync as this could try to update the same product twice.

In addition, if we are running migrations we don't want updates to run as these can lock the tables we are migrating or be blocked if the migration is already running. This can cause excessive client generation and messages like "sorry, too many clients already".

This document describes the strategy for managing concurrency.

## Decision Drivers

* Updates can be paused during migrations as long as queries still work
* Redis updates should be quick whereas incremental or full sync will take longer

## Decision Outcome

Migrations should wait for all current updates to finish and then block further updates by locking the settings table and setting the pre_migration_message_id.

All other updates should also try to lock the settings table before proceeding. Once they get the lock then they should test to see if the pre_migration_message_id column is set and if it is they should abort the operation as this means a migration is running and the service is due to be re-started.

Incremental and full imports should block for the entire import, even if the batch is split into multiple transactions.
