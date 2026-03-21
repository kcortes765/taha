# Log Feature R03 — Research firmas COM reales

**Fecha**: 20 marzo 2026
**Duración estimada**: ~15 min
**Estado**: COMPLETADO

## Qué se hizo

Investigación exhaustiva de las firmas COM exactas de 40+ funciones críticas del ETABS v19 OAPI para Python + comtypes.

### Metodología
1. Se usó R01 (etabs_api_reference.md) como base
2. Se lanzaron 3 agentes en paralelo:
   - Agente 1: Investigación de docs oficiales CSI para cada función
   - Agente 2: Búsqueda en repos GitHub reales (danielogg92, ebrahimraeyat, retug, mihdicaballero, mtavares51)
   - Agente 3: Investigación de inconsistencias entre versiones v17-v22
3. Se realizaron 8+ búsquedas web específicas por función
4. Se compiló todo en un documento único con tabla resumen

## Output
- `autonomo/research/com_signatures.md` (~800 líneas)

## Hallazgos CRÍTICOS

### 1. `FuncRS.SetFromFile` NO EXISTE EN ETABS
- Es una función de SAP2000, no de ETABS
- Esto explica el error "wrong number of arguments" en `08_spectrum_cases.py`
- **Fix**: Usar `FuncRS.SetUser(name, n, T[], Sa[], damping)` leyendo el archivo manualmente en Python

### 2. `PropArea.SetShell_1` NO EXISTE EN ETABS
- Es de SAP2000. ETABS usa `SetWall`, `SetSlab`, `SetDeck` por separado
- Si aparece en código "para ETABS", fue adaptado incorrectamente de SAP2000

### 3. `SetMassSource_1` está en `SapModel.PropMaterial`, NO en `SapModel.MassSource`
- Contraintuitivo pero confirmado por docs oficiales CSI
- Solo cambia el mass source por defecto (no crea nuevos)

### 4. Patrón `_1` de CSI
- Cuando agregan parámetros a una función, crean versión `_1` y deprecan la original
- `SetOConcrete` (8 args) → `SetOConcrete_1` (9-12 args)
- `SetOSteel` → `SetOSteel_1`

### 5. API forward-compatible desde v18
- Código v18 funciona en v19 sin cambios
- Funciones nuevas de v20+ no están en v19

### 6. `Results.JointDrifts` existe pero es inestable via comtypes
- Documentado en API 2016, debería funcionar en v19
- Si falla, usar `StoryDrifts()` o `DatabaseTables.GetTableForDisplayArray("Story Drifts")`

### 7. Bug GetNameList post-creación en v19
- `FrameObj.GetNameList()` puede retornar 0 después de crear frames exitosamente
- Problema de binding COM, no de la API real

## Impacto en el pipeline

| Problema anterior | Fix identificado |
|---|---|
| `SetFromFile` con 7 args falla | Usar `SetUser` con arrays |
| `SetMassSource_1` ubicación incierta | Está en `PropMaterial` |
| `SetShell_1` mencionado en scripts | Usar `SetWall`/`SetSlab` |
| GetNameList retorna 0 | Bug de binding, verificar en UI |
| comtypes cache stale | `py -m comtypes.clear_cache` |

## Fuentes consultadas
- Docs CSI oficiales (API 2015/2016)
- 5 repos GitHub con código real
- Eng-Tips (5+ threads)
- stru.ai, Medium (Hakan Keskin), EngineeringSkills
- ResearchGate (pregunta sobre RS functions via OAPI)
- Release notes ETABS v18-v22
