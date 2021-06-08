# sql2py

A lightweight package for generating Python functions from SQL
that can be statically type-checked.

## Why?

Writing raw SQL gets _messy_ and usually involves loads
of un-typed strings strewn everywhere.
This project solves this problem by...

1. type-checking and validating all SQL statements with the database schema,
2. generating Python functions (with type annotations) for each query, and
3. relying on the database schema as the one source of truth for data models.

This tools aims to be a drop-in replacement to an ORM.
ORMs are great, up until you want more flexibility,
and then you're writing raw SQL again.
With sql2py, _it's not possible to write a query that will fail for
syntax reasons_, and it allows for flexibility in database management.

## How?

sql2py centers around a file called `queries.sql`.
You edit this file with a list of SQL queries with descriptions.
Then sqp2py will retrieve the database schema to validate the queries
and generate a file called `queries.py` with type-annotated
functions.
These functions can be used with a static analysis tool such as [mypy](https://github.com/python/mypy).

## How does this differ from an ORM?

With an ORM, you define your database schema in the code,
and then use an Object Oriented interface to access the data.
ORMs often have complex caching mechanisms and migration management.

sql2py has none of that and relies on the database to
know the schema. This means you will need separate tools
for managing database migrations and caching.
I recommend [dbmate](https://github.com/amacneil/dbmate) for migrations
and [redis](https://redis.io/) for caching.

## Notes

- This project is in beta and is far from feature-complete. It works quite well for simple queries! If there is a feature you would like,
[open a new issue](https://github.com/jmerizia/sql2py/issues) or 
[leave a pull request](https://github.com/jmerizia/sql2py/pulls)!
- I find that this project works remarkably well with
[FastAPI](https://github.com/tiangolo/fastapi).

