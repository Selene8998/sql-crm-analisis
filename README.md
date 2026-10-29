# Análisis CRM de un programa de fidelidad (SQL)

Proyecto de práctica en SQL sobre un supermercado con programa de fidelidad: ¿quiénes son los mejores clientes, cuántos se están yendo y si las campañas de mail funcionan?

> **Los datos son ficticios**, generados con un script (`datos/generar_dataset.py`). Sirven para practicar las consultas típicas de CRM, no representan a ninguna empresa real.

## Los datos

| Tabla | Qué guarda |
|---|---|
| `clientes` | alta, canal de alta, provincia, fecha de nacimiento |
| `ventas` | una fila por compra: cliente, fecha, sucursal, canal, monto |
| `detalle_ventas` | productos de cada compra |
| `productos`, `sucursales` | catálogos |
| `campanas`, `envios_campana` | campañas de mail y si cada cliente abrió o hizo clic |

Volumen: 2.000 clientes, 28.602 ventas entre octubre 2025 y octubre 2026. Motor: SQLite (consultado desde DBeaver).

## Limpieza de datos

Antes de analizar, revisé la calidad de la tabla `clientes` (2.000 filas):

- **Valores vacíos:** comparé `COUNT(*)` con `COUNT(columna)` para cada columna. Solo `provincia` tiene faltantes: **65 clientes (3,25 %)** con valor `NULL`. El resto de las columnas está completo.
- **Decisión:** los clientes sin provincia se mantienen en el análisis y se agrupan como "Sin dato" cuando se compara por provincia.
- [x] Revisar duplicados en `clientes`.
- [x] Revisar valores vacíos y rangos de fechas y montos en `ventas`.

## Preguntas de negocio y consultas

| # | Pregunta | Técnica | Archivo |
|---|---|---|---|
| 1 | ¿Cuántos clientes, ventas y facturación total? | COUNT, SUM | `consultas/01_resumen_general.sql` |
| 2 | ¿Cómo evolucionan ventas y ticket promedio por mes? | GROUP BY, strftime | `consultas/02_ventas_y_ticket_por_mes.sql` |
| 3 | ¿Tienda u online? | GROUP BY | `consultas/03_facturacion_por_canal.sql` |
| 4 | Top clientes de los últimos 90 días | JOIN, ORDER BY, LIMIT | `consultas/04_...` |
| 5 | Clientes de una sola compra / que nunca compraron |
