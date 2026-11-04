# Debugging method

How to find the real cause, avoid working by luck, and get unstuck.

## Contents

- [Debugging](#debugging)
- [Programming by Coincidence](#programming-by-coincidence)
- [Solving Impossible Puzzles](#solving-impossible-puzzles)
- [Engineering Daybook](#engineering-daybook)
- [Power Tools (Shell, Editor, Text Manipulation)](#power-tools-shell-editor-text-manipulation)

## Debugging


**Source:** *The Pragmatic Programmer*, Topic 20 (Tips 29–34).

### What it means in practice

Debugging is problem solving. Treat it that way, not as finding someone to blame. The mindset and tactics:

- **Don't panic.** Turn off your ego and step back. Don't assume "that can't happen": it just did.
- **Reproduce it first.** **Failing test before fixing code** (Tip 31). If you can't reproduce the bug with a single command, you don't understand it yet.
- **Read the damn error message** (Tip 32).
- **Bad results:** get the data that triggered the bug and use it to drive the investigation. Use the debugger and visualize state.
- **Binary chop** through the input, the stack trace, or the release history (`git bisect`).
- **Logging and tracing** work over time and across processes, where a debugger can't follow.
- **Rubber ducking.** Explain the code line by line to someone else, or to a duck. Saying it aloud reveals your assumptions.
- **Process of elimination.** "`select` isn't broken" (Tip 33): suspect your own code before the OS, the compiler or the library.
- **Don't assume it, prove it** (Tip 34).
- Afterwards: why wasn't it caught earlier? Fix the tests. Are there other copies of the same bug? Is it a symptom of a broken window?

### Example

A customer is charged twice "sometimes". Reproduce it: a test fires two concurrent `POST /checkout` requests and gets two charges. Root cause: no idempotency key, a classic check-then-act race (`failure-sources.md`). Fix it, keep the test, and look for other endpoints with the same pattern.

### Related

- Crash Early (Dead Programs Tell No Lies) (`failure-sources.md`) — a clear crash close to the cause is the easiest bug to debug.
- Assertive Programming (`failure-sources.md`)
- Programming by Coincidence — "it works and I don't know why" is a bug that hasn't shown up yet.
- Concurrency Defense Principles (`failure-sources.md`) — suspect threading when failures look random.
- Power Tools (Shell, Editor, Text Manipulation)
- Engineering Daybook

## Programming by Coincidence


**Source:** *The Pragmatic Programmer*, Topic 38.

### What it means in practice

The book compares this to a soldier walking across a minefield: each step that doesn't explode makes them more confident, until one does. Code that works without the programmer knowing *why* is code that works by luck. Common kinds of coincidence:

- **Accidents of implementation.** Relying on undocumented behavior, call order, or a bug that happens to cancel another bug.
- **Accidents of context.** Assuming a timezone, a locale, a GUI, an English-speaking user, a writable disk.
- **Phantom patterns.** "It fails on Tuesdays", when it really fails when the batch is over 1,000 items.
- **Implicit assumptions.** Assumptions that were never written down or tested.

**Program deliberately:** always know what you're doing, and don't code blindfolded in technology or a domain you don't understand. Proceed from a plan, rely only on reliable things, document assumptions (contracts (`failure-sources.md`) and assertions (`failure-sources.md`)), test the assumptions as well as the code, prioritize the important parts, and don't be a slave to history. If existing code no longer fits, refactor it.

### Example

```java
// Works by coincidence: HashMap iteration order happened to match insertion in tests
Map<String, LineItem> items = new HashMap<>();
renderInvoice(items.values());                // lines print in a "random" order in production

// Deliberate: the order is a requirement, so make it explicit
Map<String, LineItem> items = new LinkedHashMap<>();
```

### Related

- Assertive Programming (`failure-sources.md`) and Design by Contract (`failure-sources.md`) — turn assumptions into checks.
- Debugging — "don't assume it, prove it".
- Shared State Is Incorrect State (`failure-sources.md`) — code that works only because of lucky timing.

## Solving Impossible Puzzles


**Source:** *The Pragmatic Programmer*, Topic 46.

### What it means in practice

When a problem seems impossible, the trick is usually that you're assuming a constraint that isn't real. The book's example is the Gordian knot, which Alexander "solved" by cutting it. So:

- **List every constraint** and question each one. Which are *real* (regulatory, physical, contractual) and which are just preconceptions?
- The box isn't something to think outside of. The real constraints *are* the box. Find its real edges and solve within them.
- **Get out of your own way.** Walk away, work on something else, sleep on it, explain it to someone else.
- **Fortune favors the prepared mind**: a deep and broad knowledge portfolio gives you more ideas to draw on.
- Ask: is there an easier way? Are you solving the right problem? Why is this a problem at all? Does it have to be done this way? Does it have to be done at all?

### Example

"We need real-time sync of 50M records between two databases, and the vendor's API allows 100 req/min." After listing the constraints, the real need turns out to be that the dashboard shows yesterday's totals. A nightly aggregated export removes the impossible part.


## Engineering Daybook


**Source:** *The Pragmatic Programmer*, Topic 22.

### What it means in practice

Keep a running, dated log of your work: what you did, what you learned, ideas, measurements (gauge readings, timings), decisions and why you made them, sketches, and questions to follow up. Hunt & Thomas give three benefits:

1. **More reliable than memory.** "What was the name of that company?" "What was the setting we changed last week?"
2. **A parking lot for ideas** that aren't relevant to the current task, so you can stay focused.
3. **A rubber duck.** Writing something down makes you stop and think about it, and often you find the answer.

They recommend paper, because writing by hand is different from typing, but any format you'll actually use works.

### Example

```
2026-10-30 — Invoice export
- p95 export time 41s → 6s after switching to streaming writer (benchmark: 10k invoices)
- Decided NOT to cache tax rates: rates change mid-month for 3 countries; revisit if DB load > 60%
- Idea (parking lot): validate CSV schema before import → ticket?
```

### Related

- Debugging — rubber ducking on paper.

## Power Tools (Shell, Editor, Text Manipulation)


**Source:** *The Pragmatic Programmer*, Topics 17, 18 and 21.

### What it means in practice

A woodworker's skill shows in how they use their tools. Hunt & Thomas name three tools worth mastering:

- **The shell.** GUIs are limited to what their designers anticipated. The shell lets you combine tools in ways nobody planned: automate a sequence, run it on 1,000 files, or chain it into a pipeline. Customize your shell (aliases, prompt, completion) and make it comfortable.
- **The editor.** Fluency means not thinking about the editor. Learn to move and select by word, line and block, use multiple cursors, and use refactoring commands without reaching for the mouse. To build the habit, notice every repetitive thing you do and learn a better way to do it.
- **A text manipulation language** (Python, Ruby, awk/sed, jq). Use it to generate code, migrate data, write one-off reports, and glue systems together. The book itself was built this way.

### Example

```bash
# Which endpoints threw the most 5xx errors yesterday? Composable tools, no GUI anticipated this query
zcat access-2026-10-29.log.gz | jq -r 'select(.status >= 500) | .route' | sort | uniq -c | sort -rn | head
```

### Related

- Debugging
