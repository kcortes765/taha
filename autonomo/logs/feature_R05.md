# Feature R05 — Extraer info Material Apoyo Taller — Prof. Music

## Estado: COMPLETADO

## Output
- `autonomo/research/material_apoyo_extracto.md` (~500 líneas, extracto exhaustivo)

## Resumen de lo extraído

El PDF Material Apoyo Taller 2026 (47 páginas) contiene 9 secciones (A–I). Se extrajo TODO:

### Secciones del documento
| Sección | Contenido clave |
|---------|----------------|
| A | Visualización 3D: View Walk, Set Elevation View, DirectX |
| B | Drift NCh433: 2 condiciones, tabla Joint Drifts, Diaphragm Max Over Avg Drifts |
| C | Diafragma rígido: Define → Select → Assign (3 pasos) |
| D | Section Cuts: grupo por piso, coordenadas User Defined |
| E | Ejes ETABS vs SAP: ángulos diferentes (0°=+X en ETABS, 0°=+Y en SAP) |
| F | Diagramas P-M: exportar a Excel, graficar curvas con/sin φ + puntos combos |
| G | 8 sub-combinaciones internas de ETABS para sismo modal espectral |
| H | 3 métodos torsión accidental: a) desplazar CM, b) forma 1 momentos, b) forma 2 excentricidad |
| I | 4 variantes de combinaciones de carga (19, 19, 19, 27 combos según método) |

### Hallazgos críticos
1. ETABS genera 8 sub-combos por cada combo con sismo (variación de signos P/V/M)
2. NO restar desplazamientos CQC manualmente — Drift X/Y ya son la razón correcta
3. Error tipográfico en combo 15: dice TEX, debería ser TEY
4. Para M-φ usar SAP, para P-M usar ETABS
5. Método a) requiere 5 mass sources + 4 NL estáticos auxiliares + 4 modales + 6 RS
6. Tabla "Diaphragm Max Over Avg Drifts" es la forma directa de encontrar nodo más desfavorable

## Método
- pdftotext -layout para extraer texto del PDF
- Lectura completa de las 759 líneas extraídas
- Organización por sección con tablas, fórmulas y menús exactos ETABS
