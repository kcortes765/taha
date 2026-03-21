# Feature A06 — 05_slabs.py (losas con shaft)

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/05_slabs.py`

## Resumen
Script API que dibuja TODAS las losas del Edificio 1 (20 pisos) usando `AreaObj.AddByCoord`.

### Geometria
- **Piso tipo (Stories 1-19)**: 7 paneles por piso, area = 468.4 m2/piso
- **Techo (Story 20)**: 5 paneles, area = 469.0 m2
- **Total**: 7*19 + 5 = 138 paneles de losa
- **Shaft ascensor**: hueco entre ejes 9-11 (X) y C-D (Y), omitido correctamente
- **Zona escalera** (ejes 1-3, A-B): omitida en piso tipo

### Asignaciones por panel
1. Seccion: `Losa15G30` (t=0.15m, Shell-Thin)
2. AutoMesh: 0.4m (MeshType=4, MaxSize)
3. Diafragma: `D1` (rigido) — creado en Step 0 del script

### Modifiers
- m11=m22=m12=0.25 (inercia flexion al 25%) — ya seteados en `02_materials_sections.py`

### Firmas COM usadas
- `AreaObj.AddByCoord` (§7.1) — paneles horizontales 4 nodos
- `AreaObj.SetAutoMesh` (§7.3) — MeshType=4
- `AreaObj.SetDiaphragm` (§8.2) — asignar D1
- `Diaphragm.SetDiaphragm` (§8.1) — crear D1

### Verificacion
- Importaciones de config.py validadas OK
- Sintaxis Python compilada OK
- Areas de paneles coinciden con config.py (468.4 m2 piso tipo)
- Sigue patrones de 03_walls.py y 04_beams.py
