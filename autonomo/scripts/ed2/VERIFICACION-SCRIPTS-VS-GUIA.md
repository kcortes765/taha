# Verificacion Scripts Ed.2 vs Guia UI Ed.2

**Fecha**: 2026-03-22
**Archivos comparados**:
- `autonomo/scripts/ed2/config_ed2.py` + scripts 01-12
- `docs/estudio/GUIA-EDIFICIO2-MARCOS-ETABS-v19.md`

---

## Resumen

| Categoria | Parametros verificados | OK | ERROR | Corregido |
|-----------|----------------------|----|----|-----------|
| Grilla | 4 | 4 | 0 | - |
| Pisos | 4 | 4 | 0 | - |
| Materiales G25 | 5 | 5 | 0 | - |
| Materiales A630-420H | 5 | 3 | 2 | Si |
| Secciones | 10 | 10 | 0 | - |
| Property Modifiers | 9 | 9 | 0 | - |
| Cardinal Point (Insertion) | 2 | 0 | 2 | Si |
| RZF | 2 | 1 | 1 | Si |
| Cargas | 5 | 5 | 0 | - |
| Mass Source | 4 | 4 | 0 | - |
| Torsion | 3 | 3 | 0 | - |
| Combinaciones | 7 | 7 | 0 | - |
| AutoMesh | 1 | 1 | 0 | - |
| **TOTAL** | **61** | **56** | **5** | **5/5** |

---

## Detalle parametro por parametro

### Grilla
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| Ejes X | 6 (1-6), 0-32.5m | 6 (1-6), 6.5m spacing | OK |
| Ejes Y | 6 (A-F), 0-32.5m | 6 (A-F), 6.5m spacing | OK |
| Spacing | 6.5m uniforme | 6.5m uniforme | OK |
| Area planta | 1056.25 m2 | 32.5x32.5 = 1056.25 m2 | OK |

### Pisos
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| N pisos | 5 | 5 | OK |
| h1 | 3.50m | 3.50m | OK |
| h_typ | 3.00m | 3.00m | OK |
| H total | 15.50m | 15.50m | OK |

### Materiales — Hormigon G25
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| f'c | 25 MPa = 2548.4 tonf/m2 | 25 MPa = 250 kgf/cm2 | OK |
| Ec | 4700*sqrt(25) = 23500 MPa = 2,395,520 tonf/m2 | 2,395,520 tonf/m2 | OK |
| gamma | 2.50 tonf/m3 | 2.5 tonf/m3 | OK |
| Poisson | 0.20 | 0.2 | OK |
| Factor 101.937 | Correcto | Correcto | OK |

### Materiales — Acero A630-420H
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| fy | 420 MPa = 42,814 tonf/m2 | 42,814 tonf/m2 | OK |
| fu | 630 MPa = 64,220 tonf/m2 | 64,220 tonf/m2 | OK |
| Es | 210,000 MPa = 21,406,770 tonf/m2 | 21,406,770 tonf/m2 | OK |
| **fye** | **~~fy*1.17=50,052 tonf/m2~~** | **fy*1.1=47,095 tonf/m2** | **ERROR → CORREGIDO** |
| **fue** | **~~fu*1.08=69,358 tonf/m2~~** | **fu*1.1=70,642 tonf/m2** | **ERROR → CORREGIDO** |

**Fix aplicado**: `config_ed2.py` lineas 209-210: factores cambiados a 1.10 para ambos.

### Secciones
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| C70x70G25 | 0.70x0.70, G25, P1-P2 | 0.70x0.70, G25, P1-P2 | OK |
| C65x65G25 | 0.65x0.65, G25, P3-P5 | 0.65x0.65, G25, P3-P5 | OK |
| V50x70G25 | 0.50x0.70, G25, P1-P2 | 0.50x0.70, G25, P1-P2 | OK |
| V45x70G25 | 0.45x0.70, G25, P3-P5 | 0.45x0.70, G25, P3-P5 | OK |
| L17G25 | Shell-Thin, 0.17m, G25 | Shell-Thin, 0.17m, G25 | OK |
| SECTIONS_BY_STORY | P1-2→70/50, P3-5→65/45 | P1-2→70/50, P3-5→65/45 | OK |
| Columnas 36/piso | 36 (6x6) | 36 (6x6) | OK |
| Vigas 60/piso | 60 (30X+30Y) | 60 (30X+30Y) | OK |
| Losas 25/piso | 25 (5x5) | 25 (5x5) | OK |
| Totales | 180col+300vig+125losa | 180col+300vig+125losa | OK |

### Property Modifiers
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| Col I22 | 0.70 | 0.70 | OK |
| Col I33 | 0.70 | 0.70 | OK |
| Col J | 1.0 | 1 | OK |
| Viga I22 | 0.35 | 0.35 | OK |
| Viga I33 | 0.35 | 0.35 | OK |
| Viga J | 0.0 | 0 (practica chilena) | OK |
| Losa m11 | 0.25 | 0.25 | OK |
| Losa m22 | 0.25 | 0.25 | OK |
| Losa m12 | 0.25 | 0.25 | OK |

### Cardinal Point / Insertion Point
| Parametro | config_ed2.py (antes) | Guia Ed.2 | Resultado |
|-----------|----------------------|-----------|-----------|
| **Cardinal Point** | **~~CP=10 (Centroid)~~** | **CP=8 (Top Center)** | **ERROR → CORREGIDO** |
| **StiffTransform** | **~~No (no needed for centroid)~~** | **True** | **ERROR → CORREGIDO** |

