---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Revisá este diseño de un bot interno de Slack antes del piloto. Solo son 30 personas y quiero una respuesta breve: ¿ves algo que bloquee salir o controles que deba comprobar? No quiero un proyecto de seguridad. No hay código ni resultados de pruebas adjuntos: lo siguiente describe el diseño acordado.

El comando /cliente <email> consulta únicamente plan y fecha del último pago; no muestra nombre, tarjeta, monto ni documentos. El endpoint de Lambda es público porque Slack lo llama. Antes de leer parámetros se valida la firma de Slack sobre el cuerpo crudo y una ventana de timestamp de cinco minutos; el secreto vive en el gestor de secretos. También se exige el workspace esperado y pertenencia a un grupo explícito de soporte, resuelta del lado servidor. Esas personas tienen autorización de negocio para consultar todos los clientes. No se toman permisos de campos que mande el usuario.

La consulta SQL usa parámetros y un usuario de réplica de solo lectura autorizado a una vista con email, plan y fecha. La respuesta es ephemeral al solicitante, nunca se publica en el canal. La función no hace fetch de URLs, no procesa archivos ni ejecuta contenido del usuario. Tiene límites de tamaño de entrada, timeout y cuota por usuario. En logs solo se guarda ID del actor, identificador opaco del cliente, resultado de la consulta y fecha: no email, cuerpo del comando ni secreto. El acceso a esos logs está limitado y su retención tiene plazo definido. No hay panel admin ni credenciales compartidas.

No asumas que esas medidas ya se probaron: todavía tenemos que verificar la implementación. Podés cuestionar una medida concreta si explicás el camino que deja abierto, pero no quiero una lista de riesgos genéricos.
