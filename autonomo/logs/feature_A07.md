# Feature A07 — 06_assignments.py (diafragma, mesh, apoyos)

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/06_assignments.py`

## Resumen
Script de asignaciones post-geometria para Edificio 1. Aplica 3 asignaciones criticas y ejecuta verificacion exhaustiva.

## Funcionalidad implementada

### Step 0: ensure_diaphragm()
- Crea/asegura existencia de diafragma D1 (rigido) via `Diaphragm.SetDiaphragm`

### Step 1: assign_diaphragm_to_all_areas()
- Itera TODOS los area objects (`AreaObj.GetNameList`)
- Filtra por seccion (`AreaObj.GetProperty`) — solo asigna D1 a losas (Losa15G30)
- No asigna diafragma a muros (correcto: solo losas llevan diafragma rigido)
- Safety net sobre lo que ya hace 05_slabs.py individualmente

### Step 2: ensure_automesh_all_areas()
- Aplica AutoMesh = 0.4m a TODOS los area objects (muros + losas)
- MeshType=4 (MaxSize), MaxSize1=MaxSize2=MaxSizeGeneral=0.4m
- Safety net sobre lo que ya hacen 03_walls.py y 05_slabs.py

### Step 3: set_base_restraints()
- Obtiene todos los puntos via `PointObj.GetNameList`
- Para cada punto, lee coordenada Z via `PointObj.GetCoordCartesian`
- Si Z ≈ 0.0 (tolerancia 0.01m), aplica empotamiento completo
- `PointObj.SetRestraint(name, [True, True, True, True, True, True])`
- 6 DOFs restringidos: U1, U2, U3, R1, R2, R3

### Step 4: Verificacion exhaustiva
- 4a: Verifica secciones de todas las areas (MHA30G30, MHA20G30, Losa15G30)
- 4b: Verifica secciones de todos los frames (VI20x60G30)
- 4c: Verifica que TODOS los nodos base tengan restriccion completa
- 4d: Cuenta elementos y compara contra valores esperados

## Firmas COM utilizadas (todas verificadas)
| Funcion | Firma | Fuente |
|---------|-------|--------|
| `Diaphragm.SetDiaphragm` | (Name, SemiRigid) → int | com_signatures §8.1 |
| `AreaObj.SetDiaphragm` | (Name, DiaphragmName) → int | com_signatures §8.2 |
| `AreaObj.SetAutoMesh` | (Name, 4, 0, 0, 0.4, 0.4, F, F, 0, 0.4, F, F, F, F) → int | com_signatures §7.3 |
| `AreaObj.GetNameList` | () → (count, names, ret) | com_signatures §7 |
| `AreaObj.GetProperty` | (Name) → (PropName, ret) | API standard |
| `PointObj.GetNameList` | () → (count, names, ret) | verified repos |
| `PointObj.GetCoordCartesian` | (Name) → (x, y, z, ret) | verified repos |
| `PointObj.SetRestraint` | (Name, bool[6]) → int | verified repos + taller-etabs |
| `PointObj.GetRestraint` | (Name) → (bool[6], ret) | verified repos |
| `FrameObj.GetNameList` | () → (count, names, ret) | com_signatures §6 |
| `FrameObj.GetSection` | (Name) → (PropName, ret) | API standard |

## Notas
- Auto Edge Constraints no tiene funcion API dedicada — se maneja implicitamente via AutoMesh
- El script es un safety net: 03/04/05 ya asignan propiedades individualmente
- La funcionalidad NUEVA critica son los empotramientos de base (Step 3)
- Patron consistente con demas scripts: connect → set_units → steps → verify → summary
