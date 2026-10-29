-- Clientes que nunca compraron (LEFT JOIN)
SELECT COUNT(*) AS clientes_sin_compras
FROM clientes
LEFT JOIN ventas ON clientes.cliente_id = ventas.cliente_id
WHERE ventas.venta_id IS NULL;

-- Clientes que compraron una sola vez (HAVING)
SELECT cliente_id, COUNT(*) AS compras
FROM ventas
GROUP BY cliente_id
HAVING COUNT(*) = 1;
