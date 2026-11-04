---
name: relational-databases
description: "Designs relational schemas, normalizes tables, writes and reviews SQL, chooses indexes, and handles transactions and migrations on any SQL engine. Use whenever someone models tables, adds a column or migration, writes a non-trivial query, uses an ORM, has a slow query, or handles balances, stock or uniqueness under concurrency, even if they only say \"necesito guardar esto\". Covers \"cómo modelo estas tablas\", \"qué clave uso\", \"está normalizado\", \"armame esta consulta\", \"falta un índice\" and \"cómo hago esta migración sin romper\". For whether the database should be hidden behind a port use the architect's clean-architecture. Not for operating a server, replication or NoSQL selection."
---

# Relational Databases

This skill carries a personal study of relational design as reference files. Use it to **model**, **query**, **review** or **explain**. Its point of view: a schema is a set of guarantees about data, usually longer-lived than the code around it, so it should state its rules and be changed with care.

## Before you start

Identify the engine and version, and read the real schema and migrations, not only the ORM models. Check engine-specific syntax, types, locking and index options against its documentation, because they differ.

## Modeling

Start from the entities, the relationships and their cardinality, and the rules the data must obey. Map to tables:

- **Keys.** Every table needs a primary key. Choose stable identifiers, usually a surrogate, plus a unique constraint on the natural key if one exists.
- **Constraints.** Express rules as `NOT NULL`, `UNIQUE`, `FOREIGN KEY` and `CHECK` where the database can enforce them. Rules only in application code will eventually be broken by another writer.
- **Relationships.** Many-to-many needs a junction table. Avoid comma-separated lists in a column.
- **Types.** Use exact numerics for money, and be explicit about time zones. Define what `NULL` means, or disallow it.

**Normalization.** Aim for 3NF as a default: every non-key column depends on the key, the whole key and nothing else. Find the functional dependencies and say what anomaly a violation causes. Denormalize only for a measured read need, and say how the copy stays correct.

## Querying

Write for readability: explicit joins, named CTEs for steps, and selected columns rather than `SELECT *` in application code. Check the behavior of `NULL` in comparisons, `NOT IN` and aggregates. Watch for joins that multiply rows before an aggregate. Parameterize every value; never build SQL by concatenating input.

Test a non-trivial query against sample data that includes the awkward cases: no match, several matches, and `NULL`.

## Performance and indexes

Read the actual plan (`EXPLAIN`, or its equivalent with real execution) before changing anything. Look for N+1 queries from the application first. An index helps a selective `WHERE`, join or sort. It costs storage and slows every write, so justify each one against a real query. In a composite index, column order matters: equality columns first, then range, and a leading column is required for most uses. A function applied to an indexed column generally prevents its use.

## Changing a schema

On live data, a migration can lock tables, lose data or break the running version of the code. Use expand and contract: add the new form, backfill in batches, move readers and writers, then remove the old (`references/transactions-and-migrations.md`). Get explicit permission before running a destructive migration on shared data.

## Concurrency

Any read-then-write can race. A transaction alone often doesn't prevent that at the default isolation level. Prefer atomic updates and unique constraints, and read the reference before anything involving balances, stock or uniqueness.

## Output

**Model:** a Mermaid `erDiagram` or DDL, the rules enforced, and the assumptions about the domain you'd like confirmed.

**Query:** the query, what it returns, and what was or wasn't run.

**Review:** findings most costly first: lost integrity, wrong results, then performance. Show the plan if you read one, and don't claim an improvement you didn't measure.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/modeling.md` | levels of abstraction, ER and EER models, ER-to-relational mapping, keys and the relational model |
| `references/normalization.md` | functional dependencies, normal forms, decomposition |
| `references/transactions-and-migrations.md` | transactions, isolation levels, lost updates and other races, ORMs, connections, safe schema migrations |
| `references/sql-and-indexes.md` | DDL, queries, views and procedures, clustered and non-clustered indexes, relational algebra |
