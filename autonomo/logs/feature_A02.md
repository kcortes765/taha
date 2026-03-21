# Feature A02 — 01_init_model.py (modelo nuevo + grilla)

## Estado: COMPLETADO
**Fecha**: 2026-03-21

## Output
- `autonomo/scripts/01_init_model.py` (~549 lineas, 11 funciones)

## Que hace el script

### Pipeline de 5 pasos:
1. **init_model** — `SapModel.InitializeNewModel(12)` (Tonf_m_C)
2. **create_grid_and_stories** — `File.NewGridOnly(20, 2.6, 3.4, 17, 6, avg_x, avg_y)`
   - Crea 20 pisos con h1=3.40m, h2-20=2.60m (H_total=52.80m)
   - Crea grilla uniforme placeholder (17x6 lineas)
3. **edit_grid_via_database_tables** — Edita grilla a coordenadas exactas
   - Metodo primario: DatabaseTables API ("Grid Definitions - Grid Lines")
   - Fallback 1: GridSys.SetGridSys_2 (si existe en v19)
   - Fallback 2: Log manual con tabla de posiciones (la grilla es solo visual)
4. **verify** — Verifica stories (n=20, H=52.8m), grilla y unidades (Tonf_m_C)
5. **save_model** — Guarda como `autonomo/scripts/models/Edificio1_api.edb`

### Funciones auxiliares:
- `_get_grid_system_name` — Detecta nombre del grid system (G1/Global)
- `_print_grid_reference` — Imprime tabla de posiciones de ejes
- `edit_grid_fallback` — Intenta SetGridSys_2 o da instrucciones manuales

### Grilla configurada (17 ejes X + 6 ejes Y):
```
X: 1=0.000  2=3.125  3=3.825  4=9.295  5=9.895  6=15.465  7=16.015
   8=18.565  9=18.990  10=21.665  11=24.990  12=26.315  13=27.834
   14=32.435  15=34.005  16=37.130  17=38.505

Y: A=0.000  B=0.701  C=6.446  D=7.996  E=10.716  F=13.821
```
Lx=38.505m, Ly=13.821m (total 23 lineas de grilla)

## Firmas COM usadas
- `SapModel.InitializeNewModel(eUnits)` — com_signatures.md §1.1
- `SapModel.File.NewGridOnly(7 args)` — com_signatures.md §1.3
- `SapModel.DatabaseTables.GetTableForEditingArray` — etabs_api_reference.md §20
- `SapModel.DatabaseTables.SetTableForEditingArray` — etabs_api_reference.md §20.3
- `SapModel.DatabaseTables.ApplyEditedTables` — etabs_api_reference.md §20.4
- `SapModel.GridSys.GetNameList()` — etabs_api_reference.md §5.3
- `SapModel.GridSys.SetGridSys_2` — fallback (Eng-Tips ref)
- `SapModel.Story.GetStories()` — etabs_api_reference.md §4
- `SapModel.File.Save(filepath)` — com_signatures.md

## Dependencias
- `config.py` (A01) — todas las constantes, datos de grilla, conexion COM

## Verificacion
- Sintaxis Python OK (ast.parse)
- Todas las imports de config.py verificadas
- 11 funciones, estructura modular

## Consideraciones
- `NewGridOnly` con ret=0 GARANTIZA stories correctas (leccion de lab)
- La grilla es solo visual — elementos se colocan por coordenadas exactas
- Si la edicion de grilla falla, el modelo sigue siendo funcional
- File.Save via COM solo funciona si ETABS tiene UI activa (leccion COM)
- get_story_data() puede fallar en v19 — no se aborta por eso
