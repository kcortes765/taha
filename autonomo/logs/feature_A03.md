# Feature A03 — 02_materials_sections.py

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/02_materials_sections.py` (~310 líneas)

## Qué hace el script
Define materiales y secciones en ETABS v19 via COM (comtypes):

### Materiales
1. **G30** (Concrete): f'c=3058.1 tonf/m², Ec=2,624,160 tonf/m², γ=2.5 tonf/m³, ν=0.2
   - SetMaterial → SetMPIsotropic → SetOConcrete_1 → SetWeightAndMass
2. **A630-420H** (Rebar): fy=42,813.5 tonf/m², fu=64,220.3 tonf/m², Es=20,387,400 tonf/m²
   - SetMaterial → SetMPIsotropic → SetORebar_1 → SetWeightAndMass

### Secciones Frame
3. **VI20x60G30**: Rectangular 0.20×0.60m, mat G30 (SetRectangle)

### Secciones Area
4. **MHA30G30**: Wall, Shell-Thick, t=0.30m (SetWall)
5. **MHA20G30**: Wall, Shell-Thick, t=0.20m (SetWall)
6. **Losa15G30**: Slab, Shell-Thin, t=0.15m (SetSlab)

### Modifiers
7. **Viga J=0**: Anula rigidez torsional (práctica chilena Lafontaine)
8. **Losa m=0.25**: Inercia a flexión al 25% (práctica chilena)

## Firmas COM usadas (todas verificadas en com_signatures.md)
| Función | Args | Sección |
|---------|------|---------|
| PropMaterial.SetMaterial | 2 | §2.1 |
| PropMaterial.SetMPIsotropic | 4 | §2.3 |
| PropMaterial.SetOConcrete_1 | 9 | §2.4 |
| PropMaterial.SetORebar_1 | 11 | §2.5 |
| PropMaterial.SetWeightAndMass | 3 | §2.6 |
| PropFrame.SetRectangle | 4 | §3.1 |
| PropFrame.SetModifiers | 2 | §3.2 |
| PropArea.SetWall | 5 | §4.1 |
| PropArea.SetSlab | 5 | §4.2 |
| PropArea.SetModifiers | 2 | §4.4 |

## Verificación
- Syntax check: OK (py_compile)
- Config imports: todos resuelven correctamente
- Valores numéricos: coinciden con config.py (derivados de norma)
- Incluye paso de verificación post-creación (GetMPIsotropic, GetNameList)

## Notas
- Valores en task (fy=42,000, Es=2,039,000) están redondeados/con typo; el script usa los valores exactos de config.py que son los correctos por conversión MPa→tonf/m²
- SetMaterial (legacy) elegido sobre AddMaterial para evitar complejidad de parámetros Region/Standard/Grade que varían por versión
- Shell-Thick para muros (bending out-of-plane importa), Shell-Thin para losas (estándar)
