# ADR-0007: Cancelling orders in the domain

- **Status:** Accepted
- **Date:** 2026-10-20

## Context

Cancellation logic is spreading across endpoints.

## Decision

We will place the rule "a shipped order cannot be cancelled" in the Order domain class. The domain and application layers will not depend on EF Core or ASP.NET Core. Application code will reach persistence through an interface it owns. We will enforce the dependency rule with an automated check.

## Consequences

Endpoints only translate requests and outcomes to HTTP.

## Pending

Suggestion: consider soft-deleting cancelled orders. Not agreed.
