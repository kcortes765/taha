# Auditoría Excel clase sismo - Edificio 2

- Fecha: `20260512_150626`
- Excel auditado/regenerado: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356\Edificio_2\excel\ED2_METODO_ESTATICO_MANUAL_EXCEL_20260512.xlsx`
- Modelo ETABS: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356\Edificio_2\models\ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.EDB`
- Backup Excel anterior: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356\Edificio_2\backups\ED2_METODO_ESTATICO_MANUAL_EXCEL_20260512_BACKUP_PRE_AUDIT_CLASE_20260512_150626.xlsx`

## Resultado

- Estado final: `OK`.
- Se corrigió la fuente de `P_k`: ahora viene del `.OUT` real de ETABS, no de estimación analítica.
- Se corrigió `Tx*` y `Ty*`: ahora se eligen por masa participante real API (`UX` y `UY`), no por orden visual de periodos.
- Se dejó el Excel con celdas editables amarillas, datos ETABS azules, fórmulas verdes, datos fijos grises y trazabilidad morada.

## Valores finales

- `Tx* = 0.404299 s` desde modo `2` (`UX=0.867502`).
- `Ty* = 0.404324 s` desde modo `1` (`UY=0.867495`).
- `P = 5301.283 tonf`.
- `Craw_x = 0.191689`, `Craw_y = 0.191673`.
- `Cmax = 0.147000`, por lo tanto `C usado = 0.147000` en ambas direcciones.
- `Q0x = 779.289 tonf`, `Q0y = 779.289 tonf`.

## Evidencia de clase/material

- `sismo 10_transcripcion.txt`: Edificio 2 usa método estático; corte basal por dirección; peso sísmico con permanentes + porcentaje de sobrecarga; cálculo fuera de ETABS.
- `05_NCh433_2026_para_Curso.pdf`: 6.2.3, 6.2.5, 6.2.8, Tabla 7, Tabla 8 y Tabla 9.
- `11_02c_Analisis_Estatico.pdf`: resumen de método estático `Q0 = C I P` y límites de `C`.

## Observación

La transcripción automática puede deformar decimales; por eso `n=1,40` se tomó de la Tabla 8 de NCh433:2026 y queda coherente con el material del curso.
