from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "Cuadra caja backend funcionando"}

class CorteCaja(BaseModel):
    fondo_inicial: float
    venta_total: float
    total_tarjeta: float
    otros_ingresos_efectivo: float
    gastos_efectivo: float
    gastos_tarjeta: float
    denominaciones: Dict[str, int]

@app.post("/corte-caja")
def crear_corte(corte: CorteCaja):

    efectivo_ventas = corte.venta_total - corte.total_tarjeta

    efectivo_contado = 0

    for value, amount in corte.denominaciones.items():
        efectivo_contado += int(value) * amount


    efectivo_esperado = (
                            corte.fondo_inicial + 
                            efectivo_ventas +
                            corte.otros_ingresos_efectivo -
                            corte.gastos_efectivo
                        )

    diff = efectivo_contado - efectivo_esperado

    return {
        "efectivo_ventas" : efectivo_ventas,
        "efectivo_contado" : efectivo_contado,
        "efectivo_esperado" : efectivo_esperado,
        "diff" : diff
    }