"""
Genera un dataset ficticio de un supermercado con programa de fidelidad.
Salida: crm_supermercado.db (SQLite) + carpeta csv/ con una tabla por archivo.
Todas las fechas son texto ISO (YYYY-MM-DD). "Hoy" del dataset: 2026-10-15.
"""
import csv
import os
import random
import sqlite3
from datetime import date, timedelta

random.seed(42)

HOY = date(2026, 10, 15)
INICIO = date(2025, 10, 15)          # primer día con ventas
N_CLIENTES = 2000
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(OUT_DIR, "crm_supermercado.db")
CSV_DIR = os.path.join(OUT_DIR, "csv")
os.makedirs(CSV_DIR, exist_ok=True)

# ---------------------------------------------------------------- sucursales
sucursales = [
    (1, "Martínez", "Zona Norte"),
    (2, "San Isidro", "Zona Norte"),
    (3, "Tigre", "Zona Norte"),
    (4, "San Fernando", "Zona Norte"),
    (5, "Belgrano", "CABA"),
    (6, "Palermo", "CABA"),
    (7, "Caballito", "CABA"),
    (8, "Online", "Online"),
]

# ----------------------------------------------------------------- productos
catalogo = {
    "Almacén": (["Fideos", "Arroz", "Aceite", "Harina", "Yerba", "Azúcar", "Galletitas", "Puré de tomate", "Lentejas"], (900, 4500)),
    "Bebidas": (["Gaseosa cola", "Agua mineral", "Jugo en polvo", "Cerveza", "Vino tinto", "Agua saborizada", "Soda"], (700, 6500)),
    "Lácteos": (["Leche entera", "Yogur", "Queso cremoso", "Manteca", "Dulce de leche", "Crema de leche", "Queso rallado"], (1000, 5500)),
    "Carnes": (["Asado", "Milanesa", "Pechuga de pollo", "Carne picada", "Chorizo", "Hamburguesas", "Bondiola"], (3500, 14000)),
    "Frutas y Verduras": (["Tomate", "Papa", "Banana", "Manzana", "Lechuga", "Cebolla", "Zanahoria", "Naranja"], (800, 3500)),
    "Limpieza": (["Detergente", "Lavandina", "Jabón en polvo", "Suavizante", "Limpiador de pisos", "Esponjas", "Papel higiénico"], (1100, 7500)),
    "Perfumería": (["Shampoo", "Acondicionador", "Jabón de tocador", "Desodorante", "Crema dental", "Cepillo dental"], (1300, 8500)),
    "Panadería": (["Pan lactal", "Facturas", "Pan de hamburguesa", "Tostadas", "Medialunas", "Budín"], (900, 4800)),
}
marcas = ["Campo Verde", "La Estancia", "Don Mateo", "Pura Vida", "Nativa", "Sol Dorado", "Del Valle Sur", "Casa Blanca"]

productos = []
pid = 1
for cat, (nombres, (pmin, pmax)) in catalogo.items():
    for n in nombres:
        precio = round(random.uniform(pmin, pmax), -1)
        productos.append((pid, f"{n}", cat, random.choice(marcas), precio))
        pid += 1

# ------------------------------------------------------------------ clientes
provincias = ["Buenos Aires", "CABA", "Santa Fe", "Córdoba", "Mendoza"]
prov_pesos = [55, 30, 6, 6, 3]

def rand_date(a, b):
    return a + timedelta(days=random.randint(0, (b - a).days))

clientes = []
for cid in range(1, N_CLIENTES + 1):
    alta = rand_date(date(2024, 1, 1), date(2026, 9, 30))
    canal_alta = random.choices(["tienda", "online"], [70, 30])[0]
    suc = 8 if canal_alta == "online" else random.randint(1, 7)
    nac = rand_date(date(1950, 1, 1), date(2006, 12, 31))
    prov = random.choices(provincias, prov_pesos)[0]
    if random.random() < 0.03:          # algunos datos faltantes, como en la vida real
        prov = None
    clientes.append([cid, alta, suc, canal_alta, nac, prov])

# ------------------------------------------------------------------- ventas
ventas = []          # (venta_id, cliente_id, fecha, sucursal_id, canal)
detalle = []         # (venta_id, producto_id, cantidad, precio_unitario)
venta_id = 0

def precio_en(fecha, base):
    meses = (fecha.year - INICIO.year) * 12 + fecha.month - INICIO.month
    return round(base * (1.03 ** meses), 2)       # inflación mensual de 3 %

def nueva_venta(cid, fecha, canal_alta):
    global venta_id
    venta_id += 1
    prob_online = 0.6 if canal_alta == "online" else 0.12
    canal = "online" if random.random() < prob_online else "tienda"
    suc = 8 if canal == "online" else random.randint(1, 7)
    ventas.append([venta_id, cid, fecha, suc, canal])
    for p in random.sample(productos, random.randint(2, 12)):
        detalle.append((venta_id, p[0], random.randint(1, 5), precio_en(fecha, p[4])))

# perfiles de frecuencia: promedio de días entre compras
gaps = [7, 14, 30, 60]
gaps_pesos = [10, 30, 40, 20]

