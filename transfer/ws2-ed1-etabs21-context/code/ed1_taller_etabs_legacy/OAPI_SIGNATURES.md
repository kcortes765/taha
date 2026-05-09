# CSI ETABS OAPI — Function Signatures Reference

> Compiled from CSI official CHM documentation (CSI_OAPI_Documentation.chm),
> docs.csiamerica.com, GitHub repos (ebrahimraeyat/etabs_api, retug/ETABs,
> mihdicaballero/ETABS-Ninja, danielogg92/Etabs-API-Python), Eng-Tips forums,
> stru.ai blog, and Hakan Keskin's Medium articles.
>
> Cross-referenced with actual calls in taller-etabs/ pipeline.
>
> **CRITICAL**: ETABS OAPI signatures can differ between v17, v18, v19, v20, v21.
> This document notes version differences where known. The "canonical" signatures
> below are from the **ETABSv1** type library (v19/v21).

---

## 1. SapModel.InitializeNewModel(Units)

**Path**: `cSapModel.InitializeNewModel`

```
int InitializeNewModel(eUnits Units = eUnits.kip_in_F)
```

| Param | Type | Description |
|-------|------|-------------|
| Units | eUnits (int) | Unit system enum. **Optional** — defaults to kip_in_F (=1) |

**Return**: `int` — 0 = success, nonzero = failure

**eUnits enum values** (confirmed in CHM):
| Value | Name |
|-------|------|
| 1 | lb_in_F |
| 2 | lb_ft_F |
| 3 | kip_in_F |
| 4 | kip_ft_F |
| 5 | kN_mm_C |
| 6 | kN_m_C |
| 7 | kgf_mm_C |
| 8 | kgf_m_C |
| 9 | N_mm_C |
| 10 | N_m_C |
| 11 | Ton_mm_C |
| 12 | Ton_m_C |
| 13 | kN_cm_C |
| 14 | kgf_cm_C |
| 15 | N_cm_C |
| 16 | Ton_cm_C |

**Your code**: `m.InitializeNewModel(TONF_M_C)` where TONF_M_C=12. **CORRECT**.

**Notes**:
- YES, it takes an eUnits parameter (optional).
- In COM/Python via comtypes, this is the `SapModel` object directly, not a sub-object.

---

## 2. SapModel.File.NewBlank()

**Path**: `cSapModel.cFile.NewBlank`

```
int NewBlank()
```

No parameters.

**Return**: `int` — 0 = success

**Notes**:
- Creates a completely blank model with no grids, no stories.
- You must call `InitializeNewModel()` first.
- Creates a default "MODAL" load case and "D1" diaphragm.
- **Your pipeline does NOT use NewBlank** — it uses NewGridOnly instead. This is correct because NewGridOnly creates stories.

---

## 3. SapModel.File.NewGridOnly(NumberStories, TypStoryHeight, BotStoryHeight, NumberLinesX, NumberLinesY, SpacingX, SpacingY)

**Path**: `cSapModel.cFile.NewGridOnly`

```
int NewGridOnly(
    int NumberStories,
    double TypStoryHeight,
    double BotStoryHeight,
    int NumberLinesX,
    int NumberLinesY,
    double SpacingX,
    double SpacingY
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | NumberStories | int | Number of stories |
| 2 | TypStoryHeight | double | Typical story height |
| 3 | BotStoryHeight | double | Bottom story height |
| 4 | NumberLinesX | int | Number of grid lines in X |
| 5 | NumberLinesY | int | Number of grid lines in Y |
| 6 | SpacingX | double | Spacing between X grid lines |
| 7 | SpacingY | double | Spacing between Y grid lines |

**Return**: `int` — 0 = success

**Your code** (01_init_model.py):
```python
m.File.NewGridOnly(N_STORIES, STORY_HEIGHT_TYP, STORY_HEIGHT_1,
                   GRID_LINES_X, GRID_LINES_Y, GRID_SPACING_X, GRID_SPACING_Y)
