# Spring Boot

Hand-written, in our own words, by merging *Spring Boot in Action* (Craig Walls, Spring Boot 1.3) with the official documentation for Spring Boot 4 and Spring Security 7, read through Context7 and spring.io on 2026-11-04. The book is old, so here it contributes the concepts: starters, auto-configuration, overriding, Actuator and testing layers. Its Groovy, Grails and CLI material, and older APIs, aren't used. Not generated from the vault.

**Versions at that date:** Spring Boot 4.1 is the newest line, built on the 4.0 generation: Spring Framework 7, Java 17 as a minimum, first-class Java 25, and a modular code base with new starters. Many projects remain on 3.x, where packages and test annotations differ, so check the build file first, and read the [migration guide](https://github.com/spring-projects/spring-boot/wiki) for each major version.

## Contents

- How Boot works
- Structure
- Dependency injection
- Configuration
- Web layer and errors
- Transactions
- Data access with JPA
- Calling other services and async
- Security
- Testing
- Operations

## How Boot works

- **Starters** add a coherent set of dependencies by capability; let the Boot BOM manage versions rather than pinning each one.
- **Auto-configuration** creates beans according to the classpath and properties, and **backs off when you define your own**. To change behavior, first look for a property, then a customizer, and only then replace the bean. Replacing more than needed loses what Boot was doing for you.
- When something "just happens" or doesn't, the conditions report shows why (`--debug`, or the `conditions` Actuator endpoint in a safe environment). That's the first place to look.
- Know that adding a dependency can change behavior. Adding Spring Security, for example, locks down all endpoints.

## Structure

Put the main class in a root package above everything else, since `@SpringBootApplication` scans from there; avoid the default package. The documentation's typical layout is **by feature** (`customer`, `order`), with controller, service and repository together. Spring Modulith can verify and enforce module boundaries, and ArchUnit can enforce dependency rules. Keep visibility as narrow as possible: package-private types are a cheap boundary.

## Dependency injection

Use constructor injection, with `final` fields. A single constructor needs no `@Autowired`. Avoid field injection, as it hides dependencies and makes tests harder; the book's examples use it because they're old. Beans are singletons by default, so they must not hold per-request state. A prototype-scoped bean inside a singleton becomes effectively a singleton. Circular references are a design signal, and are prohibited by default.

## Configuration

- **Sources are ordered:** command-line arguments and environment variables override `application.yaml`, and profile files override the base file. Relaxed binding means that `MY_SERVICE_URL` maps to `my.service.url`.
- **Use `@ConfigurationProperties`,** preferably immutable with constructor binding or a record, enabled through `@ConfigurationPropertiesScan`. Add `@Validated` with constraints so that bad configuration fails at startup. Use `@Value` only for the odd simple value.
- **Profiles** express environments or capabilities. Don't scatter `@Profile` through business code.
- **Secrets** come from the environment or a secret store, never committed.

## Web layer and errors

- **Controllers stay thin:** bind, validate, delegate and map. Business rules and transactions belong in services.
- **DTOs:** use records for requests and responses, never JPA entities, which cause over-posting, lazy-loading failures and a contract tied to the schema.
- **Validation:** `@Valid` on the request body with Bean Validation, plus `@Validated` for method parameters. Check that the validation starter is present, or the annotations do nothing.
- **Errors:** centralize with `@RestControllerAdvice` and `ProblemDetail` (RFC 9457). Boot's support for framework exceptions is off by default; turn it on with `spring.mvc.problemdetails.enabled=true`. Don't expose stack traces or exception messages.
- **API versioning** has first-class support in version 4; follow the project's approach.
- **JSON:** Boot 4 defaults to Jackson 3, whose packages move to `tools.jackson`, apart from the annotations. Older examples and libraries may still use Jackson 2.
- **Blocking or reactive:** Spring MVC is the default. Use WebFlux when you really need its model and the whole stack is non-blocking. Blocking calls on an event loop are a serious defect. Don't mix them casually.

## Transactions

`@Transactional` works through proxies, which produces the most common bugs:

- **Self-invocation:** a call to a `@Transactional` method from the same class bypasses the proxy, so there's no transaction. Move the method to another bean, or use `TransactionTemplate`.
- **Visibility:** apply it to public methods on Spring beans. Objects you create with `new` get nothing.
- **Rollback:** by default it only rolls back on unchecked exceptions and `Error`. A checked exception commits, unless you set `rollbackFor`. Catching an exception inside doesn't necessarily undo the rollback-only mark.
- **Placement:** on the service method that defines the unit of work, not on the controller. Keep it short, and don't make network calls inside; they hold the connection and can't be rolled back.
- **Reads:** `readOnly = true` documents intent and can help the provider.
- **Same concern with `@Async` and `@Cacheable`:** also proxy-based, with the same self-invocation issue.

## Data access with JPA

- **Open in view:** `spring.jpa.open-in-view` defaults to `true`, keeping the persistence session open for the whole request. It hides lazy-loading problems, and runs queries during serialization outside your transaction, while holding a database connection longer. For APIs, set it to `false` and fetch deliberately. In an existing app, turning it off can surface `LazyInitializationException`s, so plan for that.
- **N+1:** relationships load lazily when touched. Use a fetch join, `@EntityGraph` or a projection, and check by logging or counting queries. Prefer lazy on all associations.
- **Projections and pagination:** read models via records or interfaces, and use `Pageable`. Joining a collection fetch with pagination happens in memory, so watch for it.
- **Queries:** derived names for simple ones, and `@Query` for the rest. Use bind parameters, never concatenation.
- **Entities:** `@Version` for optimistic locking; handle the failure. Dirty checking saves managed entities at commit, without `save()`. Careful with `equals` and `hashCode` based on generated IDs, and with bidirectional relations in `toString`.
- **Schema:** use Flyway or Liquibase. `spring.jpa.hibernate.ddl-auto` defaults to `create-drop` only for an embedded database with no schema manager, and otherwise to `none`. Never use `update`, `create` or `create-drop` against a real database. `validate` can help as a check.
- **Non-JPA options:** `JdbcClient` or jOOQ can suit read-heavy or SQL-centric work better.

## Calling other services and async

- **HTTP clients:** `RestClient` for blocking and `WebClient` for reactive; HTTP service interfaces for declarative clients. `RestTemplate` is being phased out, so don't use it in new code. Inject the auto-configured builder, which carries customization and observability, and **set connect and read timeouts**.
- **Virtual threads:** `spring.threads.virtual.enabled=true` requires Java 21 or later, and the documentation strongly recommends 24 or later because pinned threads can lower throughput. They suit blocking I/O, not CPU-heavy work, and you still must limit calls to a scarce resource such as a connection pool.
- **`@Async` and `@Scheduled`:** configure the executor, and handle exceptions, since an `@Async void` failure is otherwise only logged. Scheduled tasks run on every instance unless coordinated, for example with ShedLock.
- **Events:** `@TransactionalEventListener` runs after commit, and Spring Modulith offers an event publication registry for reliable delivery between modules.

## Security

- **Filter chain:** define a `SecurityFilterChain` bean, using the lambda DSL. `WebSecurityConfigurerAdapter` is gone, so don't copy old examples; Spring Boot's default chain backs off when you define one.
- **Deny by default:** end with `.anyRequest().authenticated()` or `denyAll()`, and open specific paths. Matcher order matters, and the first match wins.
- **Method security:** `@EnableMethodSecurity` with `@PreAuthorize`. Check access to the specific object, because URL rules can't see ownership. Proxy limits apply here too.
- **JWT resource server:** `oauth2ResourceServer` with `jwt`, configured with the issuer URI, so that signatures and claims are validated. Scopes map to `SCOPE_` authorities. Check the audience as well.
- **CSRF:** keep it on for cookie-based sessions. Disabling it is reasonable only for stateless token APIs, and should be a deliberate choice rather than a copied line.
- **Other:** `DelegatingPasswordEncoder` for passwords, narrow CORS, and test with `spring-security-test`.

## Testing

Choose the smallest slice that can fail for the right reason, because full contexts are slow.

| Need | Use |
|---|---|
| Business logic | Plain JUnit without Spring |
| Controller, binding, validation, errors, security rules | `@WebMvcTest` with `MockMvcTester` |
| Repositories and queries | `@DataJpaTest`, on the real database through Testcontainers |
| Whole flow | `@SpringBootTest`, with `RestTestClient` or `MockMvc` |
| Real dependencies | Testcontainers with `@ServiceConnection` |

- **Doubles:** `@MockitoBean` replaces the removed `@MockBean`. Each different bean override creates a new context, so overuse makes the suite slow.
- **H2 differs from your production database,** so it can pass queries that fail there.
- **Transactions:** `@Transactional` on a test rolls back, but it can also hide bugs: lazy loading works, and there's no real commit. It also doesn't apply across threads with a random-port server.
- **Modules changed in version 4:** each technology has a test starter, such as `spring-boot-starter-webmvc-test`, and imports differ from 3.x. `@MockitoBean` doesn't work in `@Configuration` classes. Check the documentation for the installed version.

## Operations

- **Actuator:** only `health` is exposed over HTTP by default. Expose others deliberately, and protect them: `env`, `heapdump` and `loggers` are sensitive. Avoid `exposure.include=*` in production. Use a separate management port if appropriate.
- **Probes:** liveness and readiness are at `/actuator/health/liveness` and `/readiness`. Don't add external dependencies to liveness.
- **Graceful shutdown:** set `spring.lifecycle.timeout-per-shutdown-phase`.
- **Observability:** Micrometer and OpenTelemetry. Log with SLF4J parameters: `log.info("order {}", id)`.
- **Packaging:** buildpacks or layered jars, with a non-root container.

## Common mistakes to look for

Field injection; `@Transactional` on private methods or called from the same class; a checked exception expected to roll back; returning JPA entities; open-in-view left on with lazy relations in DTO mapping; N+1 queries; `ddl-auto=update` in production; `RestTemplate` or a client without timeouts; `csrf.disable()` in a cookie session app; `permitAll` as the fall-through; `exposure.include=*`; `@Async` without an executor; H2 standing in for the production database; examples from Boot 2 used in Boot 4.
