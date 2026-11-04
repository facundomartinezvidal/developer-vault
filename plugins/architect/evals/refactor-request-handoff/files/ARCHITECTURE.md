# Principios acordados — aceptados

- La política de precios es pura: sin lectura de repositorios, ORM ni transporte. La aplicación carga datos e invoca el cálculo.
- Todo importe está en centavos enteros. El descuento es subtotal * porcentaje // 100 (redondeo hacia abajo del descuento). No cambiar ese contrato.
- Conservar la API pública billing.quote(items, coupon_code, repository) y las claves del resultado.
- No agregar frameworks, dependencias ni servicios nuevos para este refactor.
