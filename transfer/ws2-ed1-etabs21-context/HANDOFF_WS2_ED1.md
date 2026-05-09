# Handoff WS2 - Edificio 1 ETABS 21

Fecha: 2026-05-08

## Contexto

Se migra el trabajo de Edificio 1 a una segunda workstation UCN (`WS2`) porque en la workstation anterior se perdio/bloqueo licencia de ETABS 21.

La nueva raiz de trabajo reportada por el usuario es:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`

El repo/contexto debe clonarse dentro de esa raiz:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context`

No usar `C:\Users\Civil\Documents\taha` como ruta para este flujo.

## Regla de licencia

No abrir mas de una instancia de ETABS 21. Esta regla es critica y tiene prioridad sobre cualquier automatizacion.

## Estado conocido desde WS1

Modelo anterior de referencia:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`

Correcciones base reportadas antes del bloqueo:

- vigas invertidas con `Cardinal Point = 2`
- `End Length Offset = Auto`
- `Rigid Zone Factor = 0.75`
- releases de momento y torsion donde correspondia segun criterio del profesor
- base empotrada
- losa `Losa15G30` con modificadores flexurales `m11/m22/m12 = 0.25`

Pendiente reportado antes del bloqueo:

- cargas `PP/SCP/SCT/TERP/TERT`
- fuente de masa
- diafragmas
- modal/espectral
- torsion accidental
- analisis
- extraccion de tablas

## Cambio nuevo

El usuario reporto avance y auditoria WS2 por OAPI.

Estado Edificio 1 activo probable:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`

Auditoria WS2 confirmo 20 stories, 320 vigas, 880 areas, 320/320 vigas invertidas, offsets automaticos, `RigidFact = 0.75`, apoyos base empotrados, modificadores de losa `m11/m22/m12 = 0.25` y mesh/auto mesh presente.

Releases reportados:

- `TI, M2I, M3I`: 180 frames.
- `TJ, M2J, M3J`: 100 frames.
- `TI, M2I, M3I, M2J, M3J`: 40 frames.
- Sin release: 0 frames.

Canon corregido: los releases torsionales fueron pedidos por el profesor. No corregirlos por reflejo.

Pendiente real Edificio 1: asignar diafragma a areas, cargas `PP/SCP/SCT/TERP/TERT`, mass source, modal/espectral, torsion accidental, combinaciones, analisis y tablas.

El siguiente trabajo de WS2 ya no es solo auditar: es crear copia limpia del `.EDB` activo y completar Parte 1 de Edificio 1 por pasos incrementales.

## Entregable que debe devolver WS2

Crear un reporte breve con:

- ruta exacta del `.EDB` abierto
- build ETABS
- conteos de objetos
- estado de stories
- estado de muros/vigas/losas
- estado de insertion points/offsets/releases
- estado de apoyos
- estado de mesh
- estado de diafragmas
- estado de cargas y mass source
- estado modal/espectral/torsion
- que cambio respecto a WS1
- que falta antes de analizar

Nombre sugerido del reporte:

`transfer/ws2-ed1-etabs21-context/reports/WS2_ED1_PARTE1_EJECUCION_YYYYMMDD_HHMM.md`

Si el reporte queda local en WS2, pegarlo al chat y/o traerlo de vuelta al repo.
