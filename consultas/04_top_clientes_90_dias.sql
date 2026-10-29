SELECT ventas.cliente_id, clientes.provincia, SUM(ventas.monto_total) AS gastado
FROM ventas
JOIN clientes ON ventas.cliente_id = clientes.cliente_id
WHERE ventas.fecha >= date('2026-10-15', '-90 days')
GROUP BY ventas.cliente_id, clientes.provincia
ORDER BY gastado DESC
LIMIT 10;
