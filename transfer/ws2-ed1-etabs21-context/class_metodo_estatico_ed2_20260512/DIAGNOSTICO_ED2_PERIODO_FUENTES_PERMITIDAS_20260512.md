# Diagnóstico ED2 período con fuentes permitidas

Fecha: `2026-05-12`.

## Fuentes usadas

Se excluyeron Lafontaine, documentación CSI/internet y guías `.md` destiladas. La revisión se hizo con enunciado, Material de Apoyo Taller 2026, apuntes del curso, NCh433:2026 del curso, transcripciones de clase entregadas por el usuario y evidencia directa del modelo.

También se revisaron páginas como imagen, no solo texto extraído. Carpeta de evidencia:

`fuentes_permitidas_paginas_20260512_vision/`

## Lo que exigen las fuentes

- Enunciado p. 8-9: Edificio 2 es un marco de hormigón armado de 5 pisos, planta regular, Antofagasta, suelo C, oficina, base empotrada.
- Enunciado p. 9: cachos rígidos en todos los encuentros de vigas y columnas, opción automática del programa, factor `0.75`.
- Enunciado p. 9: columnas `70/70` en pisos 1-2, `65/65` en pisos 3-5; vigas `50/70` en pisos 1-2, `45/70` en pisos 3-5; losa `17 cm`.
- Enunciado p. 11-12: diafragma rígido a nivel de piso, peso sísmico, períodos `Tx*`, `Ty*`, `Tz*`, coeficientes, corte basal, fuerzas por piso, torsión accidental, momento volcante y deformaciones.
- Material de Apoyo: muestra asignación de diafragma rígido, fuentes de masa, torsión accidental y combinaciones.
- Apuntes p. 43-44: períodos y modos se obtienen resolviendo `K - omega^2 M = 0`; `Tx*`, `Ty*`, `Tz*` se escogen desde las mayores masas equivalentes.
- NCh433:2026 p. 25 y p. 31-34: masa sísmica, método estático, `Q0 = C I P`, distribución por piso, torsión accidental y modal.

## Estado del modelo corregido

Modelo vigente:

`Edificio_2/models/ED2_CLASE_METODO_ESTATICO_AMBOS_RZ_MASA_CORREGIDA_20260512_170352.EDB`

Excel asociado:

`Edificio_2/excel/ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_20260512.xlsx`

Verificado:

- Vigas y columnas con `Rigid-zone factor = 0.75`.
- `C70x70G25`: 72 columnas.
- `C65x65G25`: 108 columnas.
- `V50x70G25`: 120 vigas.
- `V45x70G25`: 180 vigas.
- Diafragma `D1`: 130/130 áreas.
- Sin modificadores `0.25` de flexión a losas.
- Masa aplicada en este paquete: `PP + TERP + TERT + 0.25*SCP + 0*SCT`.

## Resultado modal vigente

- `Tx* = 0.400467 s`, modo 2.
- `Ty* = 0.400492 s`, modo 1.
- `Tz* = 0.354297 s`, modo 3.
- Peso sísmico total: `5248.471 tonf`.

## Por qué no coincide con períodos de 0.47-0.51 s

La sensibilidad controlada previa indica:

| Variante | Tx/Ty aprox. [s] |
| --- | ---: |
| Ambos cachos + SCT 0.25 | `0.404` |
| Ambos cachos + SCT 0 | `0.400` |
| Sin cachos en columnas | `0.468` |
| Sin cachos en vigas | `0.424` |
| Sin cachos en vigas ni columnas | `0.484` |

La masa de techo no explica la diferencia: cambiar `SCT` mueve el período cerca de `1%`. La diferencia grande aparece cuando las columnas dejan de aportar el cacho rígido efectivo. Por eso, el número `0.47-0.51 s` es compatible con un modelo donde las vigas tienen cacho rígido, pero las columnas no lo tienen efectivamente, o donde existe otro cambio de rigidez equivalente.

## Hipótesis a revisar en un modelo de compañero

1. Selección real: si aplicaron `End Length Offsets` solo a vigas, aunque visualmente parezca “todo”.
2. Columnas con `Rigid-zone factor = 0`, selección mixta, o offsets reemplazados después.
3. Material o módulo elástico distinto.
4. Dimensiones de columnas/vigas distintas.
5. Releases no deseados en vigas/columnas.
6. Diafragma incompleto.
7. Masa sísmica duplicada o mal formada.
8. Modelo desbloqueado y guardado luego de cambios manuales.

## Conclusión

Con las fuentes permitidas y la evidencia de ETABS, el modelo que sigue literalmente “vigas y columnas con cachos rígidos automáticos 0.75” da `Tx/Ty ~ 0.40 s`. Si otro modelo igual da `~0.47 s`, la causa más probable no es el cálculo manual ni el Excel, sino una diferencia efectiva de rigidez, especialmente en los cachos rígidos de columnas.
