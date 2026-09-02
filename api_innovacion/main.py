"""
main.py — El arranque de la API del módulo Innovación Curricular.

Arma la aplicación y registra el router. Nada más: la lógica vive en las
capas, no aquí.

Arranque:  uvicorn main:app --port 8030 --reload
Contratos: http://localhost:8030/docs
"""

from fastapi import FastAPI

from controllers.aliado_controller import router as router_aliado

app = FastAPI(
    title="API Innovación Curricular",
    description="Módulo Innovación Curricular — versión 1: el CRUD de aliado.",
    version="v1",
)

app.include_router(router_aliado)


@app.get("/")
async def diagnostico():
    """Responde sin tocar la base: sirve para saber si la API está viva."""
    return {"mensaje": "API Innovación Curricular — módulo de aliado",
            "version": "v1", "contratos": "/docs"}
