# Linear and associative structures

Abstract data types, stacks, queues, lists, sets and dictionaries.

## Contents

- [Abstract Data Types](#abstract-data-types)
- [Stack](#stack)
- [Queue](#queue)
- [Priority Queue](#priority-queue)
- [Linked List](#linked-list)
- [Set](#set)
- [Dictionary](#dictionary)

## Abstract Data Types

### What it means in practice

An Abstract Data Type separates **what** a structure does from **how** it does it: a *specification* (the set of operations it supports and what each one guarantees, e.g. "push adds an element, pop removes and returns the most recently added one") independent of any *implementation* (array-backed, linked, whatever). Code written against the specification doesn't need to know or care which implementation is behind it — the same idea as Program To An Interface from the design-patterns side of this vault, just introduced here as the foundational vocabulary for data structures instead of OOP design.

Every ADT covered in this course follows the same shape: a **specification** (interface: operation names, inputs, outputs, preconditions/postconditions) and one or more **implementations** (concrete data layout + algorithms realizing those operations, each with its own complexity trade-offs).

### Example

The Stack ADT's specification never mentions arrays or linked nodes — just: `push(x)`, `pop()`, `top()`, `isEmpty()`, with the guarantee that `pop()`/`top()` always return the most recently pushed element still in the stack. See Stack for the two standard implementations and how their complexity differs despite satisfying the exact same specification.

### Related

- Stack
- Queue
- Dictionary
- Linked List
- Priority Queue
- Set

## Stack

### What it means in practice

LIFO (last in, first out) ADT: elements are added and removed from the same end. Specification: `push(x)` adds x on top; `pop()` removes and returns the top element; `top()`/`peek()` returns the top element without removing it; `isEmpty()`.

Two standard implementations, same specification, same complexity for every operation:

- **Static (array-backed)**: a fixed-capacity array plus a `top` index; push/pop just move the index and write/read that slot. Simple and cache-friendly, but capacity is bounded (or needs resizing).
- **Dynamic (linked list-backed)**: push/pop operate on the head of a singly linked list. No fixed capacity, but each element carries pointer overhead.

### Example

```
ALGORITHM Push
Input: stack: Stack, x: Element
Output: (stack now has x on top)

stack.top ← stack.top + 1
stack.data[stack.top] ← x
```

```
ALGORITHM Pop
Input: stack: Stack
Output: Element

x ← stack.data[stack.top]
stack.top ← stack.top - 1
return x
```

### Complexity

All operations — `push`, `pop`, `top`, `isEmpty` — are **O(1)**, in both the array-backed and linked implementations.

### Related

- Abstract Data Types
- Queue
- Linked List
- Graph Traversal (DFS / BFS) (`trees-and-graphs.md`)

## Queue

### What it means in practice

FIFO (first in, first out) ADT: elements are added at one end and removed at the other. Specification: `enqueue(x)` adds x at the back; `dequeue()` removes and returns the element at the front; `front()` returns it without removing; `isEmpty()`.

- **Static (array-backed)**: usually implemented as a **circular buffer** — front and back indices wrap around the array's end, so removing from the front doesn't require shifting every remaining element.
- **Dynamic (linked list-backed)**: keep both a head pointer (for dequeue) and a tail pointer (for enqueue), so both operations stay O(1) without walking the list.

### Example

```
ALGORITHM Enqueue
Input: queue: Queue, x: Element
Output: (x is now at the back of queue)

queue.back ← (queue.back + 1) mod queue.capacity
queue.data[queue.back] ← x
```

```
ALGORITHM Dequeue
Input: queue: Queue
Output: Element

x ← queue.data[queue.front]
queue.front ← (queue.front + 1) mod queue.capacity
return x
```

### Complexity

`enqueue`, `dequeue`, `front`, `isEmpty` are all **O(1)** — as long as the array version uses a circular buffer (a naive array queue that shifts elements on dequeue degrades to O(n)).

### Related

- Abstract Data Types
- Stack
- Priority Queue
- Linked List
- Graph Traversal (DFS / BFS) (`trees-and-graphs.md`)

## Priority Queue

### What it means in practice

Like Queue, but elements come out in order of **priority**, not arrival order: `insert(x, priority)` adds an element; `extractMin()` (or `extractMax()`) removes and returns the highest-priority element. This is the data structure both Huffman Coding (`algorithm-strategies.md`) and Dijkstra's Algorithm (`trees-and-graphs.md`) rely on to always pick "the best remaining candidate" efficiently.

The standard implementation is a **binary heap**: a complete binary tree (stored compactly in an array — no pointers needed) where every node's priority is ≤ (min-heap) or ≥ (max-heap) both of its children's. That invariant guarantees the root is always the best element, and it's cheap to restore after any single insert/extract.

- `insert`: add the new element at the next free leaf, then **sift up** — repeatedly swap it with its parent while it violates the heap invariant.
- `extractMin`: save the root (the answer), move the last leaf into the root position, then **sift down** — repeatedly swap it with its smaller child while it violates the invariant.

### Complexity

Because the tree is always complete (never lopsided), its height is Θ(log n), and sift up/down each do at most one swap per level → both `insert` and `extractMin` are **O(log n)**. `peek` (look at the root without removing it) is O(1).

### Related

- Abstract Data Types
- Queue
- Huffman Coding (`algorithm-strategies.md`)
- Dijkstra's Algorithm (`trees-and-graphs.md`)

## Linked List

### What it means in practice

A chain of nodes, each holding a value and a pointer to the next node (`null` at the end), plus a `head` pointer to the first one. Unlike an array, there's no fixed capacity and no need to shift elements to insert/remove in the middle — but there's no O(1) random access either; reaching the k-th element means walking k pointers from the head.

This is the standard **dynamic implementation** behind Stack (push/pop at the head) and Queue (enqueue at tail, dequeue at head, with both head and tail pointers kept).

### Example

```
ALGORITHM InsertAtHead
Input: list: LinkedList, x: Element
Output: (x is the new head of list)

newNode ← new Node(value: x, next: list.head)
list.head ← newNode
```

```
ALGORITHM Search
Input: list: LinkedList, target: Element
Output: boolean

current ← list.head
while current != null
    if current.value = target
        return true
    end if
    current ← current.next
end while
return false
```

### Complexity

- Insert/remove **at the head**: **O(1)**.
- Insert/remove **at an arbitrary position**, or **search**: **O(n)** — no way to skip ahead without walking the chain.

### Related

- Abstract Data Types
- Stack
- Queue
- Binary Search Tree (`trees-and-graphs.md`) — the same node-and-pointer idea, branching instead of chained.

## Set

### What it means in practice

An unordered ADT of unique elements — no duplicates, no positional index. Specification: `insert(x)`, `remove(x)`, `contains(x)`, plus set-level operations (`union`, `intersection`, `difference`).

Two common implementations, very different trade-offs:

- **Array/list-backed**: simple, but `contains` needs a linear scan unless the array is kept sorted (then binary search works, at the cost of a slower insert since it must maintain order).
- **Hash-table-backed**: elements are placed by a hash function into buckets; `contains`/`insert`/`remove` don't need to scan anything, at the cost of no ordering and needing to handle collisions (two elements hashing to the same bucket).

### Complexity

| Implementation | insert | contains | remove |
|---|---|---|---|
| Unsorted array | O(1) | O(n) | O(n) |
| Sorted array | O(n) | O(log n) | O(n) |
| Hash table | O(1) average | O(1) average | O(1) average |

### Related

- Abstract Data Types
- Dictionary — same hashing idea, but mapping keys to values instead of just membership.

## Dictionary

### What it means in practice

An ADT mapping keys to values. Specification: `insert(key, value)`, `get(key)`, `remove(key)`, `containsKey(key)`. Two shapes:

- **Simple dictionary**: each key maps to exactly one value (a second `insert` with the same key overwrites the first).
- **Multiple dictionary**: each key can map to several values (a second `insert` with the same key adds to a collection under that key, rather than replacing it) — e.g. an index from a word to *every* document that contains it, not just one.

The standard implementation is a **hash table**: a hash function maps each key to a bucket (an array slot); the value (or, for a multiple dictionary, a small list of values) is stored at that bucket. Collisions (two keys hashing to the same bucket) are handled either by **chaining** (each bucket holds a small linked list of entries) or **open addressing** (probe for the next free slot).

### Complexity

**O(1) average case** for `insert`, `get`, `remove`, `containsKey` — assuming a reasonably uniform hash function and a load factor kept in check (the table resizes once it gets too full). **Worst case O(n)** if many keys collide into the same bucket (a degenerate hash function, or an adversarial input).

### Related

- Abstract Data Types
- Set
- Algorithm Speed (Big-O in Practice) (`complexity.md`)
