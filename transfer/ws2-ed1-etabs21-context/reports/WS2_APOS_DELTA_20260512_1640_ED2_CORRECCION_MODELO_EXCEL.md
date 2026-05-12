# WS2 APOS delta: corrección ED2 modelo + Excel

Fecha: `2026-05-12 16:40`.

## Qué se guardó

- Se corrigió el modelo ED2 de método estático:
  `prog2/CLASE_PRE_ESPECTRO_20260511_1356/Edificio_2/models/ED2_CLASE_METODO_ESTATICO_CORREGIDO_20260512_162839.EDB`.
- Se corrigió el Excel asociado:
  `prog2/CLASE_PRE_ESPECTRO_20260511_1356/Edificio_2/excel/ED2_METODO_ESTATICO_MANUAL_EXCEL_CORREGIDO_20260512.xlsx`.
- Se copió una versión descargable a:
  `C:/Users/Civil/Downloads/ED2_METODO_ESTATICO_MANUAL_EXCEL_CORREGIDO_WS2_20260512.xlsx`.
- Se replicó la evidencia al paquete Git:
  `transfer/ws2-ed1-etabs21-context/class_metodo_estatico_ed2_20260512`.

## Decisiones técnicas

- `Rigid-zone factor = 0.75` se dejó solo en vigas.
- Columnas quedaron sin cacho rígido asignado por `End Length Offsets`.
- La masa sísmica quedó como `PP + TERP + TERT + 0.25*SCP + 0*SCT`.
- `SCT` no entra a masa sísmica, pero se conserva como carga gravitacional.

## Resultados corregidos

- `Tx* = 0.461202 s`.
- `Ty* = 0.461221 s`.
- `Tz* = 0.408064 s`.
- Peso sísmico total: `5248.471 tonf`.
- `Q0x = 771.525 tonf`.
- `Q0y = 771.525 tonf`.

## Incidente ETABS

ETABS abrió un aviso de recuperación de resultados después de una corrida anómala. Se eligió recuperar resultados, se guardó el modelo para fijar compatibilidad y se cerró la instancia. No se abrió una segunda instancia.
