# Trees and graphs

Balanced search, B-trees, graph representation, traversal, shortest paths and spanning trees.

## Contents

- [Binary Search Tree](#binary-search-tree)
- [AVL Tree](#avl-tree)
- [B-Tree](#b-tree)
- [Graph Representation](#graph-representation)
- [Graph Traversal (DFS / BFS)](#graph-traversal-dfs-bfs)
- [Dijkstra's Algorithm](#dijkstras-algorithm)
- [Minimum Spanning Tree](#minimum-spanning-tree)
- [Prim's Algorithm](#prims-algorithm)
- [Kruskal's Algorithm](#kruskals-algorithm)

## Binary Search Tree

### What it means in practice

A binary tree (each node has at most two children, `left` and `right`) with the **BST invariant**: for every node, everything in its left subtree is smaller, everything in its right subtree is larger. That single invariant is what makes search fast — at each node, comparing the target to the node's key tells you which subtree (if any) could contain it, so you never need to look at the other one. Same core idea as Divide & Conquer (`algorithm-strategies.md`): recursively narrow to the one subproblem that could contain the answer.

- `search(key)`: compare to the current node; if equal, found; if smaller, recurse left; if larger, recurse right; if you hit `null`, not present.
- `insert(key)`: search for where the key *would* be, and attach a new leaf there.
- Traversal order gives the sorted sequence for free: **in-order** traversal (left, node, right) visits every key in ascending order.

### Example

```
ALGORITHM Search
Input: node: TreeNode, key: integer
Output: boolean

if node = null
    return false
else if key = node.key
    return true
else if key < node.key
    return Search(node.left, key)
else
    return Search(node.right, key)
end if
```

### Complexity

Depends entirely on the tree's shape: **O(log n)** if the tree stays roughly balanced (height ≈ log n), but degrades to **O(n)** in the worst case — inserting already-sorted data into a plain BST produces a tree that's really just a linked list, one child deep at every level. AVL trees exist specifically to guarantee the balanced case never degrades.

### Related

- Divide and Conquer (`algorithm-strategies.md`)
- AVL Tree — a self-balancing BST that fixes this worst case.
- Linked List (`linear-and-associative.md`) — what a maximally unbalanced BST degenerates into.
- B-Tree

## AVL Tree

### What it means in practice

A Binary Search Tree that automatically stays balanced, guaranteeing O(log n) search even for adversarial insertion orders. Every node tracks a **balance factor** = height(left subtree) − height(right subtree), and the tree enforces that this stays in {−1, 0, +1} for *every* node. Whenever an insert or delete pushes a node's balance factor to +2 or −2, a **rotation** restores the invariant — locally, in O(1), without touching the rest of the tree.

Four cases, based on where the imbalance came from:

- **Left-Left**: inserted into the left subtree of the left child → single **right rotation**.
- **Right-Right**: inserted into the right subtree of the right child → single **left rotation**.
- **Left-Right**: inserted into the right subtree of the left child → left rotation on the left child, then right rotation on the node.
- **Right-Left**: inserted into the left subtree of the right child → right rotation on the right child, then left rotation on the node.

### Example: single right rotation (Left-Left case)

```
ALGORITHM RotateRight
Input: node: TreeNode  // node.left exists, causing the imbalance
Output: TreeNode  // new subtree root

newRoot ← node.left
node.left ← newRoot.right
newRoot.right ← node
return newRoot  // caller re-attaches newRoot where node used to be
```

### Complexity

Balance is checked and fixed on the way back up from every insert/delete, and each rotation is O(1) — so `insert`, `remove`, and `search` are all **O(log n) worst case**, unlike a plain BST's O(n) worst case.

### Related

- Binary Search Tree
- B-Tree — a different balancing strategy (multi-way nodes instead of rotations), aimed at disk-backed storage rather than in-memory trees.

## B-Tree

### What it means in practice

A self-balancing search tree like AVL, but each node can hold **many** keys and **many** children instead of just one key and two children — designed for storage where reading a block is expensive (disks, databases), so it pays off to pack many keys into each node and keep the tree very shallow.

For a B-tree of **order m**:

- Every node has **at most m children** and **at most m−1 keys**.
- Every node (except the root and leaves) has **at least ⌈m/2⌉ children** and **at least ⌈m/2⌉−1 keys** — nodes can never get too sparse.
- The root has at least 2 children (unless it's a leaf, i.e. the whole tree is just the root).
- **Every leaf sits at the same depth** — this is what keeps the tree perfectly balanced, unlike an AVL tree's per-node balance factor.

Within a node, keys are kept sorted, and searching a node means scanning its (small) key list to find which child to descend into next — same divide-and-conquer idea as a BST, just branching m ways instead of 2.

**Insert**: descend to the right leaf and insert the key there; if the leaf now has m keys (over capacity), **split** it into two nodes and push the middle key up into the parent — which can itself overflow and split, potentially all the way up to the root (this is how the tree grows, always from the root down, keeping every leaf at the same depth).

### Complexity

Height stays **O(log_m n)** by construction (every level multiplies capacity by up to m), and each node's internal scan costs O(m) or O(log m) with binary search inside the node — so `search`, `insert`, and `remove` are all **O(log n)**, with a much smaller constant in practice than a binary tree when m is large, since far fewer block reads are needed to reach a leaf.

### Related

- AVL Tree
- Binary Search Tree

## Graph Representation

### What it means in practice

A graph is a set of **vertices** (nodes) and **edges** (connections between them, optionally weighted). Edges are either **directed** (an edge A→B is distinct from B→A) or **undirected** (A–B = B–A). Two standard ways to represent this in memory, with very different trade-offs:

- **Adjacency matrix**: a V×V boolean/weight matrix, `matrix[i][j]` = is there an edge from i to j (and its weight, if any). Checking whether a specific edge exists is O(1), but the matrix takes O(V²) space regardless of how many edges actually exist — wasteful for a **sparse** graph (few edges relative to V²).
- **Adjacency list**: an array of V lists, where list[i] holds every vertex j such that an edge i→j exists. Space is O(V + E) — proportional to what's actually there — but checking whether a specific edge exists means scanning a list instead of one array lookup.

This is the representation that Dijkstra, Prim, and Kruskal all operate on top of — those algorithms describe *what* to compute; this note is about the underlying structure they read from.

### Complexity

| | Space | Check edge (i,j) exists | Iterate all neighbors of i |
|---|---|---|---|
| Adjacency matrix | O(V²) | O(1) | O(V) |
| Adjacency list | O(V + E) | O(degree of i) | O(degree of i) |

Dense graphs (E close to V²) favor a matrix; sparse graphs (E much smaller than V²) favor a list — most real-world graphs are sparse.

### Related

- Graph Traversal
- Dijkstra's Algorithm
- Prim's Algorithm
- Kruskal's Algorithm

## Graph Traversal (DFS / BFS)

### What it means in practice

Both visit every vertex reachable from a starting vertex exactly once, but explore in a different order — and that order changes what each is naturally good for. Both need a `visited` set so they never revisit a vertex (graphs, unlike trees, can have cycles).

- **Depth-First Search**: go as deep as possible down one path before backtracking — implemented with a stack (`linear-and-associative.md`) (explicit, or the call stack via recursion). Natural for: detecting cycles, finding connected components, topological sort.
- **Breadth-First Search**: explore all neighbors at the current distance before going further — implemented with a queue (`linear-and-associative.md`). Natural for: shortest path *by number of edges* (unweighted shortest path — Dijkstra is the weighted generalization of this).

### Example

```
ALGORITHM DFS
Input: graph: Graph, start: Vertex
Output: (visits every vertex reachable from start)

visited ← empty set
Stack.push(start)

while not Stack.isEmpty()
    v ← Stack.pop()
    if v not in visited
        visited.add(v)
        for each neighbor of v
            Stack.push(neighbor)
        end for
    end if
end while
```

```
ALGORITHM BFS
Input: graph: Graph, start: Vertex
Output: (visits every vertex reachable from start, in order of distance)

visited ← empty set
Queue.enqueue(start)
visited.add(start)

while not Queue.isEmpty()
    v ← Queue.dequeue()
    for each neighbor of v
        if neighbor not in visited
            visited.add(neighbor)
            Queue.enqueue(neighbor)
        end if
    end for
end while
```

### Complexity

Both are **O(V + E)** — every vertex is enqueued/pushed once, and every edge is examined once (from whichever endpoint gets visited first).

### Related

- Graph Representation
- Stack (`linear-and-associative.md`)
- Queue (`linear-and-associative.md`)
- Dijkstra's Algorithm — BFS generalized to weighted edges.

## Dijkstra's Algorithm

### What it means in practice

Given a **directed graph with only positive edge weights** and a source vertex, find the minimum-cost path from that source to every other reachable vertex. A greedy (`algorithm-strategies.md`) algorithm: at each step, permanently finalize whichever unvisited vertex currently has the lowest known distance from the source — that vertex's tentative distance can never improve later (all remaining edges only add positive weight), so the greedy choice is provably safe.

- **Candidates**: every vertex except the source.
- **Selection function**: among unvisited vertices, pick the one with the smallest known distance so far; mark it visited/finalized.
- **Feasibility function**: relaxation — check whether reaching a neighbor *through* the newly finalized vertex is cheaper than its current known distance.
- **Solution function**: every vertex has been processed.
- **Objective function**: minimum-cost path from the source to every other vertex.

### Algorithm

```
ALGORITHM Dijkstra
Input: graph: Graph, source: Vertex
Output: array<integer>  // dist[v] = shortest distance from source to v

dist ← array of size n, all set to infinity
dist[source] ← 0
visited ← array of size n, all set to false

for i = 0 to n-1
    u ← the unvisited vertex with minimum dist[u]
    visited[u] ← true

    for each neighbor v of u
        if not visited[v] and dist[u] + weight(u, v) < dist[v]
            dist[v] ← dist[u] + weight(u, v)
        end if
    end for
end for

return dist
```

### Complexity

With an adjacency matrix and a linear scan to find the minimum-distance unvisited vertex each round: two nested loops over the vertex count → **O(V²)**. (A priority-queue-backed version gets this down to O((V+E) log V), but that's a separate implementation choice, not what this course's version uses.)

### Limitation

Requires all edge weights to be non-negative — a negative edge can make an already-finalized vertex's distance wrong in a way Dijkstra never revisits to fix. Bellman-Ford is the standard algorithm for graphs with negative edges (not covered in this course).

### Related

- Greedy Algorithms (`algorithm-strategies.md`)
- Minimum Spanning Tree
- Priority Queue (`linear-and-associative.md`) — the data structure a faster implementation of this algorithm relies on.
- Graph Representation
- Graph Traversal — Dijkstra is BFS generalized to weighted edges.

## Minimum Spanning Tree

### What it means in practice

Defined only for **undirected**, connected, weighted graphs. A spanning tree of graph G(V, A) is a subgraph G'(V, A') that keeps every vertex but only a subset of edges, such that G' is connected and acyclic (a tree — exactly V−1 edges). A **minimum** spanning tree is the spanning tree whose total edge weight is the lowest among all possible spanning trees of G.

A graph can have more than one MST — if so, they all share the same (minimum) total weight, just with a different edge subset. Two greedy algorithms solve this problem: Prim's Algorithm and Kruskal's Algorithm. If the MST is unique, both produce the same result; if several MSTs exist, they can produce different (equally optimal) ones, since each explores the graph in a different order.

### Related

- Prim's Algorithm
- Kruskal's Algorithm
- Greedy Algorithms (`algorithm-strategies.md`)
- Dijkstra's Algorithm

## Prim's Algorithm

### What it means in practice

Builds a Minimum Spanning Tree by growing a single tree one vertex at a time: start from an arbitrary vertex, and at each step add whichever vertex *not yet in the tree* is connected to the tree by the cheapest available edge — until every vertex is included. Mapped onto the greedy (`algorithm-strategies.md`) template:

- **Candidates**: vertices not yet in the tree.
- **Selection function**: the not-yet-included vertex reachable by the cheapest edge from the current tree.
- **Feasibility function**: whether to actually use that edge (implementation detail — in the simple version, always yes).
- **Solution function**: every vertex has been added.
- **Objective function**: minimum total edge weight.

### Algorithm

```
ALGORITHM Prim
Input: graph: Graph, start: Vertex
Output: array<Edge>  // the MST's edges

inTree ← array of size n, all set to false
inTree[start] ← true
mstEdges ← empty list

for i = 1 to n-1
    (u, v) ← the cheapest edge where u is in the tree and v is not
    mstEdges.add((u, v))
    inTree[v] ← true
end for

return mstEdges
```

### Complexity

With an adjacency-matrix scan to find the cheapest crossing edge each round: nested loop over the vertex count → **O(V²)**.

### Related

- Minimum Spanning Tree
- Kruskal's Algorithm
- Graph Representation
- Greedy Algorithms (`algorithm-strategies.md`)

## Kruskal's Algorithm

### What it means in practice

Builds a Minimum Spanning Tree from the *edges* instead of growing outward from a vertex like Prim does: start with every vertex as its own single-node tree, sort all edges ascending by weight, and repeatedly take the cheapest remaining edge — adding it only if its two endpoints are currently in *different* trees (merging those trees), and discarding it otherwise (it would create a cycle). Mapped onto the greedy (`algorithm-strategies.md`) template:

- **Candidates**: all edges of the graph.
- **Selection function**: the cheapest remaining edge.
- **Feasibility function**: the edge's two endpoints must be in different trees (no cycle created).
- **Solution function**: V−1 edges have been added.
- **Objective function**: minimum total edge weight.

Checking "are these two vertices already in the same tree, and if not, merge their trees" is exactly the job of a **Union-Find** (disjoint-set) data structure, even where it isn't named explicitly — `Find` answers "which tree is this vertex in," `Union` merges two trees.

### Algorithm

```
ALGORITHM Kruskal
Input: graph: Graph
Output: array<Edge>  // the MST's edges

edges ← all edges of graph, sorted ascending by weight
forest ← each vertex in its own singleton tree
mstEdges ← empty list

for each (u, v) in edges
    if Find(u) != Find(v)
        mstEdges.add((u, v))
        Union(u, v)
    end if
end for

return mstEdges
```

### Complexity

**O(E log E)**, dominated by sorting the edges (E = number of edges); the Union-Find operations themselves are nearly constant-time (Θ(log V) or better with standard optimizations), so they don't change the overall bound.

### Related

- Minimum Spanning Tree
- Prim's Algorithm
- Graph Representation
- Greedy Algorithms (`algorithm-strategies.md`)
