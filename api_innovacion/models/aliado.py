"""
Modelos Pydantic de aliado — la FRONTERA DE ENTRADA de la API.

Aquí no hay ni un solo `if` de validación: se DECLARA la forma correcta de
los datos y Pydantic valida al construir el objeto. Un cuerpo inválido muere
en 422 antes de tocar el servicio o la base.

Hay UN modelo por semántica HTTP, y esa es la razón de que PUT y PATCH se
comporten distinto sin una línea que los compare.
"""

from pydantic import BaseModel, Field


class Aliado(BaseModel):
    """POST /api/aliado — 6 campos obligatorios."""

    """El NIT del aliado. Es la llave."""
    nit: int = Field(ge=1)
    razon_social: str = Field(min_length=1, max_length=60)

    nombre_contacto: str = Field(min_length=1, max_length=60)

    """Se guarda como texto: el esquema dado no exige un formato de correo."""
    correo: str = Field(min_length=1, max_length=70)

    telefono: str = Field(min_length=1, max_length=45)

    ciudad: str = Field(min_length=1, max_length=45)


class AliadoReemplazo(BaseModel):
    """PUT /api/aliado/{nit} — reemplazo COMPLETO.

    Omitir un campo es 422, no "dejarlo como estaba": esa es la semántica
    de PUT. La llave no va aquí: identifica la fila y viaja en la ruta.
    """

    razon_social: str = Field(min_length=1, max_length=60)

    nombre_contacto: str = Field(min_length=1, max_length=60)

    """Se guarda como texto: el esquema dado no exige un formato de correo."""
    correo: str = Field(min_length=1, max_length=70)

    telefono: str = Field(min_length=1, max_length=45)

    ciudad: str = Field(min_length=1, max_length=45)


class AliadoActualizar(BaseModel):
    """PATCH /api/aliado/{nit} — parcial: solo se modifican los enviados.

    El MISMO cuerpo que el modelo de arriba rechaza con 422, aquí es válido.
    Lo decide el tipo, no un if en el servicio.
    """

    razon_social: str | None = Field(default=None, min_length=1, max_length=60)

    nombre_contacto: str | None = Field(default=None, min_length=1, max_length=60)

    """Se guarda como texto: el esquema dado no exige un formato de correo."""
    correo: str | None = Field(default=None, min_length=1, max_length=70)

    telefono: str | None = Field(default=None, min_length=1, max_length=45)

    ciudad: str | None = Field(default=None, min_length=1, max_length=45)
