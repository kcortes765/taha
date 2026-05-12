# WS2 APOS delta: diagnóstico ED2 período con ambos cachos rígidos

Fecha: `2026-05-12 17:08`.

## Motivo

Se corrigió una interpretación previa: la variante con cachos rígidos solo en vigas no debe presentarse como cierre final, sino como sensibilidad. El enunciado pide cachos rígidos automáticos `0.75` en encuentros de vigas y columnas.

## Nuevo paquete generado

- Modelo: `prog2/CLASE_PRE_ESPECTRO_20260511_1356/Edificio_2/models/ED2_CLASE_METODO_ESTATICO_AMBOS_RZ_MASA_CORREGIDA_20260512_170352.EDB`.
- Excel: `prog2/CLASE_PRE_ESPECTRO_20260511_1356/Edificio_2/excel/ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_20260512.xlsx`.
- Copia en Descargas: `C:/Users/Civil/Downloads/ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_WS2_20260512.xlsx`.

## Resultado

- `Tx* = 0.400467 s`.
- `Ty* = 0.400492 s`.
- `Tz* = 0.354297 s`.
- Peso sísmico total: `5248.471 tonf`.

## Lectura técnica

Mantener cachos en vigas y columnas baja el período porque ETABS acorta la longitud flexible de las columnas al usar offsets automáticos y `Rigid-zone factor = 0.75`. El rango `0.47-0.51 s` aparece al quitar o no aplicar efectivamente esos offsets rígidos en columnas.
