# Traspaso de operación — producción

Confirmado por la operadora saliente el 2026-11-02:

- Facturación incluye API y worker, que siguen desplegados por separado.
- La API guarda facturas en el esquema billing de un RDS PostgreSQL gestionado. El equipo de Facturación controla ese esquema y sus migraciones; no controla todo el servidor.
- API publica trabajo en una cola gestionada y worker lo consume. No se adjunta la configuración de producción: nombre de producto, protocolo y reintentos pendientes de confirmar. El transporte local no prueba el de producción.
- Worker guarda PDFs en el bucket billing-archive de S3, del que el equipo controla acceso y ciclo de vida.
- legacy-export sigue ejecutándose cada noche por un scheduler corporativo externo al repositorio. Lee el esquema billing y envía un archivo al ERP corporativo por SFTP.
- No se confirmó región, cantidad de réplicas ni qué entrada pública expone la API.