```
**CORRECT** — 7 parameters, correct order.

**Notes**:
- Also exists: `NewGridOnly` in SAP2000 has the same signature.
- The grid lines and stories created are real objects that persist.
- Creates default "Base" story at elevation 0.
- The `ret` value of 0 guarantees stories exist.

---

## 4. SapModel.PropMaterial.SetMaterial(Name, MatType)

**Path**: `cSapModel.cPropMaterial.SetMaterial`

```
int SetMaterial(
    string Name,
    eMatType MatType
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Material name |
| 2 | MatType | eMatType (int) | Material type enum |

**eMatType enum**:
| Value | Name |
|-------|------|
| 1 | Steel |
| 2 | Concrete |
| 3 | NoDesign |
| 4 | Aluminum |
| 5 | ColdFormed |
| 6 | Rebar |
| 7 | Tendon |

**Return**: `int` — 0 = success

**Your code**: `m.PropMaterial.SetMaterial('G30', 2)` — **CORRECT**.

**Deprecated?**: SetMaterial is the **legacy** method. The newer method is **AddMaterial** (see #5). However, SetMaterial still works in v19 and v21. CSI documentation marks it as "maintained for backward compatibility" but NOT formally deprecated. It simply creates a material without specifying design properties.

---

## 5. SapModel.PropMaterial.AddMaterial(Name, MatType, Region, Standard, Grade, UserName)

**Path**: `cSapModel.cPropMaterial.AddMaterial`

```
int AddMaterial(
    ref string Name,         // output: actual name assigned
    eMatType MatType,
    string Region,
    string Standard,
    string Grade,
    string UserName = ""
)
```

| # | Param | Type | Direction | Description |
|---|-------|------|-----------|-------------|
| 1 | Name | ref string | in/out | Material name (returns actual name) |
| 2 | MatType | eMatType (int) | in | Material type enum |
| 3 | Region | string | in | Region code (e.g., "Chile", "United States") |
| 4 | Standard | string | in | Standard (e.g., "ACI 318-08", "ASTM A615") |
| 5 | Grade | string | in | Grade (e.g., "fc300", "Grade 60") |
| 6 | UserName | string | in | Optional user-defined name |

**Return**: `int` — 0 = success

**Notes**:
- This is the **preferred** method per CSI. It pre-populates all design properties.
- In Python/COM, the `ref string` parameter means the function returns a tuple: `(actual_name, ret)`.
- For Chilean practice, the Region/Standard/Grade may not have exact matches. Using SetMaterial + SetOConcrete_1 is a valid alternative.

---

## 6. SapModel.PropMaterial.SetMPIsotropic(Name, E, U, A, Temp)

**Path**: `cSapModel.cPropMaterial.SetMPIsotropic`

```
int SetMPIsotropic(
    string Name,
    double E,
    double U,
    double A,
    double Temp = 0.0
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Material name |
| 2 | E | double | Modulus of elasticity |
| 3 | U | double | Poisson's ratio |
| 4 | A | double | Coefficient of thermal expansion |
| 5 | Temp | double | **Optional** — Temperature at which properties are defined. Default = 0.0 |

**Return**: `int` — 0 = success

**Your code**: `m.PropMaterial.SetMPIsotropic('G30', EC_KGF_CM2, POISSON_CONC, 9.9e-6)` — **CORRECT** (4 args, Temp omitted = default 0.0).

**Answer**: It takes **4 required + 1 optional** = 5 total. The Temp parameter IS optional and defaults to 0.0.

---

## 7. SapModel.PropMaterial.SetOConcrete_1(Name, fc, IsLightweight, fcsfactor, SSType, SSHysType, StrainAtfc, StrainUltimate, FinalSlope)

**Path**: `cSapModel.cPropMaterial.SetOConcrete_1`

```
int SetOConcrete_1(
    string Name,
    double fc,
    bool IsLightweight,
    double fcsfactor,
    int SSType,
    int SSHysType,
    double StrainAtfc,
    double StrainUltimate,
    double FinalSlope,
    double Temp = 0.0
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Material name |
| 2 | fc | double | Compressive strength f'c |
| 3 | IsLightweight | bool | True if lightweight concrete |
| 4 | fcsfactor | double | f'c shear factor (typically 1.0) |
| 5 | SSType | int | Stress-strain curve type: 1=Simple, 2=Mander |
| 6 | SSHysType | int | Hysteresis type: 1-7 (4=Takeda is common) |
| 7 | StrainAtfc | double | Strain at f'c (typ. 0.002) |
| 8 | StrainUltimate | double | Ultimate strain (typ. 0.005) |
| 9 | FinalSlope | double | Final slope ratio (typ. -0.1) |
| 10 | Temp | double | **Optional** — Temperature. Default 0.0 |

**Return**: `int` — 0 = success

**The `_1` suffix**: In CSI OAPI, the `_1` suffix indicates a **revised version** of the function. The original `SetOConcrete` had fewer parameters. CSI added `_1` when they added parameters (typically SSHysType and Temp). There is NO `SetOConcrete_2` in v19. In v21+, there may be a `SetOConcrete_2`.

**Your code**:
```python
m.PropMaterial.SetOConcrete_1('G30', FC_KGF_CM2, False, 1.0, 2, 4, 0.002, 0.005, -0.1)
```
**CORRECT** — 9 args (Temp omitted = 0.0).

---

## 8. SapModel.PropFrame.SetRectangle(Name, MatProp, T3, T2, Color, Notes, GUID)

**Path**: `cSapModel.cPropFrame.SetRectangle`

```
int SetRectangle(
    string Name,
    string MatProp,
    double T3,
    double T2,
    int Color = -1,
    string Notes = "",
    string GUID = ""
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Section name |
| 2 | MatProp | string | Material property name |
| 3 | T3 | double | Section depth (height) |
| 4 | T2 | double | Section width |
| 5 | Color | int | **Optional** — Display color (-1 = default) |
| 6 | Notes | string | **Optional** — Notes |
| 7 | GUID | string | **Optional** — GUID |

**Return**: `int` — 0 = success

**Your code**: `m.PropFrame.SetRectangle(VIGA_NAME, 'G30', VIGA_H, VIGA_B)` — **CORRECT** (4 args, 3 optional omitted).

**Notes**:
- T3 = depth (vertical dimension, "3" direction in local axes).
- T2 = width (horizontal dimension).
- 3 required + 3 optional parameters.

---

## 9. SapModel.PropArea.SetWall(Name, eWallPropType, eShellType, MatProp, Thickness, Color, Notes, GUID)

**Path**: `cSapModel.cPropArea.SetWall`

```
int SetWall(
    string Name,
    int eWallPropType,
    int eShellType,
    string MatProp,
    double Thickness,
    int Color = -1,
    string Notes = "",
    string GUID = ""
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Wall property name |
| 2 | eWallPropType | int | 0=Default, 1=Specified |
| 3 | eShellType | int | Shell type (see below) |
| 4 | MatProp | string | Material name |
| 5 | Thickness | double | Wall thickness |
| 6 | Color | int | Optional |
| 7 | Notes | string | Optional |
| 8 | GUID | string | Optional |

**eShellType enum**:
| Value | Name | Description |
|-------|------|-------------|
| 1 | ShellThin | Kirchhoff thin shell |
| 2 | ShellThick | Mindlin thick shell |
| 3 | Membrane | Membrane only |
| 4 | Plate | Plate only |
| 5 | Shell | Layered shell |
| 6 | ASI | Auto-Select (v21+) |

**Difference with SetShell_1**: SetWall is specific to wall-type area properties. SetShell_1 is the general shell property setter that works for any shell type (wall, slab, deck). SetWall internally calls SetShell_1 with wall-specific defaults.

**Your code**: `m.PropArea.SetWall(MURO_30_NAME, 1, 1, 'G30', MURO_30_ESP)` — **CORRECT** (5 args).

---

## 10. SapModel.PropArea.SetSlab(Name, eSlabType, eShellType, MatProp, Thickness, Color, Notes, GUID)

**Path**: `cSapModel.cPropArea.SetSlab`

```
int SetSlab(
    string Name,
    int eSlabType,
    int eShellType,
    string MatProp,
    double Thickness,
    int Color = -1,
    string Notes = "",
    string GUID = ""
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Slab property name |
| 2 | eSlabType | int | Slab type (see below) |
| 3 | eShellType | int | Shell type (same as SetWall) |
| 4 | MatProp | string | Material name |
| 5 | Thickness | double | Slab thickness |
| 6 | Color | int | Optional |
| 7 | Notes | string | Optional |
| 8 | GUID | string | Optional |

**eSlabType enum**:
| Value | Name |
|-------|------|
| 0 | Slab (regular) |
| 1 | Drop (drop panel) |
| 2 | Stiff |
| 3 | Ribbed (waffle) |
| 4 | Mat (foundation) |

**Your code**: `m.PropArea.SetSlab(LOSA_NAME, 0, 1, 'G30', LOSA_ESP)` — **CORRECT**.

---

## 11. SapModel.PropArea.SetShell_1(Name, eShellType, IncludesDrillingDOF, MatProp, MatAng, Thickness, Bending, Color, Notes, GUID)

**Path**: `cSapModel.cPropArea.SetShell_1`

```
int SetShell_1(
    string Name,
    int eShellType,
    bool IncludeDrillingDOF,
    string MatProp,
    double MatAng,
    double Thickness,
    double BendThick,
    int Color = -1,
    string Notes = "",
    string GUID = ""
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Property name |
| 2 | eShellType | int | Shell type enum |
| 3 | IncludeDrillingDOF | bool | Include drilling DOF |
| 4 | MatProp | string | Material name |
| 5 | MatAng | double | Material angle |
| 6 | Thickness | double | Membrane thickness |
| 7 | BendThick | double | Bending thickness |
| 8 | Color | int | Optional |
| 9 | Notes | string | Optional |
| 10 | GUID | string | Optional |

**Does it exist in v19?** YES. SetShell_1 exists in v19. The `_1` suffix indicates it replaced the original SetShell (which is deprecated). Your pipeline uses SetWall/SetSlab which are higher-level wrappers — both are correct.

---

## 12. SapModel.PointObj.AddCartesian(X, Y, Z, Name, UserName, CSys, MergeOff, MergeNumber)

**Path**: `cSapModel.cPointObj.AddCartesian`

```
int AddCartesian(
    double X,
    double Y,
    double Z,
    ref string Name = "",
    string UserName = "",
    string CSys = "Global",
    bool MergeOff = false,
    int MergeNumber = 0
)
```

| # | Param | Type | Direction | Description |
|---|-------|------|-----------|-------------|
| 1 | X | double | in | X coordinate |
| 2 | Y | double | in | Y coordinate |
| 3 | Z | double | in | Z coordinate |
| 4 | Name | ref string | out | Returns assigned name |
| 5 | UserName | string | in | Optional user name |
| 6 | CSys | string | in | Coordinate system (default "Global") |
| 7 | MergeOff | bool | in | Disable merge with existing point |
| 8 | MergeNumber | int | in | Merge tolerance number |

**Return**: In COM/Python, returns tuple: `(Name, ret)` where `Name` is the point name and `ret` is 0 on success.

**Your code**: `m.PointObj.AddCartesian(x, y, z)` — **WORKS** (3 positional args, rest default). Returns `(name_str, 0)` or similar.

---

## 13. SapModel.FrameObj.AddByCoord(xi, yi, zi, xj, yj, zj, Name, PropName, UserName, CSys)

**Path**: `cSapModel.cFrameObj.AddByCoord`

```
int AddByCoord(
    double xi,
    double yi,
    double zi,
    double xj,
    double yj,
    double zj,
    ref string Name = "",
    string PropName = "Default",
    string UserName = "",
    string CSys = "Global"
)
```

| # | Param | Type | Direction | Description |
|---|-------|------|-----------|-------------|
| 1 | xi | double | in | X coordinate of i-end |
| 2 | yi | double | in | Y coordinate of i-end |
| 3 | zi | double | in | Z coordinate of i-end |
| 4 | xj | double | in | X coordinate of j-end |
| 5 | yj | double | in | Y coordinate of j-end |
| 6 | zj | double | in | Z coordinate of j-end |
| 7 | Name | ref string | out | Returns assigned name |
| 8 | PropName | string | in | Section property name |
| 9 | UserName | string | in | Optional user name |
| 10 | CSys | string | in | Coordinate system. **YES, includes CSys.** |

**Return**: In COM/Python, returns tuple: `(Name, ret)` — `ret=0` on success.

**Your code**:
```python
m.FrameObj.AddByCoord(x_start, y_coord, z, x_end, y_coord, z,
                      '', VIGA_NAME, '', 'Global')
```
**CORRECT** — 10 parameters, includes CSys='Global'.

---

## 14. SapModel.FrameObj.AddByPoint(Point1, Point2, Name, PropName, UserName)

**Path**: `cSapModel.cFrameObj.AddByPoint`

```
int AddByPoint(
    string Point1,
    string Point2,
    ref string Name = "",
    string PropName = "Default",
    string UserName = ""
)
```

| # | Param | Type | Direction | Description |
|---|-------|------|-----------|-------------|
| 1 | Point1 | string | in | Name of point object at i-end |
| 2 | Point2 | string | in | Name of point object at j-end |
| 3 | Name | ref string | out | Returns assigned frame name |
| 4 | PropName | string | in | Section property name |
| 5 | UserName | string | in | Optional user name |

**Return**: tuple `(Name, ret)` — `ret=0` on success.

---

## 15. SapModel.AreaObj.AddByCoord(NumberPoints, X, Y, Z, Name, PropName, UserName, CSys)

**Path**: `cSapModel.cAreaObj.AddByCoord`

```
int AddByCoord(
    int NumberPoints,
    double[] X,
    double[] Y,
    double[] Z,
    ref string Name = "",
    string PropName = "Default",
    string UserName = "",
    string CSys = "Global"
)
```

| # | Param | Type | Direction | Description |
|---|-------|------|-----------|-------------|
| 1 | NumberPoints | int | in | Number of corner points (3, 4, ...) |
| 2 | X | double[] | in | Array of X coordinates |
| 3 | Y | double[] | in | Array of Y coordinates |
| 4 | Z | double[] | in | Array of Z coordinates |
| 5 | Name | ref string | out | Returns assigned name |
| 6 | PropName | string | in | Section property name |
| 7 | UserName | string | in | Optional user name |
| 8 | CSys | string | in | Coordinate system |

**Return**: tuple `(Name, ret)` — `ret=0` on success.

**Your code**:
```python
m.AreaObj.AddByCoord(4, [x, x, x, x], [y0, y1, y1, y0],
                     [z_bot, z_bot, z_top, z_top],
                     '', sec, '', 'Global')
```
**CORRECT** — 8 parameters.

---

## 16. SapModel.AreaObj.AddByPoint(NumberPoints, Point, Name, PropName, UserName)

**Path**: `cSapModel.cAreaObj.AddByPoint`

```
int AddByPoint(
    int NumberPoints,
    string[] Point,
    ref string Name = "",
    string PropName = "Default",
    string UserName = ""
)
```

| # | Param | Type | Direction | Description |
|---|-------|------|-----------|-------------|
| 1 | NumberPoints | int | in | Number of points |
| 2 | Point | string[] | in | Array of point object names |
| 3 | Name | ref string | out | Returns assigned name |
| 4 | PropName | string | in | Section property name |
| 5 | UserName | string | in | Optional user name |

**Return**: tuple `(Name, ret)` — `ret=0` on success.

---

## 17. SapModel.AreaObj.SetDiaphragm(Name, DiaphragmName, ItemType)

**Path**: `cSapModel.cAreaObj.SetDiaphragm`

```
int SetDiaphragm(
    string Name,
    string DiaphragmName,
    eItemType ItemType = eItemType.Objects
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Area object name |
| 2 | DiaphragmName | string | Diaphragm name (or "None"/"" to remove) |
| 3 | ItemType | eItemType (int) | **Optional** — 0=Object, 1=Group, 2=SelectedObjects |

**YES**, it takes ItemType as an optional third parameter.

**eItemType enum**:
| Value | Name |
|-------|------|
| 0 | Objects (default) |
| 1 | Group |
| 2 | SelectedObjects |

**Return**: `int` — 0 = success

**Your code**: `m.AreaObj.SetDiaphragm(area_name, dname)` — **CORRECT** (ItemType defaults to Objects=0).

**To remove diaphragm**: Use `"None"` as DiaphragmName. Empty string `""` may also work in some versions.

---

## 18. SapModel.LoadPatterns.Add(Name, MyType, SelfWTMultiplier, AddLoadCase)

**Path**: `cSapModel.cLoadPatterns.Add`

```
int Add(
    string Name,
    eLoadPatternType MyType,
    double SelfWTMultiplier = 0.0,
    bool AddLoadCase = true
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Load pattern name |
| 2 | MyType | eLoadPatternType (int) | Type enum (see below) |
| 3 | SelfWTMultiplier | double | **Optional** — Self-weight multiplier (default 0.0) |
| 4 | AddLoadCase | bool | **Optional** — Also create a load case (default true) |

**eLoadPatternType enum** (partial):
| Value | Name |
|-------|------|
| 1 | Dead |
| 2 | SuperDead |
| 3 | Live |
| 4 | ReduceLive |
| 5 | Quake |
| 6 | Wind |
| 7 | Snow |
| 8 | Other |
| 11 | RoofLive |

**Return**: `int` — 0 = success

**Your code**: `m.LoadPatterns.Add(name, ltype, sw, True)` — **CONFIRMED 4 params, CORRECT.**

---

## 19. SapModel.AreaObj.SetLoadUniform(Name, LoadPat, Value, Dir, Replace, CSys, ItemType)

**Path**: `cSapModel.cAreaObj.SetLoadUniform`

```
int SetLoadUniform(
    string Name,
    string LoadPat,
    double Value,
    int Dir,
    bool Replace = true,
    string CSys = "Global",
    eItemType ItemType = eItemType.Objects
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Area object name |
| 2 | LoadPat | string | Load pattern name |
| 3 | Value | double | Load value (force per area, negative = downward in Global Z) |
| 4 | Dir | int | Direction: 1=Local1, 2=Local2, 3=Local3, 4=X, 5=Y, **6=Gravity**, 7-9=projected, 10=Gravity projected, 11=Global Z |
| 5 | Replace | bool | Optional — Replace existing loads (default true) |
| 6 | CSys | string | Optional — Coordinate system |
| 7 | ItemType | eItemType (int) | Optional — Item type (0=Objects) |

**Return**: `int` — 0 = success

**Your code**:
```python
m.AreaObj.SetLoadUniform(area_name, 'SCP', -scp_tonf, 6, True, 'Global')
```
**CORRECT** — 6 args. Dir=6 means "Gravity" direction (downward).

**Note**: Value should be negative for downward loads when Dir=6 (Gravity). Your code correctly uses negative values.

---

## 20. SapModel.FrameObj.SetLoadDistributed(Name, LoadPat, MyType, Dir, Dist1, Dist2, Val1, Val2, CSys, RelDist, Replace, ItemType)

**Path**: `cSapModel.cFrameObj.SetLoadDistributed`

```
int SetLoadDistributed(
    string Name,
    string LoadPat,
    int MyType,
    int Dir,
    double Dist1,
    double Dist2,
    double Val1,
    double Val2,
    string CSys = "Global",
    bool RelDist = true,
    bool Replace = true,
    eItemType ItemType = eItemType.Objects
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Frame object name |
| 2 | LoadPat | string | Load pattern name |
| 3 | MyType | int | 1=Force, 2=Moment |
| 4 | Dir | int | Direction (1-11, same as area) |
| 5 | Dist1 | double | Start distance |
| 6 | Dist2 | double | End distance |
| 7 | Val1 | double | Value at start |
| 8 | Val2 | double | Value at end |
| 9 | CSys | string | Optional — Coordinate system |
| 10 | RelDist | bool | Optional — true=relative (0-1), false=absolute |
| 11 | Replace | bool | Optional — Replace existing loads |
| 12 | ItemType | eItemType (int) | Optional |

**Return**: `int` — 0 = success

**Answer**: **8 required + 4 optional = 12 total parameters**.

**Not used in your pipeline** — loads are applied to slabs only (AreaObj.SetLoadUniform).

---

## 21. SapModel.Func.FuncRS.SetFromFile(Name, FileName, HeaderLinesSkip, DampRatio, ValueType, ...)

**Path**: `cSapModel.cFunction.cFuncRS.SetFromFile`

**THIS IS THE PROBLEMATIC ONE.** The signature varies between ETABS versions.

### v17/v18 signature (5 params):
```
int SetFromFile(
    string Name,
    string FileName,
    int HeaderLinesSkip,
    int DampRatio_Or_ValueType,     // ambiguous in early docs
    int ValueType_Or_FreqType
)
```

### v19 signature (documented in CHM):
```
int SetFromFile(
    string Name,
    string FileName,
    int HeaderLinesSkip,
    double DampRatio,
    int ValueType
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Function name |
| 2 | FileName | string | Full path to spectrum file |
| 3 | HeaderLinesSkip | int | Number of header lines to skip |
| 4 | DampRatio | double | Damping ratio (e.g. 0.05) |
| 5 | ValueType | int | 0 = Period vs Value, 1 = Frequency vs Value |

**Return**: `int` — 0 = success

### v21+ signature (may have 6-7 params):
```
int SetFromFile(
    string Name,
    string FileName,
    int HeaderLinesSkip,
    double DampRatio,
    int ValueType,
    int FreqTypeInFile,     // 0=Period, 1=Freq (Hz), 2=Freq (rad/s)
    bool IsUser              // true = user-defined
)
```

**YOUR PROBLEM**: The review-ia version calls with 7 args:
```python
m.Func.FuncRS.SetFromFile(name, spec_file, 1, 0, 1, 2, True)
```
This matches the **v21 7-parameter signature** but fails on v19.

The taller-etabs version tries multiple variants (CORRECT defensive approach).

**RECOMMENDED for v19**: Use **5 parameters**:
```python
m.Func.FuncRS.SetFromFile(name, spec_file, 0, 0.05, 0)
# (name, file, skip_0_lines, damp_5%, period_vs_value)
```

**If this still fails in COM binding**, use `SetUser` instead (see #22).

---

## 22. SapModel.Func.FuncRS.SetUser(Name, NumberItems, Time, Value, DampRatio)

**Path**: `cSapModel.cFunction.cFuncRS.SetUser`

```
int SetUser(
    string Name,
    int NumberItems,
    ref double[] Time,
    ref double[] Value,
    double DampRatio = 0.05
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Function name |
| 2 | NumberItems | int | Number of data points |
| 3 | Time | double[] | Array of periods (seconds) |
| 4 | Value | double[] | Array of spectral values |
| 5 | DampRatio | double | **Optional** — Damping ratio (default 0.05) |

**Return**: `int` — 0 = success

**Your code tries both 5-arg and 4-arg versions** — this is correct.

**IMPORTANT NOTE**: In some COM bindings (especially comtypes with v19 TLB), the arrays must be passed as Python `list` (not numpy arrays or tuples). comtypes may also need the arrays as `VARIANT` or `SAFEARRAY`. If standard lists fail, try:
```python
import comtypes
from ctypes import c_double, POINTER
# ... convert to SAFEARRAY if needed
```

---

## 23. SapModel.LoadCases.ResponseSpectrum.SetCase(Name)

**Path**: `cSapModel.cLoadCases.cResponseSpectrum.SetCase`

```
int SetCase(
    string Name
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Response spectrum case name |

**Return**: `int` — 0 = success

**Creates a new response spectrum load case.** If it already exists, resets it.

**Your code**: `m.LoadCases.ResponseSpectrum.SetCase(case_name)` — **CORRECT**.

---

## 24. SapModel.LoadCases.ResponseSpectrum.SetLoads(Name, NumberLoads, LoadDir, Func, SF, CSys, Ang)

**Path**: `cSapModel.cLoadCases.cResponseSpectrum.SetLoads`

```
int SetLoads(
    string Name,
    int NumberLoads,
    ref string[] LoadDir,
    ref string[] Func,
    ref double[] SF,
    ref string[] CSys,
    ref double[] Ang
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | RS case name |
| 2 | NumberLoads | int | Number of loads (typically 1) |
| 3 | LoadDir | string[] | Direction: "U1", "U2", "U3" |
| 4 | Func | string[] | Function name(s) |
| 5 | SF | double[] | Scale factor(s) |
| 6 | CSys | string[] | Coordinate system(s) |
| 7 | Ang | double[] | Angle(s) |

**Return**: `int` — 0 = success

**Your code**:
```python
m.LoadCases.ResponseSpectrum.SetLoads(
    case_name, 1, [direction], ['Espectro_NCh433'],
    [sf], [''], [0.0])
```
**CORRECT** — 7 parameters. All arrays have length = NumberLoads = 1.

**Notes**: Some sources show CSys default as `"Global"` rather than `""`. Both should work but `"Global"` is safer.

---

## 25. SapModel.Analyze.RunAnalysis()

**Path**: `cSapModel.cAnalyze.RunAnalysis`

```
int RunAnalysis()
```

**No parameters.**

**Return**: `int` — 0 = success

**Your code**: `m.Analyze.RunAnalysis()` — **CORRECT**.

**Notes**:
- Blocks until analysis completes.
- For large models (20 stories, ~2000 elements), can take 2-10 minutes.
- Returns nonzero if analysis fails (instability, missing data, etc.).
- There is also `SetRunCaseFlag(CaseName, Run)` to select which cases to run.

---

## 26. SapModel.Results.Setup.SetCaseSelectedForOutput(Name)

**Path**: `cSapModel.cAnalysisResults.cAnalysisResultsSetup.SetCaseSelectedForOutput`

```
int SetCaseSelectedForOutput(
    string Name
)
```

| # | Param | Type | Description |
|---|-------|------|-------------|
| 1 | Name | string | Load case or combo name |

**Return**: `int` — 0 = success

**Your code**: `m.Results.Setup.SetCaseSelectedForOutput('Modal')` — **CORRECT**.

**Related**: `DeselectAllCasesAndCombosForOutput()` — no params, clears selection.

---

## 27. SapModel.Results.StoryDrifts(...)

**Path**: `cSapModel.cAnalysisResults.StoryDrifts`

### Signature (ETABS-specific, not in SAP2000):
```
int StoryDrifts(
    ref int NumberResults,
    ref string[] Story,
    ref string[] LoadCase,
    ref string[] StepType,
    ref double[] StepNum,
    ref string[] Direction,
    ref double[] Drift,
    ref string[] Label,
    ref double[] X,
    ref double[] Y,
    ref double[] Z
)
```

**Return structure** (11 output arrays + return int):

| Index | Type | Content |
|-------|------|---------|
| 0 | int | NumberResults |
| 1 | string[] | Story names |
| 2 | string[] | Load case names |
| 3 | string[] | Step types |
| 4 | double[] | Step numbers |
| 5 | string[] | Direction ("X" or "Y") |
| 6 | double[] | **Drift values** (delta/h) |
| 7 | string[] | Label (point label) |
| 8 | double[] | X coordinates |
| 9 | double[] | Y coordinates |
| 10 | double[] | Z coordinates |
| last | int | ret (0=success) |

**In Python/COM**: Returns a large tuple. Your parsing code correctly searches for string lists (story names) and float lists (drift values).

**Your code** tries two calling conventions:
```python
m.Results.StoryDrifts(0, [], [], [], [], [], [], [], [], [], 0)  # with placeholders
m.Results.StoryDrifts()  # no args
```
Both approaches are reasonable — the correct one depends on how comtypes generates the binding from the TLB.

---

## 28. SapModel.Results.JointDrifts(...)

**Does this exist in v19?** **NO** — `JointDrifts` does NOT exist as a direct API call in ETABS v19.

**What exists instead**:
- `StoryDrifts` — gives drift at the story level (CM and maximum)
- `JointDispl` / `JointDisplAbs` — gives displacement at individual joints

To compute joint-level drift, you need to manually compute:
1. Get joint displacements at each level using `Results.JointDispl()`
2. Compute drift = (displacement_top - displacement_bottom) / story_height

**In v21+**: There may be a `JointDrifts` function, but it's not standard in v19.

---

## 29. SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

**Path**: `cSapModel.cDatabaseTables.GetTableForDisplayArray`

```
int GetTableForDisplayArray(
    string TableKey,
    ref string FieldKeyList,
    string GroupName,
    ref int TableVersion,
    ref string[] FieldsKeysIncluded,
    ref int NumberRecords,
    ref string[] TableData
)
```

| # | Param | Type | Direction | Description |
|---|-------|------|-----------|-------------|
| 1 | TableKey | string | in | Table identifier (e.g. "Story Drifts", "Modal Participating Mass Ratios") |
| 2 | FieldKeyList | ref string | in/out | Semicolon-separated field keys to include (or "" for all) |
| 3 | GroupName | string | in | Group name filter (typically "All" or "") |
| 4 | TableVersion | ref int | out | Table version number |
| 5 | FieldsKeysIncluded | ref string[] | out | Actual field keys returned |
| 6 | NumberRecords | ref int | out | Number of records returned |
| 7 | TableData | ref string[] | out | Flat array of strings (fields × records) |

**Return**: `int` — 0 = success

**In Python/COM**:
```python
result = m.DatabaseTables.GetTableForDisplayArray(
    "Story Drifts",  # TableKey
    "",              # FieldKeyList (all fields)
    "All",           # GroupName
    0,               # TableVersion placeholder
    [],              # FieldsKeysIncluded placeholder
    0,               # NumberRecords placeholder
    []               # TableData placeholder
)
```

Returns a tuple with all the output values. The TableData is a flat array where every N consecutive elements form one record (N = number of fields).

**Common TableKey values**:
- `"Story Drifts"`
- `"Modal Participating Mass Ratios"`
- `"Base Reactions"`
- `"Story Forces"`
- `"Joint Displacements"`
- `"Frame Forces"`
- `"Area Forces and Stresses"`

**This is an alternative to the Results.* methods** and is often more reliable for extracting data because it uses the same engine as ETABS's built-in "Show Tables" command.

**Not used in your pipeline** — but could be a good alternative if Results.StoryDrifts() fails.

---

## Additional Functions Referenced in Your Code

### SapModel.PropMaterial.SetWeightAndMass(Name, MyOption, Value)
```
int SetWeightAndMass(string Name, int MyOption, double Value)
```
MyOption: 1=WeightPerVolume, 2=MassPerVolume

### SapModel.PropMaterial.SetORebar_1(Name, Fy, Fu, EFy, EFu, SSType, SSHysType, StrainAtHardening, StrainAtMaxStress, StrainAtRupture, FinalSlope)
```
int SetORebar_1(
    string Name, double Fy, double Fu,
    double EFy, double EFu,
    int SSType, int SSHysType,
    double StrainAtHardening, double StrainAtMaxStress,
    double FinalSlope, double Temp = 0.0
)
```
Your code passes 10 args — **CORRECT** (Temp defaults to 0.0).

### SapModel.PropFrame.SetModifiers(Name, Value)
```
int SetModifiers(string Name, double[] Value)
```
Value: array of 8 modifiers [A, As2, As3, J, I22, I33, Mass, Weight]

### SapModel.PropArea.SetModifiers(Name, Value)
```
int SetModifiers(string Name, double[] Value)
```
Value: array of 10 modifiers [f11, f22, f12, m11, m22, m12, v13, v23, Mass, Weight]

### SapModel.PointObj.SetRestraint(Name, Value, ItemType)
```
int SetRestraint(string Name, bool[] Value, eItemType ItemType = 0)
```
Value: array of 6 booleans [U1, U2, U3, R1, R2, R3]

### SapModel.PointObj.SetLoadForce(Name, LoadPat, Value, Replace, CSys, ItemType)
```
int SetLoadForce(
    string Name, string LoadPat,
    double[] Value,        // [F1, F2, F3, M1, M2, M3]
    bool Replace = true,
    string CSys = "Global",
    eItemType ItemType = 0
)
```

### SapModel.RespCombo.Add(Name, ComboType)
```
int Add(string Name, int ComboType)
```
ComboType: 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd, 3=SRSS, 4=Range

### SapModel.RespCombo.SetCaseList(Name, CNameType, CName, SF)
```
int SetCaseList(string Name, int CNameType, string CName, double SF)
```
CNameType: 0=LoadCase, 1=LoadCombo

### SapModel.LoadCases.ResponseSpectrum.SetModalCase(Name, ModalCase)
```
int SetModalCase(string Name, string ModalCase)
```

### SapModel.LoadCases.ResponseSpectrum.SetModalComb(Name, ModalComb, GMCf1, GMCf2)
```
int SetModalComb(string Name, int ModalComb, double GMCf1 = 0, double GMCf2 = 0)
```
ModalComb: 1=CQC, 2=SRSS, 3=AbsSum, 4=GMC, 5=NRC10%

### SapModel.LoadCases.ResponseSpectrum.SetDampConstant(Name, Damp)
```
int SetDampConstant(string Name, double Damp)
```

### SapModel.LoadCases.ModalEigen.SetNumberModes(Name, MaxModes, MinModes)
```
int SetNumberModes(string Name, int MaxModes, int MinModes = 1)
```

### SapModel.AreaObj.SetAutoMesh(Name, MeshType, N1, N2, MaxSize1, MaxSize2, PointsFromLines, PointsFromPoints, ExtendLines, MatchLines)
```
int SetAutoMesh(
    string Name, int MeshType, int N1, int N2,
    double MaxSize1, double MaxSize2,
    bool PointsFromLines, bool PointsFromPoints,
    bool ExtendLines = false, bool MatchLines = false
)
```
MeshType: 0=None, 1=N-divisions, 2=MaxSize, 3=MatchJoints

### SapModel.Results.ModalParticipatingMassRatios(...)
```
int ModalParticipatingMassRatios(
    ref int NumberResults,
    ref string[] LoadCase,
    ref string[] StepType,
    ref double[] StepNum,
    ref double[] Period,
    ref double[] Ux, ref double[] Uy, ref double[] Uz,
    ref double[] SumUx, ref double[] SumUy, ref double[] SumUz,
    ref double[] Rx, ref double[] Ry, ref double[] Rz,
    ref double[] SumRx, ref double[] SumRy, ref double[] SumRz
)
```
17 output parameters + return int = 18 fields total.

### SapModel.Results.BaseReact(...)
```
int BaseReact(
    ref int NumberResults,
    ref string[] LoadCase, ref string[] StepType, ref double[] StepNum,
    ref double[] Fx, ref double[] Fy, ref double[] Fz,
    ref double[] Mx, ref double[] My, ref double[] Mz,
    double gx = 0, double gy = 0, double gz = 0
)
```

### SapModel.Diaphragm.SetDiaphragm(Name, SemiRigid)
```
int SetDiaphragm(string Name, bool SemiRigid = false)
```

### SapModel.PropMass.SetMassSource_1 (also MassSource.SetMassSource_1)
```
int SetMassSource_1(
    bool IncludeElements,
    bool IncludeAddedMass,
    bool IncludeLoads,
    int NumberLoads,
    string[] LoadPat,
    double[] SF
)
```
- IncludeElements: Include element self-mass
- IncludeAddedMass: Include added mass (rarely used)
- IncludeLoads: Include mass from loads
- NumberLoads: Number of load patterns in arrays
- LoadPat[]: Load pattern names
- SF[]: Scale factors

**Notes**: The path varies by ETABS version:
- v19: May be `SapModel.PropMass.SetMassSource_1`
- v21+: May be `SapModel.MassSource.SetMassSource_1`
- Your code tries BOTH paths — **CORRECT defensive approach**.

### SapModel.SetModelIsLocked(LockIt)
```
int SetModelIsLocked(bool LockIt)
```

### SapModel.File.Save(FileName)
```
int Save(string FileName = "")
```

### SapModel.File.OpenFile(FileName)
```
int OpenFile(string FileName)
```

---

### SapModel.LoadCases.ResponseSpectrum.SetDiaphragmEccentricityOverride(...)
```
int SetDiaphragmEccentricityOverride(
    string Name,
    int NumberDiaphragms,
    ref string[] Diaph,
    ref double[] Eccen,
    ref bool[] Overwrite    // optional in some versions
)
```
- Name: RS case name
- NumberDiaphragms: Number of diaphragms
- Diaph[]: Diaphragm names
- Eccen[]: Eccentricity ratios (e.g., 0.05 for 5%)
- Overwrite[]: Whether to override (optional in v19)

Your code tries both 4-arg and 5-arg versions — **CORRECT**.

### SapModel.Story.SetStories(...)
```
int SetStories(
    string[] StoryNames,
    double[] StoryElevations,
    double[] StoryHeights,
    bool[] IsMasterStory,
    string[] SimilarToStory,
    bool[] SpliceAbove,
    double[] SpliceHeight
)
```
7 arrays. Your code passes all 7 — **CORRECT** but this method is unreliable in v19 when stories were already created by NewGridOnly.

---

## Summary of Issues in Your Pipeline

| Function | Status in your code | Issue |
|----------|-------------------|-------|
| InitializeNewModel | CORRECT | Uses eUnits=12 (Ton_m_C) |
| NewGridOnly | CORRECT | 7 params, correct order |
| SetMaterial | CORRECT but legacy | Works fine, not deprecated per se |
| SetMPIsotropic | CORRECT | 4 args (Temp optional) |
| SetOConcrete_1 | CORRECT | 9 args (Temp optional) |
| SetRectangle | CORRECT | 4 args (3 optional omitted) |
| SetWall | CORRECT | 5 args |
| SetSlab | CORRECT | 5 args |
| AreaObj.AddByCoord | CORRECT | 8 args including CSys |
| FrameObj.AddByCoord | CORRECT | 10 args including CSys |
| SetDiaphragm | CORRECT | 2 args (ItemType optional) |
| LoadPatterns.Add | CORRECT | 4 args |
| SetLoadUniform | CORRECT | 6 args |
| **FuncRS.SetFromFile** | **PROBLEMATIC** | v19 = 5 params, review-ia uses 7 (v21 sig) |
| **FuncRS.SetUser** | **UNCERTAIN** | Should work with 5 args in v19 |
| RS.SetLoads | CORRECT | 7 args |
| RunAnalysis | CORRECT | No params |
| StoryDrifts | UNCERTAIN | Placeholder args may not match binding |
| JointDrifts | DOES NOT EXIST in v19 | Use JointDispl instead |
| DatabaseTables | NOT USED | Could be useful fallback |

---

## Key Recommendations

1. **FuncRS.SetFromFile**: For v19, use exactly 5 params: `(name, file, 0, 0.05, 0)`.
   The review-ia version's 7-arg call is v21 only.

2. **FuncRS.SetUser**: Should work with 5 params `(name, count, T_list, Sa_list, 0.05)`.
   If it fails, the issue is likely comtypes SAFEARRAY marshaling, not the signature.

3. **Results functions**: Consider using `DatabaseTables.GetTableForDisplayArray` as a
   more reliable alternative. It bypasses the COM binding issues with `ref` parameters.

4. **JointDrifts**: Does not exist in v19. Use `StoryDrifts` or compute from
   `JointDispl` manually.

5. **All `_1` suffix functions** (SetOConcrete_1, SetORebar_1, SetShell_1): These are
   "version 1 revisions" of original functions. The original (without suffix) is
   deprecated. The `_1` is the current standard in v19.
