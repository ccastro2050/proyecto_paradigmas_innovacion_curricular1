"""
Controlador de aliado — la capa HTTP.

Su único trabajo es traducir: recibe una petición, llama al servicio y
convierte lo que pase en un código de estado.

    ValueError   → 400   (la forma es válida, la regla no se cumple)
    LookupError  → 404
    lo demás     → 500

El 422 no aparece aquí: lo produce Pydantic ANTES de entrar, cuando el cuerpo
no tiene la forma declarada en models/.
"""

from fastapi import APIRouter, HTTPException, Response

from models.aliado import (Aliado, AliadoActualizar, AliadoReemplazo)
from servicios.ensamblador import crear_servicio_aliado

router = APIRouter(prefix="/api", tags=["aliado"])

TABLA = "aliado"


def _error(estado: int, mensaje: str, detalle: str) -> HTTPException:
    return HTTPException(
        status_code=estado,
        detail={"estado": estado, "mensaje": mensaje, "detalle": detalle},
    )


# ----------------------------------------------------------------------
# GET /api/aliado — Listar (query string ?limite=N)
# ----------------------------------------------------------------------
@router.get(f"/{TABLA}")
async def listar(limite: int = 1000):
    try:
        servicio = crear_servicio_aliado()
        filas = await servicio.listar(limite)
        if not filas:
            # 204: éxito SIN contenido — "tabla vacía" no es un error.
            return Response(status_code=204)
        return {"tabla": TABLA, "limite": limite,
                "total": len(filas), "datos": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "Error al consultar.", str(excepcion))


# ----------------------------------------------------------------------
# GET /api/aliado/{llave} — Obtener uno
# ----------------------------------------------------------------------
@router.get(f"/{TABLA}/{{llave}}")
async def obtener(llave: int):
    try:
        servicio = crear_servicio_aliado()
        return await servicio.obtener(llave)
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Aliado no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "Error al consultar.", str(excepcion))


# ----------------------------------------------------------------------
# POST /api/aliado — Crear
# ----------------------------------------------------------------------
@router.post(f"/{TABLA}")
async def crear(entidad: Aliado):
    try:
        servicio = crear_servicio_aliado()
        # exclude_none: un opcional que no llegó NO se escribe como NULL
        # explícito; simplemente no entra en el INSERT.
        await servicio.crear(entidad.model_dump(exclude_none=True))
        return {"estado": 200, "mensaje": "Aliado creado exitosamente."}
    except ValueError as excepcion:
        raise _error(400, "Datos inválidos.", str(excepcion))
    except Exception as excepcion:
        # Aquí cae la llave duplicada: la defiende la base, no la API.
        raise _error(500, "No se pudo crear.", str(excepcion))


# ----------------------------------------------------------------------
# PUT /api/aliado/{llave} — Reemplazo COMPLETO
# ----------------------------------------------------------------------
@router.put(f"/{TABLA}/{{llave}}")
async def reemplazar(llave: int, entidad: AliadoReemplazo):
    try:
        servicio = crear_servicio_aliado()
        # PUT: el modelo exige TODOS los obligatorios → se escriben todos.
        filas = await servicio.actualizar(llave, entidad.model_dump())
        return {"estado": 200, "mensaje": "Aliado reemplazado.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Aliado no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo reemplazar.", str(excepcion))


# ----------------------------------------------------------------------
# PATCH /api/aliado/{llave} — Actualización PARCIAL
# ----------------------------------------------------------------------
@router.patch(f"/{TABLA}/{{llave}}")
async def actualizar(llave: int, entidad: AliadoActualizar):
    try:
        servicio = crear_servicio_aliado()
        # PATCH: solo los campos que el cliente envió. Si no envió ninguno,
        # el servicio responde con ValueError → 400.
        datos = entidad.model_dump(exclude_none=True)
        filas = await servicio.actualizar(llave, datos)
        return {"estado": 200, "mensaje": "Aliado actualizado.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Aliado no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo actualizar.", str(excepcion))


# ----------------------------------------------------------------------
# DELETE /api/aliado/{llave} — Eliminar (LÓGICO)
# ----------------------------------------------------------------------
@router.delete(f"/{TABLA}/{{llave}}")
async def eliminar(llave: int):
    try:
        servicio = crear_servicio_aliado()
        filas = await servicio.eliminar(llave)
        return {"estado": 200, "mensaje": "Aliado eliminado.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Aliado no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo eliminar.", str(excepcion))
