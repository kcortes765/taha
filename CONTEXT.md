# CONTEXT — ADSE 1S-2026

## Proyecto
Ramo Análisis y Diseño Sísmico de Edificios, UCN, IX semestre. Material de estudio + pipeline ETABS para taller.

## Archivo de salida
Los materiales de estudio van en `docs/estudio/`. Cada capítulo tiene su propio .md.

## Archivos de referencia

| Archivo | Para qué |
|---------|----------|
| `docs/apuntes/INDICE.md` | Índice maestro — ubicar cualquier tema con archivo y página |
| `docs/apuntes/*.pdf` | 14 PDFs temáticos con los apuntes del curso (leer con `pages`) |
| `docs/Normas Utilizadas ADSE/` | Normas oficiales (NCh433, DS61, DS60, ACI318, NCh3171) |
| `docs/estudio/RESUMEN-ADSE-COMPLETO.md` | Resumen general del curso |
| `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md` | Guía ETABS para taller |
| `autonomo/research/` | Investigaciones del pipeline (API, fórmulas, extractos) |
| `autonomo/scripts/` | Scripts API Python para ETABS |
| `autonomo/research/validacion_cruzada.md` | Discrepancias encontradas entre guía y scripts |
| `autonomo/research/informe_final.md` | Revisión final de calidad |

## Convenciones para material de estudio

### Estructura de cada .md
1. Título + fuente + nota introductoria breve
2. Mapa conceptual ASCII del capítulo
3. Contenido organizado por secciones del PDF original
4. Diagramas ASCII donde el PDF tiene figuras
5. Fórmulas en texto plano con notación clara
6. Notas "Claude:" con contexto, ejemplos reales, conexiones
7. Preguntas tipo control al final de cada sección principal
8. NO agregar relleno — calidad > cantidad

### Estilo
- Español, terminología del profesor Music
- Fórmulas: `Qo = C × I × P` (texto plano, legible)
- Diagramas: ASCII art con box drawing characters
- Tablas: markdown estándar
- Referencias: "Pág X del PDF original" o "Art. X.X.X de [norma]"
- Preguntas tipo control: realistas, como las haría el profesor

### Qué NO hacer
- No inventar contenido que no esté en los apuntes
- No agregar fórmulas que no aparezcan en el PDF
- No simplificar excesivamente — el material es para IX semestre de ingeniería civil
- No romper archivos existentes al editar
