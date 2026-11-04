# SQL and indexes

Defining and querying data, views and procedures, indexes, and the algebra underneath.

## Contents

- [SQL: Data Definition (DDL)](#sql-data-definition-ddl)
- [SQL: Queries (DQL)](#sql-queries-dql)
- [SQL: Views and Stored Procedures](#sql-views-and-stored-procedures)
- [Database Indexes](#database-indexes)
- [Relational Algebra](#relational-algebra)

## SQL: Data Definition (DDL)

### What it means in practice

The subset of SQL that defines and modifies the database's *structure* (schema), not its data: `CREATE`, `ALTER`, `DROP`, over databases, tables, and constraints. This is the SQL layer that realizes a relational (`modeling.md`) schema derived via ER-to-relational mapping (`modeling.md`) as actual tables.

### Example

```sql
CREATE DATABASE Store;

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE
);

CREATE TABLE Order_ (
    order_id    INT PRIMARY KEY,
    customer_id INT NOT NULL,
    total       DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

ALTER TABLE Customer ADD phone VARCHAR(20);

DROP TABLE Order_;
```

Constraints (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK`) are what make the database itself enforce the relational model (`modeling.md`)'s key concepts, rather than trusting application code to.

### Related

- Relational Model (`modeling.md`)
- ER-to-Relational Mapping (`modeling.md`)
- SQL: Queries
- Database Indexes
- SQL: Views and Stored Procedures

## SQL: Queries (DQL)

### What it means in practice

The `SELECT` statement is SQL's concrete syntax for relational algebra: `WHERE` is selection, the column list is projection, `JOIN` is join, `GROUP BY`/`HAVING` is grouping plus a filter applied *after* grouping (unlike `WHERE`, which filters *before* grouping).

- `SELECT columns FROM table WHERE condition` — project + select.
- `JOIN ... ON condition` — combine rows from two tables where the condition matches (`INNER JOIN` keeps only matches; `LEFT`/`RIGHT JOIN` also keep unmatched rows from one side, filled with `NULL`).
- `GROUP BY columns` — partition rows into groups sharing the same value(s); typically paired with an aggregate (`COUNT`, `SUM`, `AVG`...).
- `HAVING condition` — filters *groups* (works on aggregate results); `WHERE` filters *rows* before grouping ever happens.
- **Subquery** — a `SELECT` nested inside another query's `WHERE`, `FROM`, or column list.
- **Set operators** — `ALL`/`ANY` compare a value against every/some result of a subquery (`price > ALL (SELECT price FROM ...)`).

### Example

```sql
SELECT c.name, COUNT(o.order_id) AS total_orders
FROM Customer c
JOIN Order_ o ON c.customer_id = o.customer_id
WHERE o.total > 50
GROUP BY c.name
HAVING COUNT(o.order_id) > 3;
```

Customers with more than 3 orders over $50 each: `WHERE` filters individual orders before grouping; `HAVING` filters the resulting per-customer counts after grouping.

### Related

- Relational Algebra
- SQL: Data Definition
- SQL: Views and Stored Procedures

## SQL: Views and Stored Procedures

### What it means in practice

- **View** — a named, saved query that behaves like a virtual table: `SELECT * FROM MyView` runs the underlying query each time. Used to simplify a frequently-needed complex join/aggregation, or to expose only certain columns/rows of a table to certain users without duplicating data.
- **Stored procedure** — a named, reusable block of SQL logic stored in the database itself, optionally taking parameters, that can run multiple statements (not just one query) and doesn't have to return a table. **Functions** are similar but must return a single value/table and are usable inline within a query, the way a view is.

### Example

```sql
CREATE VIEW ActiveCustomers AS
SELECT customer_id, name
FROM Customer
WHERE last_order_date > DATEADD(month, -6, GETDATE());
```

```sql
CREATE PROCEDURE PlaceOrder (@customerId INT, @total DECIMAL(10,2))
AS
BEGIN
    INSERT INTO Order_ (customer_id, total) VALUES (@customerId, @total);
END;
```

### Related

- SQL: Queries
- SQL: Data Definition

## Database Indexes

### What it means in practice

Without an index, finding rows matching a `WHERE` condition means scanning every row (O(n)). An index is an auxiliary structure — almost always a B+-tree (a B-tree variant where all data sits in the leaves and the leaves are linked together in order) — built on one or more columns, that turns that lookup into an O(log n) tree search, plus O(k) to walk the leaf chain for a range of k matching rows.

Two kinds, differing in *where the actual row data lives*:

- **Clustered index** — the table's rows are physically stored in the order of the indexed column(s); the B+-tree's leaves *are* the rows. A table has at most one (it can only be physically sorted one way) — usually built on the primary key.
- **Non-clustered index** — a separate structure whose leaves hold the indexed column's value plus a pointer/reference to the actual row (which lives elsewhere, in clustered-index or heap order). A table can have several of these.

Trade-off: indexes make reads faster but writes slower (every `INSERT`/`UPDATE`/`DELETE` has to update every affected index, not just the table), and they cost extra storage.

### Related

- SQL: Data Definition
- Levels of Abstraction in Database Design (`modeling.md`)

## Relational Algebra

### What it means in practice

A formal query language over relations (`modeling.md`) — every operator takes one or two relations as input and produces a relation as output (closure), which is what lets operators be chained into more complex expressions. SQL queries are, under the hood, compiled into a plan built from these operators.

**Basic operators:**

- **Selection (σ)** — filter rows by a condition: `σ_price>100(Product)`.
- **Projection (π)** — keep only specific columns: `π_name,price(Product)`.
- **Union (∪)**, **Difference (−)** — set operations between two relations with the same schema.
- **Cartesian product (×)** — every row of A paired with every row of B.
- **Join (⋈)** — a cartesian product filtered by a matching condition between the two relations, in one operator (equivalent to `σ` after `×`, but expressed directly).
- **Rename (ρ)** — rename a relation or its attributes, needed to combine a relation with itself or resolve name clashes.

**Extended operators:**

- **Aggregation functions** (COUNT, SUM, AVG, MIN, MAX) applied over a column.
- **Grouping (γ)** — partition rows by one or more columns and apply an aggregation within each group — the algebra equivalent of SQL's `GROUP BY`.

### Example

"Names of products priced over 100": `π_name(σ_price>100(Product))` — select the rows first, then project down to just the column needed.

### Related

- Relational Model (`modeling.md`)
- SQL: Queries — SQL's `SELECT`/`WHERE`/`JOIN`/`GROUP BY` are this algebra's concrete syntax.
