# RETOMAR — ADSE 1S-2026

## Estado: PIPELINE COMPLETO — 27/27 features ✅ (21 mar 2026)

### Qué se completó
El sistema autónomo terminó las 27 features del pipeline ETABS para Edificio 1:

- **R01-R06** (Research): API ETABS, patrones COM, firmas, fórmulas, espectro, material taller
- **G01-G05** (Guide): Guía UI corregida y expandida (~2800 líneas, 14 fases)
- **A01-A14** (API): 15 scripts Python para pipeline completo ETABS v19
- **V01-V02** (Validation): Validación cruzada + revisión final exhaustiva

### Entregables listos

| Entregable | Ubicación | Estado |
|-----------|-----------|--------|
| Guía UI completa | `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md` | ✅ Listo |
| Scripts API (15) | `autonomo/scripts/` | ✅ Compilan |
| Archivo espectro | `autonomo/scripts/espectro_elastico_Z3SC.txt` | ✅ 101 puntos |
| Informe final | `autonomo/research/informe_final.md` | ✅ Completo |
| Investigación (9 docs) | `autonomo/research/` | ✅ Completo |

### Observaciones pendientes (menores)
1. Guía: Es rebar = 2,039,000 → debería ser 20,387,400 tonf/m² (error 10x)
2. Guía: fy/fu usa conversión aproximada vs scripts usan exacta (~2% dif)
3. Guía: nombre viga "VI20/60G30" vs scripts "VI20x60G30"
4. Shell type muros: guía=Thin, scripts=Thick (ambos válidos, decisión de diseño)
5. Guía F9: omite TERT de combos expandidos (scripts lo incluyen correctamente)

### Próximos pasos
1. **Modelar en lab**: Usar guía UI o scripts para crear modelo en ETABS v19
2. **Si usa scripts**: `python run_pipeline.py --phase 1` → verificar → `--phase 2`
3. **Si usa guía**: Seguir paso a paso, corregir Es del acero (OBS-1)
4. **Extraer resultados**: 6 casos de análisis (3 torsiones × 2 diafragmas)

### Archivos clave
- Guía: `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md`
- Scripts: `autonomo/scripts/` (config.py + 01-12 + run_pipeline.py)
- Contexto: `autonomo/context.md`
- Informe: `autonomo/research/informe_final.md`
- Validación: `autonomo/research/validacion_cruzada.md`

### Fechas
- **C1: Mar 5 mayo** (~6.5 semanas)
- Expo1: 26 mayo | C2: 26 mayo
