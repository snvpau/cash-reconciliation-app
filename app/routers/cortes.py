from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import services
from app.database import get_db
from app.schemas import CorteCajaCreate, CorteHistorial, CorteResultado, UtilidadResponse

router = APIRouter(prefix="/api/v1", tags=["cortes"])

@router.post(
    "/corte-caja",
    response_model = CorteResultado,
    summary = "Registrar un corte de caja",
)

def crear_corte(corte: CorteCajaCreate, db: Session = Depends(get_db)):
    #try:
        return services.crear_corte(db, corte)
    #except Exception as e:
        #raise HTTPException(
            #status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            #detail = "Error interno al procesar el corte",
        #) from e

@router.get(
    "/historial",
    response_model = list[CorteHistorial],
    summary = "Historial de cortes guardados",
)

def historial(db: Session = Depends(get_db)):
    return services.get_historial(db)

@router.get(
    "/utilidad-mensual",
    response_model = UtilidadResponse,
    summary = "Utilidad mensual",
)

def utilidad_mensual(db: Session = Depends(get_db)):
    return UtilidadResponse(total = services.get_utilidad_mensual(db))

@router.get(
    "/utilidad-total",
    response_model = UtilidadResponse,
    summary = "Utilidad total",
)

def utilidad_total(db: Session = Depends(get_db)):
    return UtilidadResponse(total = services.get_total_utilidad(db))