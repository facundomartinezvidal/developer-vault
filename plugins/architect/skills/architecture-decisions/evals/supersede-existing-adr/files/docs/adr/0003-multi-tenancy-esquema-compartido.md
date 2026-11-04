# 3. Multi-tenancy con esquema compartido

Fecha: 2023-06-02

## Estado

Aceptada

## Contexto

Somos un SaaS de gestión de RRHH con 40 clientes pyme. Somos 5 devs y queremos un solo despliegue.

## Decisión

Vamos a usar una sola base Postgres y un solo esquema, con una columna `tenant_id` en cada tabla y Row Level Security.

## Consecuencias

Operación y migraciones simples. Un cliente ruidoso afecta a los demás. No podemos ofrecer aislamiento físico de datos.
