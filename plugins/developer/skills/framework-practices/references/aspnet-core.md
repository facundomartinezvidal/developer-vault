# ASP.NET Core

Hand-written, in our own words, by merging *ASP.NET Core in Action*, 3rd ed. (Andrew Lock, .NET 7) with the official documentation and David Fowler's diagnostic guidance, read through Context7 and Microsoft Learn on 2026-11-04. Where the book and the current documentation differ, the documentation wins. Not generated from the vault.

**Versions at that date:** .NET 10 is the current LTS, supported until November 2028. .NET 8 and .NET 9 both end support on 10 November 2026. .NET 11 is a short-term release. Check the [support policy](https://dotnet.microsoft.com/platform/support/policy/dotnet-core) and the installed version.

## Contents

- Choosing the API style
- Pipeline and startup
- Dependency injection
- Async and request safety
- Validation and errors
- Configuration
- Data access with EF Core
- Calling other services and background work
- Security
- Testing
- Operations

## Choosing the API style

- **New APIs:** the documentation recommends starting with minimal APIs. Consider controllers when you need model-binding extensibility, form binding including `IFormFile`, advanced validation, application parts or OData. In an existing controller code base, keep to controllers.
- **Server-rendered pages:** Razor Pages, or MVC for larger or more customized cases. Blazor is a separate choice.
- **Organize endpoints:** route groups and extension methods per feature rather than a huge `Program.cs`. Keep handlers thin: bind, validate, call the application logic and choose the result.
- **Keep separate models** for requests and responses, away from EF entities. Otherwise you risk over-posting and exposing columns, and your API contract ends up tied to your schema.
- **Use typed results** where possible, so that responses are documented and testable. OpenAPI generation is built in through `AddOpenApi` and `MapOpenApi` on recent versions. The book covers Swashbuckle and NSwag, which still exist.

## Pipeline and startup

Middleware is a two-way chain, and order matters. A typical order is exception handling, HSTS, HTTPS redirection, static files, routing, CORS, authentication, authorization, then endpoints. Check the current recommended order in the documentation. Middleware runs on every request, so keep it fast and free of long work. Don't change headers after the response has started: use `Response.OnStarting` or check `HasStarted`. Don't call `next()` after writing the body.

`Program.cs` is the composition root. Wire concrete implementations there through extension methods per feature.

## Dependency injection

Prefer explicit constructor or handler parameters.

| Lifetime | Use for | Watch for |
|---|---|---|
| Singleton | Stateless services, caches, clients | Must be thread-safe; must not hold scoped services |
| Scoped | Per-request work, such as `DbContext` | Don't use from background threads without creating a scope |
| Transient | Light, stateless objects | Disposable transients stay alive until the scope ends |

The classic bug is the **captive dependency**: a singleton holding a scoped service such as `DbContext`, which is then shared across requests and threads. Scope validation catches it in Development, so run the app there. Keep it on in tests. `IServiceScopeFactory` is the correct way for a singleton or hosted service to use scoped services.

## Async and request safety

These cause outages rather than style problems.

- **Don't block on async:** `.Result`, `.Wait()` and `GetAwaiter().GetResult()` lead to thread pool starvation. Make the whole call stack async.
- **`Task.Run`:** don't await it immediately, and don't use it to wrap a synchronous API. ASP.NET Core already runs on the thread pool.
- **Never `async void`** in a request path. An exception crashes the process, and the request finishes early. Return `Task`.
- **Don't use `HttpContext` after the request,** or from several threads at once; it isn't thread-safe. Copy what you need first. Don't store `IHttpContextAccessor.HttpContext` in a field.
- **Fire and forget:** don't capture `HttpContext`, `DbContext` or injected scoped services in a background closure, because they'll be disposed. Use a hosted service with a queue. An in-process queue loses work on restart, so durable work needs durable storage.
- **Pass `CancellationToken`** from the request to data access and HTTP calls.
- **Don't buffer large bodies:** objects from 85,000 bytes go on the large object heap. Stream them, and paginate collections. Avoid `Request.Form`; use `ReadFormAsync`.
- **Check `ContentLength`:** it's null if the header is missing, so `ContentLength > limit` can be false for a large request. Use the server's request size limits.

## Validation and errors

- **Controllers with `[ApiController]`** return an automatic 400 on invalid models.
- **Minimal APIs:** recent versions have built-in validation with `AddValidation` and DataAnnotations; older versions need a library or manual checks. Confirm this for the installed version.
- **Business rules** go in the application or domain logic, not in attributes.
- **Errors:** register `AddProblemDetails` for RFC-style responses, and use `UseExceptionHandler` with `IExceptionHandler` (version 8 and later). Don't send stack traces or exception messages outside Development.
- **Binding failures in minimal APIs:** outside Development, `ThrowOnBadRequest` is false by default, so a bad-request binding failure returns 400 directly and bypasses your exception handlers. That's a common reason for error formats differing between environments.
- **Exceptions are slow,** so don't use them for normal flow on hot paths. Expected outcomes can be results.

## Configuration

Configuration sources are layered, and later ones override earlier ones: `appsettings.json`, `appsettings.{Environment}.json`, user secrets in Development, environment variables and command-line arguments. Use the options pattern with strongly typed classes, and `ValidateDataAnnotations` plus `ValidateOnStart`, so that bad configuration fails at startup rather than on the first request. `IOptions` is fixed, `IOptionsSnapshot` is per request, and `IOptionsMonitor` sees changes. Secrets go in user secrets locally, and in a secret store such as Key Vault in production; never in `appsettings.json` in source control.

## Data access with EF Core

- **`DbContext`** is scoped and not thread-safe. Don't run parallel queries on one instance. Use `IDbContextFactory` when you need more than one, or in hosted services.
- **Async everywhere,** and let the database do the work: filter with `Where` and project with `Select` before materializing. Watch for client evaluation.
- **Reads:** `AsNoTracking` for read-only queries, and projection to DTOs rather than loading whole graphs. Avoid N+1 with `Include` or a projection, and paginate.
- **Writes:** `SaveChanges` is a transaction on its own. Use an explicit transaction when several saves must be atomic, and don't hold it over a network call. Concurrency tokens handle lost updates; handle `DbUpdateConcurrencyException`.
- **Interpolated raw SQL:** `FromSql` parameterizes; `FromSqlRaw` with concatenated input doesn't.
- **Migrations:** review the generated code, since it can drop columns. EF Core 9 and later take a database-wide lock when migrating, so applying at startup can be acceptable for simple deployments. On older versions several instances can collide. A separate deploy step is still preferred when you need review, least-privilege credentials, a coordinated rollout or high availability. Use an idempotent script if the SQL must be reviewed, or a migration bundle, which can't be inspected yet. Do expand and contract.
- **Performance features** such as pooling and compiled queries are worth it only after measuring.

## Calling other services and background work

- **HTTP:** never create and dispose `HttpClient` per call, because it can exhaust sockets. Use `IHttpClientFactory` with named or typed clients, set timeouts, and add resilience through `Microsoft.Extensions.Http.Resilience` (the standard handler). Check that retries only apply to idempotent calls.
- **Background work:** derive from `BackgroundService`. Honor the stopping token, catch and log exceptions in the loop, and create a scope per unit of work. For long or CPU-heavy work, consider running out of process with a broker.

## Security

- **Identity:** the book's advice remains strong: consider an external identity provider for multiple apps. ASP.NET Core Identity suits a single app with its own users.
- **JWT bearer:** set `Authority` and `Audience`, and leave validation on. Prefer defaults; don't disable issuer, audience or signature checks. `MapInboundClaims = false` avoids renamed claims.
- **Authorization:** policies rather than scattered role checks. Consider a fallback policy that requires authenticated users, so that a new endpoint is closed by default. For access to a specific object, use **resource-based authorization** with `IAuthorizationService`, or scope the query by owner, because route-level attributes can't see the object.
- **Browsers:** Razor encodes by default, so treat `Html.Raw` as dangerous. Cookie authentication needs antiforgery protection. Keep CORS narrow.
- **Behind a proxy:** configure forwarded headers correctly, and only trust known proxies. Use HTTPS, with HSTS in production.
- **Several instances:** persist Data Protection keys to shared storage, or cookies and tokens break between instances.
- **Rate limiting** middleware is built in on recent versions.

## Testing

- **Unit test logic without the framework.** Handlers should have little logic, so testing them in isolation adds little.
- **Integration tests:** `WebApplicationFactory<Program>` runs the real pipeline in memory, covering routing, binding, filters and auth. Replace dependencies with `ConfigureTestServices`. Test refused access too.
- **Database:** use the real engine with Testcontainers where queries matter. The EF in-memory provider isn't relational, and it misses many behaviors; SQLite differs as well.
- **Framework:** xUnit is the usual choice. Follow the project.

## Operations

- **Logging:** `ILogger<T>` with message templates (`"Order {OrderId}"`), not interpolated strings, so that fields stay structured. Set levels by category. Avoid high-volume logs on hot paths. Write to durable output.
- **Telemetry:** OpenTelemetry for traces and metrics.
- **Health checks:** `AddHealthChecks` and `MapHealthChecks`, with separate liveness and readiness endpoints where the platform uses them.
- **Caching and compression:** cache what's measured to matter, and compress responses at the app or proxy.
- **Shutdown:** hosted services get a limited time, so handle cancellation.

## Common mistakes to look for

`.Result` or `.Wait()`; `async void`; `new HttpClient()` per call; `DbContext` in a singleton or a background closure; returning EF entities; loading then filtering in memory; missing `CancellationToken`; `ex.Message` in responses; secrets in `appsettings.json`; `[Authorize]` without a per-object check; `Database.Migrate()` at startup before EF Core 9 with several instances, or with an app account that shouldn't change the schema; `IEnumerable` from a query enumerated synchronously by the serializer.
