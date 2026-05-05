from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  
    pool_pre_ping=True, 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependency de FastAPI: abre una sesión por request y la cierra al terminar,
    aunque el endpoint lance una excepción
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()