# PLAN MAESTRO — ADSE 1S-2026
> Generado: 2026-03-21 | Alcance: estudio C1 + perfeccionamiento outputs + material completo

---

## Fase 1: Verificar y corregir outputs del pipeline autónomo (FIX)

| ID | Tarea | Descripción |
|----|-------|-------------|
| FIX01 | Corregir discrepancias críticas en scripts API | Aplicar las 3 correcciones críticas de V01: Shell type muros, TERT en Mass Source, AutoMesh. Corregir config.py (nombres SDX/SDY, TERT en combos, factor SCP en C3) |
| FIX02 | Corregir errores en guía ETABS | Es rebar 2,039,000→20,387,400, fy/fu conversión exacta, nombre viga VI20x60G30, TERT en combos expandidos |

## Fase 2: Perfeccionar material de estudio existente (PERF)

| ID | Tarea | Descripción |
|----|-------|-------------|
| PERF01 | Perfeccionar 01-Aspectos-Conceptuales.md | Reescribir leyendo el PDF original. Eliminar relleno, agregar claridad. Foco en: diafragmas (rígido/flexible/IF), matrices de rigidez (eq. directo vs rig. directa), clasificación edificios, procedimiento modal espectral 9 etapas. Diagramas ASCII precisos. Preguntas tipo control al final de cada sección. |
| PERF02 | Perfeccionar 02a-Conceptos-Fundamentales.md | Reescribir leyendo el PDF original. Foco en: Riesgo=Peligro×Vulnerabilidad, rigidez vs ductilidad vs energía, diseño convencional vs aisladores vs disipadores, etapas proyecto. Menos texto, más claridad conceptual. Preguntas tipo control. |

## Fase 3: Crear material de estudio para C1 — Sismología (STU-C1)

| ID | Tarea | Descripción |
|----|-------|-------------|
| STU01 | Crear 02b-Normativa-NCh433-DS61.md | Leer PDF 02b (25 págs). Cubrir: normas vigentes Chile, principios NCh433, zonificación (mapa, Ao), tipos de suelo DS61 (tabla A-F, Vs30), métodos geofísicos (MASW, ReMi), ejemplo clasificación suelo. Diagramas ASCII, preguntas tipo control. |
| STU02 | Crear 02c-Analisis-Estatico.md | Leer PDF 02c (16 págs). Cubrir: clasificación edificio (I), R y Ro, estados carga NCh3171, corte basal Qo=CIP, coeficiente sísmico C (fórmula, límites), fuerzas por piso, torsión accidental, diafragma rígido vs flexible, verificación deformaciones. Ejemplos numéricos con datos del taller. |
| STU03 | Crear 02d-Analisis-Dinamico-Modal-Espectral.md | Leer PDF 02d (15 págs). Cubrir: espectro diseño Sa, α(T), R*, modos (≥90% masa), CQC, torsión accidental (2 formas), condiciones drift (0.002 CM, 0.001 extremo), espectro desplazamiento. Ejemplo numérico con datos del taller. |

## Fase 4: Crear material de estudio para C2 — Análisis (STU-C2)

| ID | Tarea | Descripción |
|----|-------|-------------|
| STU04 | Crear 02e-Diseno-Edificios-R-Pushover.md | Leer PDF 02e (25 págs). Cubrir: 5 preguntas fundamentales, condiciones diseño, matrices rigidez (simetría 1 y 2 ejes), pushover (curva V-Δ), composición R*=FSRE×FIRNL×FDED, ejemplo 15+1 pisos Antofagasta, columna fuerte-viga débil, visión integral. |
| STU05 | Crear 02f-Perfil-Biosismico.md | Leer PDF 02f (27 págs). Cubrir: 13 indicadores con fórmula y criterio de cada uno, artículo Soto & Music (Antofagasta), puntos débiles edificio, análisis complementarios, diseño basado en desempeño (VISION 2000). |

## Fase 5: Crear material de estudio para C3 — Diseño (STU-C3)

| ID | Tarea | Descripción |
|----|-------|-------------|
| STU06 | Crear 03a-Muros-Normativa-y-Fallas.md | Leer PDF 03a (13 págs). Cubrir: evolución normativa muros Chile, modos de falla (corte/flexión/deslizamiento), efecto confinamiento, daños 27F, diferencias antes/después DS60. |
| STU07 | Crear 03b-Muros-Diseno.md | Leer PDF 03b (56 págs). EL MÁS IMPORTANTE PARA C3. Cubrir: esbeltez, compresión máx, diseño corte (Vc, Vs, αc, diagrama flujo), flexión compuesta (diagrama interacción, secciones T/L/C), curvatura (φu=0.008/c), confinamiento (clim, cc, Ash), detallamiento armaduras. Ejemplos numéricos paso a paso. |
| STU08 | Crear 03c-Muros-Predimensionamiento.md | Leer PDF 03c (12 págs). Cubrir: fotos muros reales, predimensionamiento por corte, ejemplo 16 pisos, disposiciones DS60. |
| STU09 | Crear 04-Marcos-Especiales-HA.md | Leer PDF 04 (32 págs). Cubrir: vigas (geométricas, longitudinal, transversal con Mpr), columnas (longitudinal, transversal, confinamiento), columna fuerte-viga débil (ΣMnc≥1.2ΣMnb), nudo (Vn, confinamiento). |
| STU10 | Crear 05a-Analisis-Estructural-ACI318.md | Leer PDF 05a (16 págs). Cubrir: esbeltez columnas (diagrama flujo), análisis 1er orden (magnificación momentos), 2do orden (P-Delta), inelástico, elementos finitos. |

## Fase 6: Problemas resueltos y ayudas de estudio (AID)

| ID | Tarea | Descripción |
|----|-------|-------------|
| AID01 | Resolver problemas propuestos 05b | Leer PDF 05b (24 págs). Resolver paso a paso los problemas tipo control: Prob 1 (rigidez rotacional, matriz rigidez), Prob 2 (asimetría, CM/CR), Prob 3 (Vs30, método estático, fuerzas por piso). Incluir procedimiento completo. |
| AID02 | Crear guía rápida de fórmulas para C1 | Compilar TODAS las fórmulas relevantes para C1 en una hoja de referencia rápida de 2-3 páginas. Organizar por tema. Solo fórmulas, sin explicación extensa. |
| AID03 | Actualizar RESUMEN-ADSE-COMPLETO.md | Integrar todo el material nuevo en el resumen. Verificar coherencia con los apuntes perfeccionados. |

## Fase 7: Cierre (CLOSE)

| ID | Tarea | Descripción |
|----|-------|-------------|
| CLOSE01 | Actualizar RETOMAR.md y memoria | Actualizar estado del proyecto con todo lo completado. |

---

## Resumen
- **20 features** en 7 fases
- **Prioridad**: FIX (corregir) → PERF (perfeccionar existente) → STU-C1 (crear para C1) → STU-C2/C3 (crear resto) → AID (ayudas) → CLOSE
- **C1 es el 5 mayo**: las fases 1-3 + AID01-02 son críticas
- Cada feature de estudio lee el PDF original y produce un .md de calidad enfermiza