**Fix aplicado**:
- `config_ed2.py`: `VIGA_CARDINAL_POINT = CP_TOP_CENTER` (8)
- `04_beams_ed2.py`: docstring actualizado
- `06_assignments_ed2.py`: nuevo Step 1 `set_beam_insertion_point()` con CP=8 + StiffTransform=True

**Impacto**: Las vigas convencionales cuelgan bajo la losa. Con CP=10 (centroide), el eje del beam queda a media altura del nivel de piso (irrealista). Con CP=8 (Top Center), la cara superior coincide con el nivel de losa (correcto).

### RZF (Rigid End Zones)
| Parametro | 06_assignments (antes) | Guia Ed.2 | Resultado |
|-----------|----------------------|-----------|-----------|
| RZF valor | 0.75 | 0.75 | OK |
| **Aplicado a** | **~~Todos los frames~~** | **Solo vigas** | **ERROR → CORREGIDO** |

**Fix aplicado**: `06_assignments_ed2.py`: `apply_rigid_end_zones()` ahora filtra por BEAM_SECTIONS y solo aplica RZF a vigas V50x70G25 y V45x70G25.

### Cargas
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| TERP | 0.140 tonf/m2, SuperDead, P1-4 | 0.140 tonf/m2, Super Dead, P1-4 | OK |
| TERT | 0.100 tonf/m2, SuperDead, P5 | 0.100 tonf/m2, Super Dead, P5 | OK |
| SCP | 0.300 tonf/m2, Live, P1-4 | 0.300 tonf/m2, Live, P1-4 | OK |
| SCT | 0.100 tonf/m2, RoofLive, P5 | 0.100 tonf/m2, Roof Live, P5 | OK |
| PP | Dead, SWM=1 | Dead, SWM=1 | OK |

### Mass Source
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| PP | 1.0 (via IncludeElements) | 1 | OK |
| TERP | 1.0 | 1 | OK |
| TERT | 1.0 | 1 | OK |
| SCP | 0.25 | 0.25 | OK |

**Nota**: SCT no incluido en mass source — correcto (guia tambien lo excluye).

### Torsion Accidental
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| ea_X | 0.10 * 32.5 = 3.25m | 3.25m constante | OK |
| ea_Y | 0.10 * 32.5 = 3.25m | 3.25m constante | OK |
| Formula | Dinamica CONSTANTE (no Zk/H) | Dinamica CONSTANTE | OK |

### Combinaciones NCh3171
| Combo | config_ed2.py COMBINATIONS | Guia Ed.2 | Resultado |
|-------|---------------------------|-----------|-----------|
| C1 | 1.4D | 1.4D | OK |
| C2 | 1.2D + 1.6*SCP + 0.5*SCT | 1.2D + 1.6L + 0.5Lr | OK |
| C3 | 1.2D + 1.0*SCP + 1.6*SCT | 1.2D + 1.0L + 1.6Lr | OK |
| C4 | 1.2D + 1.0*SCP + 0.5*SCT + 1.4*SDX | 1.2D + 1.0L + 0.5Lr + 1.4E | OK |
| C5 | 0.9D + 1.4*SDX | 0.9D + 1.4E | OK |
| C6 | 1.2D + 1.0*SCP + 0.5*SCT + 1.4*SDY | 1.2D + 1.0L + 0.5Lr + 1.4E | OK |
| C7 | 0.9D + 1.4*SDY | 0.9D + 1.4E | OK |

Donde D = PP + TERP + TERT (correcto en ambos).

**Nota**: `10_combinations_ed2.py` crea 11 combos (con ± explicitos), la guia dice que RS auto-maneja ±. Redundante pero no erroneo.

### AutoMesh
| Parametro | config_ed2.py | Guia Ed.2 | Resultado |
|-----------|--------------|-----------|-----------|
| Max size | 1.00m | 1.0m | OK |

---

## Errores encontrados y corregidos

### ERROR 1: Cardinal Point (CRITICO)
- **Archivo**: config_ed2.py, 04_beams_ed2.py, 06_assignments_ed2.py
- **Antes**: CP=10 (Centroid), sin StiffTransform
- **Despues**: CP=8 (Top Center), StiffTransform=True
- **Impacto**: Afecta posicion vertical de vigas y rigidez del marco

### ERROR 2: Expected stress factors (MENOR)
- **Archivo**: config_ed2.py lineas 209-210
- **Antes**: fye = fy*1.17, fue = fu*1.08
- **Despues**: fye = fy*1.10, fue = fu*1.10
- **Impacto**: Solo afecta diseno de capacidad (no analisis)

### ERROR 3: RZF scope (MENOR)
- **Archivo**: 06_assignments_ed2.py
- **Antes**: RZF aplicado a TODOS los frames (columnas + vigas)
- **Despues**: RZF aplicado solo a vigas
- **Impacto**: Pequeño — columnas no deberian tener rigid end zones

---

## Archivos modificados

1. `autonomo/scripts/ed2/config_ed2.py`
   - Linea 241-243: VIGA_CARDINAL_POINT → CP_TOP_CENTER (8)
   - Lineas 209-210: EFY/EFU factors → 1.10

2. `autonomo/scripts/ed2/04_beams_ed2.py`
   - Linea 15-16: Docstring actualizado CP=8
   - Linea 212-214: Log summary actualizado

3. `autonomo/scripts/ed2/06_assignments_ed2.py`
   - Nuevo Step 1: set_beam_insertion_point() con CP=8 + StiffTransform
   - Step 2 (ex-1): apply_rigid_end_zones() ahora filtra solo vigas
   - Steps renumerados (2→3, 3→4, 4→5, 5→6)
   - Import VIGA_CARDINAL_POINT agregado
   - BEAM_SECTIONS set para filtrado
