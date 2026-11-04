---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tenemos un monolito Rails con Postgres, 4 devs, ninguno con experiencia en operar brokers. Hoy mandamos mails y webhooks a clientes dentro del request y cuando un cliente tarda se nos cae el checkout. Son unos 20 mil eventos por día, con picos en Black Friday de quizás 10x. Un dev quiere meter Kafka porque "es el estándar y nos va a servir para microservicios más adelante", otro dice RabbitMQ. Ayudame a decidir y dejá la decisión escrita para que el equipo la revise.
