SELECT cliente_id, SUM(monto_total) AS gastado
FROM ventas
WHERE fecha >= date('2026-10-15', '-90 days')
GROUP BY cliente_id
ORDER BY gastado DESC
LIMIT 10;
