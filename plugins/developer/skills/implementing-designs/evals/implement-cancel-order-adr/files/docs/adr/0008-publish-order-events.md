# ADR-0008: Publish order events to Kafka

- **Status:** Proposed
- **Date:** 2026-10-28

## Decision

We will publish OrderCancelled to Kafka using a transactional outbox.
