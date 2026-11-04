# Designs in ASP.NET Core and Spring Boot

Hand-written, in our own words, from the architect plugin's skills, the framework documentation and common practice. APIs depend on the version, so confirm them through `framework-practices`. These are ways to implement a design. The accepted design decides, and it may ask for something different.

## Contents

- Clean Architecture
- Packaging and enforcement
- DDD building blocks
- Consistency and events
- Integration with other contexts
- Threat model mitigations
- A vertical slice example

## Clean Architecture

| Design concept | ASP.NET Core | Spring Boot |
|---|---|---|
| Entities, domain rules | Plain C# classes and records; no ASP.NET or EF references | Plain Java classes and records; no Spring or web types |
| Use case | Application service or handler | `@Service` class, or a plain class wired in configuration |
| Inbound adapter | Minimal API endpoint or controller | `@RestController` |
| Port (owned by the inner layer) | Interface in the application or domain project | Interface in the application or domain package |
| Outbound adapter | EF Core repository, typed `HttpClient` | Spring Data adapter, `RestClient` wrapper |
| Request and response models | Records per use case | Records per use case |
| Main, composition root | `Program.cs` and `Add…` extensions | `@SpringBootApplication` and `@Configuration` classes |
| Transaction boundary | Use case, through `SaveChanges` or an explicit transaction | `@Transactional` on the use case |
| Humble object | Thin endpoint; presenter mapping | Thin controller; mapper |

The inner layer defines the port in its own terms. `OrderRepository.save(Order)` works. An interface returning `IQueryable`, or exposing `JpaRepository`, leaks the detail through the boundary.

**Pragmatic allowances, if the design permits them.** Purity costs duplication. In a mapping-heavy case, you may annotate domain classes with JPA or map them with EF fluent configuration, which keeps the classes free of attributes. EF's fluent API in the infrastructure project supports separation well. JPA requires annotations or XML, so keeping JPA out of the domain often means a separate persistence model plus mapping. Using `@Transactional` or `@Service` in the application layer is a common and modest compromise. If the design says the domain must not depend on the framework, then these aren't options for the domain. Otherwise, state what you chose and why.

## Packaging and enforcement

| Mechanism | ASP.NET Core | Spring Boot |
|---|---|---|
| Hard module boundary | Separate projects with restricted references | Maven or Gradle modules |
| Light boundary | `internal` visibility | Package-private visibility |
| Module verification | NetArchTest or ArchUnitNET tests | Spring Modulith `ApplicationModules.verify()` |
| Dependency rules | NetArchTest or ArchUnitNET tests | ArchUnit tests |

Feature-first packaging lets you keep use cases together, and a single project or module with enforced rules is often enough to start. An architecture test should fail for the real rule, for example "domain has no dependency on `Microsoft.AspNetCore` or `Microsoft.EntityFrameworkCore`" or "domain doesn't depend on `org.springframework`".

## DDD building blocks

| Concept | ASP.NET Core with EF Core | Spring Boot with JPA |
|---|---|---|
| Entity | Class with private setters and behavior methods | Class with protected no-arg constructor required by JPA, and behavior methods |
| Value object | `record`, mapped with owned or complex types | `record` or `@Embeddable`; check the Hibernate version for record support |
| Aggregate root | The only entry point; children reached through it | Same, with `cascade` and `orphanRemoval` inside the aggregate only |
| Reference to another aggregate | By ID | By ID, not `@ManyToOne` across aggregates |
| Repository | One per aggregate root; port plus EF adapter | One per aggregate root; port plus Spring Data adapter |
| Optimistic concurrency | Concurrency token | `@Version` |
| Domain service | Plain class | Plain class |
| Factory | Static method or factory | Static method or factory |

Rules that matter:

- **Keep invariants in the aggregate:** `order.cancel(reason)` decides, and enforces the rule. Avoid public setters, because any caller could break it. Avoid an anemic model where the service holds the rules, if the design calls for rich behavior.
- **One aggregate per transaction** is the default. Changing several usually means eventual consistency through events, unless the design says otherwise.
- **Collections:** expose read-only views and mutate through root methods. EF can map to a private backing field. For JPA, return unmodifiable views.
- **Load what the invariant needs:** with lazy loading, a validation can trigger queries or fail outside a session.
- **Reads don't need aggregates.** Query with projections directly when reporting or listing, as long as the design allows that split.
- **Use the ubiquitous language** in classes, methods and tests, including at the API boundary when it serves the context.

