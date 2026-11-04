# Concurrent code

Keeping concurrent code correct: shared state, ordering, and message passing.

## Contents

- [Concurrency Defense Principles](#concurrency-defense-principles)
- [Shared State Is Incorrect State](#shared-state-is-incorrect-state)
- [Breaking Temporal Coupling](#breaking-temporal-coupling)
- [Actors and Processes](#actors-and-processes)

## Concurrency Defense Principles


**Source:** *Clean Code*, Chapter 13 and Appendix A (Brett L. Schuchert).

### What it means in practice

Concurrency is hard, and the myths make it worse: it doesn't always improve performance, it *does* change the design, and you *do* need to understand the container's threading model. Schuchert's defenses:

- **SRP.** Keep concurrency code separate from other code, because concurrent code has its own lifecycle and its own ways of failing.
- **Limit the scope of shared data.** Encapsulate it and keep the number of `synchronized` places small.
- **Use copies of data** instead of sharing it, and merge the results at the end.
- **Threads should be as independent as possible.** Ideally each thread handles one request with no shared state.
- **Know your library** (thread-safe collections, executors, nonblocking structures) and the classic models (producer-consumer, readers-writers, dining philosophers).
- **Beware dependencies between synchronized methods.** Keep synchronized sections small, and plan shutdown early, because shutdown is where deadlocks hide.
- **Testing:** treat random failures as candidate threading problems. Get the non-threaded code working first, then make threading pluggable and tunable. Run with more threads than cores and on different platforms. Instrument the code to force different interleavings.

### Example

```java
// Shared mutable counter: every request thread contends, and bugs hide in the gaps
class RateLimiter { private final Map<String,Integer> hits = new HashMap<>(); synchronized boolean allow(String ip) { ... } }

// Limit scope + use the library: one thread-safe structure, no hand-written locking
class RateLimiter {
    private final ConcurrentHashMap<String, AtomicInteger> hits = new ConcurrentHashMap<>();
    boolean allow(String ip) { return hits.computeIfAbsent(ip, k -> new AtomicInteger()).incrementAndGet() <= LIMIT; }
}
```

### Where it applies

- Shared State Is Incorrect State — Hunt & Thomas's version of "limit the scope of data", with semaphores and transactional resources.
- Actors and Processes — "threads as independent as possible" taken to the limit: no shared state at all.
- functional programming — Martin argues immutability removes most concurrency problems.

### Related

- Breaking Temporal Coupling
- SRP: Single Responsibility Principle (`objects-and-classes.md`)
- Hidden Temporal Coupling (`names-and-functions.md`)
- Design by Contract (`errors-and-boundaries.md`)

## Shared State Is Incorrect State


**Source:** *The Pragmatic Programmer*, Topic 34 (also Tip 58).

### What it means in practice

Hunt & Thomas's example is two waiters in a diner. Each checks that there's one slice of pie left in the case, and each promises it to a customer. The problem is that "read, decide, write" isn't **atomic**. Any resource that two concurrent things can change has this problem: memory, a file, a database row, an external API.

The fixes, from crude to clean:
- **Semaphores and mutexes.** They work, but every user has to remember the protocol.
- **Make the resource transactional.** Move the locking *inside* the resource so callers can't get it wrong (`pieCase.takeSlice()` either succeeds or fails, all at once). This is Tell, Don't Ask (`objects-and-classes.md`) applied to concurrency.
- **Multiple resources** mean deadlock risk. Acquire them in a consistent order, or redesign so you don't need to hold several at once.
- **Non-transactional updates** still need the same care: files, databases and external services all count as shared state.

Better still, avoid sharing state at all (Actors and Processes).

### Example

```java
// Check-then-act race: two requests both see 1 seat left and both book it
if (flight.availableSeats() > 0) { flight.setAvailableSeats(flight.availableSeats() - 1); bookings.save(...); }

// The resource guards itself: one atomic operation, success or failure
int updated = jdbc.update("UPDATE flights SET seats = seats - 1 WHERE id = ? AND seats > 0", flightId);
if (updated == 0) throw new SoldOutException(flightId);
```

### Related

- Concurrency Defense Principles — Clean Code's "limit the scope of data" and "use copies".
- Actors and Processes
- Tell, Don't Ask (`objects-and-classes.md`)
- Breaking Temporal Coupling
- Finish What You Start (Balancing Resources) (`errors-and-boundaries.md`)

## Breaking Temporal Coupling


**Source:** *The Pragmatic Programmer*, Topic 33.

### What it means in practice

Time has two aspects that matter here: **concurrency** (things happening at the same time) and **ordering** (where things happen relative to each other). Most code is written as if everything happens in sequence, one step after another, because that's how programming languages read. That *temporal coupling* is often accidental. The real requirement says "A and B must both finish before C", not "A, then B, then C".

The tool Hunt & Thomas recommend is an **activity diagram**. Draw every action, draw an arrow only where one action truly depends on another, and add synchronization bars where several must finish before the next can start. Whatever has no arrow between it can run in parallel. Their example is making a piña colada: blending has to wait for everything else, but opening the mix, measuring the rum and adding ice can all happen together.

### Example

Order fulfilment, written sequentially by habit:

```java
reserveStock(order);
chargeCard(order);       // doesn't need the stock reservation
sendConfirmation(order); // needs both
```

After drawing the real dependencies:

```java
CompletableFuture<Void> stock  = runAsync(() -> reserveStock(order));
CompletableFuture<Void> charge = runAsync(() -> chargeCard(order));
allOf(stock, charge).thenRun(() -> sendConfirmation(order));   // synchronization bar
```

### Related

- Hidden Temporal Coupling (`names-and-functions.md`) — Clean Code's G31, about the same coupling at the level of method calls: when order matters, make it explicit in the data flow.
- Concurrency Defense Principles
- Shared State Is Incorrect State — parallel steps must not share mutable state.

## Actors and Processes


**Source:** *The Pragmatic Programmer*, Topic 35.

### What it means in practice

An **actor** is an independent unit of execution with private state and a mailbox. It processes one message at a time. In response, it can send messages to other actors it knows, create new actors, and change its own state. There's no shared memory and no locks. The only way to affect an actor is to send it a message.

Since only the actor itself ever touches its state, the shared-state problem can't happen. Actors communicate asynchronously and there's no central coordinator, so a system built this way scales from threads to processes to machines without changing the model. Erlang/Elixir processes are the standard example, and Akka brings the model to the JVM.

### Example

```java
// The diner's pie case as an actor: concurrent requests are serialized through one mailbox
class SeatInventory extends AbstractBehavior<Command> {
    private int seatsLeft;
    public Receive<Command> createReceive() {
        return newReceiveBuilder()
            .onMessage(Reserve.class, r -> {
                if (seatsLeft > 0) { seatsLeft--; r.replyTo().tell(new Reserved(r.bookingId())); }
                else r.replyTo().tell(new SoldOut(r.bookingId()));
                return this;
            }).build();
    }
}
```

### Related

- Shared State Is Incorrect State
- Concurrency Defense Principles — keep threads independent, taken to the limit.
- Crash Early (Dead Programs Tell No Lies) (`errors-and-boundaries.md`)
