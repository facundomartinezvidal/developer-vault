---
name: user-interfaces
description: "Builds and reviews screens and components on any front-end stack. Use for pages, forms, tables, modals, client state and UI bugs, including loading, empty and error states, accessibility and responsive layout (\"armame esta pantalla\", \"el formulario no anda\")."
---

# User Interfaces

Use this skill to **build**, **review** or **fix** user interfaces. Its point of view: users experience all the states of a screen, not only the one in the mockup. And passing tests or types doesn't prove a UI works, so look at it running.

## Before you build

Read how the project does it: its component library, design tokens, state management, routing and data fetching. Reuse existing components, because a new button with a slightly different look adds debt. Check the current documentation for the framework's installed version, since this area moves quickly.

## What to cover

- **Every state:** loading, empty, error, partial data, success and very long content. Consider slow networks and repeated clicks.
- **Forms:** real labels, inline validation with clear messages, server errors shown beside the field, input preserved on failure, double-submit prevention, and the right input types. Client validation is for convenience; the server still has to validate.
- **Accessibility:** use semantic elements before ARIA. Everything works by keyboard, with visible focus and a logical order. Images and icon buttons have text alternatives. Check contrast, and don't rely on color alone. Dialogs manage focus. Dynamic changes are announced. Target WCAG 2.2 AA as a baseline unless told otherwise. Automated checks such as axe catch only part of these issues.
- **Layout:** works at small and large sizes, with zoom and long translated text. Follow the platform's conventions on mobile, including touch target sizes and safe areas.
- **State:** keep it as local as possible, derive rather than duplicate, and keep server data in the data-fetching layer. Put what should survive a reload or link in the URL. Handle stale responses and races when requests overlap.
- **Security:** escape by default, keep tokens out of reach of scripts when possible, and treat client checks as cosmetic. See `secure-coding`.
- **Performance:** size the bundle, split large routes, avoid needless re-renders, virtualize long lists, and optimize images. Measure with the browser's tools and Core Web Vitals before optimizing.
- **Text:** use the project's i18n setup rather than hard-coding strings, and format dates, numbers and currency by locale.

## Verifying

Run it and use the feature: the normal path, an error, and a narrow window. Use a browser or simulator tool if you have one, with screenshots as evidence; check the console and network for errors. If you can't run it, say so plainly. "It compiles" isn't "it works". Add tests through what the user sees, such as roles and labels rather than CSS classes. Use end-to-end tests for critical journeys, and be careful with snapshot tests, which get approved without being read.

## Output

**Build:** the working UI in the project's style, what you exercised and how it looked, and states you assumed. Raise decisions that are the designer's or product's, such as wording or an empty-state message.

**Review:** findings by user impact, with `file:line`: what breaks for whom, then accessibility, then the rest.
