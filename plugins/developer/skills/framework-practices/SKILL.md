---
name: framework-practices
description: "Applies current best practices of web and application frameworks, with deep guidance for ASP.NET Core and Spring Boot, and looks up the official documentation for the version installed. Use whenever code touches controllers, endpoints, dependency injection, configuration, EF Core, JPA or Hibernate, framework security, framework tests or startup, or someone asks how something should be done in a framework, even if they just say \"cómo se hace esto en Spring\" or \"esto está bien en .NET\". Also use for upgrades and for any other framework such as Django, Rails, Laravel, NestJS or Next.js. Covers \"cuál es la forma correcta en ASP.NET\", \"por qué esto rompe en Spring Boot\" and \"cómo configuro esto\". To turn an architect's design into framework code use implementing-designs; for general API contracts use api-design."
---

# Framework Practices

Use this skill to **write**, **review** or **upgrade** code that depends on a framework. Its point of view: the correct way depends on the framework's version and on the project's conventions, and most serious mistakes come from not knowing what the framework does by default. Work with the framework instead of building around it.

## Method

1. **Find the real version.** Read the build files (`*.csproj`, `global.json`, `pom.xml`, `build.gradle`, lockfiles), and note the framework, the language and the main libraries. Guidance differs a lot between versions.
2. **See how the project does it.** Follow its existing structure and libraries. A correct pattern that clashes with the rest of the code has a cost. Raise a change of convention separately instead of mixing it in.
3. **Read the matching reference** for ASP.NET Core or Spring Boot. Treat its version statements as a snapshot.
4. **Check the current documentation before relying on an API, default or annotation.** Use the Context7 MCP if it's available: resolve the library, then query one concept at a time for the installed version. Otherwise use the official documentation with web tools. If neither is available, say that the answer comes from memory and hasn't been checked. Official documentation and the installed source outrank books, references and memory.
5. **Prefer what the framework provides** for validation, errors, auth, configuration, HTTP clients and health checks. Add a library only if it pays for itself.
6. **Verify by running it:** build, tests, and the app itself when wiring or startup changed. Framework errors often appear only when the app starts or a request arrives.

## Context7 IDs that work

These were verified on 2026-11-04; resolve again if one fails, and append the version when available, as in `/websites/spring_io_spring-boot/4.0`.

| Framework | Library ID |
|---|---|
| ASP.NET Core docs | `/dotnet/aspnetcore.docs` |
| ASP.NET Core pitfalls (Fowler's guidance) | `/davidfowl/aspnetcorediagnosticscenarios` |
| EF Core | `/dotnet/entityframework.docs` |
| Spring Boot | `/websites/spring_io_spring-boot` |
| Spring Security | `/websites/spring_io_spring-security_reference` |
| Spring Modulith | `/spring-projects/spring-modulith` |

Send only the concept you're looking up. Don't put code, secrets or customer data in a query.

## What to check in any framework

Default behaviors that surprise people, object lifetimes and what's safe to share between requests, where the transaction starts and ends, how errors become responses, what's exposed without authentication, how configuration and secrets load, what runs at startup, and how tests replace dependencies. For another framework, answer these from its documentation, and give the answer in the same form.

## Upgrades

Read the official migration guide for each major version, and move one major version at a time. Removed or renamed packages and changed defaults are what break, and they can fail silently, so compare behavior as well as compilation. Check support dates: running an unsupported version means no security patches.

## Output

**Writing:** idiomatic code for that version, wired correctly, with tests in the framework's style. State the version you targeted, and what you checked in the documentation.

**Review:** findings most costly first, with `file:line`, the failure it causes under real conditions, and the framework's correct form. Separate defects from style and from what's merely outdated but still works.

**Advice:** the recommendation for this version, what the documentation says, and what changes in other versions.

## Reference files

| File | Read when the framework is… |
|---|---|
| `references/aspnet-core.md` | ASP.NET Core: minimal APIs and controllers, DI lifetimes, async pitfalls, EF Core, security, testing, operations |
| `references/spring-boot.md` | Spring Boot: structure, configuration, web, transactions, JPA, security, testing, Actuator |
