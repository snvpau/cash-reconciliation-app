from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from fastapi import FastAPI, HTTPException
from database import create_table, save_corte, get_cortes, get_utilidad_mensual, get_total_utilidad
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

create_table()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

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

    resultados = {
        "efectivo_ventas": efectivo_ventas,
        "efectivo_contado": efectivo_contado,
        "efectivo_esperado": efectivo_esperado,
        "diff": diff,
        "utilidad": utilidad,
        "estado": estado,
        "mensaje": mensaje
    }

    if estado == "Cuadra":
        save_corte(corte, resultados)
        resultados["guardado"] = True
    else:
        resultados["guardado"] = False 
        resultados["mensaje"] += " El corte no se guardará en la base de datos porque no cuadra."

    return resultados

@app.get("/historial")
def historial():
    return get_cortes()

@app.get("/utilidad-mensual")
def utilidad_mensual():
    return {"total": get_utilidad_mensual()}

@app.get("/total-utilidad")
def utilidad_total():
    return {"total": get_total_utilidad()}


