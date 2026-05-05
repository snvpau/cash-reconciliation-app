from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime
from typing import Dict

# Lo que entra

class CorteCajaCreate(BaseModel):
    fondo_inicial: float
    venta_total: float
    total_tarjeta: float
    otros_ingresos_efectivo: float
    gastos_efectivo: float
    gastos_tarjeta: float
    denominaciones: Dict[str, int]

    @field_validator(
        "fondo_inicial", "venta_total", "total_tarjeta", "otros_ingresos_efectivo",
        "gastos_efectivo", "gastos_tarjeta"
    )

    @classmethod
    def not_negatives(cls, v, info):
        if v < 0: 
            raise ValueError(f"{info.field_name} no puede ser negativo")
        return v
    
    @model_validator(mode = "after")
    def tarjeta_no_mayor_a_venta(self):
        if self.total_tarjeta > self.venta_total:
            raise ValueError("total tarjeta no puede ser mayor a venta total")
        return self
    
    # Lo que sale

class CorteResultado(BaseModel):
    efectivo_ventas: float
    efectivo_contado: float
    efectivo_esperado: float
    utilidad: float
    diff: float
    estado: str
    mensaje: str
    guardado: bool

class CorteHistorial(BaseModel):
    id: int
    fecha: datetime
    venta_total: float
    utilidad: float
    diff: float
    estado: str

    model_config = {"from_attributes": True}

class UtilidadResponse(BaseModel):
    total: float
