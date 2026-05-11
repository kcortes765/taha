# WS2 APOS Delta - Visuales Sin Solapamiento

Fecha: 2026-05-09 22:31

## Motivo

El usuario detecto solapamientos residuales en el paquete visual previo `WS2_VISUALES_TIPO_DIOS_20260509_1756`.

## Hallazgos

- `00_tablero_ejecutivo.png`: texto de la tarjeta `Notas de trazabilidad` se desbordaba.
- `01_ed1_corte_basal_qmin.png`: etiqueta de referencia `Qmin` competia visualmente con valores de barras.

## Cambios Aplicados

- Se actualizo `HECRAS2\prog2\_common\generate_report_visuals.py`.
- Se agrego envoltura de texto mediante `wrap_text`.
- Se redujo y partio el texto de notas del dashboard.
- Se movieron etiquetas de referencia de graficos de barras a badges blancos fuera del conflicto con barras/valores.
- Se regenero un paquete nuevo, sin sobrescribir el paquete historico.

## Nuevo Paquete Vigente

- Carpeta: `HECRAS2\codex_ws2_context\transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_2221`
- PNG: `png_2x\*.png`
- Categorias: `por_categoria`
- ZIP PNG: `WS2_VISUALES_TIPO_DIOS_20260509_2221_PNG_2X.zip`
- ZIP categorias: `WS2_VISUALES_TIPO_DIOS_20260509_2221_POR_CATEGORIA.zip`

## Validacion

- `python -m py_compile .\prog2\_common\generate_report_visuals.py`: OK.
- 18 PNG generados.
- Todos los PNG tienen resolucion `3200 x 2000 px`.
- 18 PNG copiados a carpetas por categoria.
- Hoja de contacto generada: `contact_sheet_png.png`.
- Inspeccion visual a tamano real:
  - `00_tablero_ejecutivo.png`: OK, notas dentro de tarjeta.
  - `01_ed1_corte_basal_qmin.png`: OK, Qmin en badge sin pisar barras/valores.
  - `03_ed1_espectro_periodos.png`: OK, Tx/Ty en badge separado.
  - `14_comparativo_utilizacion.png`: OK, etiqueta de limite/objetivo en badge separado.

## Politica

- No se abrio ETABS.
- No se modificaron `.EDB`.
- No se reescribieron archivos append-only de APOS; solo se agregan entradas nuevas.

