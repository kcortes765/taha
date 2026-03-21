# Referencia Completa — CSI ETABS OAPI (Open Application Programming Interface)

> **Versión**: ETABS v19+ (CSI API v1)
> **Lenguaje**: Python 3.8+ con `comtypes`
> **Fecha**: 20 marzo 2026
> **Propósito**: Referencia exhaustiva para automatización de modelación de edificios HA

---

## Tabla de Contenidos

1. [Conexión y Setup](#1-conexión-y-setup)
2. [SapModel — Objeto Principal](#2-sapmodel--objeto-principal)
3. [File — Archivos y Modelos](#3-file--archivos-y-modelos)
4. [Story — Pisos](#4-story--pisos)
5. [GridSys — Sistema de Grillas](#5-gridsys--sistema-de-grillas)
6. [PropMaterial — Materiales](#6-propmaterial--materiales)
7. [PropFrame — Secciones de Marco](#7-propframe--secciones-de-marco)
8. [PropArea — Secciones de Área (Muros/Losas)](#8-proparea--secciones-de-área-muroslosas)
9. [PointObj — Puntos/Nodos](#9-pointobj--puntosnodos)
10. [FrameObj — Elementos de Marco (Vigas/Columnas)](#10-frameobj--elementos-de-marco-vigascolumnas)
11. [AreaObj — Elementos de Área (Muros/Losas)](#11-areaobj--elementos-de-área-muroslosas)
12. [Diaphragm — Diafragmas](#12-diaphragm--diafragmas)
13. [LoadPatterns — Patrones de Carga](#13-loadpatterns--patrones-de-carga)
14. [LoadCases — Casos de Carga](#14-loadcases--casos-de-carga)
15. [FuncRS — Funciones de Espectro de Respuesta](#15-funcrs--funciones-de-espectro-de-respuesta)
16. [RespCombo / Combo — Combinaciones de Carga](#16-respcombo--combo--combinaciones-de-carga)
17. [MassSource — Fuente de Masa](#17-masssource--fuente-de-masa)
18. [Analyze — Análisis](#18-analyze--análisis)
19. [AnalysisResults — Resultados](#19-analysisresults--resultados)
20. [DatabaseTables — Tablas de Base de Datos](#20-databasetables--tablas-de-base-de-datos)
21. [Enumeraciones Clave](#21-enumeraciones-clave)
22. [Patrones de Uso Comunes](#22-patrones-de-uso-comunes)
23. [Errores Frecuentes y Soluciones](#23-errores-frecuentes-y-soluciones)
24. [Fuentes](#24-fuentes)

---

## 1. Conexión y Setup

### 1.1 Importaciones necesarias

```python
import comtypes.client
import sys
import os
```

### 1.2 Limpiar comtypes.gen (CRÍTICO)

Antes de importar `comtypes.client`, limpiar el cache de type libraries para evitar bindings stale:

```python
import comtypes
import shutil

gen_path = os.path.join(os.path.dirname(comtypes.__file__), 'gen')
if os.path.exists(gen_path):
    shutil.rmtree(gen_path)
    os.makedirs(gen_path)
    # Recrear __init__.py vacío
    with open(os.path.join(gen_path, '__init__.py'), 'w') as f:
        pass
```

### 1.3 Método 1: Conectar a instancia existente (RECOMENDADO)

```python
try:
    EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
except (OSError, comtypes.COMError):
    print("No se encontró instancia activa de ETABS")
    sys.exit(-1)

SapModel = EtabsObject.SapModel
```

**IMPORTANTE**: Este es el método preferido. Requiere que ETABS v19 esté abierto con un modelo (puede ser blank).

### 1.4 Método 2: Usar Helper (con precauciones)

```python
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

# Intentar GetObject primero
try:
    EtabsObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
except:
    # Solo como último recurso — PUEDE crear instancia invisible
    EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
    EtabsObject.ApplicationStart()
    # FORZAR visible
    EtabsObject.Visible = True
    import time
    time.sleep(15)  # Esperar que la UI cargue

SapModel = EtabsObject.SapModel
```

### 1.5 Método 3: Fallback robusto (prioridad cascada)

```python
def connect_etabs():
    """Conectar a ETABS con prioridad: GetActive → Helper.GetObject → CreateObject."""
    # 1. Intentar instancia activa
    try:
        obj = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        print("Conectado via GetActiveObject")
        return obj, obj.SapModel
    except:
        pass

    # 2. Intentar Helper.GetObject
    try:
        helper = comtypes.client.CreateObject('ETABSv1.Helper')
        helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
        obj = helper.GetObject("CSI.ETABS.API.ETABSObject")
        print("Conectado via Helper.GetObject")
        return obj, obj.SapModel
    except:
        pass

    # 3. CreateObject (última opción)
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    obj = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
    obj.ApplicationStart()
    obj.Visible = True
    import time
    time.sleep(15)
    print("Conectado via CreateObject (nueva instancia)")
    return obj, obj.SapModel
```

### 1.6 Mantener referencias globales (evitar GC)

```python
# SIEMPRE mantener como variables globales del módulo
_etabs_obj = None
_sap_model = None

def init():
    global _etabs_obj, _sap_model
    _etabs_obj, _sap_model = connect_etabs()
    return _sap_model
```

**LECCIÓN APRENDIDA**: Si `helper`, `EtabsObject` o `SapModel` salen de scope, el garbage collector de Python puede destruir los objetos COM y matar la conexión.

---

## 2. SapModel — Objeto Principal

`SapModel` es el objeto raíz que expone toda la API de ETABS.

### 2.1 Propiedades/Sub-objetos principales

| Sub-objeto | Acceso | Descripción |
|---|---|---|
| `File` | `SapModel.File` | Operaciones de archivo |
| `Story` | `SapModel.Story` | Gestión de pisos |
| `GridSys` | `SapModel.GridSys` | Sistema de grillas |
| `PropMaterial` | `SapModel.PropMaterial` | Materiales |
| `PropFrame` | `SapModel.PropFrame` | Secciones frame |
| `PropArea` | `SapModel.PropArea` | Secciones area |
| `PointObj` | `SapModel.PointObj` | Nodos/puntos |
| `FrameObj` | `SapModel.FrameObj` | Vigas, columnas |
| `AreaObj` | `SapModel.AreaObj` | Muros, losas |
| `LoadPatterns` | `SapModel.LoadPatterns` | Patrones de carga |
| `LoadCases` | `SapModel.LoadCases` | Casos de carga |
| `RespCombo` | `SapModel.RespCombo` | Combinaciones |
| `Analyze` | `SapModel.Analyze` | Control de análisis |
| `Results` | `SapModel.Results` | Resultados |
| `DatabaseTables` | `SapModel.DatabaseTables` | Tablas de datos |
| `Diaphragm` | `SapModel.Diaphragm` | Diafragmas |
| `Func` | `SapModel.Func` | Funciones (espectro, etc.) |

### 2.2 Métodos de SapModel

```python
# Inicializar nuevo modelo
ret = SapModel.InitializeNewModel()
# ret = 0 → éxito

# Establecer unidades del modelo
ret = SapModel.SetPresentUnits(units)
# units: entero según eUnits (ver Enumeraciones)
# Común: 6 = kN_m_C, 9 = Tonf_m_C, 15 = kgf_m_C

# Obtener unidades actuales
units = SapModel.GetPresentUnits()

# Bloquear/desbloquear modelo
ret = SapModel.SetModelIsLocked(False)  # Desbloquear para editar

# Obtener estado del modelo
locked = SapModel.GetModelIsLocked()
```

---

## 3. File — Archivos y Modelos

### 3.1 Crear modelo nuevo

```python
# Modelo en blanco
ret = SapModel.File.NewBlank()

# Modelo con grilla (template rápido)
ret = SapModel.File.NewGridOnly(
    NumberStorys,        # int — Número de pisos
    TypicalStoryHeight,  # float — Altura piso tipo (m)
    BottomStoryHeight,   # float — Altura primer piso (m)
    NumberLinesX,        # int — Líneas de grilla en X
    NumberLinesY,        # int — Líneas de grilla en Y
    SpacingX,            # float — Espaciamiento en X (m)
    SpacingY             # float — Espaciamiento en Y (m)
)
```

**Ejemplo proyecto** (Edificio 1: 20 pisos, h1=3.4m, h2-20=2.6m):
```python
# Crea grilla básica (luego ajustar pisos y ejes individualmente)
ret = SapModel.File.NewGridOnly(20, 2.6, 3.4, 17, 6, 5.0, 5.0)
```

**NOTA**: `NewGridOnly` con `ret=0` garantiza que las stories se crean correctamente. Es preferible a `NewBlank` + `Story.SetStories` por separado.

### 3.2 Abrir y guardar

```python
# Abrir archivo existente
ret = SapModel.File.OpenFile(r"C:\ruta\modelo.edb")

# Guardar modelo
ret = SapModel.File.Save(r"C:\ruta\modelo.edb")
# ADVERTENCIA: Save() via COM produce .edb CORRUPTO si ETABS abrió sin UI (CreateObject)
# FIX: Siempre abrir ETABS manualmente → File > New Model > Blank → luego scripts

# Guardar como
ret = SapModel.File.Save(r"C:\ruta\nuevo_nombre.edb")
```

---

## 4. Story — Pisos

### 4.1 SetStories

```python
ret = SapModel.Story.SetStories(
    StoryNames,       # str[] — Nombres de pisos (sin "Base")
    StoryElevations,  # float[] — Elevaciones (len = NumStories + 1, incluye Base=0)
    StoryHeights,     # float[] — Alturas (len = NumStories, sin Base)
    IsMasterStory,    # bool[] — ¿Es master story? (len = NumStories)
    SimilarToStory,   # str[] — Nombre del story similar (len = NumStories)
    SpliceAbove,      # bool[] — ¿Empalme arriba? (len = NumStories)
    SpliceHeight      # float[] — Altura de empalme (len = NumStories)
)
```

**Ejemplo para Edificio 1** (20 pisos: h1=3.4m, h2-20=2.6m):
```python
n = 20
names = [f"Story{i}" for i in range(1, n+1)]
heights = [3.4] + [2.6] * 19
elevations = [0.0]  # Base
for h in heights:
    elevations.append(elevations[-1] + h)
is_master = [True] + [False] * 19
similar = ["None"] + ["Story1"] * 19
splice = [False] * n
splice_h = [0.0] * n

ret = SapModel.Story.SetStories(names, elevations, heights, is_master, similar, splice, splice_h)
```

### 4.2 GetStories

```python
ret = SapModel.Story.GetStories()
# Retorna tupla: (NumberStories, StoryNames, StoryElevations, StoryHeights,
#                 IsMasterStory, SimilarToStory, SpliceAbove, SpliceHeight, ret)
```

### 4.3 GetNameList

```python
ret = SapModel.Story.GetNameList()
# Retorna: (NumberNames, StoryNames_array, ret)
```

### 4.4 GetElevation

```python
ret = SapModel.Story.GetElevation(StoryName)
# Retorna: (Elevation, ret)
```

### 4.5 SetMasterStory

```python
ret = SapModel.Story.SetMasterStory(StoryName, IsMasterStory)
```

**LECCIÓN**: `get_story_data()` personalizado siempre falla en v19 por binding COM — no abortar por eso. Usar `NewGridOnly` que garantiza stories correctas.

---

## 5. GridSys — Sistema de Grillas

### 5.1 SetGridSys

```python
ret = SapModel.GridSys.SetGridSys(
    Name,   # str — Nombre del grid system
    x,      # float — Origen global X
    y,      # float — Origen global Y
    RZ      # float — Rotación respecto a global (grados)
)
```

### 5.2 GetGridSys

```python
ret = SapModel.GridSys.GetGridSys(Name)
# Retorna: (x, y, RZ, ret)
```

### 5.3 GetNameList

```python
ret = SapModel.GridSys.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

**NOTA**: La grilla irregular del Edificio 1 (17 ejes X + 6 ejes Y con espaciamientos variables) se define mejor editando la grilla del template creado con `NewGridOnly`, o creando elementos directamente por coordenadas sin depender de la grilla.

---

## 6. PropMaterial — Materiales

### 6.1 SetMaterial (LEGACY — deprecated en v20+)

```python
ret = SapModel.PropMaterial.SetMaterial(
    Name,      # str — Nombre del material
    MatType    # int — Tipo: 1=Steel, 2=Concrete, 6=Rebar (eMatType)
)
```

### 6.2 AddMaterial (RECOMENDADO en v18+)

```python
ret = SapModel.PropMaterial.AddMaterial(
    Name,          # str — Nombre (output si se genera automáticamente)
    MatType,       # eMatType — Tipo de material
    Region,        # str — Región ("Chile", "United States", etc.)
    Standard,      # str — Norma ("ACI 318-08", etc.)
    Grade,         # str — Grado ("f'c 30 MPa", "Grade 420", etc.)
    UserName       # str — Nombre de usuario (opcional, "" para auto)
)
```

### 6.3 SetMPIsotropic — Propiedades mecánicas isotrópicas

```python
ret = SapModel.PropMaterial.SetMPIsotropic(
    Name,   # str — Nombre del material
    E,      # float — Módulo de elasticidad
    U,      # float — Coeficiente de Poisson
    A,      # float — Coeficiente de expansión térmica
    Temp    # float — Temperatura (opcional, default 0)
)
```

**Ejemplo G30** (f'c=30 MPa):
```python
# Ec = 4700√30 = 25,742.96 MPa
# En tonf/m²: 25,742.96 × 101.937 = 2,624,300 tonf/m²
ret = SapModel.PropMaterial.SetMPIsotropic("G30", 25742.96, 0.2, 1.0E-05)
# Si unidades son tonf/m²:
ret = SapModel.PropMaterial.SetMPIsotropic("G30", 2624300.0, 0.2, 1.0E-05)
```

### 6.4 SetOConcrete_1 — Propiedades de hormigón

```python
ret = SapModel.PropMaterial.SetOConcrete_1(
    Name,           # str — Nombre del material
    Fc,             # float — f'c (resistencia a compresión)
    IsLightweight,  # bool — ¿Hormigón liviano?
    FcsFactor,      # float — Factor fcs (default 1.0)
    SSType,         # int — Tipo curva tensión-deformación (0=Simple, 1=Mander)
    SSHysType,      # int — Tipo histerético (0=Elastic, 1=Kinematic, 2=Takeda, etc.)
    StrainAtFc,     # float — Deformación en f'c (default 0.002216)
    StrainUltimate, # float — Deformación última (default 0.005)
    FinalSlope,     # float — Pendiente final (default -0.1)
    FrictionAngle,  # float — Ángulo de fricción (opcional)
    DilatationalAngle, # float — Ángulo dilatacional (opcional)
    Temp            # float — Temperatura (opcional)
)
```

**Ejemplo G30**:
```python
ret = SapModel.PropMaterial.SetOConcrete_1(
    "G30", 30.0, False, 1.0, 1, 0, 0.002216, 0.005, -0.1
)
```

### 6.5 SetORebar_1 — Propiedades de acero de refuerzo

```python
ret = SapModel.PropMaterial.SetORebar_1(
    Name,           # str — Nombre del material
    Fy,             # float — Tensión de fluencia
    Fu,             # float — Tensión última
    EFy,            # float — Deformación en fluencia esperada
    EFu,            # float — Deformación última esperada
    SSType,         # int — Tipo curva S-S (0=Simple, 1=Park)
    SSHysType,      # int — Tipo histerético
    StrainAtHardening, # float — Deformación al inicio de endurecimiento
    StrainUltimate, # float — Deformación última
    FinalSlope,     # float — Pendiente final
    UseCaltransSSDefaults  # bool — Usar defaults Caltrans
)
```

**Ejemplo A630-420H**:
```python
ret = SapModel.PropMaterial.SetORebar_1(
    "A630-420H", 420.0, 630.0, 1.25*420, 1.0*630, 0, 0, 0.01, 0.09, -0.1, False
)
```

### 6.6 SetWeightAndMass — Peso/masa por volumen

```python
ret = SapModel.PropMaterial.SetWeightAndMass(
    Name,     # str — Nombre del material
    MyOption, # int — 1=Weight per volume, 2=Mass per volume
    Value     # float — Valor (peso/vol o masa/vol en unidades del modelo)
)
```

**Ejemplo** (peso unitario HA ≈ 2.5 tonf/m³):
```python
ret = SapModel.PropMaterial.SetWeightAndMass("G30", 1, 2.5)  # tonf/m³
```

### 6.7 GetNameList

```python
ret = SapModel.PropMaterial.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

---

## 7. PropFrame — Secciones de Marco

### 7.1 SetRectangle — Sección rectangular

```python
ret = SapModel.PropFrame.SetRectangle(
    Name,      # str — Nombre de la sección
    MatProp,   # str — Material asociado
    T3,        # float — Profundidad (peralte, dirección local 3)
    T2,        # float — Ancho (dirección local 2)
    Color,     # int — Color (opcional, -1 = default)
    Notes,     # str — Notas (opcional, "")
    GUID       # str — GUID (opcional, "")
)
```

**Ejemplo vigas invertidas 20/60**:
```python
# T3 = peralte = 0.60m, T2 = ancho = 0.20m
ret = SapModel.PropFrame.SetRectangle("VI20/60G30", "G30", 0.60, 0.20)
```

### 7.2 SetRebarBeam — Armadura de viga

```python
ret = SapModel.PropFrame.SetRebarBeam(
    Name,          # str — Nombre de la sección frame
    MatRebar,      # str — Material de la armadura
    CoverTop,      # float — Recubrimiento superior
    CoverBot,      # float — Recubrimiento inferior
    TopLeftArea,    # float — Área acero superior izquierdo
    TopRightArea,   # float — Área acero superior derecho
    BotLeftArea,    # float — Área acero inferior izquierdo
    BotRightArea    # float — Área acero inferior derecho
)
```

### 7.3 SetRebarColumn — Armadura de columna

```python
ret = SapModel.PropFrame.SetRebarColumn(
    Name,            # str — Nombre de la sección frame
    MatRebar,        # str — Material de armadura longitudinal
    MatConfinement,  # str — Material de confinamiento
    Pattern,         # int — Patrón de armado (1=Rectangular, 2=Circular)
    ConfineType,     # int — Tipo confinamiento (1=Ties/Estribos, 2=Spiral)
    Cover,           # float — Recubrimiento al centro de barra
    NumberBars3,     # int — Nº barras dirección 3
    NumberBars2,     # int — Nº barras dirección 2
    RebarSize,       # str — Tamaño barra longitudinal (e.g., "#8", "25M")
    TieSize,         # str — Tamaño estribo (e.g., "#4", "10M")
    TieSpacing,      # float — Separación estribos
    NumberBarsCirc,  # int — Nº barras en circular (solo si Pattern=2)
    NumberBars2Dir,  # bool — ¿Barras en dirección 2?
    ToBeDesigned     # bool — ¿Sección será diseñada por ETABS?
)
```

### 7.4 SetModifiers — Modificadores de rigidez

```python
ret = SapModel.PropFrame.SetModifiers(
    Name,   # str — Nombre de la sección
    Value   # float[8] — Array de 8 modificadores:
            # [0] A (axial area)
            # [1] As2 (shear area 2)
            # [2] As3 (shear area 3)
            # [3] J (torsional constant)
            # [4] I22 (moment of inertia 2-2)
            # [5] I33 (moment of inertia 3-3)
            # [6] M (mass)
            # [7] W (weight)
)
```

**Ejemplo vigas con J=0** (práctica chilena: torsion modifier = 0):
```python
mods = [1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0]  # J=0
ret = SapModel.PropFrame.SetModifiers("VI20/60G30", mods)
```

### 7.5 GetNameList

```python
ret = SapModel.PropFrame.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

---

## 8. PropArea — Secciones de Área (Muros/Losas)

### 8.1 SetWall — Sección de muro

```python
ret = SapModel.PropArea.SetWall(
    Name,          # str — Nombre de la propiedad
    WallPropType,  # int — Tipo: 0=Specified, 1=AutoSelectList (eWallPropType)
    ShellType,     # int — Tipo shell: 1=ShellThin, 2=ShellThick, 3=Membrane,
                   #       4=Plate, 5=Shell, 6=Layered (eShellType)
    MatProp,       # str — Material (no aplica si ShellType=Layered)
    Thickness,     # float — Espesor (no aplica si ShellType=Layered)
    Color,         # int — Color (opcional, -1)
    Notes,         # str — Notas (opcional, "")
    GUID           # str — GUID (opcional, "")
)
```

**Ejemplo muros proyecto**:
```python
# MHA30G30 — muro 30cm
ret = SapModel.PropArea.SetWall("MHA30G30", 0, 2, "G30", 0.30)
# MHA20G30 — muro 20cm
ret = SapModel.PropArea.SetWall("MHA20G30", 0, 2, "G30", 0.20)
```

### 8.2 SetSlab — Sección de losa

```python
ret = SapModel.PropArea.SetSlab(
    Name,       # str — Nombre de la propiedad
    SlabType,   # int — Tipo: 0=Slab, 1=Drop, 2=Stiff, 3=Ribbed, 4=Waffle (eSlabType)
    ShellType,  # int — Tipo shell (ver arriba)
    MatProp,    # str — Material
    Thickness,  # float — Espesor
    Color,      # int — Color (opcional)
    Notes,      # str — Notas (opcional)
    GUID        # str — GUID (opcional)
)
```

**Ejemplo losa proyecto**:
```python
# Losa15G30 — losa 15cm
ret = SapModel.PropArea.SetSlab("Losa15G30", 0, 1, "G30", 0.15)
```

### 8.3 SetModifiers — Modificadores de rigidez de shell

```python
ret = SapModel.PropArea.SetModifiers(
    Name,   # str — Nombre de la propiedad
    Value   # float[10] — Array de 10 modificadores:
            # [0] f11 (membrane)
            # [1] f22 (membrane)
            # [2] f12 (membrane)
            # [3] m11 (bending)
            # [4] m22 (bending)
            # [5] m12 (bending)
            # [6] v13 (shear)
            # [7] v23 (shear)
            # [8] Mass
            # [9] Weight
)
```

**Ejemplo losa con inercia al 25%** (práctica chilena):
```python
mods = [1.0, 1.0, 1.0, 0.25, 0.25, 0.25, 1.0, 1.0, 1.0, 1.0]
ret = SapModel.PropArea.SetModifiers("Losa15G30", mods)
```

### 8.4 GetNameList

```python
ret = SapModel.PropArea.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

---

## 9. PointObj — Puntos/Nodos

### 9.1 SetRestraint — Asignar restricciones (apoyos)

```python
ret = SapModel.PointObj.SetRestraint(
    Name,      # str — Nombre del punto
    Value      # bool[6] — [UX, UY, UZ, RX, RY, RZ]
               # True = restringido, False = libre
)
```

**Ejemplo empotramiento**:
```python
empotrado = [True, True, True, True, True, True]
ret = SapModel.PointObj.SetRestraint("1", empotrado)
```

### 9.2 GetNameList

```python
ret = SapModel.PointObj.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

### 9.3 GetNameListOnStory

```python
ret = SapModel.PointObj.GetNameListOnStory(StoryName)
# Retorna: (NumberNames, Names_array, ret)
```

### 9.4 GetCoordCartesian

```python
ret = SapModel.PointObj.GetCoordCartesian(
    Name,   # str — Nombre del punto
    x, y, z # float (output) — Coordenadas
)
# Retorna: (x, y, z, ret)
```

---

## 10. FrameObj — Elementos de Marco (Vigas/Columnas)

### 10.1 AddByCoord — Crear frame por coordenadas

```python
ret = SapModel.FrameObj.AddByCoord(
    x1, y1, z1,   # float — Coordenadas punto I (inicio)
    x2, y2, z2,   # float — Coordenadas punto J (fin)
    Name,          # str — Nombre (output, "" para auto)
    PropName,      # str — Sección asignada ("Default" o nombre específico)
    UserName,      # str — Nombre de usuario (opcional, "")
    CSys           # str — Sistema coordenadas (opcional, "Global")
)
# Retorna: (Name, ret) — Name contiene el nombre asignado
```

**Ejemplo viga en piso 1** (z=3.4m, eje 1, de y=0 a y=5.14):
```python
name = ""
ret = SapModel.FrameObj.AddByCoord(0, 0, 3.4, 0, 5.14, 3.4, name, "VI20/60G30")
```

### 10.2 AddByPoint — Crear frame por puntos existentes

```python
ret = SapModel.FrameObj.AddByPoint(
    Point1,    # str — Nombre del punto I
    Point2,    # str — Nombre del punto J
    Name,      # str — Nombre (output)
    PropName,  # str — Sección asignada
    UserName   # str — Nombre de usuario (opcional)
)
```

### 10.3 SetSection — Asignar sección

```python
ret = SapModel.FrameObj.SetSection(
    Name,      # str — Nombre del frame
    PropName,  # str — Nombre de la sección
    ItemType   # int — 0=Object, 1=Group, 2=SelectedObjects (opcional, default 0)
)
```

### 10.4 SetInsertionPoint — Punto de inserción (Cardinal Point)

```python
ret = SapModel.FrameObj.SetInsertionPoint(
    Name,            # str — Nombre del frame
    CardinalPoint,   # int — Punto cardinal (1-11):
                     #   1=Bottom Left      2=Bottom Center     3=Bottom Right
                     #   4=Middle Left      5=Middle Center     6=Middle Right
                     #   7=Top Left         8=Top Center        9=Top Right
                     #   10=Centroid        11=Shear Center
    Mirror2,         # bool — Espejo sobre eje local 2
    StiffTransform,  # bool — Transformar rigidez por cardinal point
    Offset1,         # float[3] — Offsets en I-End [dx, dy, dz]
    Offset2,         # float[3] — Offsets en J-End [dx, dy, dz]
    CSys,            # str — Sistema de coordenadas (opcional, "Global")
    ItemType         # int — 0=Object, 1=Group (opcional, default 0)
)
```

**Ejemplo vigas invertidas** (Bottom Center = Punto 2):
```python
ret = SapModel.FrameObj.SetInsertionPoint(
    "B1", 2, False, True, [0,0,0], [0,0,0]
)
```

### 10.5 SetLocalAxes — Ejes locales

```python
ret = SapModel.FrameObj.SetLocalAxes(
    Name,    # str — Nombre del frame
    Ang,     # float — Ángulo de rotación (grados)
    ItemType # int — (opcional, default 0)
)
```

### 10.6 SetModifiers — Modificadores (a nivel de objeto)

```python
ret = SapModel.FrameObj.SetModifiers(
    Name,     # str — Nombre del frame o grupo
    Value,    # float[8] — Mismos 8 modificadores que PropFrame.SetModifiers
    ItemType  # int — 0=Object, 1=Group, 2=SelectedObjects
)
```

### 10.7 GetNameList

```python
ret = SapModel.FrameObj.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

### 10.8 GetAllFrames (v18+)

```python
ret = SapModel.FrameObj.GetAllFrames()
# Retorna múltiples arrays: Names, PropNames, StoryNames, PointNames1, PointNames2, etc.
```

### 10.9 SetLoadDistributed — Carga distribuida en frame

```python
ret = SapModel.FrameObj.SetLoadDistributed(
    Name,      # str — Nombre del frame
    LoadPat,   # str — Patrón de carga
    MyType,    # int — 1=Force, 2=Moment
    Dir,       # int — Dirección (1=local1, 2=local2, ..., 6=GravityZ, 10=ProjX, 11=ProjY, 12=ProjZ)
    Dist1,     # float — Distancia relativa inicio (0-1)
    Dist2,     # float — Distancia relativa fin (0-1)
    Val1,      # float — Valor en inicio
    Val2,      # float — Valor en fin
    CSys,      # str — Sistema coordenadas (opcional)
    RelDist,   # bool — True si distancias son relativas
    Replace,   # bool — True para reemplazar cargas existentes
    ItemType   # int — (opcional)
)
```

---

## 11. AreaObj — Elementos de Área (Muros/Losas)

### 11.1 AddByCoord — Crear área por coordenadas

```python
ret = SapModel.AreaObj.AddByCoord(
    NumberPoints,  # int — Número de puntos (vértices)
    X,             # float[] — Array coordenadas X
    Y,             # float[] — Array coordenadas Y
    Z,             # float[] — Array coordenadas Z
    Name,          # str — Nombre (output, "" para auto)
    PropName,      # str — Propiedad de área ("Default" o nombre)
    UserName,      # str — Nombre usuario (opcional, "")
    CSys           # str — Sistema coordenadas (opcional, "Global")
)
# Retorna: (Name, ret)
```

**Ejemplo muro en eje 1** (4 esquinas, vertical):
```python
# Muro entre ejes 1-2, piso 1 (z=0 a z=3.4)
x1, y1 = 0.0, 0.0   # Eje 1
x2, y2 = 0.0, 5.14   # Eje 2
z_bot, z_top = 0.0, 3.4

X = [x1, x2, x2, x1]
Y = [y1, y2, y2, y1]
Z = [z_bot, z_bot, z_top, z_top]

name = ""
ret = SapModel.AreaObj.AddByCoord(4, X, Y, Z, name, "MHA30G30")
```

**NOTA**: Para muros, los puntos se dan en sentido antihorario vistos desde fuera. Para losas horizontales, los puntos definen el contorno en planta.

### 11.2 SetProperty — Asignar propiedad

```python
ret = SapModel.AreaObj.SetProperty(
    Name,      # str — Nombre del area
    PropName,  # str — Nombre de la propiedad de área
    ItemType   # int — 0=Object, 1=Group, 2=Selected (opcional)
)
```

### 11.3 SetDiaphragm — Asignar diafragma

```python
ret = SapModel.AreaObj.SetDiaphragm(
    Name,          # str — Nombre del area
    DiaphragmName  # str — Nombre del diafragma ("D1", etc.)
)
```

### 11.4 SetLoadUniform — Carga uniforme en área

```python
ret = SapModel.AreaObj.SetLoadUniform(
    Name,      # str — Nombre del area
    LoadPat,   # str — Patrón de carga ("SCP", "SCT", etc.)
    Value,     # float — Valor de la carga
    Dir,       # int — Dirección (6=Gravity/Z global, etc.)
    Replace,   # bool — Reemplazar cargas existentes
    CSys,      # str — Sistema coordenadas (opcional, "Global")
    ItemType   # int — 0=Object, 1=Group (opcional)
)
```

**Ejemplo sobrecarga oficinas en losa**:
```python
# SCP = 250 kgf/m² = 0.25 tonf/m² (dirección gravedad = 6)
ret = SapModel.AreaObj.SetLoadUniform("F1", "SCP", -0.25, 6, True)
```

### 11.5 SetModifiers — Modificadores de rigidez

```python
ret = SapModel.AreaObj.SetModifiers(
    Name,     # str — Nombre del area o grupo
    Value,    # float[10] — 10 modificadores (mismos que PropArea.SetModifiers)
    ItemType  # int — 0=Object, 1=Group (opcional)
)
```

### 11.6 GetNameList

```python
ret = SapModel.AreaObj.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

### 11.7 SetAutoMesh

```python
ret = SapModel.AreaObj.SetAutoMesh(
    Name,           # str — Nombre del area
    MeshType,       # int — Tipo de mesh:
                    #   0=None, 1=Auto, 2=CookieCutByPoints,
                    #   3=CookieCutByLines, 4=MaxSize, 5=PointsOnEdges
    n1, n2,         # int — Divisiones en dir 1 y 2 (para algunos tipos)
    MaxSize1,       # float — Tamaño máximo dirección 1
    MaxSize2,       # float — Tamaño máximo dirección 2
    PointOnEdge,    # bool — Puntos en bordes
    ExtendCookies,  # bool — Extender cookies
    Rotation,       # float — Rotación del mesh (grados)
    MaxSizeGeneral, # float — Tamaño máximo general
    LocalAxesOnEdge,# bool — Ejes locales en bordes
    LocalAxesOnFace,# bool — Ejes locales en cara
    RestraintsOnEdge,# bool — Restricciones en bordes
    RestraintsOnFace,# bool — Restricciones en cara
    ItemType,       # int — (opcional)
    Group,          # str — Grupo (opcional)
    SubMesh,        # bool — Sub-mesh (opcional)
    SubMeshSize     # float — Tamaño sub-mesh (opcional)
)
```

**Ejemplo AutoMesh 0.4m** (vano mínimo = 0.425m):
```python
ret = SapModel.AreaObj.SetAutoMesh(
    "W1", 4, 0, 0, 0.4, 0.4, False, False, 0.0, 0.4, False, False, False, False
)
```

---

## 12. Diaphragm — Diafragmas

### 12.1 Definir diafragma

```python
# No hay SetDiaphragm explícito a nivel de SapModel.Diaphragm en todas las versiones.
# Los diafragmas se crean implícitamente al asignarlos a áreas.
# Sin embargo, en versiones recientes:
ret = SapModel.Diaphragm.SetDiaphragm(
    Name,          # str — Nombre del diafragma
    SemiRigid      # bool — True=semi-rígido, False=rígido
)
```

### 12.2 Asignar diafragma a área

```python
# Vía AreaObj (ver sección 11.3)
ret = SapModel.AreaObj.SetDiaphragm("F1", "D1")
```

**Práctica del proyecto**:
- Diafragma rígido `D1` para casos 1-3
- Diafragma semi-rígido para casos 4-6

---

## 13. LoadPatterns — Patrones de Carga

### 13.1 Add — Agregar patrón de carga

```python
ret = SapModel.LoadPatterns.Add(
    Name,              # str — Nombre del patrón
    MyType,            # int — Tipo (eLoadPatternType):
                       #   1=Dead, 2=SuperDead, 3=Live, 4=ReduceLive,
                       #   5=Quake, 6=Wind, 7=Snow, 8=Other,
                       #   11=LiveRoof, 12=Notional
    SelfWTMultiplier,  # float — Multiplicador de peso propio (default 0)
    AddAnalysisCase    # bool — ¿Agregar caso de análisis automáticamente? (default True)
)
```

**Ejemplo patrones del proyecto**:
```python
# PP (peso propio) — ya existe como "Dead" con SWM=1
# Si necesitas crear explícitamente:
ret = SapModel.LoadPatterns.Add("PP", 1, 1.0, True)   # Dead, SWM=1
ret = SapModel.LoadPatterns.Add("TERP", 2, 0.0, True)  # SuperDead
ret = SapModel.LoadPatterns.Add("TERT", 2, 0.0, True)  # SuperDead
ret = SapModel.LoadPatterns.Add("SCP", 3, 0.0, True)   # Live
ret = SapModel.LoadPatterns.Add("SCT", 3, 0.0, True)   # Live
ret = SapModel.LoadPatterns.Add("SX", 5, 0.0, False)   # Quake (sin caso auto)
ret = SapModel.LoadPatterns.Add("SY", 5, 0.0, False)   # Quake
```

### 13.2 SetSelfWtMultiplier

```python
ret = SapModel.LoadPatterns.SetSelfWtMultiplier(
    Name,  # str — Nombre del patrón
    Value  # float — Multiplicador de peso propio
)
```

### 13.3 GetNameList

```python
ret = SapModel.LoadPatterns.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

### 13.4 GetLoadType

```python
ret = SapModel.LoadPatterns.GetLoadType(Name)
# Retorna: (Type_int, ret)
```

---

## 14. LoadCases — Casos de Carga

### 14.1 Propiedades sub-objeto

| Sub-objeto | Descripción |
|---|---|
| `LoadCases.StaticLinear` | Casos estáticos lineales |
| `LoadCases.ResponseSpectrum` | Casos de espectro de respuesta |
| `LoadCases.ModalEigen` | Análisis modal Eigen |
| `LoadCases.ModalRitz` | Análisis modal Ritz |
| `LoadCases.StaticNonlinear` | Casos estáticos no lineales |

### 14.2 StaticLinear.SetCase — Definir caso estático lineal

```python
ret = SapModel.LoadCases.StaticLinear.SetCase(Name)
# Name: str — Nombre del caso (crea nuevo o modifica existente)
```

### 14.3 StaticLinear.SetLoads — Asignar cargas a caso estático

```python
ret = SapModel.LoadCases.StaticLinear.SetLoads(
    Name,           # str — Nombre del caso
    NumberLoads,    # int — Número de cargas
    LoadType,       # str[] — Tipo: ["Load"] para patrones
    LoadName,       # str[] — Nombres de patrones: ["PP", "SCP"]
    SF              # float[] — Factores de escala: [1.0, 1.0]
)
```

### 14.4 ResponseSpectrum.SetCase — Definir caso de espectro

```python
ret = SapModel.LoadCases.ResponseSpectrum.SetCase(Name)
# Name: str — Nombre del caso de espectro
```

### 14.5 ResponseSpectrum.SetLoads — Asignar cargas al espectro

```python
ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    Name,          # str — Nombre del caso
    NumberLoads,   # int — Número de cargas
    LoadType,      # str[] — Tipo: ["U1"] para dirección X, ["U2"] para Y
    LoadName,      # str[] — Nombre función espectro: ["NCh433_DS61"]
    SF,            # float[] — Factor de escala: [9.81] (para Sa/g → m/s²)
    CSys,          # str[] — Sistema coord: ["Global"]
    Ang            # float[] — Ángulo: [0.0]
)
```

**Ejemplo casos sísmicos**:
```python
# Caso SEx (espectro en X)
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("SEx")
ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "SEx", 1, ["U1"], ["NCh433_DS61"], [9.81], ["Global"], [0.0]
)

# Caso SEy (espectro en Y)
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("SEy")
ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "SEy", 1, ["U2"], ["NCh433_DS61"], [9.81], ["Global"], [0.0]
)
```

### 14.6 ResponseSpectrum.SetModalCase

```python
ret = SapModel.LoadCases.ResponseSpectrum.SetModalCase(
    Name,       # str — Nombre del caso de espectro
    ModalCase   # str — Nombre del caso modal a usar (e.g., "Modal")
)
```

### 14.7 ResponseSpectrum.SetEccentricity

```python
ret = SapModel.LoadCases.ResponseSpectrum.SetEccentricity(
    Name,   # str — Nombre del caso
    Eccen   # float — Excentricidad (fracción de dimensión, e.g., 0.05 = 5%)
)
```

### 14.8 GetNameList

```python
ret = SapModel.LoadCases.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

---

## 15. FuncRS — Funciones de Espectro de Respuesta

### 15.1 SetUser — Definir espectro con arrays T-Sa (RECOMENDADO)

```python
ret = SapModel.Func.FuncRS.SetUser(
    Name,           # str — Nombre de la función
    NumberItems,    # int — Número de puntos T-Sa
    Period,         # float[] — Array de períodos (s)
    Value,          # float[] — Array de aceleraciones espectrales (Sa/g normalizado)
    DampRatio       # float — Razón de amortiguamiento (0.05 = 5%)
)
```

**Ejemplo espectro NCh433+DS61** (Zona 3, Suelo C):
```python
# Sa/g = (S·Ao/g) · α(T)  con  Ao=0.4g, S=1.05
# α(T) = [1 + 4.5·(T/To)^p] / [1 + (T/To)³]
# To=0.40, T'=0.45, n=1.40, p=1.60
import numpy as np

To, Tp, n, p = 0.40, 0.45, 1.40, 1.60
Ao_g, S = 0.4, 1.05

T = np.array([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40,
              0.50, 0.60, 0.70, 0.80, 0.90, 1.0, 1.2, 1.5, 2.0,
              2.5, 3.0, 3.5, 4.0, 5.0])

alpha = (1 + 4.5*(T/To)**p) / (1 + (T/To)**3)
Sa_g = S * Ao_g * alpha  # Sa/g (adimensional)

ret = SapModel.Func.FuncRS.SetUser(
    "NCh433_DS61", len(T), T.tolist(), Sa_g.tolist(), 0.05
)
```

**NOTA CRÍTICA**: Los valores de Sa se ingresan normalizados (Sa/g). El factor de escala (SF=9.81 para m/s²) se aplica al definir el LoadCase, NO en la función.

### 15.2 SetFromFile — Leer espectro desde archivo

```python
ret = SapModel.Func.FuncRS.SetFromFile(
    Name,         # str — Nombre de la función
    FileName,     # str — Ruta al archivo de texto
    HeadLines,    # int — Líneas de encabezado a saltar
    PreCharsP,    # int — Caracteres a saltar antes del período
    PreCharsV,    # int — Caracteres a saltar antes del valor
    PointsPerLine,# int — Pares de datos por línea
    ValuesPerPoint,# int — Valores por punto (período + aceleración = 2)
    DampRatio     # float — Razón de amortiguamiento
)
```

**ADVERTENCIA**: Este método puede ser inestable vía COM. La firma exacta varía entre versiones de ETABS. Es PREFERIBLE usar `SetUser` con arrays calculados en Python, lo cual es más confiable y no depende de archivos externos.

### 15.3 GetNameList

```python
ret = SapModel.Func.FuncRS.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

---

## 16. RespCombo / Combo — Combinaciones de Carga

### 16.1 Add — Crear combinación

```python
ret = SapModel.RespCombo.Add(
    Name,      # str — Nombre de la combinación
    ComboType  # int — Tipo: 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd,
               #       3=SRSS, 4=RangeAdd
)
```

### 16.2 SetCaseList — Agregar caso/combo a la combinación

```python
ret = SapModel.RespCombo.SetCaseList(
    Name,       # str — Nombre de la combinación
    CNameType,  # int — 0=LoadCase, 1=LoadCombo (eCNameType)
    CName,      # str — Nombre del caso o combo a agregar
    SF          # float — Factor de escala
)
```

**Ejemplo combinaciones NCh3171** (7 combos):
```python
# C1: 1.4PP + 1.4TERP
ret = SapModel.RespCombo.Add("C1", 0)
ret = SapModel.RespCombo.SetCaseList("C1", 0, "PP", 1.4)
ret = SapModel.RespCombo.SetCaseList("C1", 0, "TERP", 1.4)

# C2: 1.2PP + 1.2TERP + 1.6SCP + 0.5SCT
ret = SapModel.RespCombo.Add("C2", 0)
ret = SapModel.RespCombo.SetCaseList("C2", 0, "PP", 1.2)
ret = SapModel.RespCombo.SetCaseList("C2", 0, "TERP", 1.2)
ret = SapModel.RespCombo.SetCaseList("C2", 0, "SCP", 1.6)
ret = SapModel.RespCombo.SetCaseList("C2", 0, "SCT", 0.5)

# C5: 1.2PP + 1.2TERP + 1.0SCP ± 1.4SEx
ret = SapModel.RespCombo.Add("C5a", 0)  # +SEx
ret = SapModel.RespCombo.SetCaseList("C5a", 0, "PP", 1.2)
ret = SapModel.RespCombo.SetCaseList("C5a", 0, "TERP", 1.2)
ret = SapModel.RespCombo.SetCaseList("C5a", 0, "SCP", 1.0)
ret = SapModel.RespCombo.SetCaseList("C5a", 0, "SEx", 1.4)

ret = SapModel.RespCombo.Add("C5b", 0)  # -SEx
ret = SapModel.RespCombo.SetCaseList("C5b", 0, "PP", 1.2)
ret = SapModel.RespCombo.SetCaseList("C5b", 0, "TERP", 1.2)
ret = SapModel.RespCombo.SetCaseList("C5b", 0, "SCP", 1.0)
ret = SapModel.RespCombo.SetCaseList("C5b", 0, "SEx", -1.4)
```

### 16.3 GetCaseList — Obtener lista de casos en combo

```python
ret = SapModel.RespCombo.GetCaseList(Name)
# Retorna: (NumberItems, CaseType_array, CaseName_array, SF_array, ret)
```

### 16.4 GetNameList

```python
ret = SapModel.RespCombo.GetNameList()
# Retorna: (NumberNames, Names_array, ret)
```

### 16.5 Delete — Eliminar combinación

```python
ret = SapModel.RespCombo.Delete(Name)
```

---

## 17. MassSource — Fuente de Masa

### 17.1 SetMassSource_1

```python
ret = SapModel.PropMaterial.SetMassSource_1(
    IncludeElements,   # bool — Incluir masa de elementos
    IncludeAddedMass,  # bool — Incluir masa añadida
    IncludeLoads,      # bool — Incluir masa de cargas
    NumberLoads,       # int — Número de patrones de carga
    LoadPat,           # str[] — Nombres de patrones
    SF                 # float[] — Factores de escala
)
```

**NOTA**: En algunas versiones, el acceso es via `SapModel.PropMaterial.SetMassSource_1`. En otras puede ser `SapModel.MassSource.SetMassSource_1`. Verificar con la TLB del ETABS instalado.

**Ejemplo Mass Source para análisis sísmico chileno**:
```python
# Masa = elementos + TERP×1.0 + SCP×0.25
ret = SapModel.PropMaterial.SetMassSource_1(
    True,           # Incluir masa de elementos
    False,          # No masa añadida adicional
    True,           # Incluir masa de cargas
    2,              # 2 patrones de carga
    ["TERP", "SCP"],# Patrones
    [1.0, 0.25]     # Factores: TERP al 100%, SCP al 25%
)
```

---

## 18. Analyze — Análisis

### 18.1 SetActiveDOF — Grados de libertad activos

```python
ret = SapModel.Analyze.SetActiveDOF(
    DOF   # bool[6] — [UX, UY, UZ, RX, RY, RZ]
)
```

**Ejemplo** (6 DOF activos):
```python
ret = SapModel.Analyze.SetActiveDOF([True, True, True, True, True, True])
```

### 18.2 CreateAnalysisModel — Crear modelo de análisis

```python
ret = SapModel.Analyze.CreateAnalysisModel()
# No es necesario llamar esto explícitamente — RunAnalysis lo hace automáticamente
```

### 18.3 RunAnalysis — Ejecutar análisis

```python
ret = SapModel.Analyze.RunAnalysis()
# ret = 0 → éxito
```

**REQUISITO**: El modelo debe tener un file path definido antes de RunAnalysis.
Si el modelo fue creado desde cero, llamar `File.Save()` primero.

### 18.4 SetRunCaseFlag — Activar/desactivar casos para análisis

```python
ret = SapModel.Analyze.SetRunCaseFlag(
    Name,    # str — Nombre del caso de análisis
    Run,     # bool — True=ejecutar, False=no ejecutar
    All      # bool — Si True, aplica a todos los casos (Name se ignora)
)
```

**Ejemplo**: Desactivar todos, luego activar solo los necesarios:
```python
ret = SapModel.Analyze.SetRunCaseFlag("", False, True)  # Desactivar todos
ret = SapModel.Analyze.SetRunCaseFlag("Modal", True, False)
ret = SapModel.Analyze.SetRunCaseFlag("SEx", True, False)
ret = SapModel.Analyze.SetRunCaseFlag("SEy", True, False)
```

### 18.5 SetSolverOption_1 — Opciones del solver

```python
ret = SapModel.Analyze.SetSolverOption_1(
    SolverType,    # int — 0=Standard, 1=Advanced, 2=MultiThreaded
    Force32Bit,    # int — 0=No, 1=Yes
    StiffCase,     # str — Caso de rigidez para P-Delta
    UnactiveDOF    # int — Opción para DOF inactivos
)
```

---

## 19. AnalysisResults — Resultados

### 19.1 Setup — Configurar resultados

```python
# Deseleccionar todos los casos/combos de output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()

# Seleccionar caso específico para output
ret = SapModel.Results.Setup.SetCaseSelectedForOutput(CaseName)

# Seleccionar combo específico para output
ret = SapModel.Results.Setup.SetComboSelectedForOutput(ComboName)
```

### 19.2 StoryDrifts — Derivas de entrepiso

```python
ret = SapModel.Results.StoryDrifts()
# Retorna tupla:
# (NumberResults, Story[], LoadCase[], StepType[], StepNum[],
#  Direction[], Drift[], Label[], X[], Y[], Z[], ret)
```

**NOTA**: El drift se reporta como ratio (Δ/h). Para verificación NCh433: drift ≤ 0.002.

### 19.3 BaseReac — Reacciones en la base

```python
ret = SapModel.Results.BaseReac(
    NumberResults,  # int (output)
    LoadCase,       # str[] (output)
    StepType,       # str[] (output)
    StepNum,        # float[] (output)
    Fx, Fy, Fz,    # float[] (output) — Fuerzas
    Mx, My, Mz,    # float[] (output) — Momentos
    gx, gy, gz     # float (output) — Centro de gravedad
)
```

### 19.4 BaseReactWithCentroid (v20+)

```python
ret = SapModel.Results.BaseReactWithCentroid()
# Retorna resultados con centroide de las reacciones
```

### 19.5 FrameForce — Fuerzas en frames

```python
ret = SapModel.Results.FrameForce(
    Name,          # str — Nombre del frame ("" para todos)
    ItemTypeElm,   # int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
    NumberResults,  # int (output)
    Obj,           # str[] (output) — Nombre del objeto
    ObjSta,        # float[] (output) — Distancia desde I
    Elm,           # str[] (output) — Nombre del elemento
    ElmSta,        # float[] (output) — Distancia en elemento
    LoadCase,      # str[] (output) — Caso de carga
    StepType,      # str[] (output)
    StepNum,       # float[] (output)
    P,             # float[] (output) — Fuerza axial
    V2,            # float[] (output) — Corte 2
    V3,            # float[] (output) — Corte 3
    T,             # float[] (output) — Torsión
    M2,            # float[] (output) — Momento 2
    M3             # float[] (output) — Momento 3
)
```

### 19.6 JointDispl — Desplazamientos nodales

```python
ret = SapModel.Results.JointDispl(
    Name,          # str — Nombre del punto
    ItemTypeElm,   # int
    NumberResults,  # int (output)
    Obj,           # str[] (output)
    Elm,           # str[] (output)
    LoadCase,      # str[] (output)
    StepType,      # str[] (output)
    StepNum,       # float[] (output)
    U1, U2, U3,   # float[] (output) — Traslaciones
    R1, R2, R3    # float[] (output) — Rotaciones
)
```

### 19.7 JointReact — Reacciones nodales

```python
ret = SapModel.Results.JointReact(
    Name,          # str
    ItemTypeElm,   # int
    NumberResults,  # int (output)
    Obj,           # str[] (output)
    Elm,           # str[] (output)
    LoadCase,      # str[] (output)
    StepType,      # str[] (output)
    StepNum,       # float[] (output)
    F1, F2, F3,   # float[] (output) — Fuerzas
    M1, M2, M3    # float[] (output) — Momentos
)
```

### 19.8 JointDrifts — Derivas nodales

```python
ret = SapModel.Results.JointDrifts()
# Similar a StoryDrifts pero por nodo
```

---

## 20. DatabaseTables — Tablas de Base de Datos

### 20.1 GetAvailableTables — Tablas disponibles

```python
ret = SapModel.DatabaseTables.GetAvailableTables()
# Retorna: (NumberTables, TableKeys[], TableKeys[], ret)
```

### 20.2 GetTableForDisplayArray — Obtener datos de tabla

```python
ret = SapModel.DatabaseTables.GetTableForDisplayArray(
    TableKey,           # str — Nombre de la tabla
    FieldKeyList,       # str[] — Campos específicos ([] para todos)
    GroupName,          # str — Grupo ("All" para todos los objetos)
    TableVersion,       # int — Versión de tabla (default 1)
    FieldsKeysIncluded, # str[] (output) — Campos incluidos
    NumberRecords,      # int (output) — Número de registros
    TableData           # str[] (output) — Datos de la tabla
)
```

**Tablas comunes**:
| TableKey | Contenido |
|---|---|
| `"Story Definitions"` | Definición de pisos |
| `"Material Properties"` | Propiedades de materiales |
| `"Frame Section Properties"` | Secciones de frame |
| `"Area Section Properties"` | Secciones de área |
| `"Joint Displacements"` | Desplazamientos nodales |
| `"Frame Forces"` | Fuerzas en frames |
| `"Story Drifts"` | Derivas de entrepiso |
| `"Base Reactions"` | Reacciones en base |
| `"Modal Participating Mass Ratios"` | Masas participantes modales |
| `"Story Forces"` | Fuerzas por piso |
| `"Centers Of Mass And Rigidity"` | CM y CR por piso |

### 20.3 SetTableForEditingArray — Editar tabla

```python
ret = SapModel.DatabaseTables.SetTableForEditingArray(
    TableKey,           # str
    TableVersion,       # int
    FieldsKeysIncluded, # str[]
    NumberRecords,      # int
    TableData           # str[] — Datos editados
)
```

### 20.4 ApplyEditedTables — Aplicar cambios

```python
ret = SapModel.DatabaseTables.ApplyEditedTables(
    FillImport,   # bool
    NumFatalErrors,    # int (output)
    NumWarnMsgs,       # int (output)
    NumInfoMsgs,       # int (output)
    ImportLog          # str (output)
)
```

---

## 21. Enumeraciones Clave

### 21.1 eUnits — Unidades

| Valor | Unidades |
|---|---|
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
| 11 | Tonf_mm_C |
| 12 | Tonf_m_C |
| 13 | kN_cm_C |
| 14 | kgf_cm_C |
| 15 | N_cm_C |
| 16 | Tonf_cm_C |

**Para el proyecto: usar 12 = Tonf_m_C** (consistente con práctica chilena).

### 21.2 eMatType — Tipo de material

| Valor | Tipo |
|---|---|
| 1 | Steel |
| 2 | Concrete |
| 3 | NoDesign |
| 4 | Aluminum |
| 5 | ColdFormed |
| 6 | Rebar |
| 7 | Tendon |
| 8 | Masonry |

### 21.3 eLoadPatternType — Tipo de patrón de carga

| Valor | Tipo | Uso proyecto |
|---|---|---|
| 1 | Dead | PP |
| 2 | SuperDead | TERP, TERT |
| 3 | Live | SCP, SCT |
| 4 | ReduceLive | — |
| 5 | Quake | SX, SY |
| 6 | Wind | — |
| 7 | Snow | — |
| 8 | Other | — |
| 11 | LiveRoof | — |
| 12 | Notional | — |

### 21.4 eSlabType — Tipo de losa

| Valor | Tipo |
|---|---|
| 0 | Slab (maciza) |
| 1 | Drop (capitel) |
| 2 | Stiff (rígida) |
| 3 | Ribbed (nervada) |
| 4 | Waffle |

### 21.5 eWallPropType — Tipo de muro

| Valor | Tipo |
|---|---|
| 0 | Specified |
| 1 | AutoSelectList |

### 21.6 eShellType — Tipo de shell

| Valor | Tipo | Uso |
|---|---|---|
| 1 | ShellThin | Losas delgadas |
| 2 | ShellThick | Muros (recomendado) |
| 3 | Membrane | Solo membrana |
| 4 | Plate | Solo flexión |
| 5 | Shell | Membrana + flexión |
| 6 | Layered | Por capas |

### 21.7 eItemType

| Valor | Tipo |
|---|---|
| 0 | Objects |
| 1 | Group |
| 2 | SelectedObjects |

### 21.8 eCNameType (para RespCombo)

| Valor | Tipo |
|---|---|
| 0 | LoadCase |
| 1 | LoadCombo |

### 21.9 Cardinal Points (InsertionPoint)

| Valor | Posición |
|---|---|
| 1 | Bottom Left |
| 2 | Bottom Center |
| 3 | Bottom Right |
| 4 | Middle Left |
| 5 | Middle Center |
| 6 | Middle Right |
| 7 | Top Left |
| 8 | Top Center |
| 9 | Top Right |
| 10 | Centroid |
| 11 | Shear Center |

---

## 22. Patrones de Uso Comunes

### 22.1 Pipeline completo de modelación HA

```python
import comtypes.client
import sys

# 1. CONEXIÓN
EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
SapModel = EtabsObject.SapModel

# 2. NUEVO MODELO
SapModel.InitializeNewModel()
SapModel.File.NewGridOnly(20, 2.6, 3.4, 17, 6, 5.0, 5.0)
SapModel.SetPresentUnits(12)  # Tonf_m_C

# 3. MATERIALES
SapModel.PropMaterial.SetMaterial("G30", 2)  # Concrete
SapModel.PropMaterial.SetMPIsotropic("G30", 2624300.0, 0.2, 1.0E-05)
SapModel.PropMaterial.SetOConcrete_1("G30", 3000.0, False, 1.0, 1, 0, 0.002216, 0.005, -0.1)
SapModel.PropMaterial.SetWeightAndMass("G30", 1, 2.5)

SapModel.PropMaterial.SetMaterial("A630-420H", 6)  # Rebar
SapModel.PropMaterial.SetORebar_1("A630-420H", 42000.0, 63000.0, 52500.0, 63000.0,
                                   0, 0, 0.01, 0.09, -0.1, False)

# 4. SECCIONES
SapModel.PropFrame.SetRectangle("VI20/60G30", "G30", 0.60, 0.20)
SapModel.PropFrame.SetModifiers("VI20/60G30", [1,1,1,0,1,1,1,1])  # J=0

SapModel.PropArea.SetWall("MHA30G30", 0, 2, "G30", 0.30)
SapModel.PropArea.SetWall("MHA20G30", 0, 2, "G30", 0.20)
SapModel.PropArea.SetSlab("Losa15G30", 0, 1, "G30", 0.15)
SapModel.PropArea.SetModifiers("Losa15G30", [1,1,1,0.25,0.25,0.25,1,1,1,1])

# 5. GEOMETRÍA (muros, vigas, losas por AddByCoord)
# ... (loops por piso y por eje)

# 6. DIAFRAGMA
SapModel.AreaObj.SetDiaphragm("All", "D1")  # Asignar D1 a todas las losas

# 7. RESTRICCIONES (empotramientos en base)
# ... (loop por puntos en z=0)

# 8. PATRONES DE CARGA
SapModel.LoadPatterns.Add("TERP", 2, 0.0)
SapModel.LoadPatterns.Add("TERT", 2, 0.0)
SapModel.LoadPatterns.Add("SCP", 3, 0.0)
SapModel.LoadPatterns.Add("SCT", 3, 0.0)

# 9. CARGAS EN LOSAS
# ... (SetLoadUniform para cada losa/piso)

# 10. ESPECTRO
# ... (SetUser con arrays T-Sa calculados)

# 11. CASOS DE ESPECTRO
SapModel.LoadCases.ResponseSpectrum.SetCase("SEx")
SapModel.LoadCases.ResponseSpectrum.SetLoads("SEx", 1, ["U1"], ["NCh433_DS61"], [9.81], ["Global"], [0.0])

# 12. COMBINACIONES
# ... (7 combos NCh3171)

# 13. MASS SOURCE
# SapModel.PropMaterial.SetMassSource_1(True, False, True, 2, ["TERP","SCP"], [1.0, 0.25])

# 14. GUARDAR Y ANALIZAR
SapModel.File.Save(r"C:\ruta\Edificio1.edb")
SapModel.Analyze.RunAnalysis()

# 15. RESULTADOS
drifts = SapModel.Results.StoryDrifts()
base = SapModel.Results.BaseReac(0, [], [], [], [], [], [], [], [], [], 0, 0, 0)
```

### 22.2 Verificar que elementos se crearon

```python
def verify_elements(SapModel):
    """Verificar conteo de elementos creados."""
    n_frames = SapModel.FrameObj.GetNameList()[0]
    n_areas = SapModel.AreaObj.GetNameList()[0]
    n_points = SapModel.PointObj.GetNameList()[0]
    print(f"Frames: {n_frames}, Areas: {n_areas}, Points: {n_points}")
    return n_frames, n_areas, n_points
```

### 22.3 Refrescar vista

```python
def refresh_view(SapModel):
    """Refrescar la vista de ETABS."""
    SapModel.View.RefreshView(0, False)
```

---

## 23. Errores Frecuentes y Soluciones

### 23.1 comtypes.gen stale
**Síntoma**: `AttributeError` al acceder a interfaces COM.
**Solución**: Limpiar `comtypes/gen/` ANTES de importar `comtypes.client` (ver sección 1.2).

### 23.2 Instancia invisible (CreateObject)
**Síntoma**: Scripts corren pero ETABS no muestra nada; .edb corrupto.
**Solución**: NUNCA usar `CreateObject` por defecto. Usar `GetActiveObject` con ETABS ya abierto.

### 23.3 File.Save() produce .edb corrupto
**Síntoma**: El archivo .edb se guarda pero no se puede abrir.
**Causa**: ETABS fue lanzado sin UI (via `CreateObject`).
**Solución**: Abrir ETABS manualmente → File > New Model > Blank → LUEGO correr scripts.

### 23.4 RPC Server Unavailable (-2147023174)
**Síntoma**: Error COM después de operaciones pesadas (>1000 áreas + mesh).
**Causa**: La sesión COM muere por timeout o memoria.
**Solución**: Separar pipeline en fases con sesiones COM independientes.

### 23.5 FuncRS.SetFromFile firma incorrecta
**Síntoma**: Error de argumentos al llamar SetFromFile.
**Causa**: La firma varía entre versiones y la documentación no siempre coincide con la TLB.
**Solución**: Usar `FuncRS.SetUser` con arrays calculados en Python (100% confiable).

### 23.6 get_story_data() falla en v19
**Síntoma**: Las funciones de consulta de stories retornan errores.
**Causa**: Binding COM inconsistente en v19.
**Solución**: No abortar por esto. Usar `NewGridOnly` que garantiza stories correctas. Verificar visualmente en ETABS.

### 23.7 Garbage Collector destruye objetos COM
**Síntoma**: La conexión COM muere aleatoriamente.
**Causa**: Python GC libera objetos COM si salen de scope.
**Solución**: Mantener `helper`, `EtabsObject`, `SapModel` como variables globales del módulo.

### 23.8 Binding inconsistency entre GetActiveObject y CreateObject
**Síntoma**: Métodos disponibles difieren según el método de conexión.
**Causa**: Generan TLBs distintos.
**Solución**: Usar consistentemente un solo método de conexión. Preferir `GetActiveObject`.

### 23.9 AutoMesh con vano mínimo
**Síntoma**: Mesh no se genera o genera elementos degenerados.
**Causa**: Tamaño de mesh mayor que el vano más pequeño.
**Solución**: AutoMesh = 0.4m (vano mínimo del proyecto = 0.425m entre ejes 8-9).

---

## 24. Fuentes

### Documentación oficial CSI
- [CSI Developer Portal](https://www.csiamerica.com/developer)
- [CSI OAPI Knowledge Base](https://wiki.csiamerica.com/display/kb/OAPI)
- [OAPI FAQ](https://wiki.csiamerica.com/display/kb/OAPI+FAQ)
- [ETABS API 2016 Namespace](https://docs.csiamerica.com/help-files/etabs-api-2016/html/6a9c8a48-232d-761c-5421-1ff5ae019a4c.htm)

### Funciones documentadas en docs.csiamerica.com
- [cSapModel.InitializeNewModel](https://docs.csiamerica.com/help-files/etabs-api-2016/html/592ff586-daba-0591-a52e-ddb6e939f7b9.htm)
- [cFile.NewGridOnly](https://docs.csiamerica.com/help-files/etabs-api-2016/html/cb79539c-729f-7231-1625-b8f15e018e1f.htm)
- [cFile.OpenFile](https://docs.csiamerica.com/help-files/etabs-api-2016/html/ab8ad3e2-ebcf-7cd9-636b-ec9cccdc85a8.htm)
- [cStory.SetStories](https://docs.csiamerica.com/help-files/etabs-api-2016/html/d840a5fd-1599-8263-d65f-338a7b5ee001.htm)
- [cStory.GetStories](https://docs.csiamerica.com/help-files/etabs-api-2016/html/3f804fa8-9fef-a9f0-8517-87676c0ea8ef.htm)
- [cPropMaterial.SetMaterial](https://docs.csiamerica.com/help-files/etabs-api-2016/html/2a077afc-162f-5e1f-c4bd-10494950c9b1.htm)
- [cPropMaterial.AddMaterial](https://docs.csiamerica.com/help-files/etabs-api-2016/html/0b7d6dbe-a817-3539-ded2-05a597d3f6cc.htm)
- [cPropMaterial.SetMPIsotropic](https://docs.csiamerica.com/help-files/etabs-api-2016/html/2963d35a-d38d-275d-10c4-1574e2c82fbc.htm)
- [cPropMaterial.SetOConcrete_1](https://docs.csiamerica.com/help-files/etabs-api-2016/html/6bc3a61c-6e41-716a-a401-937b2042e30b.htm)
- [cPropMaterial.SetWeightAndMass](https://docs.csiamerica.com/help-files/etabs-api-2016/html/c570f36b-c233-7a3a-722b-79873bb7b1a8.htm)
- [cPropFrame.SetRectangle](https://docs.csiamerica.com/help-files/etabs-api-2016/html/5cd12822-51cc-7148-0807-ccafcadb78e9.htm)
- [cPropFrame.SetRebarBeam](https://docs.csiamerica.com/help-files/etabs-api-2016/html/64dd6c3b-b4a4-9e2b-25b3-246aea547147.htm)
- [cPropFrame.SetRebarColumn](https://docs.csiamerica.com/help-files/etabs-api-2016/html/590ba8ae-6bab-eb0a-b0f5-6303b03bf051.htm)
- [cPropFrame.SetModifiers](https://docs.csiamerica.com/help-files/etabs-api-2016/html/511bdadb-f147-812f-f69b-de6f6e723ca1.htm)
- [cPropArea.SetWall](https://docs.csiamerica.com/help-files/etabs-api-2016/html/20e9156e-132b-d46b-fe42-8ef7002d8dba.htm)
- [cPropArea.SetSlab](https://docs.csiamerica.com/help-files/etabs-api-2016/html/5dc4e0d8-87be-b466-fd29-ac59f5b2bffe.htm)
- [cAreaObj.AddByCoord](https://docs.csiamerica.com/help-files/etabs-api-2016/html/2ae59c04-cac4-236c-f396-d9532759e4d9.htm)
- [cAreaObj.SetProperty](https://docs.csiamerica.com/help-files/etabs-api-2016/html/dbf7c729-66b9-6244-03e1-b688ad9301db.htm)
- [cAreaObj.SetLoadUniform](https://docs.csiamerica.com/help-files/etabs-api-2016/html/2eec7223-f6ba-2756-af3e-10ee14ea0120.htm)
- [cFrameObj.SetSection](https://docs.csiamerica.com/help-files/etabs-api-2016/html/a9c5ea96-1f73-baf4-3825-9d1e6001a71c.htm)
- [cFrameObj.SetLocalAxes](https://docs.csiamerica.com/help-files/etabs-api-2016/html/a4f27656-a0f3-618c-ed40-869aa738eb50.htm)
- [cFrameObj.SetInsertionPoint](https://docs.csiamerica.com/help-files/etabs-api-2015/html/2d10b1f6-3681-9816-51df-cbcfebb26364.htm)
- [cLoadPatterns.GetNameList](https://docs.csiamerica.com/help-files/etabs-api-2016/html/ad30b175-a222-0ba3-8084-ffdfc46d352d.htm)
- [cCombo.SetCaseList](https://docs.csiamerica.com/help-files/etabs-api-2016/html/f6569f31-e57a-a342-2adb-4df42f865e76.htm)
- [cCaseResponseSpectrum.SetCase](https://docs.csiamerica.com/help-files/etabs-api-2016/html/100ab45e-bef4-4226-ce99-3e3452e7b6e8.htm)
- [cAnalyze.RunAnalysis](https://docs.csiamerica.com/help-files/etabs-api-2016/html/4b00dc5d-9b60-e088-1b39-d7f7687145fc.htm)
- [cAnalyze.CreateAnalysisModel](https://docs.csiamerica.com/help-files/etabs-api-2016/html/08c37fd5-4e3f-a689-d9d7-36c8a10e53ef.htm)
- [cAnalysisResults.StoryDrifts](https://docs.csiamerica.com/help-files/etabs-api-2016/html/e55e16e2-b7b0-2864-f3dc-b781f4062325.htm)
- [cAnalysisResults.FrameForce](https://docs.csiamerica.com/help-files/etabs-api-2016/html/87689f3e-4175-1627-618b-c4ebae5e89b5.htm)
- [SetMassSource_1](https://docs.csiamerica.com/help-files/etabs-api-2015/html/3f256ea8-6c8d-76b0-acae-e1d370413b37.htm)
- [SetActiveDOF](https://docs.csiamerica.com/help-files/etabs-api-2015/html/15e8ec93-f5a6-0f87-88f2-43479a3c846e.htm)

### Tutoriales y ejemplos
- [EngineeringSkills — ETABS Python API Introduction](https://www.engineeringskills.com/posts/an-introduction-to-the-etabs-python-api)
- [Stru.ai — ETABS API Beginner Guide 2025](https://stru.ai/blog/etabs-api-beginner-guide)
- [Stru.ai — Master ETABS Seismic Analysis Automation](https://stru.ai/blog/etabs-seismic-automation)
- [Stru.ai — ETABS API Automation 2025](https://stru.ai/blog/etabs-api-automation-2025)
- [GitHub — danielogg92/Etabs-API-Python](https://github.com/danielogg92/Etabs-API-Python)
- [GitHub — ebrahimraeyat/etabs_api](https://github.com/ebrahimraeyat/etabs_api)
- [GitHub — jantozor/CSiAPIExamples](https://github.com/jantozor/CSiAPIExamples)
- [Re-tug — ETABS API Database Tables Examples](https://re-tug.com/post/etabs-api-more-examples-database-tables/18)
- [Hakan Keskin — Extracting Story Drifts](https://hakan-keskin.medium.com/extracting-story-drifts-and-joint-displacements-in-etabs-with-python-6b886aac89ba)

### Documentación local del proyecto (verificada)
- `docs/Material taller/Material Apoyo Taller 2026.pdf` — Prof. Music (47p)
- `docs/Material taller/Paso a Paso ETABS M.Lafontaine.pdf` — Tutorial completo (143p)
- `docs/Material taller/Manual de ETABS v19.pdf` — Referencia interfaz (239p)
- Archivo CHM oficial: `C:\Program Files\Computers and Structures\ETABS 19\CSi API ETABS v1.chm`

---

## Apéndice A: Mapa de funciones por fase del pipeline

| Fase | Funciones API principales |
|---|---|
| **Conexión** | `GetActiveObject`, `SapModel` |
| **Modelo nuevo** | `InitializeNewModel`, `File.NewGridOnly`, `SetPresentUnits` |
| **Pisos** | `Story.SetStories`, `Story.GetStories` |
| **Materiales** | `PropMaterial.SetMaterial`, `SetMPIsotropic`, `SetOConcrete_1`, `SetWeightAndMass` |
| **Secciones frame** | `PropFrame.SetRectangle`, `SetModifiers` |
| **Secciones area** | `PropArea.SetWall`, `SetSlab`, `SetModifiers` |
| **Muros** | `AreaObj.AddByCoord`, `SetProperty`, `SetAutoMesh` |
| **Vigas** | `FrameObj.AddByCoord`, `SetSection`, `SetInsertionPoint` |
| **Losas** | `AreaObj.AddByCoord`, `SetProperty`, `SetDiaphragm`, `SetLoadUniform` |
| **Restricciones** | `PointObj.SetRestraint` |
| **Cargas** | `LoadPatterns.Add`, `SetSelfWtMultiplier`, `AreaObj.SetLoadUniform` |
| **Espectro** | `Func.FuncRS.SetUser`, `LoadCases.ResponseSpectrum.SetCase/SetLoads` |
| **Combos** | `RespCombo.Add`, `SetCaseList` |
| **Mass Source** | `SetMassSource_1` |
| **Análisis** | `Analyze.SetActiveDOF`, `SetRunCaseFlag`, `RunAnalysis` |
| **Resultados** | `Results.StoryDrifts`, `BaseReac`, `FrameForce`, `JointDispl` |
| **Tablas** | `DatabaseTables.GetTableForDisplayArray` |

## Apéndice B: Convención de retorno

Todas las funciones API retornan un entero:
- `0` = Éxito
- `≠ 0` = Error

En Python con comtypes, muchas funciones retornan tuplas donde el último elemento es el código de retorno. Ejemplo:
```python
result = SapModel.Story.GetNameList()
# result = (NumberNames, Names_array, ret_code)
n_stories = result[0]
story_names = result[1]
ret = result[-1]  # 0 = OK
```

## Apéndice C: Notas sobre compatibilidad ETABS v19

1. **ETABS v19 usa CSI OAPI v1** (no v0 ni v2)
2. **ProgID para COM**: `"CSI.ETABS.API.ETABSObject"`
3. **Helper ProgID**: `"ETABSv1.Helper"`
4. **Interface QueryInterface**: `comtypes.gen.ETABSv1.cHelper`
5. **Algunas funciones `_1` (como SetOConcrete_1) son la versión actualizada** — la versión sin `_1` puede ser legacy
6. **SetMassSource_1 está documentado en ETABS 2015 API** — funciona en v19
7. **DatabaseTables.GetTableForDisplayArray** puede tener bug si FieldKeys ≠ FieldNames (corregido en v20+)
8. **Archivo CHM**: `CSi API ETABS v1.chm` en el directorio de instalación contiene la referencia completa
