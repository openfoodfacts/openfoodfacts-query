Make a note here of any migrations that need to be added in that would not be backward compatible with previous deployed versions.

For example, if an old table needs to be dropped or a column is renamed.

We do this because migrations are run before the previous instance of the service is stopped in order to minimize downtime.

# Pending migrations

- drop table loaded_tag