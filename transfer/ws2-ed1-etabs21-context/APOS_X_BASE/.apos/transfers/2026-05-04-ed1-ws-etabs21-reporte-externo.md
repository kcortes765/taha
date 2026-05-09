# 2026-05-04 - Ed.1 WS ETABS 21, reporte externo

Fuente: reporte pegado por el usuario desde otra IA / correo. No verificado localmente en este equipo porque los `.EDB` viven en la WS UCN.

## Rutas WS reportadas

- Modelo original corregido:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_01_Grilla_v01.EDB`
- Backup antes de correcciones:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\backups\ED1_01_Grilla_v01_pre_correcciones_20260502_193648.EDB`
- Copia de trabajo para terminar Parte 1:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`

## Estado ETABS reportado

- No hay ETABS corriendo ahora.
- La automatizacion posterior se bloqueo por licencia.
- El bloqueo fue posterior a las correcciones base, no durante ellas.
- Build confirmado por reporte: ETABS 21.2.0.

## Correcciones base aplicadas por API COM sobre el modelo original

- 320 vigas con `Cardinal Point = 2` para vigas invertidas.
- Vigas con `End Length Offset = Auto`.
- `Rigid Zone Factor = 0.75`.
- Releases corregidos: solo momentos `M2/M3` donde correspondia.
- Sin liberacion indebida de axial, corte ni torsion.
- 50 puntos de base empotrados en 6 GDL.
- `Losa15G30` con modificadores flexurales `m11/m22/m12 = 0.25`.
- Modelo confirmado como ETABS 21 build 21.2.0.

## Parte 1 alcanzada

- Se creo `ED1_PARTE1_COMPLETA_TRABAJO.EDB` desde el modelo corregido.
- Alcance fijado: Parte 1, Edificio 1 solamente.

## No alcanzado antes del bloqueo de licencia

- Patrones/cargas `PP`, `SCP`, `SCT`, `TERP`, `TERT`.
- Fuente de masa.
- Diafragmas.
- Modal.
- Espectros.
- Torsion accidental.
- Analisis.
- Extraccion de tablas.

## Proximo paso canonico

Cuando ETABS 21 vuelva a estar licenciado, continuar solo sobre:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`

Orden:

1. Re-verificar correcciones base.
2. Asignar diafragma rigido.
3. Crear patrones de carga del enunciado.
4. Aplicar cargas de uso, terminaciones y techo.
5. Definir fuente de masa.
6. Crear modal/espectral.
7. Resolver casos rigido/semi-rigido para las 6 combinaciones de torsion.
8. Exportar tablas de peso sismico, CM/CR, periodos, corte basal, drifts, Story Forces y esfuerzos en muros eje 1/eje F.

