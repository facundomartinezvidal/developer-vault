# Normalization

Functional dependencies and normal forms.

## Functional Dependencies

### What it means in practice

A functional dependency **X → Y** means: knowing the value of attribute set X always determines the value of attribute set Y — two rows that agree on X must agree on Y. This is the formal tool behind key (`modeling.md`) concepts and normalization:

- A **superkey** is exactly a set of attributes that functionally determines *every* attribute in the relation.
- A **candidate key** is a minimal superkey — remove any attribute and the dependency breaks.
- **Redundancy** happens when a non-key attribute is repeated across rows because of a functional dependency that isn't fully "respected" by the table's current shape — this is exactly what normalization removes.

### Closure and canonical cover

The **closure** of a set of attributes X (written X⁺) is every attribute functionally determined by X, directly or transitively, given a set of FDs — computing it is how you check whether X is a (super)key: X is a superkey iff X⁺ includes every attribute in the relation.

A set of FDs can usually be rewritten in a smaller, equivalent form — the **canonical cover**: no redundant FDs, no FD with an attribute on its left side that isn't actually needed. This is what makes checking normal forms tractable — testing every attribute combination against a bloated FD set is far more work than testing against its minimal, equivalent canonical cover.

### Related

- Relational Model (`modeling.md`)
- Normal Forms

## Normal Forms

### What it means in practice

A strictly nested progression of criteria a relation can satisfy — each normal form fixes a specific kind of redundancy/anomaly the previous one still allowed, and each is a stricter subset of the one before it (5NF ⊂ 4NF ⊂ BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF). All of them are defined in terms of functional dependencies (or, from 4NF onward, generalizations of that idea).

#### 1NF — First Normal Form

Every attribute holds a single, atomic value — no repeating groups, no multi-valued or nested columns (e.g. no single `phone_numbers` column holding a comma-separated list). This is the baseline: a relation isn't a valid relation at all without it.

#### 2NF — Second Normal Form

1NF, plus: no **partial dependency** — every non-key attribute must depend on the *whole* primary key, not just part of it. Only matters when the primary key is composite (more than one attribute); with a single-attribute key, 1NF automatically implies 2NF.

#### 3NF — Third Normal Form

2NF, plus: no **transitive dependency** — a non-key attribute can't depend on another non-key attribute (it must depend directly on the key). Example violation: `Order(order_id, customer_id, customer_city)` where `customer_city` depends on `customer_id`, not directly on `order_id`.

#### BCNF — Boyce-Codd Normal Form

A tighter version of 3NF: for *every* non-trivial functional dependency X → Y in the relation, X must be a superkey — not just part of a candidate key, the whole thing. Every BCNF relation is in 3NF, but a 3NF relation can fail BCNF when a determinant is part of a candidate key without being one itself. BCNF eliminates more anomalies than 3NF, but doesn't always preserve every original functional dependency after decomposition — 3NF is sometimes preferred in practice for that reason.

#### 4NF — Fourth Normal Form

BCNF, plus: no non-trivial **multivalued dependency** unless the determinant is a superkey. A multivalued dependency X ↠ Y means: for a fixed X, the set of Y values associated with it doesn't depend on any other attribute in the relation. Typical violation: a table listing `(employee, skill, language)` where an employee's skills and languages are independent of each other, but the table forces every skill to be paired with every language — this redundantly repeats every skill for every language, even though no real dependency exists between them.

#### 5NF — Fifth Normal Form (Project-Join Normal Form)

4NF, plus: every non-trivial **join dependency** is implied by the candidate keys — the relation can't be losslessly split into three or more smaller relations (a pattern functional and multivalued dependencies can't capture) without that split being forced by the keys themselves. Rare in practice; mostly relevant for relations recording three-or-more-way many-to-many facts.

### Related

- Functional Dependencies
- Relational Model (`modeling.md`)
- Levels of Abstraction in Database Design (`modeling.md`)
