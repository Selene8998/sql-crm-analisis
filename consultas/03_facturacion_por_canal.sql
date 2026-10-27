-- Pregunta: ¿cuánto se factura en tienda vs online?
SELECT canal, COUNT(*) AS ventas, SUM(monto_total) AS facturacion
FROM ventas
GROUP BY canal;
-- Pendiente: sumar el % del total por canal.
