---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Quiero explicarle a una dev nueva estas relaciones del modelo, con un diagrama de clases Mermaid y unas pocas líneas. No necesito un mapa de servicios. Un Pedido tiene una o más LineasPedido; las líneas se crean y eliminan dentro del pedido y no viven por separado. Cada línea conserva cantidad y precioAcordado de tipo Dinero (importe y moneda). Guarda el productoId del catálogo, sin poseer al Producto. El Cliente existe independientemente del Pedido y se referencia por clienteId. Un Pedido puede confirmarse y una línea de un pedido confirmado no puede modificarse. El modelo está acordado; no inventes repositorios ni herencia ni detalles de base de datos.
