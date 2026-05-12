# Diagnóstico período ED2 con cachos rígidos en vigas y columnas

Fecha: `2026-05-12 17:05`.

## Corrección de criterio

La versión con cachos rígidos solo en vigas se conserva únicamente como sensibilidad. No corresponde usarla como cierre si se sigue literalmente el enunciado.

El enunciado actualizado indica para Edificio 2: cachos rígidos en todos los encuentros de vigas y columnas, opción automática, factor `0.75`.

## Modelo alineado al enunciado

- Modelo: `Edificio_2/models/ED2_CLASE_METODO_ESTATICO_AMBOS_RZ_MASA_CORREGIDA_20260512_170352.EDB`.
- Excel: `Edificio_2/excel/ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_20260512.xlsx`.
- Reporte: `Edificio_2/reports/ED2_AMBOS_RZ_MASA_CORREGIDA_20260512_170352.md`.
- CSV modal: `Edificio_2/results/modal_participating_mass_ratios_ambos_rz_masa_corregida_20260512_170352.csv`.

## Configuración verificada

- Cachos rígidos `0.75` en:
  - `C70x70G25`: 72 columnas.
  - `C65x65G25`: 108 columnas.
  - `V50x70G25`: 120 vigas.
  - `V45x70G25`: 180 vigas.
- Diafragma `D1`: 130/130 áreas asignadas.
- Masa sísmica: `PP + TERP + TERT + 0.25*SCP + 0*SCT`.
- `SCT` se conserva como carga gravitacional, pero no entra en masa sísmica.

## Resultados con ambos cachos y masa corregida

- `Tx* = 0.400467 s`, modo 2.
- `Ty* = 0.400492 s`, modo 1.
- `Tz* = 0.354297 s`, modo 3.
- Peso sísmico total: `5248.471 tonf`.
- `Q0x = 771.525 tonf`.
- `Q0y = 771.525 tonf`.

## Comparación de sensibilidad

| Variante | Tx/Ty aprox. [s] | Interpretación |
| --- | ---: | --- |
| Ambos cachos + SCT 0.25 | `0.404` | Modelo original de clase antes de corregir masa techo |
| Ambos cachos + SCT 0 | `0.400` | Modelo alineado a enunciado + clase |
| Sin cachos en columnas | `0.468` | Se parece a valores de compañeros cerca de `0.47` |
| Sin cachos en vigas | `0.424` | Aumenta poco respecto de ambos cachos |
| Sin cachos en vigas ni columnas | `0.484` | Cae dentro del rango alto observado por compañeros |

## Lectura técnica

La diferencia principal no viene del Excel ni de `SCT`; viene de cómo ETABS interpreta `Automatic from Connectivity` en columnas. Según documentación CSI, ETABS calcula offsets automáticos en columnas usando las dimensiones de las vigas que llegan al extremo de la columna, y el `Rigid-zone factor` define qué fracción de ese offset se considera rígida para flexión y corte.

Con vigas de altura `0.70 m`, una columna típica de `3.0 m` puede quedar con una longitud flexible aproximada:

`Lf = 3.0 - 0.75*(0.70 + 0.70) = 1.95 m`

En una lectura idealizada de flexión lateral, la rigidez crece aproximadamente con `1/L^3`. Por eso acortar la longitud flexible de columnas baja fuertemente el período. Si otro modelo tiene realmente cachos en vigas y columnas con el mismo `0.75`, misma masa, mismas secciones, mismos modificadores y diafragma rígido, debería quedar cerca de `0.40 s`, no cerca de `0.47-0.51 s`.

## Conclusión

Si el profesor exige aplicar literalmente cachos rígidos automáticos `0.75` en vigas y columnas, el período bajo `~0.40 s` es consistente con ETABS.

Si el curso está obteniendo `~0.47 s`, lo más probable es que en esos modelos las columnas no estén recibiendo efectivamente el cacho rígido `0.75`, o que se esté usando un criterio distinto de offsets/rigidez efectiva aunque visualmente parezca “aplicado a todo”.
