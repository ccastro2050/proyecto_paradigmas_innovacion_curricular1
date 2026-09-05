# Mapa de versiones — Módulo Innovación Curricular

> La ruta completa del proyecto. Cada versión se especifica **solo cuando
> la anterior está cerrada** (commit + tag). Este mapa da la dirección; el
> spec kit de cada versión da el detalle.
>
> La ruta es la que define
> [modulo_innovacion_curricular.md](../../../ProyectosDeAula/docs/modulo_innovacion_curricular.md);
> aquí no se inventa nada, se ordena.

## La estrategia: back y front EN PARALELO

**Cada versión entrega su parte de la API *y* su parte del front**, y una
versión **no está cerrada** si la API responde y la pantalla no.

El front es **Flask** sobre Python 3.12, en un tercer contenedor, en el
puerto **8028**. Habla con la API solo por HTTP: no tiene cadena
de conexión, ni driver de base de datos, ni servicio `postgres` en su
`depends_on`.

Está exigido por el **Artículo 1.1** de la [constitución](../1_constitution.md).

## La ruta

| Versión | Qué agrega (acumulativo) | Estado |
|---|---|---|
| **v1** | CRUD completo de las **tablas sin clave foránea**, con los catálogos del Excel cargados | **En curso** ([spec](v1_aliado/2_spec.md)) |
| v2 | CRUD de las **15 tablas con clave foránea**: las FK como listas desplegables cargadas desde la API, y validación de integridad referencial | Sin especificar |
| v3 | **JWT**, sesiones y control de acceso por roles; CRUD de `usuario`, `rol` y `rol_usuario` solo para administradores | Sin especificar |
| v4 | **10 consultas multitabla** (4+ tablas cada una), dashboard con gráficos, páginas corporativas, responsive/PWA y **publicación** en un servidor | Sin especificar |

## Qué tabla entra en qué versión

Las 25 tablas de la base, repartidas:

| Versión | Tablas |
|---|---|
| **v1** | `aliado` · `area_conocimiento` · `universidad` · `aspecto_normativo` · `practica_estrategia` · `enfoque` · `car_innovacion` |
| v2 | `facultad` · `programa` · `acreditacion` · `registro_calificado` · `activ_academica` · `pasantia` · `premio` · `docente_departamento` · `alianza` · `programa_ac` · `programa_pe` · `programa_ci` · `an_programa` · `enfoque_rc` · `aa_rc` |
| v3 | `rol` · `usuario` · `rol_usuario` |

> **Ojo:** las 25 tablas **existen en la base desde la v1** (Artículo 5 de
> la [constitución](../1_constitution.md)). Lo que reparte esta tabla es
> qué puede **nombrar el código** de cada versión, no qué existe en el
> motor.

## Lo que este ejemplo construye

La v1 de este repositorio se construye sobre **`aliado`**: una rebanada
vertical completa —controlador, servicio, repositorio, interfaces,
peticiones y prueba sin base de datos— sobre la tabla **con más campos de
las siete sin clave foránea** (seis: `nit`, `razon_social`,
`nombre_contacto`, `correo`, `telefono`, `ciudad`).

El Excel de referencia **no trae un solo aliado** —su hoja tiene la
cabecera y nada más—, así que arranca con **14 filas de ejemplo,
inventadas y anunciadas como tales**: correos en `example.com`, teléfonos
con `555` y el aviso escrito encima del `INSERT`, porque un dato inventado
que no se anuncia termina citado como si fuera del módulo.

El smoke test recorre el ciclo sobre esos datos —**listar → crear → total
15 → borrar → total 14**— y compara contra la pantalla lo que la API
devolvió. Lo que se perdió al sembrar está dicho en `4_research.md`
D-v1-9: el **204 del listado vacío** sigue en el contrato pero ya no se ve
al arrancar.

Las demás tablas de la v1 son **ese mismo patrón** con otros nombres. El
equipo que tome este ejemplo lo revisa, y **si está de acuerdo lo retoma y
lo completa; si no, lo rehace a su manera** — lo que no puede es cambiar la
especificación sin pasar por sus compuertas.

## Reglas del mapa

1. **No se anticipa nada de una versión futura** (Artículo 1 de la
   constitución): en la v1 no aparece una FK, ni un programa, ni un token.
2. **Una versión cerrada no se reabre**: los ajustes van en la siguiente.
3. **Regresión obligatoria**: al cerrar la vN, los criterios de todas las
   versiones anteriores deben seguir pasando.
4. El repositorio siempre muestra la **versión en curso, funcionando**.
