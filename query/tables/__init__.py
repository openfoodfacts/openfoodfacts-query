"""Each table, or set of very similar tables (like tags) has a module.
This contains all of the SQL for modifying the data and structure of the table,
so even migrations call out to functions in these modules.
The tables modules will contain limited business logic,
mostly where this would be the equivalent of a database trigger"""
