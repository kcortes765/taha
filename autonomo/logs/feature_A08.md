# Feature A08 — 07_loads.py (patrones y cargas)

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/07_loads.py` (~420 líneas)

## Qué hace el script

### 1. Crea 5 patrones de carga (LoadPatterns.Add)
| Patrón | Tipo ETABS | SWM | Descripción |
|--------|-----------|-----|-------------|
| PP | Dead (1) | 1.0 | Peso propio automático |
| TERP | SuperDead (2) | 0.0 | Terminaciones pisos |
| TERT | SuperDead (2) | 0.0 | Terminaciones techo |
| SCP | Live (3) | 0.0 | Sobrecarga pisos |
| SCT | RoofLive (12) | 0.0 | Sobrecarga techo |

### 2. Elimina patrón "Dead" por defecto
- ETABS crea "Dead" automáticamente en NewGridOnly
- Script lo elimina (o pone SWM=0 como fallback) para evitar doble peso propio

### 3. Clasifica losas por zona y piso
- Obtiene todas las áreas con GetNameList
- Filtra solo losas (sección = Losa15G30) via GetProperty
- Obtiene coordenadas esquinas via GetPoints + GetCoordCartesian
- Clasifica por elevación Z: piso (stories 1-19) vs techo (story 20)
- Para pisos: clasifica por rango Y → corredor (ejes C-D) vs oficina

### 4. Aplica cargas uniformes (AreaObj.SetLoadUniform, Dir=6)
| Zona | TERP | SCP | TERT | SCT |
|------|------|-----|------|-----|
| Piso oficina | -0.140 | -0.250 | — | — |
| Piso pasillo | -0.140 | -0.500 | — | — |
| Techo | — | — | -0.100 | -0.100 |

Valores en tonf/m². Negativos = gravedad (Dir=6 = Global Z up).

### 5. Verificación
- Confirma que los 5 patrones existen (GetNameList)
- Resumen de asignaciones por zona
- Estimación de peso total por sobrecarga (para validación)

## Conteos esperados
- Losas piso: 133 (7 paneles × 19 pisos)
  - Oficinas: 95 (5 paneles × 19)
  - Pasillos: 38 (2 paneles × 19)
- Losas techo: 5
- Total: 138 losas
- Total asignaciones de carga: 276 (TERP×133 + SCP×133 + TERT×5 + SCT×5)

## Firmas COM utilizadas (verificadas contra com_signatures.md)
- `LoadPatterns.Add(Name, MyType, SWM, AddAnalysisCase)` — §9.1
- `LoadPatterns.Delete(Name)` — eliminación patrón
- `LoadPatterns.SetSelfWtMultiplier(Name, Value)` — fallback
- `LoadPatterns.GetNameList()` — verificación
- `AreaObj.SetLoadUniform(Name, LoadPat, Value, Dir, Replace)` — §9.2
- `AreaObj.GetNameList()` — enumerar áreas
- `AreaObj.GetProperty(Name)` — obtener sección
- `AreaObj.GetPoints(Name)` — obtener puntos esquina
- `PointObj.GetCoordCartesian(Name)` — coordenadas punto

## Detección de pasillo
- Criterio: losa con min(Y) ≈ Y_C (6.446) y max(Y) ≈ Y_D (7.996)
- Tolerancia: 0.15m
- Corresponde a paneles 4 y 5 de SLAB_PANELS_FLOOR en config.py

## Fuentes consultadas
- config.py: LOAD_PATTERNS, valores de carga, GRID_Y, SLAB_PANELS
- com_signatures.md: §9.1 (LoadPatterns.Add), §9.2 (SetLoadUniform)
- etabs_api_reference.md: §13 (LoadPatterns), §11.4 (SetLoadUniform)
- python_etabs_patterns.md: patrones de código verificados
- Enunciado Taller ADSE 1S-2026: valores de carga
