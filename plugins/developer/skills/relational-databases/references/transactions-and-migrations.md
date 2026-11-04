# Transactions, concurrency and migrations

Hand-written from common practice, drawing on Kleppmann's *Designing Data-Intensive Applications*; not generated from the vault. Isolation and locking differ by engine and version, so check its documentation.

## Transactions

A transaction makes a group of changes all-or-nothing and isolates them from others. Keep them short, with no network calls or user waits inside: long ones hold locks and can stall the whole table. Handle commit failures and retries for serialization errors and deadlocks, which are normal under load. Check where your ORM or framework starts and ends them, since that's often implicit.

## Isolation

| Level | Prevents | Still allows |
|---|---|---|
| Read committed (common default) | Dirty reads | Non-repeatable reads, lost updates |
| Repeatable read, snapshot | Above, plus non-repeatable reads | Write skew; details vary by engine |
| Serializable | All of the above | Needs retries on conflict |

Defaults differ by engine. A transaction alone doesn't prevent every race.

## Common race conditions

- **Lost update:** two read-modify-write operations. Use an atomic `UPDATE x = x + 1`, `SELECT … FOR UPDATE`, or optimistic version checks.
- **Check then insert:** two requests both see no row. A unique constraint is the real guard; handle the conflict with an upsert.
- **Write skew:** two transactions check a shared rule and update different rows, such as "at least one doctor on call". Use serializable or lock the rows involved.
- **Balances and stock:** enforce with `CHECK` constraints or a conditional update, and check the number of rows affected.

## ORMs

Check the SQL it generates. The usual problems are N+1 queries, loading entire rows, lazy loading outside a transaction, and implicit saves. Fall back to raw parameterized SQL when that's clearer.

## Connections

Use a pool of bounded size, set timeouts on queries and lock waits, and release connections on failure. Serverless platforms or many instances can exhaust a database's limit.

## Migrations

Schema changes go in versioned migrations, reviewed and tested like code, on realistic volumes. During a deploy old and new code run at once, so use **expand and contract**:

1. Add the new nullable column or table. Avoid long table locks.
2. Write to both, or deploy code that handles both.
3. Backfill in small batches, with throttling. Don't run one massive update.
4. Switch reads.
5. Stop writing the old form.
6. Remove the old column in a later release.

Check what locks an operation takes in your engine. Adding a column with a default, changing a type, and adding an index or a foreign key may block writes; many engines offer online variants such as `CREATE INDEX CONCURRENTLY`, and validating constraints separately. Set a lock timeout, so that a migration doesn't queue behind a long query and block everyone else.

Plan the way back. Dropped data can't be recovered by a down migration, so take a backup, test the restore, and get approval before running anything destructive on shared data.

## Other choices

Store times in UTC. Soft deletes complicate each query and unique constraint, so use them only if needed. Tenant isolation needs enforcement on every query, such as a scoped layer or row-level security. Plan partitioning and read replicas only once you've measured a need; replica lag means that a user may not see their own write.
