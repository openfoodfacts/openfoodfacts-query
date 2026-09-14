# Explain database structure

Open Food Facts Query copies selected product data from Open Food Facts into PostgreSQL.
The goal is not to reproduce the full MongoDB document as-is, but to reshape it into tables that are easier to query for filters, counts, and aggregations.

## Main idea

The database is organized around a few families of tables:

- `product`: the main table, with one row per product and the main scalar fields that are often queried or sorted on
- `product_*_tag`: facet tables, used for arrays of values such as categories, brands, labels, countries, ingredients tags, and many other `*_tags` fields
- `product_update_event` and `product_update`: tables for product events and a lighter event history used by queries
- `nutrient` and `product_nutrient`: normalized nutrient tables
- a few derived tables such as scans or product/country statistics

## Product information

The `product` table is the root table.
It stores the product code and a selection of direct product fields such as the name, creator, timestamps, completeness, nutriscore, environmental score, and scan counters.

During imports, raw product JSON is first loaded into the temporary `product_temp` table.
From there, the ingestion code updates `product` and the related tables.

## Facets

Many Open Food Facts fields are arrays, especially the `*_tags` fields.
Instead of storing those arrays in one column, Query expands them into separate tables such as `product_categories_tag`, `product_brands_tag`, or `product_labels_tag`.
Each row links one product to one facet value.

This makes filtering and aggregations much simpler in SQL.
In practice, these tables are what back most "facet" style queries.

## Nutrients

Nutrients are stored separately from the root `product` table.
The `nutrient` table stores the list of known nutrient keys, and `product_nutrient` stores the value for one nutrient on one product.

The import code mainly keeps values normalized at the product / nutrient level, using the `_100g` values from `nutriments` or the aggregated nutrition structure when present.
That keeps nutrient filtering and sorting consistent.

## Product events

`product_update_event` stores the raw event message as JSON, together with message and timestamp metadata.
`product_update` is a more query-friendly version of that history: it links an event to a product, a revision, an update type, a contributor, and an update date.

So the database keeps both:

- the original event payload for traceability
- a lean relational table for reporting and queries on product history

## How code maps tables

The project does not use a classic ORM with one class per table.
Instead, each table, or group of very similar tables, is handled by a module in `query.tables`.
Those modules contain the SQL to create the table and the helper functions used to populate or update it.
Migrations also call those functions.

Python classes in `query.models` are mostly API and event models.
For example, query models build the list of allowed fields from `query.tables.product`, so the database structure and the query API stay aligned.
