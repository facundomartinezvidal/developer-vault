---
name: data-structures-and-algorithms
description: "Chooses data structures and algorithms and reasons about cost, in any language. Use when code is slow on large inputs, for Big-O, caching or profiling, or for sorting, search, graph and dynamic programming problems (\"esto tarda mucho\", \"qué estructura uso\"). Queries: relational-databases."
---

# Data Structures and Algorithms

This skill carries a personal study of structures and algorithms as reference files. Use it to **choose**, **analyze**, **implement** or **explain**. Its point of view: decide from the operations you need and the real input size, and measure before optimizing.

## Choosing

1. **List the operations and how often each happens.** Lookup, insert, ordered traversal, range, min or max, membership. Also note input size, how it grows, and whether order or duplicates matter.
2. **Use the standard library.** Prefer the language's built-in collections and sorts over writing your own. Check their documented complexity and worst case. Implement your own only if asked, or for a concrete need with evidence.
3. **Compare with the real constraints.** A hash map gives expected O(1) lookup but no order. A balanced tree gives O(log n) and ordered ranges. An array has cache locality that often beats its asymptotic rivals on small data, and linked lists rarely win in practice.

| You need | Look at |
|---|---|
| Fast membership or lookup by key | Set, dictionary (hash) |
| Sorted order, range queries | Balanced tree, sorted array |
| Repeated min or max | Priority queue (heap) |
| FIFO, LIFO | Queue, stack |
| Relationships, reachability | Graph: adjacency list if sparse, matrix if dense |
| Unweighted shortest path | BFS |
| Weighted shortest path without negative edges | Dijkstra (fails with negative edges) |
| Connect everything at the lowest cost | Prim, Kruskal |
| On-disk or database lookup | B-tree |

## Analyzing

State what `n` is, and give the time and space cost with the reasoning: nested loops over the same data, hidden work inside library calls or queries in a loop. Distinguish worst, average and amortized when it matters. Recurrences are solved with the Master Theorem or a recursion tree.

Greedy is only correct when you can justify it: coin change works for some coin systems and fails for others. Say why it holds, or give a counterexample. For problems with overlapping subproblems, see `references/dynamic-programming.md`.

## Performance

Don't optimize without evidence. Profile or measure to find the hot path (`references/profiling-and-optimization.md`); the cost is often in I/O, allocations or a query in a loop, not the algorithm. Fix big complexity problems first. Keep the clear version when `n` stays small, and state the size at which that changes. Report numbers only if you measured them, and with what input.

## Output

**Choosing:** the recommendation, why it fits the operations, its cost, and the input size at which you'd reconsider.

**Implementing:** clear code with the invariants or the non-obvious step explained. Test empty input, one element, duplicates, boundaries and an adversarial case.

**Explaining:** the idea, a worked example, the cost, and when it fails.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/complexity.md` | algorithm speed, asymptotic notation, recurrences, designing for performance |
| `references/linear-and-associative.md` | abstract data types, stacks, queues, priority queues, linked lists, sets, dictionaries |
| `references/trees-and-graphs.md` | BST, AVL, B-tree, graph representation and traversal, Dijkstra, Prim, Kruskal |
| `references/algorithm-strategies.md` | divide and conquer, binary search, mergesort, quicksort, greedy, knapsack, coin change, Huffman |
| `references/dynamic-programming.md` | dynamic programming, memoization, common state shapes, backtracking |
| `references/profiling-and-optimization.md` | measuring, profilers and benchmarks, usual performance suspects, caching |
