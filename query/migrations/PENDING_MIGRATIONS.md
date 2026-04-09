Make a note here of any migrations that need to be added in that would not be backward compatible with previous deployed versions.

For example, if an old table needs to be dropped or a column is renamed.

We do this because migrations are run before the previous instance of the service is stopped in order to minimize downtime.

# Pending migrations

- Drop obsolete column from products, product_tags, product_country and product_ingredients
  as it is now condensed in collection_id column
- Drop last_updated from settings as it is now in collection_type table