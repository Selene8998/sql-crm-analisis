-- Pregunta: ¿cuántos clientes, cuántas ventas y cuánto se facturó en total?
SELECT COUNT(*) AS clientes FROM clientes;
SELECT COUNT(*) AS ventas, SUM(monto_total) AS facturacion FROM ventas;
