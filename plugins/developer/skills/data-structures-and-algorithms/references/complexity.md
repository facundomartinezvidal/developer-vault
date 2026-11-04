# Complexity and performance

How to reason about cost, and when performance deserves design attention.

## Contents

- [Algorithm Speed (Big-O in Practice)](#algorithm-speed-big-o-in-practice)
- [Asymptotic Complexity](#asymptotic-complexity)
- [Recurrence Relations](#recurrence-relations)
- [Designing for Performance](#designing-for-performance)

## Algorithm Speed (Big-O in Practice)

> Estimate the Order of Your Algorithms. — Tip 63 &nbsp;·&nbsp; Test Your Estimates. — Tip 64

**Source:** *The Pragmatic Programmer*, Topic 39.

### What it means in practice

The formal theory is in Asymptotic Complexity. Hunt & Thomas's point is that a working programmer should estimate an algorithm's order *by reflex*, using quick rules of thumb:

- **Simple loops** are O(n). **Nested loops** are O(n·m), so O(n²) when both depend on the same input.
- **Binary chop** (halving each time) is O(log n). **Divide and conquer** (split, recurse, combine) is O(n log n).
- **Combinatoric** problems (permutations, subsets) are O(2ⁿ) or O(n!), and need heuristics.

Then **test your estimates**: time the code with realistic input sizes and use a profiler. Constant factors, caches, I/O and the size of the input change what's actually fastest. The best algorithm isn't always the fastest one. For small inputs, an O(n²) insertion sort can beat O(n log n), and the simplest code that's fast enough is the right choice. Watch out for premature optimization.

### Example

```java
// O(n·m): for each of 50k orders, scan 200k customers → 10^10 comparisons, minutes
for (Order o : orders) for (Customer c : customers) if (c.id().equals(o.customerId())) ...

// O(n + m): index once, look up in O(1)
Map<CustomerId, Customer> byId = customers.stream().collect(toMap(Customer::id, c -> c));
for (Order o : orders) { Customer c = byId.get(o.customerId()); ... }
```

### Related

- Asymptotic Complexity — the formal definitions behind the rules of thumb.
- Recurrence Relations — where the O(n log n) of divide and conquer comes from.
- Divide and Conquer (`algorithm-strategies.md`), Binary Search (`algorithm-strategies.md`), MergeSort (`algorithm-strategies.md`) — the textbook cases.
- Dictionary (`linear-and-associative.md`) — the O(1) lookup in the example.
- Designing for Performance — Ousterhout: measure first, then design the critical path to be naturally fast.

## Asymptotic Complexity

### What it means in practice

An algorithm is **correct** if it produces the right result for *every* valid input, and **efficient** if it does so within a bounded amount of resources (time, memory). Two different implementations of the same algorithm never differ by more than a constant factor — this is why complexity is measured by counting elementary operations (assignment, comparison, arithmetic, array access — each cost 1) as a function of input size, independent of language or hardware, rather than by timing an actual run.

From those elementary-operation counts, a few composition rules give the total cost:
- A sequence of steps: sum their costs.
- A conditional (`if/else`): cost of evaluating the condition, plus the cost of whichever branch is worse (for a worst-case bound).
- A loop: number of iterations × cost of the body.
- A function call: 1 (for the call itself) + the callee's own cost.

Three cases are usually distinguished — **worst case** (maximum cost over all inputs of size n), **average case** (mean cost), **best case** (minimum cost) — with worst case the one that matters most in practice, since it upper-bounds the others and gives a safety guarantee regardless of input.

**Big-O** (O) expresses an *upper bound* on growth rate as input size grows — "this algorithm never does asymptotically worse than this." **Big-Omega** (Ω) is the matching *lower bound*, and **Big-Theta** (Θ) is used when the upper and lower bounds coincide — i.e. the algorithm's growth rate is tightly known, not just bounded above. In practice, most complexity claims (`O(n log n)`, `O(n²)`) describe the worst case.

### Example

```
for i = 0 to n-1        // n iterations
    for j = 0 to n-1    // n iterations, each
        x ← x + 1       // constant cost
    end for
end for
```

Outer loop runs n times; for each, the inner loop runs n times doing constant work → n × n × O(1) = **O(n²)**.

### Related

- Recurrence Relations — how complexity is derived for *recursive* algorithms instead of loop-nesting.
- Designing for Performance
- Algorithm Speed (Big-O in Practice)

## Recurrence Relations

### What it means in practice

A recursive algorithm's cost T(n) is naturally expressed in terms of T of a smaller input — a recurrence. Two shapes come up constantly:

- **Subtraction type** — each call makes *a* recursive calls, each on input size (n − b), plus non-recursive work of degree k (a polynomial p(n) with degree k). Rule of thumb: if **a = 1**, the complexity is **Θ(n^(k+1))**; if **a > 1**, it blows up to exponential, roughly **O(a^(n/b))**.
- **Division type** — each call makes *a* recursive calls, each on input size (n / b), plus non-recursive work of degree k. Rule of thumb: compare a to b^k — if **a = b^k**, complexity is **Θ(n^k · log n)**; if a and b^k diverge, the complexity shifts toward whichever term dominates (roughly O(n^k) when a ≤ b^k, or O(n^(log_b a)) when a > b^k, per the general Master Theorem this rule approximates).

### Example: Factorial (subtraction type)

```
ALGORITHM Factorial
Input: n: integer
Output: integer

if n = 0
    return 1
else
    return n * Factorial(n - 1)
end if
```

One recursive call (a=1), input shrinks by 1 each time (b=1), constant non-recursive work (k=0). Since a=1 → **Θ(n^(0+1)) = Θ(n)**.

### Example: binary search over a balanced tree (division type)

```
ALGORITHM FindValue
Input: node: TreeNode, value: integer
Output: boolean

if node = null
    return false
else if value = node.key
    return true
else if value < node.key
    return FindValue(node.left, value)
else
    return FindValue(node.right, value)
end if
```

One recursive call (a=1), input halves each time (b=2), constant non-recursive work (k=0). Since a = b^k (1 = 2^0) → **Θ(n^0 · log n) = Θ(log n)**.

### Where this goes wrong

When a > 1 and the recursion branches into multiple calls per level without sharing work — see Fibonacci via Divide & Conquer (`algorithm-strategies.md`) for exactly this failure mode (a=2, b=1 → exponential, from redundant recomputation).

### Related

- Asymptotic Complexity
- Divide and Conquer (`algorithm-strategies.md`)
- Binary Search (`algorithm-strategies.md`)
- Fibonacci via Divide & Conquer (`algorithm-strategies.md`)
- Palindrome Check (`algorithm-strategies.md`)
- Algorithm Speed (Big-O in Practice)

## Designing for Performance

> Clean design and high performance are compatible.

**Source:** *A Philosophy of Software Design*, Chapter 20.

### What it means in practice

Ousterhout's position is between "optimize everything" (which adds complexity everywhere) and "never think about performance" (which leaves you with many small slowdowns that no single fix solves):

1. **Know what's naturally expensive.** Network round-trips, disk and flash I/O, dynamic memory allocation, and cache misses. Use micro-benchmarks to learn the costs. Then, when two designs are *equally clean*, choose the one that's naturally faster.
2. **Measure before modifying.** Intuitions about where time goes are often wrong. Measure the system to get a baseline and find the real bottleneck.
3. **Design around the critical path.** For code that really matters, ask what the *minimum* work for the common case is. Design the cleanest code that does only that, and handle special cases off the fast path, ideally with a single test that routes all of them away.

Simpler code tends to be faster, because it does less unnecessary work.

### Example

An API for listing a customer's orders makes N+1 queries (one for the orders, then one per order for its items), and it's slow. After measuring, the critical path is "fetch orders with their items for one customer". The redesign is one query with a join, mapped in one pass. The rare case "include archived orders" takes a separate, slower path behind a single flag check.

### Related

- Algorithm Speed (Big-O in Practice) — Hunt & Thomas: estimate the order of the algorithm, then test the estimate.
- Asymptotic Complexity
