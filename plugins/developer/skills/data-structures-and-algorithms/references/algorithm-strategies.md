# Algorithm strategies

Divide and conquer, and greedy algorithms including when greedy fails.

## Contents

- [Divide and Conquer](#divide-and-conquer)
- [Binary Search](#binary-search)
- [MergeSort](#mergesort)
- [QuickSort](#quicksort)
- [Fibonacci via Divide & Conquer](#fibonacci-via-divide-conquer)
- [Palindrome Check](#palindrome-check)
- [Greedy Algorithms](#greedy-algorithms)
- [Coin Change Problem](#coin-change-problem)
- [Fractional Knapsack](#fractional-knapsack)
- [Huffman Coding](#huffman-coding)

## Divide and Conquer

### What it means in practice

Split a "large" problem recursively into "smaller" problems of the *same nature*, until the pieces are trivially solvable, then combine the sub-solutions back into the answer for the original problem. Every Divide & Conquer algorithm is defined by three parts (not every problem needs all three in a nontrivial way):

1. **Base case(s)** — input sizes small enough to solve directly, no further recursion.
2. **Subproblems** — how the input splits into smaller, independently-solvable pieces of the same kind.
3. **Combination** — how the subproblems' answers get unified into the size-n answer.

The complexity of a D&C algorithm is exactly a recurrence relation (`complexity.md`): the cost of splitting/combining plus the cost of the recursive calls it makes.

### Examples

The two smallest, clearest illustrations of the base-case/subproblem/combination shape:

- Binary Search — one subproblem, no combination step, Θ(log n).
- Palindrome Check — one subproblem, no combination step, Θ(n).

For examples where the *combination* step actually does real work, see MergeSort; for examples where the *split* step does the real work instead, see QuickSort.

### When it goes wrong

D&C isn't automatically efficient — see Fibonacci via Divide & Conquer for a case where naive recursive splitting recomputes the same subproblem many times, blowing up to exponential time.

### Related

- Recurrence Relations (`complexity.md`)
- Binary Search
- Palindrome Check
- MergeSort
- QuickSort
- Fibonacci via Divide & Conquer
- Binary Search Tree (`trees-and-graphs.md`) — the same narrow-to-one-subproblem idea, as a persistent structure instead of a one-off search.
- Algorithm Speed (Big-O in Practice) (`complexity.md`)

## Binary Search

### What it means in practice

Fits Divide & Conquer directly: given a sorted sequence and a target value, compare the target to the sequence's midpoint and recurse into whichever half could still contain it — the other half is discarded entirely without being looked at.

- **Base case**: one element left → check it directly (or an empty range → not found).
- **Subproblem**: only one of the two halves is ever explored, never both.
- **Combination**: not needed — whichever single branch ran already has the final answer.

### Example

```
ALGORITHM BinarySearch
Input: S: array<integer>, target: integer, low: integer, high: integer
Output: boolean

if low > high
    return false
end if

mid ← (low + high) / 2

if S[mid] = target
    return true
else if target < S[mid]
    return BinarySearch(S, target, low, mid - 1)
else
    return BinarySearch(S, target, mid + 1, high)
end if
```

### Complexity

One recursive call, input halved each time — by the division-type recurrence (`complexity.md`) rule (a=1, b=2, k=0, a = b^k) → **Θ(log n)**.

### Related

- Divide and Conquer
- Recurrence Relations (`complexity.md`)
- Algorithm Speed (Big-O in Practice) (`complexity.md`)

## MergeSort

### What it means in practice

Fits Divide & Conquer directly: split the sequence in half, sort each half recursively, then **merge** the two already-sorted halves back into one sorted sequence. All of the actual "sorting work" happens in the merge step, not in the splitting.

- **Base case**: a single-element sequence is already sorted.
- **Subproblems**: sort the left half and the right half independently.
- **Combination**: merge the two sorted halves — walk both with a pointer each, repeatedly take the smaller of the two current heads, advance that pointer, until one half is exhausted, then append the rest of the other.

### Example

```
ALGORITHM MergeSort
Input: S: array<integer>, low: integer, high: integer
Output: (sorts S in place between low and high)

if low < high
    mid ← (low + high) / 2
    MergeSort(S, low, mid)
    MergeSort(S, mid + 1, high)
    Merge(S, low, mid, high)
end if
```

```
ALGORITHM Merge
Input: S: array<integer>, low: integer, mid: integer, high: integer
Output: (S[low..high] is sorted, assuming both halves already are)

i ← low
j ← mid + 1
result ← new array of size (high - low + 1)
k ← 0

while i <= mid and j <= high
    if S[i] <= S[j]
        result[k] ← S[i]; i ← i + 1
    else
        result[k] ← S[j]; j ← j + 1
    end if
    k ← k + 1
end while

// copy whichever half still has leftover elements
// then copy result back into S[low..high]
```

### Complexity

The recurrence is **T(n) = 2T(n/2) + Θ(n)** — two recursive calls on half the input, plus a merge step that's a single pass over n elements. This resolves to **Θ(n log n)**, in the best, average, *and* worst case — MergeSort's cost doesn't depend on the input's initial order, unlike QuickSort.

Trade-off: merging needs an auxiliary array, so MergeSort uses **Θ(n)** extra space, unlike an in-place sort.

### Related

- QuickSort
- Divide and Conquer
- Algorithm Speed (Big-O in Practice) (`complexity.md`)

## QuickSort

### What it means in practice

Also Divide & Conquer, but the work happens in the *split* instead of the merge: pick a **pivot** element, partition the sequence so everything smaller than the pivot ends up to its left and everything larger to its right (the pivot lands in its final sorted position), then recurse on both sides independently. Unlike MergeSort, there's no combination step — once both sides are sorted, the whole sequence is sorted, in place.

- **Base case**: a sequence of one or two elements.
- **Subproblems**: partition around a pivot, then sort the left part and the right part.
- **Combination**: none needed — the partition already placed the pivot correctly and the two sides don't overlap.

Pivot choice matters directly: a pivot close to the median gives a balanced split (fast); a pivot close to either extreme gives a lopsided split (slow). The simplest strategy is just taking the first (or last) element as pivot — cheap to compute, but vulnerable to already-sorted or reverse-sorted input.

### Example

```
ALGORITHM QuickSort
Input: S: array<integer>, low: integer, high: integer
Output: (sorts S in place between low and high)

if low < high
    p ← Partition(S, low, high)
    QuickSort(S, low, p - 1)
    QuickSort(S, p + 1, high)
end if
```

```
ALGORITHM Partition
Input: S: array<integer>, low: integer, high: integer
Output: integer  // final index of the pivot

pivot ← S[low]
i ← low

for j = low + 1 to high
    if S[j] < pivot
        i ← i + 1
        swap(S[i], S[j])
    end if
end for

swap(S[low], S[i])
return i
```

### Complexity

- **Average case**: pivot lands near the middle often enough that the recursion behaves like MergeSort's — **O(n log n)**.
- **Worst case**: pivot always lands at one extreme (e.g. already-sorted input with "always take the first element" as the pivot rule) — every partition only shrinks the problem by one element, giving **O(n²)**.

Unlike MergeSort, QuickSort sorts **in place** — no auxiliary array needed — but its worst case is genuinely quadratic, which MergeSort never hits.

### Related

- MergeSort
- Divide and Conquer

## Fibonacci via Divide & Conquer

### What it means in practice

Fibonacci fits the Divide & Conquer template cleanly — base case, two subproblems, combine by summing — but it's the textbook example of D&C applied where it *shouldn't* be: the naive recursive version recomputes the same subproblem exponentially many times, because F(n-1) and F(n-2) both go on to independently recompute F(n-3), F(n-4), and so on, with no way for one branch to reuse what the other already calculated.

### Example

```
ALGORITHM Fibonacci
Input: n: integer
Output: integer

if n < 2
    return 1
else
    return Fibonacci(n - 1) + Fibonacci(n - 2)
end if
```

- **Base case**: n < 2 → return 1.
- **Subproblems**: F(n-1) and F(n-2).
- **Combination**: sum the two results.

### Complexity

Two recursive calls per invocation (a=2), input shrinks by a constant each time (b=1) → by the subtraction-type recurrence (`complexity.md`) rule, a > 1 means exponential time, roughly **O(2^n)**.

The reason, explicitly: the same value gets calculated multiple times without any way to reuse it — F(3) gets recomputed independently inside the F(5) and F(4) branches, F(2) even more often, and so on down the call tree.

### The fix (forward pointer)

This exact failure — pure recursion recomputing shared subproblems — is what memoization / Dynamic Programming exists to fix, by caching each subproblem's result the first time it's computed. Not covered yet in this course at this point (Unit 4), but this is the motivating example for why it's needed.

### Related

- Divide and Conquer
- Recurrence Relations (`complexity.md`)

## Palindrome Check

### What it means in practice

Fits Divide & Conquer: to check whether a sequence reads the same forwards and backwards, compare its two end elements — if they differ, it's not a palindrome; if they match, the answer depends entirely on whether the sequence with both ends stripped is itself a palindrome.

- **Base case**: length 0 or 1 → trivially a palindrome.
- **Subproblem**: the same check on the sequence with both ends removed (only reached if the ends matched).
- **Combination**: pass through the subproblem's result directly — no extra work needed once the ends matched.

### Example

```
ALGORITHM IsPalindrome
Input: S: array<char>, low: integer, high: integer
Output: boolean

if low >= high
    return true
else if S[low] != S[high]
    return false
else
    return IsPalindrome(S, low + 1, high - 1)
end if
```

### Complexity

One recursive call, input shrinks by 2 each time — by the subtraction-type recurrence (`complexity.md`) rule (a=1, b=2, k=0, a=1) → **Θ(n)**.

### Related

- Divide and Conquer
- Recurrence Relations (`complexity.md`)

## Greedy Algorithms

### What it means in practice

A greedy algorithm builds a solution step by step, at each step making the choice that looks best *right now*, using only currently available information — it never looks ahead at future consequences and never reconsiders a decision once made. Mainly used for optimization problems. It's efficient almost by definition (no backtracking, no exploring alternatives) but correctness is **not automatic** — a greedy strategy has to be proven correct for the specific problem; the same strategy shape can be optimal for one problem and wrong for a superficially similar one.

Every greedy algorithm in this course is built from four pieces:

- **Candidate set** — everything still eligible to be added to the solution.
- **Selection function** — picks the best remaining candidate (this is the "greedy" choice).
- **Feasibility function** — checks whether the selected candidate can validly join the solution so far.
- **Solution function** — checks whether the current partial solution already solves the problem.
- **Objective function** — what's actually being maximized or minimized.

### Example: where greedy fails

Coin Change with denominations {6, 4, 1} for a target of 8: greedy picks the largest usable denomination first (6), then fills the rest with 1s → {6, 1, 1}, 3 coins. The actual optimal is {4, 4}, 2 coins. Same greedy *shape*, wrong answer — because this denomination set doesn't have the structural property (every denomination is a multiple of the next-smaller one, roughly) that makes "largest first" provably optimal.

### Related

- Coin Change Problem
- Fractional Knapsack
- Huffman Coding
- Dijkstra's Algorithm (`trees-and-graphs.md`)
- Prim's Algorithm (`trees-and-graphs.md`)
- Kruskal's Algorithm (`trees-and-graphs.md`)
- Minimum Spanning Tree (`trees-and-graphs.md`)

## Coin Change Problem

### What it means in practice

Given a target amount v and a set of coin denominations (unlimited supply of each), return change using as few coins as possible. Mapped onto the greedy template:

- **Candidates**: the available denominations.
- **Selection function**: try the highest-value coin not yet ruled out.
- **Feasibility function**: the chosen coin can't exceed the amount still owed.
- **Solution function**: the target amount has been reached.
- **Objective function**: minimize the total number of coins used.

### Example

```
ALGORITHM GreedyChange
Input: coins: array<integer>  // sorted descending
       amount: integer
Output: integer  // number of coins used

count ← 0
i ← 0

while amount > 0
    if coins[i] <= amount
        amount ← amount - coins[i]
        count ← count + 1
    else
        i ← i + 1
    end if
end while

return count
```

Complexity: **O(amount)** in the worst case for the coin-selection loop, plus **O(n log n)** if the denominations need sorting first (n = number of denominations).

### When it's correct — and when it isn't

For a denomination set like {$100, $50, $25, $10, $5, $1}, greedy is correct — this is what makes change-making with standard currency systems work with the "largest first" shortcut. But it's **not correct for arbitrary denomination sets**: with {6, 4, 1} and a target of 8, greedy picks 6 then two 1s → 3 coins, while the actual optimal is 4 + 4 → 2 coins. There's no shortcut for the general case — it needs a different technique (Dynamic Programming, not covered yet in this course).

### Related

- Greedy Algorithms
- Fractional Knapsack

## Fractional Knapsack

### What it means in practice

n objects, each with a weight and a value, and a knapsack with capacity P. Unlike the classic 0-1 version, objects here can be **split** — taking a fraction x of object i contributes x·weight and x·value. Goal: maximize total value without exceeding capacity P. Mapped onto the greedy template:

- **Candidates**: the remaining objects.
- **Selection function**: pick the object with the highest value/weight ratio.
- **Feasibility function**: if the whole object doesn't fit, take a fraction of it that does.
- **Solution function**: the knapsack is full, or every object's been considered.
- **Objective function**: maximize total value.

### Example

4 objects, capacity P = 17:

| Object | Value | Weight | Ratio |
|---|---|---|---|
| 1 | 5 | 9 | 0.56 |
| 2 | 2 | 5 | 0.40 |
| 3 | 7 | 3 | 2.33 |
| 4 | 4 | 6 | 0.67 |

Taking objects by descending ratio (3, 4, 1, 2): object 3 fully (weight 3, value 7), object 4 fully (weight 6, value 4), object 1 fully (weight 9 — total so far 18, over capacity) → take only 8/9 of object 1 instead (weight 8, value 40/9 ≈ 4.44). Capacity exhausted at 17; total value ≈ 15.44.

```
ALGORITHM FractionalKnapsack
Input: items: array<Item>  // sorted descending by value/weight
       capacity: integer
Output: real  // total value

totalValue ← 0
remaining ← capacity

for i = 0 to n-1
    if items[i].weight <= remaining
        totalValue ← totalValue + items[i].value
        remaining ← remaining - items[i].weight
    else
        fraction ← remaining / items[i].weight
        totalValue ← totalValue + fraction * items[i].value
        remaining ← 0
    end if
end for

return totalValue
```

### Complexity

**O(n log n)**, dominated by sorting the items by ratio; the main loop itself is O(n).

### Why greedy works here (and not for 0-1 knapsack)

Because objects are fractionable, always taking the best available ratio is provably optimal — there's no scenario where saving capacity for a "better combination" beats greedily taking the best ratio first. The moment objects must be taken whole (the 0-1 knapsack variant), this breaks: a locally-best object might not fit alongside the rest of the optimal set, and greedy can lock in a wrong choice with no way to undo it — that variant needs Dynamic Programming instead.

### Related

- Greedy Algorithms
- Coin Change Problem

## Huffman Coding

### What it means in practice

Compresses a message into the smallest possible **prefix-free** binary encoding (no codeword is a prefix of another, so a decoder never needs a separator to know where one code ends and the next begins), by giving frequent symbols shorter codes and rare symbols longer ones. A greedy algorithm: repeatedly merge the two lowest-frequency nodes, which is provably the right local choice for building a globally optimal prefix code.

- **Candidates**: the symbols, each starting as its own tree node.
- **Selection function**: always take the two lowest-frequency nodes.
- **Feasibility function**: none needed — any two lowest-frequency nodes can always merge.
- **Solution function**: one node remains (the completed tree).
- **Objective function**: minimize total encoded message length.

### Algorithm

1. Put every symbol in a min-priority queue, keyed by frequency.
2. Repeatedly extract the two lowest-frequency nodes, merge them into a new internal node whose frequency is their sum, and insert that node back into the queue.
3. Repeat until one node (the tree's root) remains.
4. Each symbol's code is the path from root to its leaf (0 for one branch, 1 for the other).

```
ALGORITHM Huffman
Input: symbols: array<Symbol>  // each with a frequency
Output: TreeNode  // root of the Huffman tree

queue ← MinPriorityQueue(symbols)

while queue.size() > 1
    left ← queue.extractMin()
    right ← queue.extractMin()
    merged ← new TreeNode(frequency: left.frequency + right.frequency, left: left, right: right)
    queue.insert(merged)
end while

return queue.extractMin()
```

### Example

Message of 10,000 symbols with frequencies A=45, B=13, C=12, D=16, E=9, F=5 (thousands). Fixed-length coding (3 bits × 6 symbols) costs 30,000 bits total.

Merge trace: `<F:5, E:9, C:12, B:13, D:16, A:45>` → merge F+E → X1:14 → merge C+B → X2:25 → merge X1+D → X3:30 → merge X2+X3 → X4:55 → merge X4+A → X5:100 (root).

Resulting codes: A→`0`, B→`101`, C→`100`, D→`111`, E→`1101`, F→`1100` — total encoded size **22,400 bits**, versus 30,000 for fixed-length. Shorter codes go to the more frequent symbols (A, the most frequent, gets the shortest code).

### Complexity

Priority queue `insert`/`extractMin` are each Θ(log n). The algorithm does Θ(n) of each → **Θ(n log n)** total.

### Related

- Greedy Algorithms
- Priority Queue (`linear-and-associative.md`) — the data structure this algorithm's selection step relies on.