## Consistency and events

- **In-process domain events:** raised by the aggregate, and dispatched before or after commit. Choose deliberately. A handler that must succeed with the change runs inside the transaction. Side effects such as email run after commit: Spring has `@TransactionalEventListener`, and EF Core has `SaveChanges` interceptors or a dispatcher around the unit of work.
- **Reliable publishing across systems:** a database write and a broker publish can't be atomic. Use a transactional **outbox**, by writing the event in the same transaction and relaying it afterward. Spring Modulith's event publication registry helps within a modular monolith. In .NET, a library such as MassTransit or Wolverine offers one, or write a small one with a hosted service. Consumers must be idempotent, as delivery is at least once.
- **Sagas or process managers** apply if the design requires a multi-step process. Define compensations for every failure, because there's no rollback across services.
- **Check the boundary against the code:** a design's "atomic" needs a single transaction on one database, or a stated alternative.

## Integration with other contexts

- **Anticorruption layer:** an adapter behind a port that translates the external model into yours. External DTOs, enums and error codes stop there. Test the translation with contract or recorded examples.
- **Open host, published language:** versioned DTOs that are separate from the domain model, plus a contract test.
- **Shared kernel:** a small shared module with joint ownership. Don't let it grow by convenience.
- **Separate contexts in a monolith:** separate modules and schemas, with no joins across them, and calls only through published interfaces or events.

## Threat model mitigations

Turn each accepted mitigation into a specific control and a test.

| Threat | ASP.NET Core | Spring Boot | Verify with |
|---|---|---|---|
| Access to another user's object | Resource-based authorization, scoped queries | `@PreAuthorize`, scoped queries | Second user gets 403 or 404 |
| Missing authentication on new endpoints | Fallback authorization policy | `anyRequest().authenticated()` | Anonymous request refused, over all routes |
| Forged tokens | JWT bearer with authority and audience | Resource server with issuer and audience | Bad signature, wrong audience, expired |
| Tampering in transit | HTTPS, HSTS | TLS at the proxy, forwarded headers | Configuration check |
| Repudiation | Structured audit events | Structured audit events | Event emitted with who and what |
| Information disclosure | Problem details, no exception text | `ProblemDetail`, no stack traces | Error response contains no internals |
| Denial of service | Rate limiter, size limits, timeouts | Limits at gateway or filter, timeouts | Limit triggers |
| Secrets exposure | Key Vault or environment | Secret store or environment | Secret scanning; config at startup |

Use `secure-coding` for details. Record any mitigation that lives outside the code, such as at a gateway, and who verifies it.

## A vertical slice example

"Cancel an order": a rule says only unshipped orders can be cancelled. The sketches are illustrative.

```csharp
// Domain: no framework references
public sealed class Order {
    public void Cancel(string reason) {
        if (Status == OrderStatus.Shipped) throw new OrderAlreadyShipped(Id);
        Status = OrderStatus.Cancelled;
        Raise(new OrderCancelled(Id, reason));
    }
}
// Application: owns the port and the unit of work
public sealed class CancelOrder(IOrders orders) {
    public async Task Handle(CancelOrderCommand c, CancellationToken ct) {
        var order = await orders.Get(c.OrderId, ct) ?? throw new OrderNotFound(c.OrderId);
        order.Cancel(c.Reason);
        await orders.Save(order, ct);
    }
}
```

```java
// Domain: no framework references, other than what the design allows
public class Order {
    public void cancel(String reason) {
        if (status == OrderStatus.SHIPPED) throw new OrderAlreadyShipped(id);
        status = OrderStatus.CANCELLED;
        raise(new OrderCancelled(id, reason));
    }
}
// Application: transaction at the use case, port owned here
@Service
class CancelOrder {
    private final Orders orders;
    CancelOrder(Orders orders) { this.orders = orders; }
    @Transactional
    public void handle(CancelOrderCommand c) {
        var order = orders.get(c.orderId()).orElseThrow(() -> new OrderNotFound(c.orderId()));
        order.cancel(c.reason());
        orders.save(order);
    }
}
```

The endpoint maps the request to a command, checks that the user may act on this order, and maps `OrderAlreadyShipped` to a 409 problem response. Tests: the rule at domain level without a framework; the adapter on a real database; one integration test through the pipeline, including the refused user.
