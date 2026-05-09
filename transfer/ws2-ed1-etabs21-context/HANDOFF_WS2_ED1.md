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
- releases solo `M2/M3` donde correspondia
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

El usuario reporta que despues de WS1 se avanzo un poco en WS2 por UI, pero ese avance no esta documentado aun.

Por eso el primer trabajo de WS2 no es seguir modelando: es auditar el estado real del `.EDB` actual.

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

`transfer/ws2-ed1-etabs21-context/reports/WS2_REPORTE_MODELO_ED1_YYYYMMDD_HHMM.md`

Si el reporte queda local en WS2, pegarlo al chat y/o traerlo de vuelta al repo.
