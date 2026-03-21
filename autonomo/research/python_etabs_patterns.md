# Patrones Python + comtypes + ETABS — Investigación Completa

> **Feature**: R02
> **Fecha**: 20 marzo 2026
> **Propósito**: Patrones verificados de uso de Python con ETABS via comtypes, compilados de repos reales, documentación oficial, tutoriales y foros.
> **Complementa**: `etabs_api_reference.md` (R01) — referencia de funciones API

---

## Tabla de Contenidos

1. [Ecosistema: Repos, Paquetes y Recursos](#1-ecosistema-repos-paquetes-y-recursos)
2. [Conexión COM — Patrones Verificados](#2-conexión-com--patrones-verificados)
3. [Ciclo de Vida COM](#3-ciclo-de-vida-com)
4. [Manejo de Errores](#4-manejo-de-errores)
5. [Materiales — Definición Programática](#5-materiales--definición-programática)
6. [Geometría — Frames, Areas, Points](#6-geometría--frames-areas-points)
7. [Cargas — Asignación y Patrones](#7-cargas--asignación-y-patrones)
8. [Análisis — Configuración y Ejecución](#8-análisis--configuración-y-ejecución)
9. [Resultados — Extracción y Post-Proceso](#9-resultados--extracción-y-post-proceso)
10. [Database Tables API](#10-database-tables-api)
11. [Diferencias entre Versiones](#11-diferencias-entre-versiones)
12. [Bugs Conocidos y Workarounds](#12-bugs-conocidos-y-workarounds)
13. [Best Practices y Performance](#13-best-practices-y-performance)
14. [Aplicación a Nuestro Pipeline](#14-aplicación-a-nuestro-pipeline)
15. [Fuentes Completas](#15-fuentes-completas)

---

## 1. Ecosistema: Repos, Paquetes y Recursos

### 1.1 Repositorios GitHub Verificados

| # | Repo | Stars | Descripción | Lenguaje |
|---|------|-------|-------------|----------|
| 1 | [danielogg92/Etabs-API-Python](https://github.com/danielogg92/Etabs-API-Python) | 67 | Funciones wrapper limpias (get/set) | comtypes |
| 2 | [mitchell-tesch/CSiPy](https://github.com/mitchell-tesch/CSiPy) | 38 | Wrapper OOP completo, 30+ interfaces | pythonnet (.NET) |
| 3 | [youandvern/ETABS_building_drift_check](https://github.com/youandvern/ETABS_building_drift_check) | 21 | GUI PyQt5 drift+torsión, incluye .EDB | comtypes |
| 4 | [retug/ETABs](https://github.com/retug/ETABs) | 19 | Diaphragm slicer, Database Tables | comtypes v1.1.7 |
| 5 | [mihdicaballero/ETABS-Ninja](https://github.com/mihdicaballero/ETABS-Ninja) | 14 | Drift via DB Tables, matplotlib, colorama | comtypes |
| 6 | [ebrahimraeyat/etabs_api](https://github.com/ebrahimraeyat/etabs_api) | — | Paquete PyPI `etabs-api`, ETABS 2018+ | comtypes |
| 7 | [jantozor/CSiAPIExamples](https://github.com/jantozor/CSiAPIExamples) | — | Ejemplos oficiales multi-lenguaje | Todos |
| 8 | [mtavares51/etabs_python_modelling](https://github.com/mtavares51/etabs_python_modelling) | — | Modelación paramétrica | comtypes |

**Hallazgo clave**: Todos los repos (excepto CSiPy) usan `comtypes` — es el estándar de facto.

### 1.2 Paquetes PyPI

| Paquete | Install | Backend | Descripción |
|---------|---------|---------|-------------|
| **comtypes** | `pip install comtypes` | COM | Base fundamental. v1.1.7+ recomendada |
| **etabs-api** | `pip install etabs-api` | comtypes | Wrapper alto nivel ETABS 2018+/SAFE. Módulos frame_obj, area, database |
| **pytabs** | `pip install pytabs` | pythonnet | Alternativa .NET API. Python 3.10+, IntelliSense via stubs |
| **Sap2000py** | `pip install Sap2000py` | comtypes | SAP2000 (misma familia API CSI). Patrones transferibles |

**Para nuestro pipeline**: Solo necesitamos `comtypes`. Opcionalmente `etabs-api` para simplificar.

### 1.3 Tutoriales y Blogs Clave

| Recurso | URL | Contenido |
|---------|-----|-----------|
| **Stru.ai** (10+ artículos) | stru.ai/blog/etabs-api-beginner-guide | Setup, COM, análisis sísmico, post-proceso |
| **Hakan Keskin** (9 artículos Medium) | hakan-keskin.medium.com | Drift, modal, pushover, time history, AI |
| **NeutralAXIS** | neutralaxis.github.io/ETABS/ | Getting started, 3 métodos conexión |
| **Re-Tug** | re-tug.com | Database Tables API, Diaphragm Slicer |
| **VIKTOR.ai** | viktor.ai/blog | SAP2000/ETABS integration, post-proceso |
| **EngineeringSkills** | engineeringskills.com | Intro ETABS Python API |
| **CSI Official Example 7** | docs.csiamerica.com | Python: crear modelo, analizar, extraer |
| **PythonForStructuralEngineers** | pythonforstructuralengineers.com | Curso ETABS Automation |

### 1.4 Documentación Oficial CSI

| Recurso | URL/Ubicación |
|---------|---------------|
| **API Help Files** | docs.csiamerica.com/help-files/etabs-api-2016/ |
| **CHM local** | `C:\Program Files\...\ETABS XX\CSI API ETABS v1.chm` |
| **Wiki OAPI** | wiki.csiamerica.com/display/kb/OAPI |
| **OAPI FAQ** | wiki.csiamerica.com/display/kb/OAPI+FAQ |
| **Developer Portal** | csiamerica.com/developer |
| **Release Notes** | installs.csiamerica.com/software/ETABS/{ver}/ |

### 1.5 Foros Principales

**Eng-Tips es el foro principal** (Stack Overflow tiene casi nada sobre ETABS API).

Threads más relevantes:
- Error attaching Python to ETABS (comtypes version)
- ETABS v18 Cannot attach (limpiar comtypes.gen)
- Section Cut Definition (cambios v19→v20)
- Mass Source via API (firma SetMassSource_1)
- FrameObj.GetSection, GetGridSys_2

---

## 2. Conexión COM — Patrones Verificados

### 2.1 Método 1: GetActiveObject (RECOMENDADO)

```python
# Fuente: danielogg92/Etabs-API-Python, youandvern/ETABS_building_drift_check
# Requiere: ETABS abierto con modelo cargado
import comtypes.client
import sys

try:
    EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
except (OSError, comtypes.COMError):
    print("No running instance of the program found or failed to attach.")
    sys.exit(-1)

SapModel = EtabsObject.SapModel
```

**Ventajas**: UI activa, File.Save funciona, estable.
**Repos que lo usan**: danielogg92, youandvern.

### 2.2 Método 2: Helper.GetObject (v18+)

```python
# Fuente: mihdicaballero/ETABS-Ninja, retug/ETABs, danielogg92 (método 2)
# ProgID 'ETABSv1.Helper' es universal para v18-v22+
import comtypes.client

helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

try:
    EtabsObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
except (OSError, comtypes.COMError):
    print("No running instance of the program found or failed to attach.")
    sys.exit(-1)

SapModel = EtabsObject.SapModel
```

**Ventajas**: Más robusto en algunas versiones de comtypes. Soporta computador remoto via `GetObjectHost`.
**Repos que lo usan**: mihdicaballero, retug, danielogg92 (método 2).

### 2.3 Método 3: Helper.CreateObject (PELIGROSO)

```python
# Fuente: youandvern/ETABS_building_drift_check, mitchell-tesch/CSiPy
# SOLO usar como último recurso
import comtypes.client

helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

# CreateObject o CreateObjectProgID
EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")

# CRÍTICO: Forzar visibilidad
try:
    EtabsObject.Visible = True
except:
    pass

EtabsObject.ApplicationStart()
import time
time.sleep(15)  # Esperar a que UI cargue

SapModel = EtabsObject.SapModel
SapModel.InitializeNewModel()
```

**PELIGROS**:
- Puede crear instancia INVISIBLE (bug documentado en Eng-Tips y GitHub)
- `File.Save()` puede producir .edb CORRUPTO sin UI funcional
- Requiere forzar `Visible=True` y esperar 15s

### 2.4 Patrón Robusto Completo (try-fallback)

```python
# Compilado de múltiples repos + nuestra experiencia
import os
import sys
import time
import shutil

def clean_comtypes_gen():
    """Limpiar cache stale de comtypes (ANTES de import comtypes.client)."""
    try:
        import comtypes
        gen_path = os.path.join(os.path.dirname(comtypes.__file__), 'gen')
        if os.path.exists(gen_path):
            for item in os.listdir(gen_path):
                if item != '__init__.py':
                    path = os.path.join(gen_path, item)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
    except:
        pass

def connect_etabs(create_if_missing=False):
    """
    Conectar a ETABS con prioridad:
    1. GetActiveObject → 2. Helper.GetObject → 3. CreateObject (si create_if_missing)
    Returns: (EtabsObject, SapModel)
    """
    import comtypes.client

    # Método 1: GetActiveObject
    try:
        EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        print("Conectado via GetActiveObject")
        return EtabsObject, EtabsObject.SapModel
    except OSError:
        pass

    # Método 2: Helper.GetObject
    try:
        helper = comtypes.client.CreateObject('ETABSv1.Helper')
        import comtypes.gen.ETABSv1 as ETABSv1
        helper = helper.QueryInterface(ETABSv1.cHelper)
        EtabsObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
        print("Conectado via Helper.GetObject")
        return EtabsObject, EtabsObject.SapModel
    except Exception:
        pass

    # Método 3: Crear nueva instancia (PELIGROSO)
    if create_if_missing:
        helper = comtypes.client.CreateObject('ETABSv1.Helper')
        import comtypes.gen.ETABSv1 as ETABSv1
        helper = helper.QueryInterface(ETABSv1.cHelper)
        EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        try:
            EtabsObject.Visible = True
        except:
            pass
        EtabsObject.ApplicationStart()
        time.sleep(15)
        print("WARN: Instancia creada via CreateObject")
        return EtabsObject, EtabsObject.SapModel

    raise ConnectionError("No se pudo conectar a ETABS. Ábrelo manualmente primero.")

# Uso:
clean_comtypes_gen()
etabs, model = connect_etabs(create_if_missing=False)
```

### 2.5 Alternativa: win32com (menos común)

```python
# Alternativa a comtypes (menos usada pero funcional)
import win32com.client

# Conectar a instancia existente
EtabsObject = win32com.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
# O crear nueva
EtabsObject = win32com.client.Dispatch("CSI.ETABS.API.ETABSObject")
```

### 2.6 ProgID por Versión

| ProgID | Versión ETABS |
|--------|---------------|
| `ETABSv17.Helper` | ETABS 17 solamente |
| `ETABSv1.Helper` | ETABS 18, 19, 20, 21, 22+ (universal) |
| `CSI.ETABS.API.ETABSObject` | Todas las versiones |

---

## 3. Ciclo de Vida COM

### 3.1 Desconexión Correcta

```python
# Fuente: mitchell-tesch/CSiPy, docs CSI
# Secuencia correcta de cierre:
ret = SapModel.File.Save(model_path)       # 1. Guardar
ret = EtabsObject.ApplicationExit(False)   # 2. Cerrar (False = no guardar de nuevo)
SapModel = None                            # 3. Liberar referencia COM
EtabsObject = None
```

**CRÍTICO**: Si no se cierra correctamente, ETABS.exe sigue en background.

### 3.2 Patrón try/finally

```python
# Fuente: docs CSI, best practice general COM
try:
    EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = EtabsObject.SapModel
    # ... operaciones ...
finally:
    if SapModel is not None:
        SapModel = None
    if EtabsObject is not None:
        EtabsObject = None
```

### 3.3 Separación de Sesiones COM (Pipeline Largo)

```python
# Fuente: nuestra experiencia + documentación CSI
# Para pipelines largos (13+ pasos), la sesión COM puede morir

# ---- Fase 1: Geometría ----
EtabsObject.ApplicationStart()
SapModel = EtabsObject.SapModel
# ... crear geometría ...
SapModel.File.Save(path)
EtabsObject.ApplicationExit(False)

import time
time.sleep(10)  # Esperar cierre completo

# ---- Fase 2: Análisis (sesión COM fresca) ----
EtabsObject2 = helper.GetObject("CSI.ETABS.API.ETABSObject")
SapModel2 = EtabsObject2.SapModel
SapModel2.File.OpenFile(path)
# ... configurar análisis ...
```

Esto es válido según documentación CSI: `ApplicationStart()` / `OpenFile()` / `ApplicationExit()` están diseñados para este patrón.

### 3.4 Protección contra Garbage Collector

```python
# Fuente: mihdicaballero/ETABS-Ninja, nuestra experiencia
# Mantener referencias COM en variables GLOBALES del módulo

# MAL: variables locales pueden ser recolectadas por GC
def do_stuff():
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    EtabsObject = helper.GetObject(...)
    SapModel = EtabsObject.SapModel
    # helper puede ser GC'd antes de que termine → crash COM

# BIEN: variables a nivel de módulo
_helper = None
_etabs = None
_model = None

def connect():
    global _helper, _etabs, _model
    _helper = comtypes.client.CreateObject('ETABSv1.Helper')
    _etabs = _helper.GetObject(...)
    _model = _etabs.SapModel
```

---

## 4. Manejo de Errores

### 4.1 Convención de Return Values

| Valor | Significado |
|-------|-------------|
| `0` | **Éxito** — operación completada |
| `!= 0` | **Error** — operación falló |

No hay documentación oficial sobre significados específicos de códigos no-cero.

### 4.2 Patrón de Verificación (de repos reales)

```python
# Fuente: mitchell-tesch/CSiPy (función handle())
def handle(ret):
    """Verificar return value de API. Lanzar excepción si falla."""
    if ret != 0:
        raise RuntimeError(f"ETABS API call failed with code {ret}")

# Uso:
handle(SapModel.PropMaterial.SetMPIsotropic("G30", 25743.0, 0.2, 10e-6))
handle(SapModel.FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, name, prop))
```

### 4.3 Funciones que Retornan Tuplas

```python
# Muchas funciones retornan tuplas: (dato1, dato2, ..., ret_code)
ret = SapModel.FrameObj.GetNameList()
# ret[0] = número de frames
# ret[1] = lista de nombres
# ret[2] = código de error (en algunas versiones)

# El orden PUEDE variar entre versiones — consultar CHM local
```

### 4.4 Verificación Post-Creación

```python
# Fuente: nuestro pipeline (scripts 03/04/05)
# Obtener lista ANTES
count_before = SapModel.FrameObj.GetNameList()[0]

# Crear elemento
ret = SapModel.FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, name, propName)

# Verificar DESPUÉS
count_after = SapModel.FrameObj.GetNameList()[0]
assert count_after > count_before, "Frame no se creó!"
```

---

## 5. Materiales — Definición Programática

### 5.1 Obtener Materiales Existentes

```python
# Fuente: danielogg92/Etabs-API-Python/Etabs_Get_Functions.py
def get_all_materials(SapModel):
    SapModel.SetPresentUnits(9)  # N_mm_C para MPa
    mat_types = {1:'Steel', 2:'Concrete', 3:'NoDesign', 4:'Aluminum',
                 5:'ColdFormed', 6:'Rebar', 7:'Tendon', 8:'Masonry'}
    mat_name_list = SapModel.PropMaterial.GetNameList()
    materials = {}
    for i in range(mat_name_list[0]):
        mat_name = mat_name_list[1][i]
        mat_props = SapModel.PropMaterial.GetMaterial(mat_name)
        mat_type = mat_types[mat_props[0]]
        if mat_type == 'Concrete':
            mat_conc = SapModel.PropMaterial.GetOConcrete_1(mat_name)
            materials[mat_name] = {'type': mat_type, 'fc': mat_conc[0]}
        elif mat_type == 'Steel':
            mat_steel = SapModel.PropMaterial.GetOSteel_1(mat_name)
            materials[mat_name] = {'type': mat_type, 'fy': mat_steel[0], 'fu': mat_steel[1]}
    return materials
```

### 5.2 Crear Materiales (Hormigón)

```python
# Fuente: danielogg92/Etabs-API-Python/Etabs_Set_Functions.py (adaptado para Chile)
def create_concrete_G30(SapModel):
    """Crear hormigón G30 (f'c=30 MPa) según práctica chilena."""
    name = "G30"
    # Agregar material tipo Concrete
    SapModel.PropMaterial.AddMaterial(name, 2, "User", "", "G30", UserName=name)

    # Propiedades del concreto
    SapModel.PropMaterial.SetOConcrete_1(name,
        30.0,       # fc [MPa]
        False,      # isLightweight
        0.0,        # fcsFact
        2,          # SSType (Mander)
        4,          # SSHysType (Takeda)
        0.003,      # strainAtFc
        0.003)      # strainUlt

    # Propiedades isótropas
    Ec = 4700 * (30**0.5)  # = 25,743 MPa
    SapModel.PropMaterial.SetMPIsotropic(name, Ec, 0.2, 10e-6)

    # Peso y masa
    SapModel.PropMaterial.SetWeightAndMass(name, 1, 24.0e-6)  # kN/mm³ → 24 kN/m³
```

### 5.3 Crear Materiales (Acero de Refuerzo)

```python
# Basado en danielogg92 + práctica chilena
def create_rebar_A630(SapModel):
    """Crear acero A630-420H (fy=420 MPa)."""
    name = "A630-420H"
    SapModel.PropMaterial.AddMaterial(name, 6, "User", "", "A630", UserName=name)
    SapModel.PropMaterial.SetORebar_1(name,
        420.0,      # fy [MPa]
        630.0,      # fu [MPa]
        0.002,      # strainAtHardening
        0.09,       # strainUlt
        2,          # SSType
        4,          # SSHysType
        False,      # useCaltrans
        0)          # strainAtFyNeg (= strainAtFy)
    SapModel.PropMaterial.SetMPIsotropic(name, 200000.0, 0.3, 12e-6)
    SapModel.PropMaterial.SetWeightAndMass(name, 1, 77.0e-6)
```

---

## 6. Geometría — Frames, Areas, Points

### 6.1 Obtener Todos los Frames

```python
# Fuente: danielogg92/Etabs-API-Python/Etabs_Get_Functions.py
def get_all_frames(SapModel):
    frame_objs = SapModel.FrameObj.GetAllFrames()
    frames = []
    for i in range(frame_objs[0]):
        frames.append({
            'name':    frame_objs[1][i],
            'prop':    frame_objs[2][i],
            'story':   frame_objs[3][i],
            'pt1':     frame_objs[4][i],
            'pt2':     frame_objs[5][i],
            'x1':      frame_objs[6][i],  'y1': frame_objs[7][i],  'z1': frame_objs[8][i],
            'x2':      frame_objs[9][i],  'y2': frame_objs[10][i], 'z2': frame_objs[11][i],
            'cardPt':  frame_objs[19][i],
        })
    return frames
```

### 6.2 Obtener Puntos de un Área

```python
# Fuente: retug/ETABs/01-Diaphragm Slicer/section_cut_tool.py
# Leer áreas seleccionadas y obtener sus puntos/coordenadas
areas = SapModel.SelectObj.GetSelected()
area_obj = []
for type_obj, obj_name in zip(areas[1], areas[2]):
    if type_obj == 5:   # 5 = Area object
        area_obj.append(obj_name)

PointData = []
for area in area_obj:
    pts = SapModel.AreaObj.GetPoints(area)[1]
    for pnt in pts:
        coords = SapModel.PointObj.GetCoordCartesian(pnt)
        PointData.append((coords[0], coords[1], coords[2]))
```

### 6.3 Crear Secciones de Marco

```python
# Fuente: mihdicaballero/ETABS-Ninja + danielogg92 (adaptado para proyecto)

# Viga invertida 20/60
SapModel.PropFrame.SetRectangle("VI20/60G30", "G30", 0.6, 0.2)
# Modificador de torsión J=0 (práctica chilena)
modifiers = [1, 1, 1, 0.01, 1, 1, 1, 1]  # J ≈ 0
SapModel.PropFrame.SetModifiers("VI20/60G30", modifiers)

# Columna circular (ejemplo de ETABS-Ninja)
def create_circular_section(SapModel, name, mat, diam, cover,
                            n_bars, bar_diam, tie_diam, tie_spacing):
    SapModel.PropFrame.SetCircle(name, mat, diam)
    SapModel.PropFrame.SetRebarColumn(
        name, "A630-420H", "A630-420H",
        2, 1, cover, n_bars, 0, 0,
        bar_diam, tie_diam, tie_spacing, 0, 0, False)
```

### 6.4 Crear Vigas y Asignar Punto Cardinal

```python
# Fuente: danielogg92 + nuestra experiencia
# Cardinal Point para vigas invertidas: Punto 2 (Bottom Center)
ret = SapModel.FrameObj.AddByCoord(x1, y1, z, x2, y2, z, name, "VI20/60G30")
SapModel.FrameObj.SetInsertionPoint(name, 2, False, False, [0,0,0], [0,0,0])
# Cardinal points: 1=BottomLeft, 2=BottomCenter, ..., 8=TopCenter, ..., 11=Centroid
```

### 6.5 Crear Losas con AutoMesh

```python
# Fuente: nuestra experiencia + retug
# Crear losa por coordenadas (4 puntos)
x_coords = [x1, x2, x2, x1]
y_coords = [y1, y1, y2, y2]
z_coords = [z, z, z, z]
ret = SapModel.AreaObj.AddByCoord(4, x_coords, y_coords, z_coords, name, "Losa15G30")

# AutoMesh con tamaño máximo 0.4m (vano mínimo = 0.425m)
SapModel.AreaObj.SetAutoMesh(name, 1, 2, 2, 0, 0, True, False, False, 0.4, 0.4, False, False, False, 0, 0, 0, 0)

# Asignar diafragma
SapModel.AreaObj.SetDiaphragm(name, "D1")

# Modificador de inercia al 25% (práctica chilena)
area_modifiers = [0.25, 0.25, 1, 0.25, 1, 1, 1, 1, 1, 1]
SapModel.AreaObj.SetModifiers(name, area_modifiers)
```

### 6.6 Lock/Unlock del Modelo

```python
# Fuente: retug/ETABs, documentación CSI
# DESBLOQUEAR antes de modificar
SapModel.SetModelIsLocked(False)

# ... hacer modificaciones ...

# El modelo se bloquea automáticamente al correr análisis
# IMPORTANTE: Desbloquear BORRA todos los resultados previos
```

---

## 7. Cargas — Asignación y Patrones

### 7.1 Crear Load Patterns

```python
# Fuente: R01 (etabs_api_reference.md) + repos
# eLoadPatternType: 1=Dead, 2=SuperDead, 3=Live, 5=Quake, 7=Other

# Peso propio (SelfWtMultiplier = 1)
SapModel.LoadPatterns.Add("PP", 1, 1.0)       # Dead, SWM=1

# Terminaciones permanentes (SWM=0, no cuenta peso propio de nuevo)
SapModel.LoadPatterns.Add("TERP", 2, 0.0)     # SuperDead
SapModel.LoadPatterns.Add("TERT", 2, 0.0)     # SuperDead (techo)

# Sobrecargas
SapModel.LoadPatterns.Add("SCP", 3, 0.0)      # Live
SapModel.LoadPatterns.Add("SCT", 3, 0.0)      # Live (techo)
```

### 7.2 Asignar Cargas Uniformes a Áreas

```python
# Fuente: Eng-Tips thread, retug
# Carga uniforme en dirección Z (gravedad)
for area_name in slab_names:
    # Terminación permanente: -200 kgf/m² (negativa = hacia abajo)
    SapModel.AreaObj.SetLoadUniform(area_name, "TERP", -200, 6)  # 6 = dir Z local
    # Sobrecarga: -250 kgf/m²
    SapModel.AreaObj.SetLoadUniform(area_name, "SCP", -250, 6)
```

---

## 8. Análisis — Configuración y Ejecución

### 8.1 Espectro de Respuesta con SetUser (RECOMENDADO)

```python
# Fuente: documentación CSI + ResearchGate (confirmado: SetFromFile no existe en OAPI v19)
# SetUser ES la solución definitiva para espectros programáticos
import numpy as np

# Calcular espectro NCh433+DS61 en Python
T_values = np.arange(0.0, 5.01, 0.01)
Ao, S, To, Tp, n, p = 0.4, 1.05, 0.40, 0.45, 1.40, 1.60
Sa_values = []
for T in T_values:
    if T == 0:
        alpha = 1.0
    else:
        alpha = (1 + 4.5*(T/To)**p) / (1 + (T/To)**3)
    Sa = S * Ao * alpha  # Sa/g
    Sa_values.append(Sa)

# Definir función de espectro en ETABS
ret = SapModel.Func.FuncRS.SetUser(
    "NCh433_Z3_SC",            # Nombre
    len(T_values),              # Número de puntos
    T_values.tolist(),          # Períodos [s]
    Sa_values,                  # Aceleraciones [g]
    0.05                        # Damping ratio (5%)
)
assert ret == 0, f"SetUser falló: {ret}"
```

### 8.2 Casos de Espectro de Respuesta

```python
# Fuente: R01 + stru.ai
# Dirección X
SapModel.LoadCases.ResponseSpectrum.SetCase("SEx")
SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "SEx", 1, ["U1"], ["NCh433_Z3_SC"], [9.81], [""], [0.0])

# Dirección Y
SapModel.LoadCases.ResponseSpectrum.SetCase("SEy")
SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "SEy", 1, ["U2"], ["NCh433_Z3_SC"], [9.81], [""], [0.0])

# SF=9.81 porque espectro está en g y modelo en m/s²
```

### 8.3 Mass Source (NCh433)

```python
# Fuente: documentación CSI + Eng-Tips
# Masa sísmica = PP + 0.25×SCP (Art. 5.5.1 NCh433)
ret = SapModel.PropMaterial.SetMassSource_1(
    True,       # IncludeElements (peso propio)
    False,      # IncludeAddedMass
    True,       # IncludeLoads
    1,          # NumberLoads
    ["SCP"],    # LoadPat
    [0.25]      # sf
)
if ret != 0:
    print("WARN: SetMassSource_1 falló — intentar via Database Tables")
```

**NOTA**: La ruta exacta (`SapModel.PropMaterial.SetMassSource_1` vs `SapModel.MassSource.SetMassSource_1`) debe verificarse en la TLB local.

### 8.4 Combinaciones de Carga (NCh3171)

```python
# Fuente: R01 (etabs_api_reference.md)
combos = {
    "C1": [("PP", 1.4), ("TERP", 1.4)],
    "C2": [("PP", 1.2), ("TERP", 1.2), ("SCP", 1.6)],
    "C3": [("PP", 1.2), ("TERP", 1.2), ("SCP", 1.0), ("SEx", 1.4)],
    "C4": [("PP", 1.2), ("TERP", 1.2), ("SCP", 1.0), ("SEy", 1.4)],
    "C5": [("PP", 0.9), ("TERP", 0.9), ("SEx", 1.4)],
    "C6": [("PP", 0.9), ("TERP", 0.9), ("SEy", 1.4)],
    "C7": [("PP", 1.2), ("TERP", 1.2), ("SCP", 1.6), ("SCT", 0.5)],
}

for combo_name, cases in combos.items():
    SapModel.RespCombo.Add(combo_name, 0)  # 0 = linear add
    for case_name, sf in cases:
        SapModel.RespCombo.SetCaseList(combo_name, 0, case_name, sf)
```

### 8.5 DOF y Análisis

```python
# Fuente: R01 + documentación CSI
# Activar 6 DOF
SapModel.Analyze.SetActiveDOF([True, True, True, True, True, True])

# Correr análisis
ret = SapModel.Analyze.RunAnalysis()
if ret != 0:
    print(f"Análisis falló: {ret}")
```

---

## 9. Resultados — Extracción y Post-Proceso

### 9.1 Story Drifts (via Results API)

```python
# Fuente: youandvern/ETABS_building_drift_check/APItest.py
import pandas as pd

def get_story_drifts(SapModel, combo_name, drift_limit=0.002):
    """Extraer drifts por piso para un combo dado."""
    SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    SapModel.Results.Setup.SetComboSelectedForOutput(combo_name)

    # Inicializar listas vacías (requerido por API)
    NumberResults = 0
    Stories = []; LoadCases = []; StepTypes = []; StepNums = []
    Directions = []; Drifts = []; Labels = []
    Xs = []; Ys = []; Zs = []

    [NumberResults, Stories, LoadCases, StepTypes, StepNums,
     Directions, Drifts, Labels, Xs, Ys, Zs, ret] = \
        SapModel.Results.StoryDrifts(
            NumberResults, Stories, LoadCases, StepTypes, StepNums,
            Directions, Drifts, Labels, Xs, Ys, Zs)

    records = []
    for i in range(NumberResults):
        records.append({
            'Story': Stories[i],
            'Combo': LoadCases[i],
            'Direction': Directions[i],
            'Drift': Drifts[i],
            'DCR': Drifts[i] / drift_limit
        })

    df = pd.DataFrame(records)
    return df.sort_values('Drift', ascending=False)
```

### 9.2 Verificación de Torsión (JointDrifts)

```python
# Fuente: youandvern/ETABS_building_drift_check/APItest.py
def get_torsion_check(SapModel, combo_name):
    """Verificar torsión: ratio max/avg desplazamiento por piso."""
    SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    SapModel.Results.Setup.SetComboSelectedForOutput(combo_name)

    [NumberResults, Stories, Label, Names, LoadCases,
     StepType, StepNum, DispX, DispY, DriftX, DriftY, ret] = \
        SapModel.Results.JointDrifts(0, [], '', '', [], [], [], [], [], [], [])

    records = []
    for i in range(NumberResults):
        records.append({
            'Label': Label[i], 'Story': Stories[i],
            'DispX': DispX[i], 'DispY': DispY[i]
        })

    df = pd.DataFrame(records)

    # Ratio torsión por piso
    torsion = []
    for story in df.Story.unique():
        sdf = df[df.Story == story]
        avg_x = abs(sdf.DispX.mean())
        max_x = sdf.DispX.abs().max()
        ratio = max_x / avg_x if avg_x > 0 else float('inf')
        torsion.append({'Story': story, 'Avg': avg_x, 'Max': max_x, 'Ratio': ratio})

    return pd.DataFrame(torsion)
```

### 9.3 Section Cut Forces

```python
# Fuente: retug/ETABs/01-Diaphragm Slicer
SapModel.Results.Setup.SetCaseSelectedForOutput("SEx")

NumberResults = 0
SCut = []; LoadCase = []; StepType = []; StepNum = []
F1 = []; F2 = []; F3 = []; M1 = []; M2 = []; M3 = []

result = SapModel.Results.SectionCutAnalysis(
    NumberResults, SCut, LoadCase, StepType, StepNum,
    F1, F2, F3, M1, M2, M3)

shear = result[6]    # F1 = corte
moment = result[10]  # M3 = momento
```

### 9.4 Base Reactions

```python
# Fuente: stru.ai + Hakan Keskin
SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
SapModel.Results.Setup.SetCaseSelectedForOutput("SEx")

NumberResults = 0
LoadCase = []; StepType = []; StepNum = []
Fx = []; Fy = []; Fz = []; Mx = []; My = []; Mz = []
gx = 0.0; gy = 0.0; gz = 0.0

result = SapModel.Results.BaseReac(
    NumberResults, LoadCase, StepType, StepNum,
    Fx, Fy, Fz, Mx, My, Mz, gx, gy, gz)

print(f"Corte basal X: {result[4][0]:.1f}")  # Fx
print(f"Corte basal Y: {result[5][0]:.1f}")  # Fy
```

---

## 10. Database Tables API

### 10.1 Listar Tablas Disponibles

```python
# Fuente: danielogg92/Etabs-API-Python/Database_Tables.py
def get_all_tables(SapModel):
    """Listar todas las tablas disponibles en el modelo."""
    table_data = SapModel.DatabaseTables.GetAllTables()
    tables = {}
    for i in range(table_data[0]):
        tables[table_data[1][i]] = {
            'name': table_data[2][i],
            'import_type': table_data[3][i],  # 0=no, 1=importable, 2=interactive
            'is_empty': table_data[4][i]
        }
    return tables
```

### 10.2 Leer Tabla → DataFrame (Patrón Universal)

```python
# Fuente: mihdicaballero/ETABS-Ninja/etabsninja/get_database.py
# TODOS los repos que leen tablas usan este patrón
import pandas as pd

def table_to_dataframe(SapModel, table_key, group_name=""):
    """Leer cualquier tabla de ETABS y convertir a DataFrame."""
    table = SapModel.DatabaseTables.GetTableForDisplayArray(
        table_key, [], table_key, 0, [], 0, [])

    fields = table[2]         # Lista de nombres de columnas
    n = len(fields)           # Número de columnas
    flat_data = table[4]      # Lista plana de datos

    # Reshape: lista plana → filas
    data = [list(flat_data[i:i+n]) for i in range(0, len(flat_data), n)]
    return pd.DataFrame(data, columns=fields)

# Uso:
df_drifts = table_to_dataframe(SapModel, "Story Drifts")
df_forces = table_to_dataframe(SapModel, "Frame Forces - Envelopes")
```

### 10.3 Escribir/Editar Tablas

```python
# Fuente: retug/ETABs (Section Cut Definitions)
# 1. Desbloquear modelo
SapModel.SetModelIsLocked(False)

# 2. Preparar datos
TableKey = 'Section Cut Definitions'
TableVersion = 1
FieldsKeysIncluded = ['Name', 'Defined By', 'Group', 'Result Type', ...]
NumberRecords = len(data_rows)
TableData = [...]  # Lista plana de valores

# 3. Escribir
SapModel.DatabaseTables.SetTableForEditingArray(
    TableKey, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

# 4. Aplicar cambios
SapModel.DatabaseTables.ApplyEditedTables(FillImport=True)
```

### 10.4 Story Drifts via Database Tables (alternativa)

```python
# Fuente: mihdicaballero/ETABS-Ninja
# Ventaja: más flexible que Results API, permite filtrar por load case
SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(["SEx", "SEy"])

table_name = "Story Drifts"
fields = SapModel.DatabaseTables.GetAllFieldsInTable(table_name)[2]
data = SapModel.DatabaseTables.GetTableForDisplayArray(table_name, fields, "All")

# Reshape
cols = data[2]
n = len(cols)
flat = data[4]
rows = [flat[i:i+n] for i in range(0, len(flat), n)]
df = pd.DataFrame(rows, columns=cols)
df['Drift'] = df['Drift'].astype(float)

# Agrupar por piso y dirección, obtener máximo
result = df.groupby(['Story', 'Direction'])['Drift'].max()
```

---

## 11. Diferencias entre Versiones

### 11.1 Resumen de Compatibilidad

| Versión | Cambio API clave |
|---------|------------------|
| **v17 y anterior** | ProgID `ETABSv17.Helper`. **NO compatible** con v18+ |
| **v18** | API forward-compatible introducida. ProgID `ETABSv1.Helper`. CSiAPIv1.DLL |
| **v19** | Mejoras varias. `get_story_data()` frecuentemente falla (bug). Es nuestra versión |
| **v20** | `Get/SetNumberModes` actualizado. Cambios en Database Table names |
| **v21** | `GetTee_1`/`SetTee_1` actualizados (radio filete) |
| **v22** | ETABSv1.dll → .NET Standard 2.0. Soporte .NET 8 plugins |

### 11.2 Regla de Oro

**Código escrito para v18 funciona en v19, v20, v21, v22** sin recompilar.
Esto aplica cross-product: ETABS v18+ ≡ SAP2000 v21+ ≡ CSiBridge v21+ ≡ SAFE v20+.

### 11.3 Precauciones

- **Database Table names** pueden cambiar entre versiones (v19→v20 confirmado)
- Siempre verificar con `GetAvailableTables()` antes de leer una tabla
- **FuncRS.SetFromFile** no existe en OAPI v19 (confirmado por ResearchGate 2023)
- **FuncRS.SetUser** SÍ funciona en v18+ — es la solución

---

## 12. Bugs Conocidos y Workarounds

### 12.1 Tabla Resumen

| Bug | Severidad | Workaround |
|-----|-----------|------------|
| CreateObject → instancia INVISIBLE | Alta | Abrir ETABS manualmente, usar GetActiveObject |
| File.Save → .edb CORRUPTO sin UI | Alta | Abrir ETABS manual → File > New > Blank → scripts |
| comtypes.gen cache stale | Media | Limpiar gen/ antes de import (ver §2.4) |
| RPC -2147023174 (sesión muerta) | Alta | Separar pipeline en fases COM independientes |
| SetFromFile no existe en OAPI | Media | Usar SetUser con arrays calculados en Python |
| get_story_data() falla en v19 | Baja | No abortar, usar NewGridOnly para stories |
| SetMassSource_1 solo modifica default | Baja | Database Tables API como alternativa |

### 12.2 Recuperación de .edb Corruptos

```
Opciones (de wiki.csiamerica.com):
1. El archivo .$et se crea cada vez que se guarda → puede reimportarse
2. El archivo .ebk es backup del último archivo abierto
3. Exportar a .e2k y reimportar puede arreglar corrupciones
```

---

## 13. Best Practices y Performance

### 13.1 Orden de Operaciones Recomendado (CSI)

```
1. Conectar a ETABS (preferir GetActiveObject)
2. Desbloquear modelo: SetModelIsLocked(False)
3. Definir materiales y secciones
4. Crear geometría (grids, stories, frames, areas)
5. Asignar propiedades (diafragma, mesh, releases)
6. Definir cargas (load patterns, load cases)
7. Definir combinaciones
8. Guardar: SapModel.File.Save(path)
9. Correr análisis: SapModel.Analyze.RunAnalysis()
10. Extraer resultados
11. Guardar y cerrar
```

### 13.2 Constantes de Unidades Verificadas

| Valor | Unidades | Repos que lo usan |
|-------|----------|-------------------|
| 3 | kip_in_F | ETABS-Ninja |
| 4 | kip_ft_F | retug |
| 5 | kN_mm_C | danielogg92 |
| **6** | **kN_m_C** | **danielogg92 (nuestro caso)** |
| 9 | N_mm_C | danielogg92 |
| 10 | N_m_C | danielogg92 |

### 13.3 Performance Tips

```python
# 1. Database Tables para operaciones masivas (más rápido que API individual)
table_key = "Frame Assignments - Section Properties"
ret = SapModel.DatabaseTables.GetTableForEditingArray(table_key, "")
# ... modificar ...
SapModel.DatabaseTables.SetTableForEditingArray(...)
SapModel.DatabaseTables.ApplyEditedTables(True)

# 2. RefreshView UNA sola vez al final (no después de cada elemento)
for wall in walls:
    SapModel.AreaObj.AddByCoord(...)
SapModel.View.RefreshView(0, False)  # Solo al final

# 3. Lock/Unlock conscientemente
SapModel.SetModelIsLocked(False)  # BORRA resultados previos
```

### 13.4 Thread Safety

**La API es COM STA (Single-Threaded Apartment) → NO thread-safe.**
Para paralelismo: usar procesos separados, cada uno con su instancia ETABS y sesión COM.

### 13.5 Productividad Reportada (fuentes múltiples)

- Ahorro ~40% tiempo en tareas repetitivas
- Productividad 2-3x con operaciones batch
- Reducción ~60% errores en configuración de análisis sísmico

---

## 14. Aplicación a Nuestro Pipeline

### 14.1 Stack Confirmado

```bash
pip install comtypes    # v1.1.7+ — BASE
# Opcional:
pip install etabs-api   # Wrapper alto nivel (evaluar si simplifica)
pip install pandas      # Para post-proceso de resultados
pip install numpy       # Para cálculo de espectro
```

### 14.2 Decisiones de Diseño Confirmadas por la Comunidad

| Decisión | Justificación |
|----------|---------------|
| **GetActiveObject como método principal** | Todos los repos lo usan. Evita instancias invisibles y .edb corruptos |
| **SetUser en vez de SetFromFile** | SetFromFile no existe en OAPI v19. SetUser funciona 100% en v18+ |
| **Separar pipeline en fases COM** | Validado por docs CSI y nuestra experiencia (RPC error tras geometría pesada) |
| **Database Tables para resultados masivos** | Más rápido y flexible que Results API |
| **comtypes.gen cleanup** | Bug real (issue #182 comtypes). Ningún otro repo lo necesita → puede ser específico de nuestro lab |
| **J=0 en vigas** | Práctica chilena confirmada por Material Apoyo Taller |
| **Inercia losa 25%** | Práctica chilena confirmada por Lafontaine |
| **AutoMesh 0.4m** | Menor que vano mínimo 0.425m |

### 14.3 Workflow Recomendado para Lab

```
1. Kill ETABS en Task Manager (si hay fantasma)
2. Abrir ETABS v19 manualmente
3. File > New Model > Blank
4. python clean_comtypes_gen.py  (solo si hay errores previos)
5. python run_all.py --fase 1    (geometría, sesión COM fresca)
6. [ETABS guarda y cierra automáticamente]
7. Abrir ETABS v19 manualmente de nuevo
8. python run_all.py --fase 2    (análisis, sesión COM fresca)
9. Verificar resultados en ETABS UI
```

### 14.4 Verificaciones Esperadas

| Métrica | Valor esperado |
|---------|----------------|
| T1 (período fundamental) | ~1.0–1.3 s |
| Peso total | ~9,368 tonf (468 m² × 20p × 1 t/m²) |
| Drift máximo | < 0.002 |
| Qmín (corte basal mínimo) | 655 tonf (0.07 × 1 × 9,368) |

---

## 15. Fuentes Completas

### Repositorios GitHub
- [danielogg92/Etabs-API-Python](https://github.com/danielogg92/Etabs-API-Python) — 67★, MIT, funciones wrapper
- [mitchell-tesch/CSiPy](https://github.com/mitchell-tesch/CSiPy) — 38★, MIT, .NET wrapper OOP
- [youandvern/ETABS_building_drift_check](https://github.com/youandvern/ETABS_building_drift_check) — 21★, drift+torsión GUI
- [retug/ETABs](https://github.com/retug/ETABs) — 19★, MIT, diaphragm slicer
- [mihdicaballero/ETABS-Ninja](https://github.com/mihdicaballero/ETABS-Ninja) — 14★, MIT, drift DB Tables
- [ebrahimraeyat/etabs_api](https://github.com/ebrahimraeyat/etabs_api) — LGPL, paquete PyPI
- [jantozor/CSiAPIExamples](https://github.com/jantozor/CSiAPIExamples) — ejemplos oficiales CSI

### Paquetes PyPI
- [comtypes](https://pypi.org/project/comtypes/) — COM automation base
- [etabs-api](https://pypi.org/project/etabs-api/) — wrapper alto nivel
- [pytabs](https://pypi.org/project/pytabs/) — .NET API wrapper

### Tutoriales y Blogs
- [Stru.ai — ETABS API Beginner Guide 2025](https://stru.ai/blog/etabs-api-beginner-guide)
- [Stru.ai — ETABS Seismic Automation](https://stru.ai/blog/etabs-seismic-automation)
- [Hakan Keskin — CSI API Tool](https://hakan-keskin.medium.com/csi-api-tool-python-integration-with-etabs-sap2000-and-safe-516f60a19e6c)
- [Hakan Keskin — Story Drifts](https://hakan-keskin.medium.com/extracting-story-drifts-and-joint-displacements-in-etabs-with-python-6b886aac89ba)
- [Hakan Keskin — Pushover](https://hakan-keskin.medium.com/pushover-analysis-in-etabs-with-python-extracting-and-filtering-hinge-results-bd7b3ed64f20)
- [NeutralAXIS — Getting Started](https://neutralaxis.github.io/ETABS/ETABS%20API/Getting_Started/)
- [Re-Tug — Database Tables](https://re-tug.com/post/etabs-api-more-examples-database-tables/18)
- [VIKTOR.ai — ETABS Integration](https://docs.viktor.ai/docs/tutorials/integrate-etabs-sap2000/)
- [EngineeringSkills — Intro ETABS Python API](https://www.engineeringskills.com/posts/an-introduction-to-the-etabs-python-api)
- [Fabriccio Livia — LinkedIn](https://www.linkedin.com/pulse/etabs-automation-building-models-python-fabriccio-livia-saenz-rsxwe)
- [CSI Official Python Example](http://docs.csiamerica.com/help-files/common-api(from-sap-and-csibridge)/Example_Code/Example_7_(Python).htm)

### Documentación Oficial CSI
- [Developer Portal](https://www.csiamerica.com/developer)
- [API Help 2016](https://docs.csiamerica.com/help-files/etabs-api-2016/)
- [OAPI Wiki](https://wiki.csiamerica.com/display/kb/OAPI)
- [OAPI FAQ](https://wiki.csiamerica.com/display/kb/OAPI+FAQ)
- [Plugins Wiki](https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2012754/Plugins)

### Foros
- [Eng-Tips — Error attaching Python](https://www.eng-tips.com/threads/error-when-getting-python-to-attach-to-etabs.477451/)
- [Eng-Tips — ETABS v18 Cannot attach](https://www.eng-tips.com/threads/etabs-v18-api-cannot-attach-python-with-etabs.477710/)
- [Eng-Tips — Section Cut Definition v19→v20](https://www.eng-tips.com/threads/etabs-api-troubles-section-cut-definition.502839/)
- [Eng-Tips — Mass Source API](https://www.eng-tips.com/threads/etabs-api-add-new-mass-source.521909/)
- [Eng-Tips — FrameObj.GetSection](https://www.eng-tips.com/threads/etabs-api-frameobj-getsection.477453/)

### Release Notes ETABS
- [v19.0.0](http://installs.csiamerica.com/software/ETABS/19/ReleaseNotesETABSv1900.pdf)
- [v20.0.0](https://www.csiamerica.com/software/ETABS/20/ReleaseNotesETABSv2000.pdf)
- [v21.0.0](https://www.csiamerica.com/software/ETABS/21/ReleaseNotesETABSv2100.pdf)
- [v22.0.0](https://www.csiamerica.com/software/ETABS/22/ReleaseNotesETABSv2200.pdf)
