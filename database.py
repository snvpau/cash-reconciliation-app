import sqlite3

db_name = "corte_caja.db"

def create_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cortes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fondo_inicial REAL,
            venta_total REAL,
            total_tarjeta REAL,
            otros_ingresos_efectivo REAL,
            gastos_efectivo REAL,
            gastos_tarjeta REAL,
            denominaciones TEXT,
            efectivo_ventas REAL,
            efectivo_contado REAL,
            efectivo_esperado REAL,
            diff REAL,
            utilidad REAL,
            estado TEXT,
            mensaje TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_corte(corte, resultados):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO cortes (
            fondo_inicial,
            venta_total,
            total_tarjeta,
            otros_ingresos_efectivo,
            gastos_efectivo,
            gastos_tarjeta,
            efectivo_ventas,
            efectivo_contado,
            efectivo_esperado,
            diff,
            utilidad,
            estado,
            mensaje
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        corte.fondo_inicial,
        corte.venta_total,
        corte.total_tarjeta,
        corte.otros_ingresos_efectivo,
        corte.gastos_efectivo,
        corte.gastos_tarjeta,
        resultados["efectivo_ventas"],
        resultados["efectivo_contado"],
        resultados["efectivo_esperado"],
        resultados["diff"],
        resultados["utilidad"],
        resultados["estado"],
        resultados["mensaje"]
    ))

    conn.commit()
    conn.close()

def get_cortes():

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT fecha, venta_total, utilidad, diff, estado
        FROM cortes
        ORDER BY fecha DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    cortes = []
    for row in rows:
        cortes.append({
            "fecha": row[0],
            "venta_total": row[1],
            "utilidad": row[2],
            "diff": row[3],
            "estado": row[4]
        })

    return cortes

def get_total_utilidad():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(utilidad) FROM cortes
    """)

    result = cursor.fetchone()
    total_utilidad = result[0] if result[0] is not None else 0
    
    conn.close()

    return total_utilidad 

def get_utilidad_mensual():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(utilidad) 
        FROM cortes 
        WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
    """)

    result = cursor.fetchone()
    total = result[0] if result[0] is not None else 0

    conn.close()
    return total