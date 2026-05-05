from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Float, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


def _now_cdmx() -> datetime:
    return datetime.now(ZoneInfo("America/Mexico_City"))


class CorteCaja(Base):
    __tablename__ = "cortes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now_cdmx)

    # Inputs usuario

    fondo_inicial: Mapped[float] = mapped_column(Float, nullable=False)
    venta_total: Mapped[float] = mapped_column(Float, nullable=False)
    total_tarjeta: Mapped[float] = mapped_column(Float, nullable=False)
    otros_ingresos_efectivo: Mapped[float] = mapped_column(Float, nullable=False)
    gastos_efectivo: Mapped[float] = mapped_column(Float, nullable=False)
    gastos_tarjeta: Mapped[float] = mapped_column(Float, nullable=False)

    #Resultados 

    efectivo_ventas: Mapped[float] = mapped_column(Float, nullable=False)
    efectivo_contado: Mapped[float] = mapped_column(Float, nullable=False)
    efectivo_esperado: Mapped[float] = mapped_column(Float, nullable=False)
    diff: Mapped[float] = mapped_column(Float, nullable=False)
    utilidad: Mapped[float] = mapped_column(Float, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    mensaje: Mapped[str] = mapped_column(String(200), nullable=False)
