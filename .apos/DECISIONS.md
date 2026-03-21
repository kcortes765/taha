# DECISIONS — ADSE 1S-2026

## DEC-001 — Automatizar modelado ETABS via Python COM API
- Fecha: ~2026-02 (retroactiva)
- Decisor: Humano
- Contexto: El taller requiere modelar 2 edificios en ETABS. Hacerlo manual toma horas y es propenso a errores. El alumno tiene experiencia en Python.
- Decisión: Pipeline de 13 scripts Python que controlan ETABS 19 via comtypes COM API
- Alternativas descartadas: Modelado manual en ETABS (lento, no reproducible), importar desde CAD (no disponible)
- Estado: vigente

## DEC-002 — Stack vanilla para App C1
- Fecha: ~2026-02 (retroactiva)
- Decisor: Humano
- Contexto: Se necesitaba una app de estudio para el Control 1. No se quería setup complejo.
- Decisión: HTML+CSS+JS vanilla, Three.js r128, Chart.js 4.4.1, MathJax 3 (CDN)
- Alternativas descartadas: React (overkill), Streamlit (limitado para interactivos 3D)
- Estado: vigente

## DEC-003 — Separar pipeline en 2 sesiones COM (fase 1 geometría, fase 2 análisis)
- Fecha: 2026-03-05
- Decisor: Claude + Humano
- Contexto: La sesión COM de ETABS 19 muere después de geometría pesada (1720 areas + mesh). RPC error -2147023174.
- Decisión: run_all.py soporta --fase 1/2/all. ETABS se reinicia entre fases.
- Estado: vigente

## DEC-004 — Losas modeladas como huella real (no envolvente)
- Fecha: 2026-03-10
- Decisor: Claude + Humano
- Contexto: Las losas cubrían la envolvente completa (532 m²) en vez de la huella real (468 m²), generando masa y CM incorrectos.
- Decisión: 7 paneles por piso tipo, 5 por techo, con gap para shaft. Área real = 468.4 m².
- Estado: vigente

## DEC-005 — Eje F: muro horizontal de 7.7m centrado en eje 10
- Fecha: 2026-03-20
- Decisor: 3 IAs (validación cruzada) + Humano
- Contexto: Controversia sobre si eje F tenía 2 stubs laterales (4-5, 14-15) o 1 muro central. Planos pág 3, 7 confirman muro central.
- Decisión: Coordenada directa GRID_X['10']-4.25 a GRID_X['10']+3.45 (no alineado con grilla)
- Estado: vigente

## DEC-006 — Muros dir Y divididos en bloque sur (A-C) y norte (D-F)
- Fecha: 2026-03-20
- Decisor: IA + validación contra elevaciones (page6)
- Contexto: Los muros no cruzan el pasillo C-D. Se dividen en 2 tramos para cada eje.
- Decisión: MUROS_DIR_Y separados por bloque. Ejes 6,7,15 solo norte; 8,9,10 stubs sur.
- Estado: vigente — pendiente verificación visual en ETABS

## DEC-007 — Geometría requiere auditoría visual antes de avanzar a fase 2
- Fecha: 2026-03-20
- Decisor: Humano
- Contexto: 3 iteraciones de config.py por diferentes IAs. Ninguna ha producido geometría visualmente correcta en ETABS.
- Decisión: No avanzar a fase 2 (análisis) hasta confirmar geometría visualmente.
- Estado: vigente — bloqueante

## DEC-008 — Cambiar de pipeline COM a modelación manual en ETABS v19
- Fecha: 2026-03-20
- Decisor: Humano
- Contexto: El pipeline COM tuvo 3 iteraciones de geometría sin resultado visual correcto. La sesión COM es inestable (RPC errors). El enfoque manual permite seguir al profesor y compañeros en clase, y usar la guía como referencia paralela.
- Decisión: Modelar Ed.1 manualmente en ETABS v19, con guía paso a paso exhaustiva generada por IA. Pipeline COM se preserva como referencia.
- Alternativas descartadas: Seguir iterando config.py (3 intentos fallidos), importar DXF (no disponible)
- Estado: vigente

## DEC-009 — Enfoque dual: guía UI perfecta + scripts API Python
- Fecha: 2026-03-20
- Decisor: Humano
- Contexto: La guía manual (DEC-008) sigue siendo el enfoque principal, pero el usuario quiere también scripts API perfectos como backup y para automatización futura. Requiere investigación exhaustiva de CSI OAPI.
- Decisión: Producir ambos entregables via agente autónomo (27 features, ~8-10h). Orquestador Python maneja rate limits y continuidad.
- Alternativas descartadas: Solo guía manual (pierde automatización), solo API (ya falló 3 veces sin investigación previa)
- Estado: vigente
