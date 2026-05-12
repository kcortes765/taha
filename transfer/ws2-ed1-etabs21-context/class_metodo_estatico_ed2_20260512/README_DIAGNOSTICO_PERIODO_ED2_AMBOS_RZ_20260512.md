# Diagnóstico período ED2 con fuentes permitidas

Fecha: `2026-05-12 17:45`.

## Alcance

Este diagnóstico deja fuera Lafontaine, documentación CSI/internet y guías `.md` destiladas. La lectura se apoya solo en:

- Enunciado actualizado del taller.
- Material de Apoyo Taller 2026.
- Apuntes del curso.
- NCh433:2026 usada por el curso.
- Transcripciones de clase entregadas por el usuario.
- Evidencia directa de ETABS/exportaciones del modelo.

Además de texto extraído, se revisaron páginas renderizadas como imagen. La evidencia visual queda en:

- `fuentes_permitidas_paginas_20260512_vision/`

## Lectura de fuentes

El enunciado de Edificio 2 define un edificio de 5 pisos en Antofagasta, uso oficina, suelo C, marcos de hormigón armado, planta 32.5 m x 32.5 m, base empotrada y diafragma rígido a nivel de piso. En la página 9 indica explícitamente considerar cachos rígidos en todos los encuentros de vigas y columnas, con opción automática del programa y factor de rigidez `0.75`.

El mismo enunciado entrega dimensiones: columnas `70/70` en pisos 1-2, columnas `65/65` en pisos 3-5, vigas `50/70` en pisos 1-2, vigas `45/70` en pisos 3-5 y losa de `17 cm`. También entrega cargas de techo y pisos.

Las páginas de análisis sísmico del enunciado piden para Edificio 2: peso sísmico, períodos asociados a mayores masas traslacionales y rotacional `Tx*`, `Ty*`, `Tz*`, coeficientes sísmicos, corte basal, fuerzas por piso, torsión accidental, momento volcante y verificación de deformaciones.

El Material de Apoyo muestra la asignación de diafragma rígido, definición de fuentes de masa, torsión accidental en ETABS, cargas laterales aplicadas al centro de masa y combinaciones. Los apuntes del curso muestran el cálculo modal desde `K - omega^2 M = 0` y la selección de los períodos desde las masas equivalentes máximas. NCh433:2026 indica masa sísmica con cargas permanentes más porcentaje de sobrecarga, método estático, corte basal `Q0 = C I P`, distribución por piso y torsión accidental.

## Modelo vigente

- Modelo: `Edificio_2/models/ED2_CLASE_METODO_ESTATICO_AMBOS_RZ_MASA_CORREGIDA_20260512_170352.EDB`.
- Excel: `Edificio_2/excel/ED2_METODO_ESTATICO_MANUAL_EXCEL_AMBOS_RZ_MASA_CORREGIDA_20260512.xlsx`.
- Reporte local: `Edificio_2/reports/ED2_AMBOS_RZ_MASA_CORREGIDA_20260512_170352.md`.
- CSV modal: `Edificio_2/results/modal_participating_mass_ratios_ambos_rz_masa_corregida_20260512_170352.csv`.

Configuración verificada por exportación/API:

- Cachos rígidos `0.75` en `C70x70G25`: 72 columnas.
- Cachos rígidos `0.75` en `C65x65G25`: 108 columnas.
- Cachos rígidos `0.75` en `V50x70G25`: 120 vigas.
- Cachos rígidos `0.75` en `V45x70G25`: 180 vigas.
- Diafragma `D1`: 130/130 áreas asignadas.
- Masa sísmica aplicada en el modelo vigente: `PP + TERP + TERT + 0.25*SCP + 0*SCT`.
- El Excel mantiene `SCT` como input editable; cambiarlo a `0.25` permite recalcular si el profesor pide incluir sobrecarga de techo en masa sísmica.

## Resultados vigentes

- `Tx* = 0.400467 s`, modo 2.
- `Ty* = 0.400492 s`, modo 1.
- `Tz* = 0.354297 s`, modo 3.
- Peso sísmico total: `5248.471 tonf`.
- `Q0x = 771.525 tonf`.
- `Q0y = 771.525 tonf`.

## Sensibilidad controlada

La comparación clave no viene de Excel; viene de corridas controladas donde solo se cambia la asignación de cachos rígidos. El patrón observado fue:

| Variante | Tx/Ty aprox. [s] | Lectura |
| --- | ---: | --- |
| Ambos cachos + SCT 0.25 | `0.404` | Modelo inicial antes de corregir masa de techo |
| Ambos cachos + SCT 0 | `0.400` | Modelo vigente alineado con ambos cachos |
| Sin cachos en columnas | `0.468` | Se acerca a valores reportados cerca de `0.47` |
| Sin cachos en vigas | `0.424` | Aumenta poco respecto de ambos cachos |
| Sin cachos en vigas ni columnas | `0.484` | Entra en el rango alto observado |

La diferencia por `SCT` es pequeña: pasar de `SCT=0.25` a `SCT=0` mueve el período de aproximadamente `0.404 s` a `0.400 s`. Eso no explica períodos de `0.47-0.51 s`.

## Diagnóstico

Con los datos controlados, el período bajo de `~0.40 s` aparece cuando el modelo tiene cachos rígidos automáticos `0.75` efectivamente asignados en vigas y columnas. El rango `~0.47 s` aparece en nuestro propio ensayo cuando las columnas no tienen activo el efecto de cacho rígido, aunque las vigas sí lo tengan.

Por lo tanto, si otro modelo tiene igual geometría, secciones, masa, diafragma, apoyos y materiales, pero da `~0.47-0.51 s`, el primer punto a revisar no es el Excel: es si las columnas quedaron realmente con `Automatic from Connectivity` y `Rigid-zone factor = 0.75`, o si se seleccionaron solo vigas, si las columnas quedaron con factor cero, si una operación posterior reemplazó offsets, o si la UI muestra una selección mixta que parece correcta pero no lo es.

Otros factores que pueden subir período, pero no fueron el efecto dominante en nuestras pruebas:

- Menor rigidez de material o módulo elástico distinto.
- Dimensiones de columnas/vigas menores que las del enunciado.
- Releases indebidos en marcos.
- Diafragma no asignado a todas las losas.
- Masa sísmica duplicada o patrones mal incluidos.
- Modelo desbloqueado y guardado después de cambios manuales no trazados.

## Conclusión defendible

No se puede declarar que los compañeros estén mal solo por el número. Sí se puede decir que, con el enunciado leído literalmente y con cachos rígidos `0.75` efectivos en vigas y columnas, nuestro modelo queda en `Tx/Ty ~ 0.40 s`. La hipótesis más fuerte para explicar `0.47-0.51 s` es que esos modelos no están aplicando efectivamente el cacho rígido en columnas, o tienen otro cambio de rigidez que alarga el sistema.

Para comparar limpiamente, ambos modelos deben mostrar tablas/exportaciones de: Frame End Length Offsets para vigas y columnas, Mass Source, secciones, materiales, releases, diafragmas y tabla modal con masas participantes.
