# SQL Good

A package for statically type-checked SQL queries.

## Why?

Writing raw SQL gets _messy_ and usually involves loads
of un-typed strings strewn everywhere.
This project solves this problem by...

1. type-checking and validating all SQL statements with the database schema,
2. generating Python functions (with type annotations) for each query, and
3. relying on the database schema as the one source of truth for data models.

ORMs are great tools, but they are often chosen for ease of use and avoiding the
common pitfalls that raw SQL introduces.
However, with sqlgood, _it's not possible to write a query that will fail for
syntax reasons_, and it allows for flexibility in database management.

## How?

sqlgood centers around a file called `good.sql`.
You edit this file with a list of SQL queries with descriptions.
Then SQL good will retrieve the database schema to validate the queries
and turn each query into a callable function with type annotations,
which can be used with a static analysis tool such as [mypy](https://github.com/python/mypy).

**This guarantees that all SQL statements will execute correctly.**

## Notes

- I actively use sqlgood in some projects, but it definitely still needs a lot of work.
- I find that this project works remarkably well with
[FastAPI](https://github.com/tiangolo/fastapi). See this [example](TODO).

