---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tenemos un monolito para alquiler de equipos industriales, mantenido por un equipo de seis personas. Queremos ordenar el modelo antes de decidir si extraer servicios. El arquitecto anterior propuso un contexto por sustantivo: Cliente, Equipo, Contrato y Factura.

En las entrevistas apareció esto: para quien cotiza, un equipo es una categoría con capacidad y tarifa; para quien entrega, es una unidad con número de serie, inspecciones y disponibilidad. Una reserva promete capacidad de una categoría, pero recién al preparar la entrega se asignan las unidades. Un contrato puede cubrir varias entregas. Facturación debe conservar los datos fiscales y precios acordados aunque luego cambien en el CRM o en el tarifario. El equipo comercial dice "cliente" para el grupo empresario y cobranzas para cada razón social deudora. El CRM lo maneja otra empresa y no podemos pedirle cambios; sus estados son lead/active/inactive. Nuestro negocio necesita distinguir habilitación comercial y bloqueo por deuda. No tenemos evidencia de que cada diferencia requiera un equipo o despliegue propio.

Revisá la propuesta y recomendá límites y relaciones. Mostrá cómo representarías la información que cruza los límites, qué conservarías junto por ahora y qué preguntas podrían cambiar tu decisión. No necesito clases ni estructura de carpetas todavía.
