# WS2 APOS delta: diagnóstico ED2 período con ambos cachos rígidos

Fecha: `2026-05-12 17:45`.

## Motivo

Se corrigió una interpretación previa: la variante con cachos rígidos solo en vigas no debe presentarse como cierre final, sino como sensibilidad. El enunciado pide cachos rígidos automáticos `0.75` en encuentros de vigas y columnas.

También se depuró la documentación para esta discusión: no se usa Lafontaine, documentación CSI/internet ni guías `.md` destiladas como fuente de verdad. Se usan enunciado, Material de Apoyo Taller 2026, apuntes, NCh433:2026 del curso, transcripciones y evidencia directa de ETABS.

## Nuevo paquete generado

- Modelo: `prog2/CLASE_PRE_ESPECTRO_20260511_1356/Edificio_2/models/ED2_CLASE_METODO_ESTATICO_AMBOS_RZ_MASA_CORREGIDA_20260512_170352.EDB`.
- Excel: `prog2/CLASE_PRE_ESPECTRO_20260511_1356/Edificio_2/excel/ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_20260512.xlsx`.
- Copia en Descargas: `C:/Users/Civil/Downloads/ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_WS2_20260512.xlsx`.
- Reporte depurado: `transfer/ws2-ed1-etabs21-context/class_metodo_estatico_ed2_20260512/DIAGNOSTICO_ED2_PERIODO_FUENTES_PERMITIDAS_20260512.md`.

## Resultado

- `Tx* = 0.400467 s`.
- `Ty* = 0.400492 s`.
- `Tz* = 0.354297 s`.
- Peso sísmico total: `5248.471 tonf`.

## Lectura técnica

La sensibilidad controlada muestra que el rango `0.47-0.51 s` aparece cuando las columnas no tienen efectivo el cacho rígido, o cuando existe una pérdida equivalente de rigidez. Con vigas y columnas asignadas según enunciado, el período queda alrededor de `0.40 s`.
