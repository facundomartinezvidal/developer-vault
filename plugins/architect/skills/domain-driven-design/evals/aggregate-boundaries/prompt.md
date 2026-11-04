---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tengo un sistema de pedidos B2B en TypeScript. Hoy cuando se confirma un pedido abro una transacción que actualiza el Order, sus OrderLines, descuenta el stock de cada Product y actualiza el crédito disponible del Customer. En horario pico tengo deadlocks y timeouts por todos lados, sobre todo con productos populares. Reglas de negocio: el total del pedido no puede pasar el límite de crédito del cliente; no se puede cambiar una línea de un pedido ya confirmado; idealmente no sobrevender, pero el comercial me dijo que si se sobrevende un poco se resuelve por teléfono con el cliente. ¿Cómo lo modelo?
