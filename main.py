from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.routers import cortes

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Iniciando CuadraCaja en modo: {settings.app_env}")
    Base.metadata.create_all(bind=engine)
    logger.info(f"Tablas vetificadas en la base de datos")
    yield
    logger.info(f"CuadraCaja apagándose")

app = FastAPI(
    title="CuadraCaja API",
    description="Sistema de conciliación de caja para el cálculo de utilidades reales",
    version="1.0.0",
    lifespan = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(cortes.router)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/", include_in_schema="False")
def home():
    return FileResponse("frontend/index.html")

@app.get("/health", tags=["sistema"])
def health():
    return {"status" : "ok", "env": settings.app_env}


