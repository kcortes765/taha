# Feature A13 — 12_extract_results.py (drift, fuerzas, modos)

## Estado: COMPLETADO

## Resumen
Script completo de extraccion de resultados post-analisis para Edificio 1 (20 pisos muros HA). Extrae 7 categorias de resultados via COM API (ETABS v19) y exporta a consola, CSV y markdown.

## Archivos creados
- `autonomo/scripts/12_extract_results.py` (~850 lineas)
- `autonomo/research/resultados_esperados.md` (~180 lineas)

## Contenido del script

### 7 secciones de extraccion
1. **Modal results** — Periodos, participacion de masa (UX, UY, RZ), clasificacion de modos (Trans-X/Y, Torsion, Mixed), R*(T1)
2. **Story drifts** — Condicion 1 (CM) y 2 (punto max), envolvente por piso, verificacion NCh433 Art. 5.9 (limite 0.002)
3. **Base shear** — Reacciones por caso (gravedad + sismico), peso sismico W, Cmin/Cmax, ratio V/Qmin
4. **CM/CR** — Centros de masa y rigidez por piso, excentricidades naturales y accidentales
5. **Story forces** — Corte y momento volcante por piso para SDX/SDY
6. **Wall forces** — Fuerzas en muros de borde (ejes 1 y F), via Pier Forces o area elements
7. **P-M demands** — Puntos de demanda (Pu, Mu) por combo para diagramas de interaccion

### Infraestructura
- `parse_db_table()` — parser generico y robusto para DatabaseTables.GetTableForDisplayArray
- `print_table()` — formateador de tablas en consola
- `export_csv_file()` — exportacion CSV automatica a `results/`
- `generate_summary_md()` — generacion de markdown con todos los resultados

### Opciones CLI
- `--no-csv` — solo consola
- `--no-summary` — sin markdown
- `--sections 1 3 5` — extraccion selectiva

## Decisiones tecnicas

1. **DatabaseTables como metodo principal**: Mas confiable que funciones directas de Results para muchas tablas. Fallback a Results.StoryDrifts() y Results.BaseReac() cuando DatabaseTables falla.

2. **Drift con espectro elastico**: El pipeline usa espectro elastico (no reducido). Para T >> To (este edificio), principio de igualdad de desplazamientos aplica — drift de ETABS comparable directo contra limite 0.002.

3. **Wall forces via Pier Forces**: Si no hay pier labels definidos en ETABS, el script identifica muros de borde desde config.py y orienta al usuario para definir piers.

4. **P-M fallback global**: Si no hay piers, extrae reacciones globales por combo como referencia para diseno.

## Firmas COM verificadas
- Results.Setup.DeselectAllCasesAndCombosForOutput(): 0 args
- Results.Setup.SetCaseSelectedForOutput(CaseName): 1 arg
- Results.Setup.SetComboSelectedForOutput(ComboName): 1 arg
- Results.StoryDrifts(): 0 input → 12-element tuple
- Results.BaseReac(): 0 input → 14-element tuple
- DatabaseTables.GetTableForDisplayArray(Key,"","All",1,[],0,[]): 4 input

## Archivos CSV generados (al ejecutar)
- modal_results.csv
- story_drifts.csv
- drift_envelope.csv
- base_reactions.csv
- cm_cr_per_story.csv
- story_forces.csv
- wall_forces_axis_1.csv / wall_forces_axis_F.csv (si hay piers)
- pm_pier_*.csv / pm_global_reactions.csv
