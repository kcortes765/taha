# Feature V01 — Validación Cruzada API vs UI Guide

**Estado**: ✅ COMPLETADA
**Fecha**: 2026-03-21

## Resumen

Validación exhaustiva fase por fase (FASE 0-12) comparando los 13 scripts API (`autonomo/scripts/`) contra la guía UI (`docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md`).

## Resultados

Se encontraron **14 discrepancias**:
- **3 CRÍTICAS**: Shell-Thin vs Thick (D01), TERT omitido en Mass Source (D02), AutoMesh 0.4m vs 1.0m (D03)
- **4 MODERADAS**: Es acero incorrecto en guía (D04), conversión fy/fu aproximada (D05), factores Expected fy/fu (D06), nombre viga VI20/60G30 vs VI20x60G30 (D07)
- **7 MENORES**: SCT en mass source (D08), opciones mass source (D09), nombres sísmicos en config (D10-D11), factores combinaciones (D12, D14), comentario conteo muros (D13)

## Correcciones aplicadas a scripts API

1. **config.py**: `AUTOMESH_SIZE` 0.40 → 1.00 m (D03)
2. **config.py**: `MASS_SOURCE_PATTERNS` — agregado `'TERT': 1.0` (D02)
3. **config.py**: `COMBINATIONS` — corregido SX/SY→SDX/SDY, agregado TERT a todas las combos, corregido factor SCP en C3 (D10-D12, D14)
4. **config.py**: Comentario `N_MUROS_DIR_X` 22→23 segmentos (D13)
5. **02_materials_sections.py**: `SetWall()` — SHELL_THICK→SHELL_THIN para muros (D01)

## Discrepancias NO corregidas (requieren decisión del usuario)

- **D04**: Es acero en guía UI tiene error de orden de magnitud (2,039,000 vs 20,387,400 tonf/m²) — API es correcta, corregir guía
- **D05-D06**: Conversiones aproximadas en guía vs exactas en API — API es más precisa, mantener API
- **D07**: Nombre viga VI20/60G30 vs VI20x60G30 — cosmético, ETABS acepta ambos

## Outputs

- `autonomo/research/validacion_cruzada.md` — Informe completo con análisis detallado
- `autonomo/logs/feature_V01.md` — Este archivo
