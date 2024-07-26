# Product Event Aggregation

## Context and Problem Statement

We would like to be able to support a variety of queries on events that have been recorded on products over time. For example, for the producer's dashboard we want to be able to show the number of edits and distinct products updated over a month.

## Decision Drivers

* Queries should run quickly
* Database space consumed should not be excessive
* Data should be reasonably up to date, i.e. any ETL / ELT process should keep up with the rate at which events are being created

## Considered Options

* Query the raw event tables
* Create specific aggregate tables for each aggregate dimension
* Create a relational model of events against products

## Decision Outcome

Chosen option: "Create a relational model of events against products", because it offers the best compromise in terms of acceptable query performance with minimal storage space and does not require new tables to be created for every possible aggregate dimension.

### Consequences

In general we should try and map things to a relational model, but only at the most granular level of detail that makes sense, e.g. total count of actions in one day.

It has been observed that PostgreSQL performs much better when dealing with small record sizes, so text fields should be normalised where possible so that an integer id can be stored instead.

## Pros and Cons of the Options

### Query the raw event tables

In this option the raw events are simply loaded into a table and then views are created to query this table, joining to the product table to obtain the required dimension.

* Good: Only the raw events are being stored
* Good: Import of data is as fast as possible
* Bad: Query performance is poor. Even with indexing typical queries were taking around 2 minutes

### Create specific aggregate tables for each aggregate dimension

With this option the raw events would be ingested and then a follow-up process would run to aggregate those events by the required dimension, e.g. for producer's dashboard this would be aggregating by day, action and owner with a total update count plus a count of distinct products updated.

* Good: Queries run very quickly (sub 100ms)
* Bad: Additional tables, processes and storage need to be assigned for each new query dimension
* Bad: It is difficult to incrementally refresh tables where distinct counts are included (as cannot work out the new distinct count from the combination of new events plus existing distinct count)

### Create a relational model of events against products

With this option the raw events would be ingested and then a follow-up process would run to just aggregate those events by action, contributor and day against the product. Different views can then be provided to query this data, joining to the product to obtain the required dimension.

With this option it was important to keep the size of the relational table as small as possible, so an enumeration was used for the action and the contributors were normalised into a separate table so that only the id needed to be stored in the event table.

* Neutral: Queries performance is acceptable (sub 1s)
* Good: Queries to support different dimensions do not require addition storage or import processes
* Good: Aggregated counts are not distinct, so can be refreshed incrementally

