# Enrutamiento de skills — 2026-11-07

**Pregunta:** ¿recortar las descripciones a 300 caracteres y sacar del listado las skills de rol empeora la elección de skill?

**Cómo se midió:** un subagente enrutador por corrida recibió solo el listado (nombre y descripción) y los 33 pedidos de `definition.json`, y eligió una skill o `none` por pedido. A: descripciones de `main` (`baseline-descriptions.json`) más las skills de rol, 25 skills y 16.484 caracteres. B: descripciones recortadas, sin skills de rol, 21 skills y 5.869 caracteres. Dos corridas por variante. Puntaje determinista contra `accept`.

| Corrida | Típicos | Vecinos | Negativos |
|---|---|---|---|
| A1, A2 | 21/21 | 6/6 | 6/6 |
| B1, B2 | 21/21 | 6/6 | 6/6 |

**Conclusión:** en estos pedidos, el recorte no empeoró la elección (pass^2 = 1 en ambas variantes). Como las dos aciertan todo, el conjunto no distingue diferencias finas. Tampoco mide el beneficio buscado: que las descripciones no se descarten cuando el listado real, con otros plugins, supera su presupuesto. Elecciones completas en `results.json`.

**Límites:** el enrutador vio solo estas skills, no el listado completo de Claude Code; un modelo; pedidos escritos por quien diseñó el cambio.
