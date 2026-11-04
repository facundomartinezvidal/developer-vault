---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Revisá el diseño de este módulo TypeScript, no lo implementes. Es un monolito y las dependencias apuntan hacia las interfaces internas. No vamos a cambiar de base ni desplegar servicios nuevos. Importamos CSV de proveedores por HTTP y por un job nocturno. El proveedor confirmó que el próximo mes cambia el layout: agrega una columna al principio y pasa el importe de centavos enteros a decimal con moneda. Tenemos que poder mostrar qué filas se rechazaron por datos inválidos y continuar con las válidas.

Estas son las piezas actuales (esquema):

```ts
interface CsvReader { read(file: Uint8Array): string[][] }
interface RowWriter { insert(batchId: string, rows: ImportedRow[]): Promise<void> }
// insert hace commits por bloques de 100. Si falla un bloque, los anteriores quedan.
// No guarda un estado consultable por batchId ni impone unicidad por fila.
interface ImportedRow { externalId: string; amountMinor: number }

// Caller HTTP
const rows = reader.read(file);
const valid = rows.filter(r => r[0] && /^\d+$/.test(r[2]));
const entities = valid.map(r => ({ externalId: r[0], amountMinor: Number(r[2]) }));
await writer.insert(batchId, entities);
return { imported: entities.length };
// El middleware HTTP reintenta una vez si ve timeout.

// Caller job nocturno
const rows = reader.read(file);
const entities = rows.filter(r => r[0] && /^\d+$/.test(r[2]))
  .map(r => ({ externalId: r[0], amountMinor: Number(r[2]) }));
await writer.insert(batchId, entities);
// El job vuelve a ejecutar el archivo completo si falla.

// Wrapper del entrypoint HTTP, fuera del núcleo de importación
class AuthorizedImport {
  constructor(private access: Access, private inner: ImportPort) {}
  async run(actor: Actor, batch: Batch): Promise<ImportResult> {
    await this.access.require(actor, "supplier-import");
    return this.inner.run(actor, batch);
  }
}
```

Un compañero propone resolverlo poniendo los dos callers detrás de una interfaz genérica `execute<T>(input): Promise<T>` y fusionando `AuthorizedImport` con el importador porque tiene la misma firma. ¿Eso simplifica el diseño? Proponé una alternativa concreta con firma y ejemplo de uso. Qué cambiaría al llegar el nuevo CSV, qué prometería el resultado y qué harías con los reintentos. No necesito una plataforma extensible de importación.
