---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

El martes le tengo que explicar a gerencia general cómo encaja nuestra plataforma de pagos. No son técnicos. Es así: los comercios usan un panel web de React, hay una API en Go sobre Kubernetes, Postgres con réplicas, Kafka para eventos, y un worker que concilia. Hablamos con Visa y Mastercard a través de un procesador que se llama Prisma, facturamos con AFIP y mandamos los extractos a un banco por SFTP. Armame el diagrama.
