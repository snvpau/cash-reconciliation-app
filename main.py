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

    from fastapi import HTTPException

    if corte.total_tarjeta > corte.venta_total:
            raise HTTPException(status_code = 400, detail = "Total tarjeta no puede ser mayor que venta total")
    
    if (
        corte.fondo_inicial < 0 or
        corte.venta_total < 0 or
        corte.total_tarjeta < 0 or
        corte.otros_ingresos_efectivo < 0 or
        corte.gastos_efectivo < 0 or
        corte.gastos_tarjeta < 0
    ):

        raise HTTPException(status_code=400, detail = "Los montos no pueden ser negativos.")

    for value, amount in corte.denominaciones.items():
        if amount < 0:
            raise HTTPException(status_code=400, detail = "Las denominaciones no pueden ser negativas.")


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

    utilidad = corte.venta_total - (corte.gastos_efectivo + corte.gastos_tarjeta)

    if diff == 0:
        estado = "Cuadra"
    elif diff < 0:
        estado = "Faltante"
    else:
        estado = "Sobrante"

    if estado == "Cuadra":
        mensaje = "El corte cuadra correctamente."
    elif estado == "Faltante":
        mensaje = f"Hay un faltante de ${abs(diff)} en caja"
    else:
        mensaje = f"Hay un sobrante de ${abs(diff)} en caja"

    return {
        "efectivo_ventas": efectivo_ventas,
        "efectivo_contado": efectivo_contado,
        "efectivo_esperado": efectivo_esperado,
        "diff": diff,
        "utilidad": utilidad,
        "estado": estado,
        "mensaje": mensaje
    }

  

