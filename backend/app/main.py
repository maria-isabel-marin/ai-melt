# backend/app/main.py

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Settings (módulo vacío o con variables de entorno)
from app.config import settings  

# Importa tus routers
from app.routers import metaphor
# Si en el futuro usas un “job” router, podrías importarlo aquí:
# from app.routers import job

# Motor (asyncio‐Mongo) para BD
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title="AI-MELT API",
    description="Microservicio FastAPI para MELT (Metaphor Identification)",
    version="1.0.0"
)

# 1) Configuración de CORS (ajusta según tu front‐end real)
origins = [
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Eventos de startup/shutdown para conectar y cerrar conexión a Mongo
@app.on_event("startup")
async def startup_db_client():
    # Asume que settings.MONGO_URI y settings.DATABASE_NAME existen en config.py
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URI)
    app.mongodb = app.mongodb_client[settings.DATABASE_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# 3) Montamos únicamente el router “metaphor”
app.include_router(
    metaphor.router,
    prefix="/metaphor",
    tags=["Metaphor Identification"]
)

# Si más adelante quieres exponer endpoints de “job”, descomenta:
# app.include_router(job.router, prefix="/job", tags=["Job"])

@app.get("/")
async def root():
    return {"message": "AI-MELT API is up and running."}

# 4) Si prefieres arrancar Uvicorn mediante `python main.py`, déjalo así:
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
