# Explain database structure

Open Food Facts Query copies selected product data from Open Food Facts into PostgreSQL.

It was set up to replace MongoDB facet-style queries (counts, filters, sorting),
but it uses a relational structure that is also useful for analytics.

## Main idea

The database is organized around a few families of tables:

- `product`: the main table, with one row per product and the scalar fields that are often filtered or sorted on
- `product_*_tag`: facet tables for arrays of values such as categories, brands, labels, countries, and many other `*_tags` fields
- `product_update_event` and `product_update`: tables for product events and a lighter event history used by queries
- `nutrient` and `product_nutrient`: normalized nutrient tables
- a few derived tables such as `product_country`, which supports country-specific filtering and popularity sorting

## Product information

The `product` table is the root table.
It stores the product code and a selection of direct product fields such as the name, creator, timestamps, completeness, nutriscore, environmental score, and scan counters.

The `collection_id` column is also important.
It encodes both the product family and the state of the product in one value: for example food, obsolete food, petfood, beauty, generic product, or deleted.
The query code maps API-level filters such as `product_type` and `obsolete` to a `collection_id`, and then uses that value in SQL to keep queries simple.
The same identifier is copied to related tables that are queried directly, so filtering stays consistent across the schema.

## Facets

Many Open Food Facts fields are arrays, especially the `*_tags` fields.
These values are often normalized and mapped to [taxonomies](https://wiki.openfoodfacts.org/Taxonomies_introduction).

Instead of storing those arrays in one column, Query expands them into separate tables such as `product_categories_tag`, `product_brands_tag`, or `product_labels_tag`.
Each row links one product to one facet value.

This makes filtering and aggregations much simpler in SQL.
In practice, these tables are what back most "facet" style queries.

`product_country` follows the same idea, but with a dedicated table because it also stores popularity counters used for country-specific sorting.

## Nutrients

Nutrients are stored separately from the root `product` table.
The `nutrient` table stores the list of known nutrient keys, and `product_nutrient` stores the value for one nutrient on one product.

The import code mainly keeps values normalized at the product / nutrient level, using the `_100g` values from `nutriments` or the aggregated nutrition structure when present.
That keeps nutrient filtering and sorting consistent.

## Product events

`product_update_event` stores the raw event message as JSON, together with message and timestamp metadata.
`product_update` is a more query-friendly version of that history: it links an event to a product, a revision, an update type, a contributor, and an update date.
The `contributor` table stores the event `user_id` values in its `code` column.

So the database keeps both:

- the original event payload for traceability
- a lean relational table for reporting and queries on product history

## Indexes

The schema already defines the main indexes used by the query layer.
For example, `product` has indexes on `code`, `process_id`, and several common sort/filter columns, each `product_*_tag` table has an index on `product_id`, and tables such as `product_country`, `product_nutrient`, `product_update`, and `product_update_event` have dedicated indexes for their main access patterns.

## Some notes about the code

The project does not use a classic ORM with one class per table.
Instead, each table, or group of very similar tables, is handled by a module in `query.tables`.
Those modules contain the SQL to create the table and the helper functions used to populate or update it, and migrations call those modules as well.

Python classes in `query.models` are mostly API and event models rather than table definitions.
For example, query models build the list of allowed fields from `query.tables.product`, so the database structure and the query API stay aligned.

During imports, raw product JSON is first loaded into the temporary `product_temp` table.
From there, the ingestion code updates `product` and the related tables.
