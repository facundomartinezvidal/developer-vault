# Modeling relational data

From entity-relationship models to relational tables.

## Contents

- [Levels of Abstraction in Database Design](#levels-of-abstraction-in-database-design)
- [Entity-Relationship Model](#entity-relationship-model)
- [Extended Entity-Relationship Model](#extended-entity-relationship-model)
- [ER-to-Relational Mapping](#er-to-relational-mapping)
- [Relational Model](#relational-model)

## Levels of Abstraction in Database Design

### What it means in practice

A database is designed through three progressively more concrete models, each answering a different question:

- **Conceptual model** — *what* does the domain look like, independent of any DBMS? Entities, relationships, business rules. This is where the Entity-Relationship model lives.
- **Logical model** — how is that structured for a *particular kind* of database (relational, document, graph...), still independent of a specific product? This is where the Relational Model lives — tables, keys, constraints, but no vendor-specific SQL dialect yet.
- **Physical model** — how is it actually stored on a specific DBMS: file organization, indexes (`sql-and-indexes.md`), partitioning, storage engine details.

Same relationship as Abstract Data Types' specification/implementation split, applied to an entire database instead of a single structure: the conceptual model is "what", the physical model is "how", and the logical model is the bridge between them.

### Database lifecycle

Design flows conceptual → logical → physical, but a real database's lifecycle keeps cycling back: requirements analysis, conceptual design, logical design (including normalization (`normalization.md`)), physical design, implementation, and then ongoing maintenance/evolution that can loop back to any earlier stage as requirements change.

### Related

- Entity-Relationship Model
- Relational Model
- Database Indexes (`sql-and-indexes.md`)
- Normal Forms (`normalization.md`)

## Entity-Relationship Model

### What it means in practice

A conceptual modeling notation for describing a domain before touching any database technology. Three core building blocks:

- **Entity** — a distinguishable "thing" the database needs to track (a `Customer`, an `Order`). Drawn as a rectangle.
- **Attribute** — a property of an entity (a `Customer` has a `name`, an `email`). Drawn as an oval attached to its entity; one attribute (or combination) is marked as the entity's **identifier/key**.
- **Relationship** — an association between two (or more) entities (`Customer` *places* `Order`). Drawn as a diamond connecting the entities involved.

Relationships carry **cardinality constraints** — how many instances of one entity can relate to how many of another:

- **1:1** — one `Employee` manages one `Department`, one `Department` has one manager.
- **1:N** — one `Customer` places many `Orders`, each `Order` belongs to one `Customer`.
- **N:M** — many `Students` enroll in many `Courses`; this shape can't be represented directly in the relational model without an intermediate structure (see ER-to-Relational Mapping).

### Related

- Extended ER Model — adds inheritance-like constructs on top of this.
- ER-to-Relational Mapping
- Levels of Abstraction
- Relational Model

## Extended Entity-Relationship Model

### What it means in practice

Adds constructs to the plain ER Model for situations a basic entity/relationship/attribute vocabulary can't express cleanly — mainly **generalization/specialization**, the ER equivalent of inheritance:

- **Specialization** — starting from a general entity (`Vehicle`) and splitting it into more specific subtypes (`Car`, `Truck`), each inheriting `Vehicle`'s attributes and adding its own.
- **Generalization** — the reverse direction: noticing several entities share common attributes and factoring them into a shared supertype.

Two independent dimensions describe how a specialization behaves:

- **Disjoint vs. overlapping** — can an instance belong to more than one subtype at once (a `Vehicle` that's both `Car` and `Truck`)? Disjoint says no, overlapping says yes.
- **Total vs. partial** — must every instance of the supertype belong to *some* subtype? Total participation requires it; partial allows supertype instances that don't fall into any listed subtype.

### Related

- Entity-Relationship Model
- ER-to-Relational Mapping

## ER-to-Relational Mapping

### What it means in practice

The rule set for turning an ER diagram into relational tables:

- **Entity** → its own table; its identifying attribute(s) become the primary key.
- **1:N relationship** → add the "1" side's primary key as a foreign key on the "N" side's table (e.g. `Order` gets a `customer_id` column). No new table needed.
- **N:M relationship** → cannot be represented with a foreign key on either side (each row would need multiple values in one column). Instead, create a **junction table** whose primary key is the combination of both entities' foreign keys — e.g. `Enrollment(student_id, course_id)` for a `Student`–`Course` N:M relationship.
- **1:1 relationship** → the foreign key can go on either side (whichever participates less often, if participation is partial on one side).
- **Multivalued attribute** (an attribute that can hold several values per entity, e.g. a person's multiple phone numbers) → its own table, referencing the owning entity's primary key as a foreign key.

### Related

- Entity-Relationship Model
- Relational Model
- Extended ER Model
- SQL: Data Definition (DDL) (`sql-and-indexes.md`)

## Relational Model

### What it means in practice

The logical model behind SQL databases: data lives in **relations** (tables) — a set of **tuples** (rows), each assigning a value to every **attribute** (column) in the relation's fixed schema. No row order and no duplicate rows are guaranteed by the model itself (a table is conceptually a *set* of tuples).

A handful of key types, in increasing strictness:

- **Superkey** — any set of attributes that uniquely identifies a tuple (possibly with redundant attributes in it).
- **Candidate key** — a *minimal* superkey — remove any attribute from it and it stops being unique.
- **Primary key** — the candidate key chosen to be *the* official identifier for the table.
- **Alternate key** — any candidate key that wasn't chosen as primary.
- **Foreign key** — an attribute (or set of attributes) in one table that references a primary key in another, encoding a relationship between the two tables.

These same key concepts are exactly what Functional Dependencies (`normalization.md`) and normalization (`normalization.md`) are built on.

### Related

- Entity-Relationship Model
- ER-to-Relational Mapping
- Functional Dependencies (`normalization.md`)
- Relational Algebra (`sql-and-indexes.md`)
- Levels of Abstraction in Database Design
- Normal Forms (`normalization.md`)
- SQL: Data Definition (DDL) (`sql-and-indexes.md`)
