-- Pregunta: ¿cómo evolucionan las ventas y el ticket promedio mes a mes?
SELECT strftime('%Y-%m', fecha) AS mes,
       COUNT(*) AS ventas,
       ROUND(AVG(monto_total), 2) AS ticket_promedio
FROM ventas
GROUP BY mes
ORDER BY mes;