churn = {}           # cliente_id -> fecha en que deja de comprar
for c in clientes:
    cid, alta, _, canal_alta, _, _ = c
    if random.random() < 0.35:
        churn[cid] = rand_date(max(alta, INICIO) + timedelta(days=15), HOY + timedelta(days=60))
    gap = random.choices(gaps, gaps_pesos)[0]
    actual = max(alta, INICIO) + timedelta(days=random.randint(0, gap))
    fin = min(churn.get(cid, HOY), HOY)
    while actual <= fin:
        nueva_venta(cid, actual, canal_alta)
        actual += timedelta(days=max(1, int(random.expovariate(1 / gap))))

# ------------------------------------------------------------------ campañas
campanas = [
    (1, "Cyber Navidad", "2025-12-01", "2025-12-07", "Todos"),
    (2, "Vuelta a clases", "2026-03-02", "2026-03-08", "Todos"),
    (3, "Reactivación Invierno", "2026-06-15", "2026-06-21", "Inactivos"),
    (4, "Día de la Primavera", "2026-09-21", "2026-09-27", "Todos"),
]
envios = []
ult_compra = {}
for v in ventas:
    ult_compra[v[1]] = max(ult_compra.get(v[1], date.min), v[2])

for camp_id, _, ini, _, segmento in campanas:
    f_envio = date.fromisoformat(ini)
    elegibles = [c for c in clientes if c[1] < f_envio]
    if segmento == "Inactivos":
        elegibles = [c for c in elegibles
                     if (f_envio - ult_compra.get(c[0], date.min)).days > 60]
    muestra = random.sample(elegibles, min(len(elegibles), 800))
    for c in muestra:
        abrio = 1 if random.random() < 0.35 else 0
        clic = 1 if abrio and random.random() < 0.30 else 0
        envios.append((camp_id, c[0], f_envio, abrio, clic))
        # efecto de la campaña: quien abre/clickea tiene más chance de comprar en los 14 días siguientes
        p_compra = 0.45 if clic else (0.28 if abrio else 0.08)
        if random.random() < p_compra:
            f_compra = f_envio + timedelta(days=random.randint(0, 14))
            if f_compra <= HOY:
                nueva_venta(c[0], f_compra, c[3])

ventas.sort(key=lambda v: (v[2], v[0]))

# totales de venta
total_por_venta = {}
for d in detalle:
    total_por_venta[d[0]] = total_por_venta.get(d[0], 0) + d[2] * d[3]

# ------------------------------------------------------------ escribir SQLite
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.executescript("""
CREATE TABLE sucursales(sucursal_id INTEGER PRIMARY KEY, nombre TEXT, zona TEXT);
CREATE TABLE clientes(cliente_id INTEGER PRIMARY KEY, fecha_alta TEXT, sucursal_alta INTEGER,
                      canal_alta TEXT, fecha_nacimiento TEXT, provincia TEXT);
CREATE TABLE productos(producto_id INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, marca TEXT, precio_lista REAL);
CREATE TABLE ventas(venta_id INTEGER PRIMARY KEY, cliente_id INTEGER, fecha TEXT, sucursal_id INTEGER,
                    canal TEXT, monto_total REAL);
CREATE TABLE detalle_ventas(venta_id INTEGER, producto_id INTEGER, cantidad INTEGER, precio_unitario REAL);
CREATE TABLE campanas(campana_id INTEGER PRIMARY KEY, nombre TEXT, fecha_inicio TEXT, fecha_fin TEXT, segmento TEXT);
CREATE TABLE envios_campana(campana_id INTEGER, cliente_id INTEGER, fecha_envio TEXT, abrio INTEGER, hizo_clic INTEGER);
""")

tablas = {
    "sucursales": (["sucursal_id", "nombre", "zona"], sucursales),
    "clientes": (["cliente_id", "fecha_alta", "sucursal_alta", "canal_alta", "fecha_nacimiento", "provincia"],
                 [[c[0], c[1].isoformat(), c[2], c[3], c[4].isoformat(), c[5]] for c in clientes]),
    "productos": (["producto_id", "nombre", "categoria", "marca", "precio_lista"], productos),
    "ventas": (["venta_id", "cliente_id", "fecha", "sucursal_id", "canal", "monto_total"],
               [[v[0], v[1], v[2].isoformat(), v[3], v[4], round(total_por_venta[v[0]], 2)] for v in ventas]),
    "detalle_ventas": (["venta_id", "producto_id", "cantidad", "precio_unitario"], detalle),
    "campanas": (["campana_id", "nombre", "fecha_inicio", "fecha_fin", "segmento"], campanas),
    "envios_campana": (["campana_id", "cliente_id", "fecha_envio", "abrio", "hizo_clic"],
                       [[e[0], e[1], e[2].isoformat(), e[3], e[4]] for e in envios]),
}

for nombre, (cols, filas) in tablas.items():
    marcadores = ",".join("?" * len(cols))
    cur.executemany(f"INSERT INTO {nombre}({','.join(cols)}) VALUES ({marcadores})", filas)
    with open(os.path.join(CSV_DIR, f"{nombre}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(filas)

cur.executescript("""
CREATE INDEX ix_ventas_cliente ON ventas(cliente_id);
CREATE INDEX ix_ventas_fecha ON ventas(fecha);
CREATE INDEX ix_detalle_venta ON detalle_ventas(venta_id);
CREATE INDEX ix_envios_cliente ON envios_campana(cliente_id);
""")
con.commit()

for t in tablas:
    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t:16s} {n:>8,d} filas")
con.close()
