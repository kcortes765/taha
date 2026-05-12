# Edificio 2 - Método estático manual clase 2026-05-12

Este paquete deja transferido a Git el estado trabajado para continuar desde otro PC.

## Contenido

- `Edificio_2/excel/ED2_METODO_ESTATICO_MANUAL_EXCEL_20260512.xlsx`: Excel final del método estático manual.
- `Edificio_2/models/ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.EDB`: modelo ETABS 21 asociado al estado de clase.
- `Edificio_2/models/ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.OUT`: evidencia de masas por diafragma/piso.
- `Edificio_2/models/ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.LOG`: log ETABS del modelo.
- `Edificio_2/models/ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.msh`: archivo auxiliar de malla ETABS.
- `Edificio_2/reports/AUDITORIA_EXCEL_CLASE_SISMO_20260512_20260512_150626.md`: reporte vigente de auditoría.
- `Edificio_2/reports/AUDITORIA_EXCEL_CLASE_SISMO_20260512_20260512_150626.json`: datos estructurados de auditoría.
- `Edificio_2/reports/AUDITORIA_EXCEL_CLASE_SISMO_20260512_20260512_150626.log`: log de ejecución del auditor.
- `Edificio_2/results/modal_participating_mass_ratios_api_20260512_150626.csv`: modos y masas participantes desde API ETABS.
- `Edificio_2/results/story_weights_from_etabs_out_20260512_150626.csv`: pesos sísmicos por piso desde `.OUT`.
- `scripts_usados/auditar_y_rehacer_excel_clase_sismo_20260512.py`: script usado para auditar y regenerar el Excel.

No se incluyen archivos pesados de resultados `.Y*` ni matrices `.K*`; el modelo se puede abrir y reanalizar en ETABS 21.

## Valores finales

- `Tx* = 0.404299 s`, modo 2, máxima masa participante `UX`.
- `Ty* = 0.404324 s`, modo 1, máxima masa participante `UY`.
- `P = 5301.283 tonf`.
- `Craw_x = 0.191689`, `Craw_y = 0.191673`.
- `Cmax = 0.147000`; se usa `C = 0.147000`.
- `Q0x = Q0y = 779.289 tonf`.
- `sum(Fx) - Q0x = 0.000`.
- `sum(Fy) - Q0y = 0.000`.

## Nota de uso

Para continuar en laptop:

1. Descargar o hacer `git pull` de la rama `codex/ws2-ed1-etabs21-context`.
2. Abrir el Excel desde `class_metodo_estatico_ed2_20260512/Edificio_2/excel`.
3. Si se quiere revisar ETABS, abrir el `.EDB` con ETABS 21 y correr `Modal` si se desean recalcular modos.
4. Para ingresar el método estático a ETABS después de los cálculos manuales, usar la hoja `05_Cargas_ETABS`.
