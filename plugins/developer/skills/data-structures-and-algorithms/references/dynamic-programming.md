# Dynamic programming and backtracking

Hand-written summary of standard material; not generated from the vault, whose notes on this are still pending.

## When dynamic programming applies

It needs two properties: **overlapping subproblems**, where the same smaller problems recur, and **optimal substructure**, where the best answer is built from the best answers to subproblems. Typical signals: counting ways, a minimum or maximum over choices, or "can you reach". Greedy may work if a local choice can be proved safe; otherwise DP considers all of them.

## Method

1. **Define the state:** the smallest information that determines the rest. This is the crucial step. For example, `best[i]` is the best answer considering the first `i` items.
2. **Write the recurrence:** how a state follows from smaller ones, and the base cases.
3. **Choose a form.** Top-down: recursion plus a cache, simple to write, only computing what's needed, with stack depth limits to watch. Bottom-up: fill a table in dependency order, avoiding recursion, and often allowing less memory.
4. **Compute the cost:** number of states × work per state.
5. **Reduce memory** if each row only depends on the previous one. To reconstruct the solution itself, keep the choices or walk back through the table.

## Common shapes

| Shape | Examples | State |
|---|---|---|
| Linear | Fibonacci, house robber | Position |
| Knapsack | Subset sum, coin change with arbitrary coins | Item, remaining capacity |
| Two sequences | Edit distance, longest common subsequence, diff | Position in each |
| Intervals | Matrix chain, palindromes | Start, end |
| Grid | Path counts | Row, column |
| Trees, DAG | Longest path in a DAG | Node, plus a small flag |
| Bitmask | Small traveling salesman | Subset of visited |

## Backtracking

Build a candidate step by step, undoing a choice if it can't lead to a solution. It suits permutations, constraint problems and search where all solutions may be needed. Prune early, since it's exponential otherwise. If the same state recurs, add memoization, and then it's effectively DP.

## In real code

Check the library first: `difflib`, edit distance and shortest paths are often already there. A cache on a pure function is frequently all that's needed. State the input size at which an exponential approach stops working, and test it on the base cases and on one case worked out by hand.
