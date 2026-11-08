---
name: api-design
description: "Designs and reviews APIs other code depends on: HTTP endpoints, RPC, GraphQL, webhooks, events and public library functions. Use for request and response shapes, status codes, errors, pagination, idempotency, versioning and breaking changes (\"qué status devuelvo\", \"esto rompe a los clientes\")."
---

# API Design

Use this skill to **design**, **implement**, **review** or **evolve** an API. Its point of view: an API is a promise to code you may not control. It's cheap to add to and expensive to take back, so publish less and make its behavior explicit.

## Start from the caller

Find out who calls it and what they're trying to get done. Write the calling code or an example request first, because a clumsy example reveals a clumsy API. Read existing endpoints, and follow their conventions for naming, errors and pagination: a consistent API beats a locally better one. Use an existing spec, such as OpenAPI, if the project has one, and keep it updated.

## What to define

Include what applies, in proportion to the change.

- **Resources and operations.** Name things in the domain's terms, not after your tables. Don't expose internal structures, since they then become part of the contract. Use separate types for requests, responses and persistence.
- **Methods and status codes (HTTP).** GET is safe, PUT and DELETE are idempotent, POST isn't. Use 200, 201, 202, 204; 400 or 422 for invalid input; 401 unauthenticated; 403 forbidden; 404 not found; 409 conflict; 429 rate limited; 5xx only for server faults, so clients can decide whether to retry.
- **Errors.** One machine-readable format with a stable code, a human message, field details, and a correlation ID, such as RFC 9457 problem details. Clients should never need to parse the message. Internals stay out.
- **Validation.** At the boundary: types, ranges, sizes and unknown fields. Report all field errors together where that's helpful.
- **Lists.** Always paginate; limits are easy to set now and hard later. Prefer cursors for large or changing data. Offsets are fine for small and stable data. Define the sort order and use allowlists for filters.
- **Idempotency.** Networks fail and clients retry. Payments and other creates that shouldn't duplicate need an idempotency key, stored with the result under a unique constraint. Define what happens on a timeout.
- **Concurrency.** Decide what happens with two writers: ETags and `If-Match`, version columns, or an explicit last-write-wins.
- **Long work.** Return 202 with a status resource or a webhook, rather than holding the request.
- **Data types.** ISO 8601 UTC for times, and strings or integer minor units for money. Make null, absent and empty mean defined things. Use stable IDs that don't reveal counts when that matters.
- **Security.** Authentication, per-object authorization, rate limits, and size limits. Load `secure-coding` for these.

For webhooks and events, define signature verification, retries, ordering and duplicate delivery; consumers must tolerate all of them. Include an event ID and a version.

For library APIs, follow the language's idioms for errors, naming, async and options. Keep the surface small, make misuse difficult through types, and document contract and failure behavior. Mind semantic versioning.

## Evolving without breaking

Find out who the clients are before you change anything. Usually compatible: adding optional request fields or new response fields, when clients ignore unknown ones. Breaking: removing or renaming fields, changing types, meanings, defaults or error codes, tightening validation, or adding an enum value that strict clients can't handle.

To change something incompatible: add the new form alongside, migrate clients, measure use of the old form, announce the deprecation, and then remove it. Version only when you must, using the project's convention, since each live version has a cost.

## Output

**Design:** the contract as an example or spec, including failure cases, plus the decisions the user should confirm. Note what you left out on purpose.

**Implementation:** the code following the project's patterns, tests for success and failure, including refused access, and any updated docs or spec. Report what you ran.

**Review:** findings most costly first, with `file:line`, focused on what clients experience. Mark any breaking change explicitly.
