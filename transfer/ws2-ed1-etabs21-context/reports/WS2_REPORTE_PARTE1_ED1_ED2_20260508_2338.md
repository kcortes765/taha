# WS2 Reporte Parte 1 Edificio 1 y Edificio 2

- Fecha: 2026-05-08 23:38 America/Santiago
- Workspace real: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
- Carpeta operativa nueva: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2`
- ETABS usado: 21.2.0, una sola instancia, PID `23284`
- Regla licencia aplicada: antes de cada bloque OAPI se ejecuto `Get-Process ETABS -ErrorAction SilentlyContinue`

## 1. Estado confirmado Edificio 1

- `.EDB` original probable: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`
- Copia trabajada: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`
- Backup original: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\backups\ED1_PARTE1_COMPLETA_TRABAJO_ORIG_20260508_2213.*`
- Auditoria:
  - 20 pisos, alturas `3.4 + 19x2.6 m`, altura total `52.8 m`
  - 880 areas, 320 frames, 1350 puntos
  - areas: `MHA30G30=260`, `MHA20G30=320`, `Losa15G30=300`
  - frames: `VI20/60G30=320`
  - apoyos base empotrados: 50 puntos
- Cambios/corrida:
  - cargas `TERP`, `TERT`, `SCP`, `SCT` con no aglomeracion
  - masa: peso propio por masa de elementos + `TERP + TERT + 0.25*SCP`
  - espectro NCh433:2026 importado via tabla ETABS `Functions - Response Spectrum - User Defined`
  - casos `SEx`, `SEy`, `SEx_b2`, `SEy_b2`
  - R*: `R*x=8.8673`, `R*y=8.8449`
  - Qmin: `W=10529.794 tonf`, `Qmin=737.086 tonf`
  - final: `SEx=740.771 tonf`, `SEy=740.771 tonf`, ratio `1.005`
  - drift max exportado observado: aprox. `0.001353 < 0.002`
- Estado: base dinamica rigida Parte 1 ejecutada/exportada. No se tocaron releases torsionales.

## 2. Estado confirmado Edificio 2

- `.EDB` original probable: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\Edif2\Edificio2_Estatico con carga sismica.EDB`
- Copia trabajada: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`
- Backup original: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\backups\Edificio2_Estatico_con_carga_sismica_ORIG_20260508_2213.*`
- Auditoria:
  - 5 pisos reales: `3.5 + 4x3.0 m`
  - 130 areas `L17G25`
  - 480 frames: 180 columnas, 300 vigas
  - secciones: `C70x70G25=72`, `C65x65G25=108`, `V50x70G25=120`, `V45x70G25=180`
  - apoyos base empotrados: 36 puntos
  - diafragma `D1`
- Corrida oficial Parte 1:
  - modal auxiliar: `Tx=0.408 s`, `Ty=0.408 s`, `Tz=0.359 s`
  - `W=5378.458 tonf`, `W/area=1.018406 tonf/m2`
  - `Cx=Cy=0.147`, `Cmin=0.070`, `Cmax=0.147`
  - `Vd=790.633 tonf`
  - `EX=779.555 tonf`, `EY=779.555 tonf` (brecha aprox. 1.4%, aceptada por verificador)
  - torsion accidental: `TEX_WS2=1851.152 tonf*m`, `TEY_WS2=1851.152 tonf*m`
  - drift CM max `0.000816 < 0.002`
  - exceso torsional max `0.000250 < 0.001`
- Verificador final: `PASS`
- Advertencia: ETABS no expuso CR real; se exporto CM real y CR placeholder explicito `etabs_cm_table_placeholder_cr_zero`.

## 3. Archivos .EDB encontrados y activo probable

- Edificio 1 activo trabajado: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`
- Edificio 2 activo trabajado: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`
- Manifest de copias: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\WS2_PROG2_COPY_MANIFEST_20260508_2213.csv`
- Los `.EDB` vivos originales no fueron modificados directamente.

## 4. Que cambio respecto al estado WS1

- Se creo `prog2` con copias fechadas y backups por edificio.
- Se incorporo helper OAPI seguro para ETABS 21 con `GetObjectProcess` por PID.
- Edificio 1 paso de auditoria/modelo UI a corrida dinamica base con R*, Qmin y exportaciones.
- Edificio 2 paso de modelo estatico existente a pipeline programatico verificado con `PASS`.
- En Edificio 2 se separaron los patrones historicos `TEX/TEY` de los nuevos `TEX_WS2/TEY_WS2`, porque los historicos arrastraban estado interno no visible que contaminaba torsion/drift.

## 5. Que falta para Parte 1 Edificio 1

- Si el criterio del profesor acepta la base dinamica rigida con torsion accidental y Qmin, Edificio 1 ya tiene resultados utilizables.
- Si la rubrica exige literalmente la matriz completa de seis variantes de Edificio 1, falta:
  - crear/copiar variantes separadas
  - correrlas una por una en la misma instancia ETABS
  - exportar tabla comparativa formal
  - preservar releases torsionales pedidos por el profesor
- No se debe declarar cerrada esa matriz sin evidencia nueva.

## 6. Que falta para Parte 1 Edificio 2

- Parte 1 programatica esta cerrada con `PASS`.
- Falta solo preparar material de informe humano: tablas y graficos `V(z)`/momento volcante desde CSV, capturas UI si se requieren visualmente.

## 7. Riesgos tecnicos

- Licencia: no abrir segunda instancia ETABS 21.
- Edificio 1: matriz formal completa podria estar pendiente si se exige como entregable literal.
- Edificio 2: `CR` real no fue expuesto por ETABS; no se invento, se marco placeholder.
- Edificio 2: no reutilizar `TEX/TEY` historicos para WS2; usar `TEX_WS2/TEY_WS2`.
- ETABS tablas: algunas tablas de resultados Ed2 solo quedaron disponibles si `RunAnalysis` y extraccion ocurrian dentro de la misma sesion COM; por eso se creo `ws2_run_extract_ed2.py`.

## 8. Siguiente accion segura

1. Mantener una sola instancia ETABS.
2. Si se continua Ed1: crear variantes desde la copia `prog2`, no desde el original, y correrlas una a una.
3. Si se arma informe Ed2: usar `HECRAS2\prog2\Edif2\results\ed2_summary.json`, `ed2_static_distribution.csv`, `ed2_story_forces_summary.csv`, `ed2_drift_envelope.csv`.
4. Antes de cualquier script OAPI nuevo: `Get-Process ETABS -ErrorAction SilentlyContinue`.

## 9. Evidencia usada

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_audit_20260508_2221.md`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_run-adjust-export_20260508_2247.md`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_run-adjust-export_20260508_2247.json`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\reports\ED2_PARTE1_PROG2_audit_20260508_2258.md`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\logs\ed2_ws2_run_extract_ws2_forcecouple_20260508_233410.log`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\logs\ed2_verify_final_20260508_233545.log`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_summary.json`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_base_reactions.csv`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_drift_envelope.csv`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context\transfer\ws2-ed1-etabs21-context\reports\WS2_ETABS_OAPI_SESSION_SAFETY_20260508_2205.md`
