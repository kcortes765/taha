# WS2 APOS delta 2026-05-12 15:32 - Excel método estático Edificio 2

## Intención

Guardar en método APOS y transferir a Git el estado de la auditoría del Excel de método estático manual para Edificio 2.

## Cambios guardados

- Se creó el paquete repo-local `class_metodo_estatico_ed2_20260512`.
- Se transfirió el Excel final `ED2_METODO_ESTATICO_MANUAL_EXCEL_20260512.xlsx`.
- Se transfirió el modelo ETABS 21 asociado `ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.EDB`.
- Se transfirieron evidencias `.OUT`, `.LOG`, `.msh`, CSV, JSON, reporte y script auditor.
- Se documentó que el reporte vigente es `AUDITORIA_EXCEL_CLASE_SISMO_20260512_20260512_150626.md`.

## Resultado técnico registrado

- `P = 5301.283 tonf`, desde `.OUT` real de ETABS.
- `Tx* = 0.404299 s`, modo 2, máxima masa participante `UX`.
- `Ty* = 0.404324 s`, modo 1, máxima masa participante `UY`.
- `C usado = 0.147000`.
- `Q0x = Q0y = 779.289 tonf`.
- Las fuerzas por piso cierran contra el corte basal: `sum(Fx)-Q0x = 0.000`, `sum(Fy)-Q0y = 0.000`.

## Política

- No se agregaron archivos pesados de resultados `.Y*` ni matrices `.K*`.
- No se modificó `.system`.
- No se tocaron skills globales, hooks ni configuración global.
- No se reescribieron memorias append-only.
