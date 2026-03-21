# Log — Feature R01: Research CSI OAPI

**Estado**: COMPLETADA
**Fecha**: 20 marzo 2026
**Output**: `autonomo/research/etabs_api_reference.md`

## Resumen

Investigación exhaustiva de la API oficial de CSI para ETABS (OAPI). Se consultaron:
- docs.csiamerica.com (páginas individuales de funciones API 2015/2016)
- wiki.csiamerica.com (Knowledge Base OAPI, FAQ)
- csiamerica.com/developer (portal de desarrollo)
- 4 repositorios GitHub con ejemplos Python+comtypes
- 3 blogs técnicos (stru.ai, EngineeringSkills, Medium)
- Foros Eng-Tips y ResearchGate

## Contenido del documento

El documento cubre 20 categorías completas:

1. **Conexión y Setup** — 3 métodos de conexión COM, limpieza comtypes.gen, GC protection
2. **SapModel** — Objeto raíz, sub-objetos, unidades
3. **File** — NewBlank, NewGridOnly, OpenFile, Save
4. **Story** — SetStories, GetStories (con ejemplo 20 pisos)
5. **GridSys** — SetGridSys, GetGridSys
6. **PropMaterial** — SetMaterial, AddMaterial, SetMPIsotropic, SetOConcrete_1, SetORebar_1, SetWeightAndMass
7. **PropFrame** — SetRectangle, SetRebarBeam, SetRebarColumn, SetModifiers
8. **PropArea** — SetWall, SetSlab, SetModifiers (con ejemplos proyecto)
9. **PointObj** — SetRestraint, GetNameList, GetCoordCartesian
10. **FrameObj** — AddByCoord, SetSection, SetInsertionPoint (cardinal points 1-11), SetModifiers
11. **AreaObj** — AddByCoord, SetProperty, SetDiaphragm, SetLoadUniform, SetAutoMesh
12. **Diaphragm** — SetDiaphragm, asignación a áreas
13. **LoadPatterns** — Add (con eLoadPatternType), SetSelfWtMultiplier
14. **LoadCases** — StaticLinear, ResponseSpectrum (SetCase, SetLoads, SetModalCase, SetEccentricity)
15. **FuncRS** — SetUser (RECOMENDADO), SetFromFile (inestable), ejemplo espectro NCh433+DS61
16. **RespCombo** — Add, SetCaseList (con ejemplo 7 combos NCh3171)
17. **MassSource** — SetMassSource_1 (con ejemplo TERP×1.0 + SCP×0.25)
18. **Analyze** — SetActiveDOF, RunAnalysis, SetRunCaseFlag, SetSolverOption_1
19. **AnalysisResults** — StoryDrifts, BaseReac, FrameForce, JointDispl, JointReact
20. **DatabaseTables** — GetAvailableTables, GetTableForDisplayArray

Además:
- 9 tablas de enumeraciones (eUnits, eMatType, eLoadPatternType, eSlabType, eShellType, etc.)
- Pipeline completo de modelación HA (ejemplo de código)
- 9 errores frecuentes con soluciones (comtypes.gen stale, instancia invisible, .edb corrupto, etc.)
- Mapa de funciones por fase del pipeline
- 40+ links a documentación oficial verificada
- Notas de compatibilidad ETABS v19

## Decisiones tomadas

1. **SetUser > SetFromFile** para espectros: SetFromFile tiene firma inestable entre versiones. SetUser con arrays calculados en Python es 100% confiable.
2. **Documenté funciones de ETABS API 2015 y 2016** porque v19 usa CSI API v1 que es compatible con ambas.
3. **Incluí todas las lecciones COM aprendidas** del proyecto (de memory y context.md).
4. **Valores de enumeraciones**: Algunos valores numéricos exactos (eMatType, eLoadPatternType) fueron inferidos de ejemplos de código reales y documentación parcial. Deberían verificarse contra la TLB local del ETABS instalado.

## Limitaciones

- No pude acceder al archivo CHM oficial (requiere ETABS instalado)
- Algunos valores de enumeraciones pueden diferir en la v19 específica del lab
- SetAutoMesh tiene muchos parámetros opcionales; la firma documentada puede no ser exacta para v19
- MassSource: la ruta de acceso (`SapModel.PropMaterial.SetMassSource_1` vs `SapModel.MassSource.SetMassSource_1`) debe verificarse en el lab

## Próximos pasos sugeridos

- R02: Verificar firmas contra la TLB real del ETABS v19 del lab
- R03: Crear snippets probados para cada función crítica
