from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from zoneinfo import ZoneInfo
from loguru import logger

from app.models import CorteCaja
from app.schemas import CorteCajaCreate, CorteResultado


def calcular_corte(corte: CorteCajaCreate) -> dict:
    efectivo_ventas = corte.venta_total - corte.total_tarjeta

    efectivo_contado = sum(
        int(denominacion) * cantidad
        for denominacion, cantidad in corte.denominaciones.items()
    )

    efectivo_esperado = (
        corte.fondo_inicial
        + efectivo_ventas
        + corte.otros_ingresos_efectivo
        - corte.gastos_efectivo
    )

    diff = round(efectivo_contado - efectivo_esperado, 2)
    utilidad = round(
        corte.venta_total - (corte.gastos_efectivo + corte.gastos_tarjeta), 2
    )

    if diff == 0:
        estado = "Cuadra"
        mensaje = "El corte cuadra correctamente."
    elif diff < 0:
        monto = abs(diff)
        estado = "Faltante"
        mensaje = f"Hay un faltante de ${monto:.2f} en caja."
    else:
        monto = abs(diff)
        estado = "Sobrante"
        mensaje = f"Hay un sobrante de ${monto:.2f} en caja."

    return {
        "efectivo_ventas": efectivo_ventas,
        "efectivo_contado": efectivo_contado,
        "efectivo_esperado": efectivo_esperado,
        "diff": diff,
        "utilidad": utilidad,
        "estado": estado,
        "mensaje": mensaje,
    }


def crear_corte(db: Session, corte: CorteCajaCreate) -> CorteResultado:
    resultados = calcular_corte(corte)
    guardado = resultados["estado"] == "Cuadra"

    if guardado:
        db_corte = CorteCaja(
            fondo_inicial=corte.fondo_inicial,
            venta_total=corte.venta_total,
            total_tarjeta=corte.total_tarjeta,
            otros_ingresos_efectivo=corte.otros_ingresos_efectivo,
            gastos_efectivo=corte.gastos_efectivo,
            gastos_tarjeta=corte.gastos_tarjeta,
            efectivo_ventas=resultados["efectivo_ventas"],
            efectivo_contado=resultados["efectivo_contado"],
            efectivo_esperado=resultados["efectivo_esperado"],
            diff=resultados["diff"],
            utilidad=resultados["utilidad"],
            estado=resultados["estado"],
            mensaje=resultados["mensaje"],
        )
        db.add(db_corte)
        db.commit()
        db.refresh(db_corte)
        logger.info(f"Corte guardado | utilidad=${resultados['utilidad']:.2f}")
    else:
        resultados["mensaje"] += " El corte no se guardó porque no cuadra."
        logger.warning(f"Corte no guardado | estado={resultados['estado']}")

    return CorteResultado(**resultados, guardado=guardado)


def get_historial(db: Session) -> list[CorteCaja]:
    return db.query(CorteCaja).order_by(CorteCaja.fecha.desc()).all()


def get_utilidad_mensual(db: Session) -> float:
    now = datetime.now(ZoneInfo("America/Mexico_City"))
    result = db.query(func.sum(CorteCaja.utilidad)).filter(
        extract("year", CorteCaja.fecha) == now.year,
        extract("month", CorteCaja.fecha) == now.month,
    ).scalar()
    return round(result or 0.0, 2)


def get_total_utilidad(db: Session) -> float:
    result = db.query(func.sum(CorteCaja.utilidad)).scalar()
    return round(result or 0.0, 2)