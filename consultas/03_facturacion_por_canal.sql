-- Pregunta: ¿cuánto factura cada canal y qué % del total representa?
SELECT canal,
       SUM(monto_total) AS facturacion,
       ROUND(SUM(monto_total) * 100.0 / (SELECT SUM(monto_total) FROM ventas), 1) AS porcentaje
FROM ventas
GROUP BY canal;
