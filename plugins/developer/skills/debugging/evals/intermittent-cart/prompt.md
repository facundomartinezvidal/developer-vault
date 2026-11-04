---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

test_cart.py falla a veces según cómo los corra: `python3 -m unittest test_cart.CartTest.test_empty_total` pasa solo, pero `python3 -m unittest test_cart` falla. Arreglalo.

Input files: cart.py, test_cart.py
