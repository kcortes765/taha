# Firmas COM Exactas — CSI ETABS v19 OAPI (Python + comtypes)

> **Feature**: R03
> **Fecha**: 20 marzo 2026
> **Propósito**: Referencia DEFINITIVA de firmas COM para cada función crítica del pipeline.
> **Complementa**: R01 (referencia API general), R02 (patrones Python)

---

## Tabla de Contenidos

1. [Convenciones](#convenciones)
2. [Modelo e Inicialización](#1-modelo-e-inicialización)
3. [Materiales](#2-materiales)
4. [Secciones Frame](#3-secciones-frame)
5. [Secciones Area](#4-secciones-area)
6. [Geometría — Puntos](#5-geometría--puntos)
7. [Geometría — Frames](#6-geometría--frames)
8. [Geometría — Áreas](#7-geometría--áreas)
9. [Diafragmas](#8-diafragmas)
10. [Patrones y Cargas](#9-patrones-y-cargas)
11. [Espectro de Respuesta](#10-espectro-de-respuesta)
12. [Casos de Carga — Response Spectrum](#11-casos-de-carga--response-spectrum)
13. [Fuente de Masa](#12-fuente-de-masa)
14. [Análisis](#13-análisis)
15. [Resultados](#14-resultados)
16. [Database Tables](#15-database-tables)
17. [Inconsistencias entre Versiones](#16-inconsistencias-entre-versiones)
18. [Funciones que NO existen en ETABS](#17-funciones-que-no-existen-en-etabs)
19. [Fuentes](#18-fuentes)

---

## Convenciones

- **Req**: parámetro requerido | **Opt**: parámetro opcional (con default)
- **ref**: parámetro pasado por referencia (output en COM, se pasa vacío y la API lo llena)
- **ret = 0**: éxito en todas las funciones CSI
- 🔴 = INCONSISTENTE entre versiones | ⚠️ = cuidado especial | ✅ = estable
- Unidades del proyecto: **12 = Tonf_m_C**
- Versión objetivo: **ETABS v19** (API forward-compatible desde v18)

---

## 1. Modelo e Inicialización

### 1.1 `SapModel.InitializeNewModel` ✅

```
ret = SapModel.InitializeNewModel(eUnits)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `eUnits` | int | Opt (default=4=kip_ft_F) | Unidades del modelo. Usar **12** para Tonf_m_C |

**Return**: int (0=éxito)

**Nota**: El parámetro eUnits es opcional. Si se omite, usa kip_ft_F. SIEMPRE pasarlo explícitamente.

**Uso correcto**:
```python
ret = SapModel.InitializeNewModel(12)  # Tonf_m_C
```

---

### 1.2 `SapModel.File.NewBlank` ✅

```
ret = SapModel.File.NewBlank()
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| — | (ninguno) | — | — | Crea modelo completamente en blanco |

**Return**: int (0=éxito)

**Nota**: Crea un modelo vacío sin grilla ni pisos. Para nuestro proyecto es preferible `NewGridOnly`.

---

### 1.3 `SapModel.File.NewGridOnly` ✅

```
ret = SapModel.File.NewGridOnly(NumberStorys, TypicalStoryHeight, BottomStoryHeight, NumberLinesX, NumberLinesY, SpacingX, SpacingY)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `NumberStorys` | int | Req | Número de pisos |
| 2 | `TypicalStoryHeight` | float | Req | Altura piso tipo |
| 3 | `BottomStoryHeight` | float | Req | Altura primer piso |
| 4 | `NumberLinesX` | int | Req | Líneas de grilla en X |
| 5 | `NumberLinesY` | int | Req | Líneas de grilla en Y |
| 6 | `SpacingX` | float | Req | Espaciamiento uniforme X |
| 7 | `SpacingY` | float | Req | Espaciamiento uniforme Y |

**Return**: int (0=éxito)

**Total args**: 7 (todos requeridos)

**Verificado en**: docs.csiamerica.com API 2016, Eng-Tips thread 516841, repos danielogg92, mtavares51.

**Uso correcto** (Edificio 1):
```python
ret = SapModel.File.NewGridOnly(20, 2.6, 3.4, 17, 6, 5.0, 5.0)
```

**LECCIÓN**: Con `ret=0`, las stories se crean correctamente. Es preferible a NewBlank + Story.SetStories.

---

## 2. Materiales

### 2.1 `SapModel.PropMaterial.SetMaterial` ✅ (Legacy)

```
ret = SapModel.PropMaterial.SetMaterial(Name, MatType)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del material |
| 2 | `MatType` | int (eMatType) | Req | 1=Steel, 2=Concrete, 6=Rebar |

**Return**: int (0=éxito)

**Total args**: 2

**Estado**: NO formalmente deprecated, pero CSI recomienda `AddMaterial` en v18+. `SetMaterial` sigue funcionando en v19.

**Uso correcto**:
```python
ret = SapModel.PropMaterial.SetMaterial("G30", 2)       # Concrete
ret = SapModel.PropMaterial.SetMaterial("A630-420H", 6)  # Rebar
```

---

### 2.2 `SapModel.PropMaterial.AddMaterial` ✅ (Recomendado v18+)

```
ret = SapModel.PropMaterial.AddMaterial(ref Name, MatType, Region, Standard, Grade, UserName)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | ref str | Req | Nombre (output — la API lo genera o confirma) |
| 2 | `MatType` | int (eMatType) | Req | 1=Steel, 2=Concrete, 6=Rebar |
| 3 | `Region` | str | Req | "Chile", "United States", etc. |
| 4 | `Standard` | str | Req | "ACI 318-08", etc. |
| 5 | `Grade` | str | Req | "f'c 30 MPa", "Grade 420", etc. |
| 6 | `UserName` | str | Opt ("") | Nombre personalizado |

**Return**: tupla (Name, ret) en COM

**Total args**: 6

**Nota**: El parámetro `Name` es por referencia — en comtypes se pasa un string vacío y la API devuelve el nombre asignado.

---

### 2.3 `SapModel.PropMaterial.SetMPIsotropic` ✅

```
ret = SapModel.PropMaterial.SetMPIsotropic(Name, E, U, A, Temp)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del material |
| 2 | `E` | float | Req | Módulo de elasticidad |
| 3 | `U` | float | Req | Coeficiente de Poisson |
| 4 | `A` | float | Req | Coeficiente de expansión térmica |
| 5 | `Temp` | float | Opt (0.0) | Temperatura de referencia |

**Return**: int (0=éxito)

**Total args**: 4 requeridos + 1 opcional = 5

**Verificado**: Repos danielogg92, ebrahimraeyat, mtavares51 todos usan 4 args (sin Temp). Funciona en v19.

**Uso correcto** (G30):
```python
# En Tonf_m_C: Ec = 4700√30 × 101.937 = 2,624,300 tonf/m²
ret = SapModel.PropMaterial.SetMPIsotropic("G30", 2624300.0, 0.2, 1.0E-05)
```

---

### 2.4 `SapModel.PropMaterial.SetOConcrete_1` ✅

```
ret = SapModel.PropMaterial.SetOConcrete_1(Name, Fc, IsLightweight, FcsFactor, SSType, SSHysType, StrainAtFc, StrainUltimate, FinalSlope, FrictionAngle, DilatationalAngle, Temp)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del material |
| 2 | `Fc` | float | Req | f'c (en unidades del modelo) |
| 3 | `IsLightweight` | bool | Req | ¿Hormigón liviano? |
| 4 | `FcsFactor` | float | Req | Factor fcs (típico 1.0) |
| 5 | `SSType` | int | Req | 0=Simple, 1=Mander |
| 6 | `SSHysType` | int | Req | 0=Elastic, 1=Kinematic, 2=Takeda... |
| 7 | `StrainAtFc` | float | Req | Deformación en f'c (típico 0.002216) |
| 8 | `StrainUltimate` | float | Req | Deformación última (típico 0.005) |
| 9 | `FinalSlope` | float | Req | Pendiente final curva σ-ε (típico -0.1) |
| 10 | `FrictionAngle` | float | Opt (0.0) | Ángulo de fricción (análisis no lineal) |
| 11 | `DilatationalAngle` | float | Opt (0.0) | Ángulo dilatacional |
| 12 | `Temp` | float | Opt (0.0) | Temperatura de referencia |

**Return**: int (0=éxito)

**Total args**: 9 requeridos + 3 opcionales = 12 máximo

**DIFERENCIA vs SetOConcrete (sin _1)**: La versión original `SetOConcrete` solo tenía 8 parámetros (sin FinalSlope, FrictionAngle, DilatationalAngle, Temp). La `_1` es la versión extendida desde API 2016. Patrón CSI: sufijo `_1` = versión revisada con más parámetros.

**Uso correcto** (G30, con 9 args mínimos):
```python
# f'c = 3000 tonf/m² (30 MPa × 101.937) si unidades Tonf_m_C
ret = SapModel.PropMaterial.SetOConcrete_1("G30", 3000.0, False, 1.0, 1, 0, 0.002216, 0.005, -0.1)
```

---

### 2.5 `SapModel.PropMaterial.SetORebar_1` ✅

```
ret = SapModel.PropMaterial.SetORebar_1(Name, Fy, Fu, EFy, EFu, SSType, SSHysType, StrainAtHardening, StrainUltimate, FinalSlope, UseCaltransDefaults)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del material |
| 2 | `Fy` | float | Req | Tensión de fluencia |
| 3 | `Fu` | float | Req | Tensión última |
| 4 | `EFy` | float | Req | Tensión fluencia esperada |
| 5 | `EFu` | float | Req | Tensión última esperada |
| 6 | `SSType` | int | Req | 0=Simple, 1=Park |
| 7 | `SSHysType` | int | Req | Tipo histerético |
| 8 | `StrainAtHardening` | float | Req | Deformación inicio endurecimiento |
| 9 | `StrainUltimate` | float | Req | Deformación última |
| 10 | `FinalSlope` | float | Req | Pendiente final |
| 11 | `UseCaltransDefaults` | bool | Req | Usar defaults Caltrans |

**Return**: int (0=éxito)

**Total args**: 11

---

### 2.6 `SapModel.PropMaterial.SetWeightAndMass` ✅

```
ret = SapModel.PropMaterial.SetWeightAndMass(Name, MyOption, Value)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del material |
| 2 | `MyOption` | int | Req | 1=Weight/vol, 2=Mass/vol |
| 3 | `Value` | float | Req | Valor en unidades del modelo |

**Return**: int (0=éxito)

**Total args**: 3

**Uso correcto**:
```python
ret = SapModel.PropMaterial.SetWeightAndMass("G30", 1, 2.5)  # 2.5 tonf/m³
```

---

## 3. Secciones Frame

### 3.1 `SapModel.PropFrame.SetRectangle` ✅

```
ret = SapModel.PropFrame.SetRectangle(Name, MatProp, T3, T2, Color, Notes, GUID)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre de la sección |
| 2 | `MatProp` | str | Req | Material asociado |
| 3 | `T3` | float | Req | Profundidad/peralte (eje local 3) |
| 4 | `T2` | float | Req | Ancho (eje local 2) |
| 5 | `Color` | int | Opt (-1) | Color (-1 = default) |
| 6 | `Notes` | str | Opt ("") | Notas |
| 7 | `GUID` | str | Opt ("") | Identificador único |

**Return**: int (0=éxito)

**Total args**: 4 requeridos + 3 opcionales = 7

**Uso correcto** (vigas invertidas 20/60):
```python
ret = SapModel.PropFrame.SetRectangle("VI20/60G30", "G30", 0.60, 0.20)
```

---

### 3.2 `SapModel.PropFrame.SetModifiers` ✅

```
ret = SapModel.PropFrame.SetModifiers(Name, Value)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre de la sección |
| 2 | `Value` | float[8] | Req | [A, As2, As3, J, I22, I33, M, W] |

**Return**: int (0=éxito)

**Total args**: 2

**Uso correcto** (J=0 para vigas):
```python
ret = SapModel.PropFrame.SetModifiers("VI20/60G30", [1,1,1, 0.0, 1,1,1,1])
```

---

## 4. Secciones Area

### 4.1 `SapModel.PropArea.SetWall` ✅

```
ret = SapModel.PropArea.SetWall(Name, eWallPropType, eShellType, MatProp, Thickness, Color, Notes, GUID)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre de la propiedad |
| 2 | `eWallPropType` | int | Req | 0=Specified, 1=AutoSelectList |
| 3 | `eShellType` | int | Req | 1=Thin, 2=Thick, 3=Membrane, 5=Shell |
| 4 | `MatProp` | str | Req | Material |
| 5 | `Thickness` | float | Req | Espesor |
| 6 | `Color` | int | Opt (-1) | Color |
| 7 | `Notes` | str | Opt ("") | Notas |
| 8 | `GUID` | str | Opt ("") | Identificador |

**Return**: int (0=éxito)

**Total args**: 5 requeridos + 3 opcionales = 8

**Verificado**: docs.csiamerica.com/help-files/etabs-api-2016/html/20e9156e-*.htm

**Uso correcto**:
```python
ret = SapModel.PropArea.SetWall("MHA30G30", 0, 2, "G30", 0.30)  # ShellThick
ret = SapModel.PropArea.SetWall("MHA20G30", 0, 2, "G30", 0.20)
```

---

### 4.2 `SapModel.PropArea.SetSlab` ✅

```
ret = SapModel.PropArea.SetSlab(Name, eSlabType, eShellType, MatProp, Thickness, Color, Notes, GUID)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre de la propiedad |
| 2 | `eSlabType` | int | Req | 0=Slab, 1=Drop, 2=Stiff, 3=Ribbed, 4=Waffle |
| 3 | `eShellType` | int | Req | 1=Thin, 2=Thick, 5=Shell |
| 4 | `MatProp` | str | Req | Material |
| 5 | `Thickness` | float | Req | Espesor |
| 6 | `Color` | int | Opt (-1) | Color |
| 7 | `Notes` | str | Opt ("") | Notas |
| 8 | `GUID` | str | Opt ("") | Identificador |

**Return**: int (0=éxito)

**Total args**: 5 requeridos + 3 opcionales = 8

**Uso correcto**:
```python
ret = SapModel.PropArea.SetSlab("Losa15G30", 0, 1, "G30", 0.15)  # ShellThin
```

---

### 4.3 `SapModel.PropArea.SetShell_1` 🔴 NO EXISTE EN ETABS

**`SetShell_1` es una función de SAP2000, NO de ETABS.**

ETABS usa métodos separados: `SetWall`, `SetSlab`, `SetDeck`, `SetSlabRibbed`. No tiene un método genérico `SetShell_1`.

**Si ves `SetShell_1` en código para ETABS, es un error** — el código fue escrito originalmente para SAP2000.

---

### 4.4 `SapModel.PropArea.SetModifiers` ✅

```
ret = SapModel.PropArea.SetModifiers(Name, Value)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre de la propiedad |
| 2 | `Value` | float[10] | Req | [f11, f22, f12, m11, m22, m12, v13, v23, Mass, Weight] |

**Return**: int (0=éxito)

**Total args**: 2

**Uso correcto** (losa inercia 25%):
```python
ret = SapModel.PropArea.SetModifiers("Losa15G30", [1,1,1, 0.25,0.25,0.25, 1,1, 1,1])
```

---

## 5. Geometría — Puntos

### 5.1 `SapModel.PointObj.AddCartesian` ✅

```
ret = SapModel.PointObj.AddCartesian(X, Y, Z, ref Name, UserName, CSys, MergeOff, MergeNumber)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `X` | float | Req | Coordenada X |
| 2 | `Y` | float | Req | Coordenada Y |
| 3 | `Z` | float | Req | Coordenada Z |
| 4 | `Name` | ref str | Req | Nombre (output, pasar "") |
| 5 | `UserName` | str | Opt ("") | Nombre personalizado |
| 6 | `CSys` | str | Opt ("Global") | Sistema de coordenadas |
| 7 | `MergeOff` | bool | Opt (False) | Desactivar merge automático |
| 8 | `MergeNumber` | int | Opt (0) | Tolerancia de merge |

**Return**: tupla (Name, ret) en COM

**Total args**: 3 requeridos + 5 opcionales = 8

**Nota**: En la práctica, los puntos se crean automáticamente al agregar frames o áreas por coordenadas. No es necesario crear puntos explícitamente en la mayoría de los casos.

---

## 6. Geometría — Frames

### 6.1 `SapModel.FrameObj.AddByCoord` ✅

```
ret = SapModel.FrameObj.AddByCoord(xi, yi, zi, xj, yj, zj, ref Name, PropName, UserName, CSys)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `xi` | float | Req | X inicio (punto I) |
| 2 | `yi` | float | Req | Y inicio |
| 3 | `zi` | float | Req | Z inicio |
| 4 | `xj` | float | Req | X fin (punto J) |
| 5 | `yj` | float | Req | Y fin |
| 6 | `zj` | float | Req | Z fin |
| 7 | `Name` | ref str | Req | Nombre (output, pasar "") |
| 8 | `PropName` | str | Opt ("Default") | Sección asignada |
| 9 | `UserName` | str | Opt ("") | Nombre personalizado |
| 10 | `CSys` | str | Opt ("Global") | Sistema de coordenadas |

**Return**: tupla (Name, ret) en COM

**Total args**: 6 requeridos + 4 opcionales = 10

**Verificado**: repos danielogg92, mtavares51, ebrahimraeyat, docs CSI.

**Uso correcto**:
```python
name = ""
ret = SapModel.FrameObj.AddByCoord(0, 0, 3.4, 0, 5.14, 3.4, name, "VI20/60G30")
# ret = (nombre_asignado, 0) si éxito
```

**Bug conocido v19**: `FrameObj.GetNameList()` a veces retorna 0 frames aunque AddByCoord reporta éxito. Puede ser problema de binding COM. Verificar abriendo .edb en ETABS UI.

---

### 6.2 `SapModel.FrameObj.AddByPoint` ✅

```
ret = SapModel.FrameObj.AddByPoint(Point1, Point2, ref Name, PropName, UserName)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Point1` | str | Req | Nombre del punto I |
| 2 | `Point2` | str | Req | Nombre del punto J |
| 3 | `Name` | ref str | Req | Nombre (output, pasar "") |
| 4 | `PropName` | str | Opt ("Default") | Sección asignada |
| 5 | `UserName` | str | Opt ("") | Nombre personalizado |

**Return**: tupla (Name, ret) en COM

**Total args**: 2 requeridos + 3 opcionales = 5

---

### 6.3 `SapModel.FrameObj.SetInsertionPoint` ✅

```
ret = SapModel.FrameObj.SetInsertionPoint(Name, CardinalPoint, Mirror2, StiffTransform, Offset1, Offset2, CSys, ItemType)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del frame |
| 2 | `CardinalPoint` | int | Req | 1-11 (2=Bottom Center para vigas invertidas) |
| 3 | `Mirror2` | bool | Req | Espejo eje local 2 |
| 4 | `StiffTransform` | bool | Req | Transformar rigidez |
| 5 | `Offset1` | float[3] | Req | Offset punto I [dx,dy,dz] |
| 6 | `Offset2` | float[3] | Req | Offset punto J [dx,dy,dz] |
| 7 | `CSys` | str | Opt ("Global") | Sistema coordenadas |
| 8 | `ItemType` | int | Opt (0) | 0=Object, 1=Group |

**Total args**: 6 requeridos + 2 opcionales = 8

---

### 6.4 `SapModel.FrameObj.SetLoadDistributed` ✅

```
ret = SapModel.FrameObj.SetLoadDistributed(Name, LoadPat, MyType, Dir, Dist1, Dist2, Val1, Val2, CSys, RelDist, Replace, ItemType)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del frame |
| 2 | `LoadPat` | str | Req | Patrón de carga |
| 3 | `MyType` | int | Req | 1=Force, 2=Moment |
| 4 | `Dir` | int | Req | Dirección (6=Gravity, 10=ProjX, 11=ProjY, 12=ProjZ) |
| 5 | `Dist1` | float | Req | Distancia inicio (0-1 si relativa) |
| 6 | `Dist2` | float | Req | Distancia fin (0-1 si relativa) |
| 7 | `Val1` | float | Req | Valor al inicio |
| 8 | `Val2` | float | Req | Valor al fin |
| 9 | `CSys` | str | Opt ("Global") | Sistema coordenadas |
| 10 | `RelDist` | bool | Opt (True) | True = distancias relativas |
| 11 | `Replace` | bool | Opt (True) | Reemplazar cargas existentes |
| 12 | `ItemType` | int | Opt (0) | 0=Object, 1=Group |

**Return**: int (0=éxito)

**Total args**: 8 requeridos + 4 opcionales = 12

**Uso correcto** (carga uniforme en viga):
```python
ret = SapModel.FrameObj.SetLoadDistributed(
    "B1", "SCP", 1, 6, 0.0, 1.0, -0.25, -0.25, "Global", True, True
)
```

---

## 7. Geometría — Áreas

### 7.1 `SapModel.AreaObj.AddByCoord` ✅

```
ret = SapModel.AreaObj.AddByCoord(NumberPoints, X, Y, Z, ref Name, PropName, UserName, CSys)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `NumberPoints` | int | Req | Número de vértices (típico 4) |
| 2 | `X` | float[] | Req | Array de coordenadas X |
| 3 | `Y` | float[] | Req | Array de coordenadas Y |
| 4 | `Z` | float[] | Req | Array de coordenadas Z |
| 5 | `Name` | ref str | Req | Nombre (output, pasar "") |
| 6 | `PropName` | str | Opt ("Default") | Propiedad de área |
| 7 | `UserName` | str | Opt ("") | Nombre personalizado |
| 8 | `CSys` | str | Opt ("Global") | Sistema coordenadas |

**Return**: tupla (Name, ret) en COM

**Total args**: 4 requeridos + 4 opcionales = 8

**Verificado**: docs CSI API 2016, Eng-Tips thread 477551, repos ebrahimraeyat, retug.

**Uso correcto** (muro vertical):
```python
X = [0.0, 0.0, 0.0, 0.0]
Y = [0.0, 5.14, 5.14, 0.0]
Z = [0.0, 0.0, 3.4, 3.4]
name = ""
ret = SapModel.AreaObj.AddByCoord(4, X, Y, Z, name, "MHA30G30")
```

---

### 7.2 `SapModel.AreaObj.AddByPoint` ✅

```
ret = SapModel.AreaObj.AddByPoint(NumberPoints, PointNames, ref Name, PropName, UserName)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `NumberPoints` | int | Req | Número de puntos |
| 2 | `PointNames` | str[] | Req | Array de nombres de puntos |
| 3 | `Name` | ref str | Req | Nombre (output) |
| 4 | `PropName` | str | Opt ("Default") | Propiedad de área |
| 5 | `UserName` | str | Opt ("") | Nombre personalizado |

**Return**: tupla (Name, ret)

**Total args**: 2 requeridos + 3 opcionales = 5

---

### 7.3 `SapModel.AreaObj.SetAutoMesh` ✅

```
ret = SapModel.AreaObj.SetAutoMesh(Name, MeshType, n1, n2, MaxSize1, MaxSize2, PointOnEdge, ExtendCookies, Rotation, MaxSizeGeneral, LocalAxesOnEdge, LocalAxesOnFace, RestraintsOnEdge, RestraintsOnFace, ItemType, Group, SubMesh, SubMeshSize)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del area |
| 2 | `MeshType` | int | Req | 0=None, 1=Auto, 4=MaxSize |
| 3 | `n1` | int | Req | Divisiones dir 1 |
| 4 | `n2` | int | Req | Divisiones dir 2 |
| 5 | `MaxSize1` | float | Req | Tamaño máx dir 1 |
| 6 | `MaxSize2` | float | Req | Tamaño máx dir 2 |
| 7 | `PointOnEdge` | bool | Req | Puntos en bordes |
| 8 | `ExtendCookies` | bool | Req | Extender cookies |
| 9 | `Rotation` | float | Req | Rotación |
| 10 | `MaxSizeGeneral` | float | Req | Tamaño máx general |
| 11 | `LocalAxesOnEdge` | bool | Req | — |
| 12 | `LocalAxesOnFace` | bool | Req | — |
| 13 | `RestraintsOnEdge` | bool | Req | — |
| 14 | `RestraintsOnFace` | bool | Req | — |
| 15+ | Opcionales... | — | Opt | ItemType, Group, SubMesh, SubMeshSize |

**Total args**: 14 requeridos + 4 opcionales = 18

**Uso correcto** (AutoMesh 0.4m):
```python
ret = SapModel.AreaObj.SetAutoMesh("W1", 4, 0, 0, 0.4, 0.4, False, False, 0, 0.4, False, False, False, False)
```

---

## 8. Diafragmas

### 8.1 `SapModel.Diaphragm.SetDiaphragm` ✅

```
ret = SapModel.Diaphragm.SetDiaphragm(Name, SemiRigid)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del diafragma |
| 2 | `SemiRigid` | bool | Req | True=semi-rígido, False=rígido |

**Return**: int (0=éxito)

**Total args**: 2

---

### 8.2 `SapModel.AreaObj.SetDiaphragm` ✅

```
ret = SapModel.AreaObj.SetDiaphragm(Name, DiaphragmName, ItemType)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del area |
| 2 | `DiaphragmName` | str | Req | Nombre del diafragma ("D1") |
| 3 | `ItemType` | int | Opt (0) | 0=Object, 1=Group, 2=Selected |

**Return**: int (0=éxito)

**Total args**: 2 requeridos + 1 opcional = 3

**Uso correcto**:
```python
ret = SapModel.AreaObj.SetDiaphragm("F1", "D1")
```

---

## 9. Patrones y Cargas

### 9.1 `SapModel.LoadPatterns.Add` ✅

```
ret = SapModel.LoadPatterns.Add(Name, MyType, SelfWTMultiplier, AddAnalysisCase)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del patrón |
| 2 | `MyType` | int (eLoadPatternType) | Req | 1=Dead, 2=SuperDead, 3=Live, 5=Quake |
| 3 | `SelfWTMultiplier` | float | Opt (0.0) | Multiplicador peso propio |
| 4 | `AddAnalysisCase` | bool | Opt (True) | Agregar caso de análisis automáticamente |

**Return**: int (0=éxito)

**Total args**: 2 requeridos + 2 opcionales = 4 CONFIRMADO

**Uso correcto** (patrones del proyecto):
```python
ret = SapModel.LoadPatterns.Add("PP", 1, 1.0, True)    # Dead, SWM=1
ret = SapModel.LoadPatterns.Add("TERP", 2, 0.0, True)  # SuperDead
ret = SapModel.LoadPatterns.Add("TERT", 2, 0.0, True)  # SuperDead
ret = SapModel.LoadPatterns.Add("SCP", 3, 0.0, True)   # Live
ret = SapModel.LoadPatterns.Add("SCT", 3, 0.0, True)   # Live
ret = SapModel.LoadPatterns.Add("SX", 5, 0.0, False)   # Quake (sin caso auto)
ret = SapModel.LoadPatterns.Add("SY", 5, 0.0, False)   # Quake
```

---

### 9.2 `SapModel.AreaObj.SetLoadUniform` ✅

```
ret = SapModel.AreaObj.SetLoadUniform(Name, LoadPat, Value, Dir, Replace, CSys, ItemType)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del area |
| 2 | `LoadPat` | str | Req | Patrón de carga |
| 3 | `Value` | float | Req | Valor de la carga (negativo = hacia abajo) |
| 4 | `Dir` | int | Req | 6=Gravity (Z global hacia abajo) |
| 5 | `Replace` | bool | Opt (True) | Reemplazar cargas existentes |
| 6 | `CSys` | str | Opt ("Global") | Sistema coordenadas |
| 7 | `ItemType` | int | Opt (0) | 0=Object, 1=Group |

**Return**: int (0=éxito)

**Total args**: 4 requeridos + 3 opcionales = 7

**Uso correcto**:
```python
# SCP oficinas = 0.25 tonf/m² hacia abajo
ret = SapModel.AreaObj.SetLoadUniform("F1", "SCP", -0.25, 6, True)
```

---

## 10. Espectro de Respuesta

### 10.1 `SapModel.Func.FuncRS.SetUser` ✅ (RECOMENDADO)

```
ret = SapModel.Func.FuncRS.SetUser(Name, NumberItems, Period, Value, DampRatio)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre de la función |
| 2 | `NumberItems` | int | Req | Número de puntos T-Sa |
| 3 | `Period` | float[] | Req | Array de períodos (s) |
| 4 | `Value` | float[] | Req | Array de Sa/g (normalizado) |
| 5 | `DampRatio` | float | Opt (0.05) | Razón de amortiguamiento |

**Return**: int (0=éxito)

**Total args**: 4 requeridos + 1 opcional = 5

**NOTA IMPORTANTE**: Los valores Sa se ingresan como Sa/g (adimensionales). El factor de escala SF=9.81 se aplica en el LoadCase, NO aquí.

**Verificado en**: stru.ai seismic automation, repos danielogg92, mihdicaballero.

⚠️ **NOTA sobre path**: Algunos recursos usan `SapModel.Func.ResponseSpectrum.SetUser(...)` en lugar de `SapModel.Func.FuncRS.SetUser(...)`. Ambos paths pueden funcionar dependiendo de la versión y binding COM. En v19 con comtypes, verificar cuál está disponible en el TLB generado.

---

### 10.2 `SapModel.Func.FuncRS.SetFromFile` 🔴 NO EXISTE EN ETABS

```
⚠️ ESTA FUNCIÓN NO EXISTE EN LA API DE ETABS ⚠️
```

**Hallazgo CRÍTICO confirmado por múltiples fuentes (ResearchGate, Eng-Tips, docs CSI)**:

- `SetFromFile` es una función de **SAP2000**, NO de ETABS
- En SAP2000 la firma era: `(Name, FileName, HeadLines, PreChars, PointsPerLine, ValueType, FreeFormat)` — 7 args
- SAP2000 luego la marcó obsoleta y creó `SetFromFile_1` con 8 args
- **ETABS nunca tuvo esta función**

**ESTO EXPLICA EL ERROR** en el script `08_spectrum_cases.py` del pipeline: estaba llamando una función que no existe.

**ALTERNATIVA CORRECTA para ETABS v19**:
```python
# 1. Leer archivo de espectro manualmente en Python
import numpy as np
data = np.loadtxt("espectro_NCh433_DS61.txt", skiprows=1)
T = data[:, 0].tolist()
Sa_g = data[:, 1].tolist()

# 2. Definir con SetUser
ret = SapModel.Func.FuncRS.SetUser("NCh433_DS61", len(T), T, Sa_g, 0.05)
```

---

## 11. Casos de Carga — Response Spectrum

### 11.1 `SapModel.LoadCases.ResponseSpectrum.SetCase` ✅

```
ret = SapModel.LoadCases.ResponseSpectrum.SetCase(Name)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del caso |

**Return**: int (0=éxito)

**Total args**: 1

---

### 11.2 `SapModel.LoadCases.ResponseSpectrum.SetLoads` ⚠️

```
ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(Name, NumberLoads, LoadType, LoadName, SF, CSys, Ang)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del caso |
| 2 | `NumberLoads` | int | Req | Número de cargas |
| 3 | `LoadType` | str[] | Req | Dirección: ["U1"] para X, ["U2"] para Y |
| 4 | `LoadName` | str[] | Req | Función espectro: ["NCh433_DS61"] |
| 5 | `SF` | float[] | Req | Factor escala: [9.81] |
| 6 | `CSys` | str[] | Req | Sistema coord: ["Global"] |
| 7 | `Ang` | float[] | Req | Ángulo: [0.0] |

**Return**: int (0=éxito)

**Total args**: 7

⚠️ **CUIDADO**: Algunos recursos muestran 8 args adicionales (con arrays de 0.0 extra). La firma base es 7, pero en algunas versiones el binding COM puede requerir arrays placeholder adicionales. Si falla con 7 args, probar con arrays extra de 0.0 al final.

**Uso correcto**:
```python
# Caso SEx (espectro en X)
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("SEx")
ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "SEx", 1, ["U1"], ["NCh433_DS61"], [9.81], ["Global"], [0.0]
)
```

---

### 11.3 `SapModel.LoadCases.ResponseSpectrum.SetModalCase` ✅

```
ret = SapModel.LoadCases.ResponseSpectrum.SetModalCase(Name, ModalCase)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del caso espectro |
| 2 | `ModalCase` | str | Req | Nombre del caso modal ("Modal") |

**Return**: int (0=éxito)

**Total args**: 2

---

### 11.4 `SapModel.LoadCases.ResponseSpectrum.SetEccentricity` ✅

```
ret = SapModel.LoadCases.ResponseSpectrum.SetEccentricity(Name, Eccen)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del caso |
| 2 | `Eccen` | float | Req | Excentricidad (0.05 = 5%) |

**Return**: int (0=éxito)

**Total args**: 2

---

## 12. Fuente de Masa

### 12.1 `SapModel.PropMaterial.SetMassSource_1` ⚠️

```
ret = SapModel.PropMaterial.SetMassSource_1(IncludeElements, IncludeAddedMass, IncludeLoads, NumberLoads, LoadPat, SF)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `IncludeElements` | bool | Req | Incluir masa de elementos |
| 2 | `IncludeAddedMass` | bool | Req | Incluir masa añadida |
| 3 | `IncludeLoads` | bool | Req | Incluir masa de cargas |
| 4 | `NumberLoads` | int | Req | Número de patrones de carga |
| 5 | `LoadPat` | str[] | Req | Nombres de patrones |
| 6 | `SF` | float[] | Req | Factores de escala |

**Return**: int (0=éxito)

**Total args**: 6

⚠️ **UBICACIÓN CRÍTICA**: La función está en `SapModel.PropMaterial`, **NO** en `SapModel.MassSource`. Esto es contraintuitivo pero está confirmado por la documentación oficial CSI (API 2015/2016).

⚠️ **LIMITACIÓN**: Solo cambia el mass source **por defecto**. No crea mass sources adicionales. Para agregar un mass source nuevo, usar DatabaseTables como alternativa.

**Uso correcto** (análisis sísmico chileno):
```python
# Masa = elementos + TERP×1.0 + SCP×0.25
ret = SapModel.PropMaterial.SetMassSource_1(
    True,            # Incluir masa de elementos
    False,           # No masa añadida
    True,            # Incluir masa de cargas
    2,               # 2 patrones
    ["TERP", "SCP"], # Patrones
    [1.0, 0.25]      # TERP=100%, SCP=25%
)
```

---

## 13. Análisis

### 13.1 `SapModel.Analyze.SetActiveDOF` ✅

```
ret = SapModel.Analyze.SetActiveDOF(DOF)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `DOF` | bool[6] | Req | [UX, UY, UZ, RX, RY, RZ] |

**Total args**: 1

---

### 13.2 `SapModel.Analyze.SetRunCaseFlag` ✅

```
ret = SapModel.Analyze.SetRunCaseFlag(Name, Run, All)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `Name` | str | Req | Nombre del caso (ignorado si All=True) |
| 2 | `Run` | bool | Req | True=ejecutar, False=no |
| 3 | `All` | bool | Opt (False) | Aplicar a todos los casos |

**Total args**: 2 requeridos + 1 opcional = 3

---

### 13.3 `SapModel.Analyze.RunAnalysis` ✅

```
ret = SapModel.Analyze.RunAnalysis()
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| — | (ninguno) | — | — | Ejecuta el análisis |

**Return**: int (0=éxito)

**Total args**: 0

**REQUISITO**: El modelo debe tener un path de archivo definido (haber sido guardado con File.Save previamente).

---

## 14. Resultados

### 14.1 `SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput` ✅

```
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
```

**Total args**: 0

---

### 14.2 `SapModel.Results.Setup.SetCaseSelectedForOutput` ✅

```
ret = SapModel.Results.Setup.SetCaseSelectedForOutput(CaseName)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `CaseName` | str | Req | Nombre del caso a seleccionar |

**Return**: int (0=éxito)

**Total args**: 1

---

### 14.3 `SapModel.Results.Setup.SetComboSelectedForOutput` ✅

```
ret = SapModel.Results.Setup.SetComboSelectedForOutput(ComboName)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `ComboName` | str | Req | Nombre del combo a seleccionar |

**Return**: int (0=éxito)

**Total args**: 1

---

### 14.4 `SapModel.Results.StoryDrifts` ✅

```
ret = SapModel.Results.StoryDrifts()
```

**Total args de entrada**: 0

**Return**: tupla de 12 elementos:
```
(NumberResults,     # int — número de resultados
 Story[],           # str[] — nombre del piso
 LoadCase[],        # str[] — caso de carga
 StepType[],        # str[] — tipo de paso
 StepNum[],         # float[] — número de paso
 Direction[],       # str[] — dirección ("X" o "Y")
 Drift[],           # float[] — valor del drift (Δ/h)
 Label[],           # str[] — etiqueta del nodo
 X[],               # float[] — coordenada X del nodo
 Y[],               # float[] — coordenada Y del nodo
 Z[],               # float[] — coordenada Z del nodo
 ret)               # int — 0=éxito
```

**Disponible desde**: ETABS 2016 (v16+). Confirmado en v19.

**Verificado**: Medium Hakan Keskin, repos youandvern, mihdicaballero.

---

### 14.5 `SapModel.Results.JointDrifts` ⚠️

```
ret = SapModel.Results.JointDrifts()
```

**Total args de entrada**: 0

**Return**: tupla con arrays:
```
(NumberResults,
 Story[],           # nombre del piso
 Label[],           # etiqueta del nodo
 Name[],            # nombre del nodo
 LoadCase[],        # caso de carga
 StepType[],
 StepNum[],
 DisplacementX[],   # desplazamiento en X
 DisplacementY[],   # desplazamiento en Y
 DriftX[],          # drift en X
 DriftY[],          # drift en Y
 ret)
```

**Disponible desde**: ETABS 2016 (API 2016). Documentado en docs CSI.

⚠️ **PRECAUCIÓN**: Aunque está documentado en API 2016, algunos usuarios reportan que no funciona correctamente en todas las versiones via comtypes. Si falla, usar `StoryDrifts()` como alternativa o extraer drifts via `DatabaseTables.GetTableForDisplayArray("Story Drifts", ...)`.

---

### 14.6 `SapModel.Results.BaseReac` ✅

```
ret = SapModel.Results.BaseReac(NumberResults, LoadCase, StepType, StepNum, Fx, Fy, Fz, Mx, My, Mz, gx, gy, gz)
```

**Total args de entrada**: 0 (todos son output por referencia)

**Return**: tupla de 13 elementos:
```
(NumberResults, LoadCase[], StepType[], StepNum[],
 Fx[], Fy[], Fz[], Mx[], My[], Mz[], gx, gy, gz, ret)
```

**Verificado**: Medium Hakan Keskin (extracting base reactions), repos danielogg92.

---

## 15. Database Tables

### 15.1 `SapModel.DatabaseTables.GetAvailableTables` ✅

```
ret = SapModel.DatabaseTables.GetAvailableTables()
```

**Total args**: 0

**Return**: (NumberTables, TableKeys[], TableKeys[], ret)

---

### 15.2 `SapModel.DatabaseTables.GetTableForDisplayArray` ✅

```
ret = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
```

| # | Parámetro | Tipo | Req/Opt | Descripción |
|---|-----------|------|---------|-------------|
| 1 | `TableKey` | str | Req | Nombre de la tabla |
| 2 | `FieldKeyList` | str | Req | Campos a incluir ("" para todos) |
| 3 | `GroupName` | str | Req | Grupo ("All" para todos) |
| 4 | `TableVersion` | int | Opt (1) | Versión de tabla |
| 5 | `FieldsKeysIncluded` | ref str[] | Output | Campos incluidos |
| 6 | `NumberRecords` | ref int | Output | Número de registros |
| 7 | `TableData` | ref str[] | Output | Datos de la tabla |

**Return**: tupla con outputs + ret

**Total args de entrada**: 4 (el resto son outputs)

**Tablas más usadas**:

| TableKey | Contenido |
|----------|-----------|
| `"Story Definitions"` | Pisos |
| `"Material Properties"` | Materiales |
| `"Frame Section Properties"` | Secciones frame |
| `"Area Section Properties"` | Secciones area |
| `"Joint Displacements"` | Desplazamientos |
| `"Story Drifts"` | Drifts (alternativa a Results.StoryDrifts) |
| `"Base Reactions"` | Reacciones base |
| `"Modal Participating Mass Ratios"` | Masas participantes |
| `"Centers Of Mass And Rigidity"` | CM y CR |

**Verificado**: repos retug/ETABs (database tables examples), ebrahimraeyat/etabs_api, Eng-Tips thread 497218.

**Uso correcto**:
```python
ret = SapModel.DatabaseTables.GetTableForDisplayArray(
    "Story Drifts", "", "All", 1, [], 0, []
)
fields = ret[4]   # FieldsKeysIncluded
n_records = ret[5] # NumberRecords
data = ret[6]      # TableData (flat array)
```

---

## 16. Inconsistencias entre Versiones

### 16.1 Ruptura mayor: v17 → v18

| Aspecto | v17 y anteriores | v18+ (v18, v19, v20, v21, v22) |
|---------|-----------------|-------------------------------|
| Compatibilidad | Cada versión podía romper API | Forward-compatible |
| API cross-product | Solo ETABS | SAP2000, CSiBridge, SAFE |
| Remote API | No | Sí (excepto v22) |

**Implicación**: Código escrito para v18 debería funcionar en v19 sin cambios.

---

### 16.2 Funciones con sufijo `_1` (versión revisada)

| Función original | Función `_1` | Diferencia |
|-----------------|-------------|-----------|
| `SetOConcrete` (8 args) | `SetOConcrete_1` (9-12 args) | +FinalSlope, FrictionAngle, DilatationalAngle, Temp |
| `SetOSteel` | `SetOSteel_1` | Patrón similar — args extendidos |
| `SetMassSource` | `SetMassSource_1` | Versión revisada |
| `SetFromFile` (SAP2000) | `SetFromFile_1` (SAP2000) | Versión revisada (obsoleta SAP2000 v14.12+) |

**Patrón CSI**: Cuando agregan parámetros, crean versión `_1` y marcan la original como obsoleta.

---

### 16.3 Problemas de comtypes por versión

| Versión comtypes | Problema |
|-----------------|---------|
| 1.1.2 | Requiere modificar `__init__.py` manualmente |
| 1.1.7 | Bugs con salida modal en ETABS |
| 1.1.8 | COMError con ETABS 19.0.2 |
| 1.2+ | Generalmente estable |

**Fix universal**: `py -m comtypes.clear_cache` antes de cada sesión crítica.

---

### 16.4 Bug GetTableForEditingArray (v19.1.0)

En ETABS v19.1.0, `GetTableForEditingArray` puede retornar null keys. Workaround: usar `GetTableForDisplayArray` si solo necesitas leer datos.

---

### 16.5 Bug AnalysisResults StepNumber (v22.5.0)

Varias funciones de `cAnalysisResults` retornaban el número de paso en vez del tiempo para casos de time history. Corregido en v22.5.1.

---

### 16.6 Bug GetNameList post-creación (v19)

`FrameObj.GetNameList()` y `AreaObj.GetNameList()` pueden retornar 0 elementos inmediatamente después de crear objetos via API. Posibles causas:
- Binding COM inconsistente (GetActiveObject vs CreateObject generan TLBs distintos)
- Los objetos existen pero el binding no los ve

**Workaround**: Guardar y reabrir el modelo, o verificar en la UI de ETABS.

---

## 17. Funciones que NO existen en ETABS

| Función | Existe en | NO existe en | Error típico |
|---------|-----------|-------------|-------------|
| `FuncRS.SetFromFile` | SAP2000 | ETABS | "wrong number of arguments" |
| `FuncRS.SetFromFile_1` | SAP2000 | ETABS | Función no encontrada |
| `PropArea.SetShell_1` | SAP2000 | ETABS | Usar SetWall/SetSlab |
| `FuncRS.SetASCE716` | — | ETABS | No disponible |

**Regla**: Si ves estas funciones en código "para ETABS", el código fue originalmente escrito para SAP2000 y adaptado incorrectamente.

---

## 18. Fuentes

### Documentación oficial CSI
- [CSI Developer Portal](https://www.csiamerica.com/developer)
- [ETABS API 2016 Help Files](https://docs.csiamerica.com/help-files/etabs-api-2016/)
- [SetWall Method](https://docs.csiamerica.com/help-files/etabs-api-2016/html/20e9156e-132b-d46b-fe42-8ef7002d8dba.htm)
- [SetSlab Method](https://docs.csiamerica.com/help-files/etabs-api-2016/html/5dc4e0d8-87be-b466-fd29-ac59f5b2bffe.htm)
- [NewGridOnly Method](https://docs.csiamerica.com/help-files/etabs-api-2016/html/cb79539c-729f-7231-1625-b8f15e018e1f.htm)
- [SetOConcrete_1 Method](https://docs.csiamerica.com/help-files/etabs-api-2016/html/6bc3a61c-6e41-716a-a401-937b2042e30b.htm)
- [SetMassSource_1 Method (API 2015)](https://docs.csiamerica.com/help-files/etabs-api-2015/html/3f256ea8-6c8d-76b0-acae-e1d370413b37.htm)
- [JointDrifts Method](https://docs.csiamerica.com/help-files/etabs-api-2016/html/054be507-4dd9-3c99-243f-566743acbdc1.htm)
- [StoryDrifts Method](https://docs.csiamerica.com/help-files/etabs-api-2016/html/e55e16e2-b7b0-2864-f3dc-b781f4062325.htm)
- [Example 7 (Python)](http://docs.csiamerica.com/help-files/common-api(from-sap-and-csibridge)/Example_Code/Example_7_(Python).htm)

### Repos GitHub verificados
- [danielogg92/Etabs-API-Python](https://github.com/danielogg92/Etabs-API-Python) — 67★, wrappers comtypes
- [ebrahimraeyat/etabs_api](https://github.com/ebrahimraeyat/etabs_api) — PyPI `etabs-api`, ETABS 2018+
- [retug/ETABs](https://github.com/retug/ETABs) — Database Tables, comtypes v1.1.7
- [mihdicaballero/ETABS-Ninja](https://github.com/mihdicaballero/ETABS-Ninja) — Drift, matplotlib
- [mtavares51/etabs_python_modelling](https://github.com/mtavares51/etabs_python_modelling) — Modelación paramétrica

### Blogs y tutoriales
- [Stru.ai — ETABS Seismic Automation](https://stru.ai/blog/etabs-seismic-automation)
- [Stru.ai — ETABS API 2025](https://stru.ai/blog/etabs-api-automation-2025)
- [Stru.ai — ETABS Beginner Guide](https://stru.ai/blog/etabs-api-beginner-guide)
- [EngineeringSkills — ETABS Python API Intro](https://www.engineeringskills.com/posts/an-introduction-to-the-etabs-python-api)
- [Hakan Keskin — Story Drifts Python](https://hakan-keskin.medium.com/extracting-story-drifts-and-joint-displacements-in-etabs-with-python-6b886aac89ba)
- [Hakan Keskin — Base Reactions Python](https://hakan-keskin.medium.com/extracting-modal-analysis-results-and-base-reactions-in-etabs-with-python-af12da00ca5f)
- [re-tug.com — Database Tables](https://re-tug.com/post/etabs-api-more-examples-database-tables/18)

### Foros
- [Eng-Tips — NewGridOnly](https://www.eng-tips.com/threads/etabs-api-newgridonly-method.516841/)
- [Eng-Tips — Add Area by Coord](https://www.eng-tips.com/threads/add-area-by-coord-method-etabs-api.477551/)
- [Eng-Tips — Mass Source API](https://www.eng-tips.com/threads/etabs-api-add-new-mass-source.521909/)
- [Eng-Tips — Database Tables](https://www.eng-tips.com/threads/csi-api-database-tables-help.497218/)
- [ResearchGate — Define RS Function via OAPI](https://www.researchgate.net/post/How_to_define_a_response_spectrum_function_in_ETABS_SAP2000_using_OAPI)

### Release Notes oficiales
- [ETABS v18.0.1](http://installs.csiamerica.com/software/ETABS/18/ReleaseNotesETABSv1801.pdf)
- [ETABS v20.0.0](https://www.csiamerica.com/software/ETABS/20/ReleaseNotesETABSv2000.pdf)
- [ETABS v22.0.0](https://www.csiamerica.com/software/ETABS/22/ReleaseNotesETABSv2200.pdf)
- [ETABS v22.5.1](https://www.csiamerica.com/software/ETABS/22/ReleaseNotesETABSv2251plus2250.pdf)

---

## Resumen rápido — Tabla de firmas

| Función | Args req | Args opt | Total | Estado |
|---------|---------|---------|-------|--------|
| `InitializeNewModel` | 0 | 1 (eUnits) | 1 | ✅ |
| `File.NewBlank` | 0 | 0 | 0 | ✅ |
| `File.NewGridOnly` | 7 | 0 | 7 | ✅ |
| `PropMaterial.SetMaterial` | 2 | 0 | 2 | ✅ Legacy |
| `PropMaterial.AddMaterial` | 5 | 1 | 6 | ✅ |
| `PropMaterial.SetMPIsotropic` | 4 | 1 | 5 | ✅ |
| `PropMaterial.SetOConcrete_1` | 9 | 3 | 12 | ✅ |
| `PropMaterial.SetORebar_1` | 11 | 0 | 11 | ✅ |
| `PropMaterial.SetWeightAndMass` | 3 | 0 | 3 | ✅ |
| `PropFrame.SetRectangle` | 4 | 3 | 7 | ✅ |
| `PropFrame.SetModifiers` | 2 | 0 | 2 | ✅ |
| `PropArea.SetWall` | 5 | 3 | 8 | ✅ |
| `PropArea.SetSlab` | 5 | 3 | 8 | ✅ |
| `PropArea.SetShell_1` | — | — | — | 🔴 NO EXISTE |
| `PropArea.SetModifiers` | 2 | 0 | 2 | ✅ |
| `PointObj.AddCartesian` | 3 | 5 | 8 | ✅ |
| `FrameObj.AddByCoord` | 6 | 4 | 10 | ✅ |
| `FrameObj.AddByPoint` | 2 | 3 | 5 | ✅ |
| `FrameObj.SetInsertionPoint` | 6 | 2 | 8 | ✅ |
| `FrameObj.SetLoadDistributed` | 8 | 4 | 12 | ✅ |
| `AreaObj.AddByCoord` | 4 | 4 | 8 | ✅ |
| `AreaObj.AddByPoint` | 2 | 3 | 5 | ✅ |
| `AreaObj.SetDiaphragm` | 2 | 1 | 3 | ✅ |
| `AreaObj.SetLoadUniform` | 4 | 3 | 7 | ✅ |
| `AreaObj.SetAutoMesh` | 14 | 4 | 18 | ✅ |
| `LoadPatterns.Add` | 2 | 2 | 4 | ✅ |
| `Func.FuncRS.SetUser` | 4 | 1 | 5 | ✅ |
| `Func.FuncRS.SetFromFile` | — | — | — | 🔴 NO EXISTE |
| `RS.SetCase` | 1 | 0 | 1 | ✅ |
| `RS.SetLoads` | 7 | 0 | 7 | ⚠️ |
| `RS.SetModalCase` | 2 | 0 | 2 | ✅ |
| `RS.SetEccentricity` | 2 | 0 | 2 | ✅ |
| `PropMaterial.SetMassSource_1` | 6 | 0 | 6 | ⚠️ |
| `Analyze.SetActiveDOF` | 1 | 0 | 1 | ✅ |
| `Analyze.SetRunCaseFlag` | 2 | 1 | 3 | ✅ |
| `Analyze.RunAnalysis` | 0 | 0 | 0 | ✅ |
| `Results.Setup.SetCaseSelectedForOutput` | 1 | 0 | 1 | ✅ |
| `Results.StoryDrifts` | 0 | 0 | 0 | ✅ |
| `Results.JointDrifts` | 0 | 0 | 0 | ⚠️ |
| `Results.BaseReac` | 0 | 0 | 0 | ✅ |
| `DatabaseTables.GetTableForDisplayArray` | 4 | 0 | 4+3out | ✅ |

---

*Documento generado el 20 marzo 2026 como parte del feature R03 del agente autónomo ETABS.*
*Fuentes: docs CSI oficiales, 5+ repos GitHub, Eng-Tips, stru.ai, Medium, ResearchGate.*
