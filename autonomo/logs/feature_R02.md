# Log — Feature R02: Research Python + comtypes + ETABS — Patrones y Ejemplos

**Estado**: COMPLETADA
**Fecha**: 20 marzo 2026
**Output**: `autonomo/research/python_etabs_patterns.md`

## Resumen

Investigación exhaustiva de patrones de uso de Python con ETABS via comtypes. Se consultaron:
- 8 repositorios GitHub con código real verificado
- 4 paquetes PyPI (comtypes, etabs-api, pytabs, Sap2000py)
- 10+ tutoriales y blogs (Stru.ai, Hakan Keskin, NeutralAXIS, Re-Tug, VIKTOR, EngineeringSkills)
- 11 threads Eng-Tips (foro principal para ETABS API)
- Documentación oficial CSI (docs.csiamerica.com, wiki, developer portal)
- Release notes de ETABS v19-v22

## Contenido del documento

El documento cubre 15 secciones:

1. **Ecosistema completo** — 8 repos GitHub, 4 paquetes PyPI, 10+ tutoriales, documentación CSI, foros
2. **Conexión COM** — 3 métodos verificados con snippets de repos reales + patrón robusto compilado
3. **Ciclo de vida COM** — Desconexión, try/finally, separación de sesiones, protección GC
4. **Manejo de errores** — Return values, verificación post-creación, patrón handle()
5. **Materiales** — Get/Set concreto y acero (adaptado para Chile: G30, A630-420H)
6. **Geometría** — Frames, areas, puntos, secciones, cardinal points, AutoMesh, diafragma
7. **Cargas** — Load patterns, cargas uniformes a áreas
8. **Análisis** — Espectro SetUser (solución definitiva), MassSource, combinaciones NCh3171, DOF
9. **Resultados** — StoryDrifts, JointDrifts (torsión), SectionCuts, BaseReactions
10. **Database Tables** — Listar, leer→DataFrame, escribir/editar, drifts via DB Tables
11. **Diferencias entre versiones** — v17→v22, compatibilidad forward desde v18
12. **Bugs conocidos** — 7 bugs documentados con workarounds verificados
13. **Best practices** — Orden operaciones, unidades, performance, thread safety
14. **Aplicación a nuestro pipeline** — Stack, decisiones confirmadas, workflow lab
15. **Fuentes completas** — 50+ URLs verificadas

## Fuentes consultadas (3 investigaciones paralelas)

### Agente 1: GitHub
- 50+ repos encontrados, 8 significativos documentados
- Snippets de código reales citados con repo fuente
- Patrones comunes identificados: conexión (3 variantes), DB Tables reshape, StoryDrifts

### Agente 2: PyPI + Tutoriales + Foros
- 9 paquetes PyPI relevantes documentados
- 10+ tutoriales con código real
- Eng-Tips confirmado como foro principal (SO tiene casi nada)

### Agente 3: CSI Oficial + Bugs + Versiones
- Documentación oficial localizada (API help files, CHM, wiki, developer portal)
- 8 bugs documentados con workarounds verificados
- Diferencias v17-v22 mapeadas
- Thread safety confirmada: NO thread-safe (COM STA)

## Hallazgos clave

1. **SetUser > SetFromFile**: SetFromFile NO EXISTE en OAPI v19 (confirmado ResearchGate 2023). SetUser funciona 100% en v18+.
2. **Todos los repos usan comtypes** (excepto CSiPy que usa pythonnet). Es el estándar de facto.
3. **Ningún otro repo limpia comtypes.gen** — nuestro bug puede ser específico del lab.
4. **Database Tables API** es significativamente más rápida para operaciones masivas.
5. **API forward-compatible desde v18** — código v18 funciona en v19-v22.
6. **etabs-api (PyPI)** de ebrahimraeyat podría simplificar nuestro pipeline (evaluar).
7. **El patrón GetActiveObject + ETABS manual** es el consenso universal para estabilidad.

## Decisiones tomadas

1. Compilé snippets SOLO de repos reales (citados con fuente) — no inventé código.
2. Adapté ejemplos australianos (danielogg92) a práctica chilena (G30, A630-420H, NCh433).
3. Incluí sección 14 específica para nuestro pipeline con workflow de lab.
4. Documenté alternativa `win32com` aunque no la recomiendo sobre comtypes.

## Documentos auxiliares generados por los agentes

Los agentes crearon 3 documentos intermedios en `docs/estudio/`:
- `ETABS-PYTHON-GITHUB-REPOS.md` — Detalle completo de 8 repos
- `ETABS-Python-Ecosystem-Research.md` — PyPI, tutoriales, foros
- `ETABS-API-RESEARCH.md` — Docs oficiales, bugs, versiones, best practices

Estos complementan el documento final compilado en `autonomo/research/`.
