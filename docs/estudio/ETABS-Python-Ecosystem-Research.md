# ETABS + Python Ecosystem: Paquetes, Tutoriales y Recursos

> Investigacion realizada el 20 marzo 2026. Cubre PyPI, GitHub, blogs, foros y documentacion oficial.

---

## PARTE 1 -- Paquetes PyPI

### 1.1 pytabs (recomendado si usas .NET API)

| Campo | Detalle |
|-------|---------|
| **Nombre** | pytabs |
| **PyPI** | https://pypi.org/project/pytabs/ |
| **GitHub** | https://github.com/mitchell-tesch/pytabs |
| **Autor** | Mitchell Tesch |
| **Licencia** | MIT |
| **Python** | >= 3.10 |
| **Dependencia clave** | `pythonnet` (NO comtypes) |
| **Install** | `pip install pytabs` |
| **Docs** | https://mitchell-tesch.github.io/pytabs/pytabs.html |

**Que hace**: Wrapper Python para la **API .NET** de CSI ETABS (ETABSv1.dll). Provee IntelliSense via stub file generado con IronPython Stubs. Interface Pythonica sobre el namespace ETABSv1.

**Diferencia clave**: Usa `pythonnet` (CLR/.NET interop), NO `comtypes` (COM interop). Esto significa que trabaja con la DLL .NET directamente en vez del COM object.

**Proyecto relacionado**: El mismo autor creo [CSiPy](https://github.com/mitchell-tesch/CSiPy), un wrapper mas generico para la CSi .NET API (soporta ETABS, SAP2000, CSiBridge).

---

### 1.2 etabs-api

| Campo | Detalle |
|-------|---------|
| **Nombre** | etabs-api |
| **PyPI** | https://pypi.org/project/etabs-api/ |
| **GitHub** | https://github.com/ebrahimraeyat/etabs_api |
| **Autor** | Ebrahim Raeyat Roknabadi |
| **Licencia** | LGPL |
| **Dependencias** | comtypes |
| **Install** | `pip install etabs-api` |

**Que hace**: Paquete Python para comunicarse con CSI ETABS 2018+ y CSI SAFE. Usa comtypes como backend COM. Incluye modulos para:
- `frame_obj.py` -- manipulacion de frames
- `area.py` -- manipulacion de areas
- `database.py` -- acceso a database tables
- Y mas modulos especializados

**Ecosistema del autor**:
- [civilTools](https://github.com/ebrahimraeyat/civilTools) -- Herramientas de ingenieria civil (coeficiente sismico codigo iraniano, secciones de acero)
- [OSAFE](https://github.com/ebrahimraeyat/OSAFE) -- Workbench FreeCAD para crear fundaciones en CSI SAFE desde modelos ETABS
- Soporta punching shear segun ACI 318-19

---

### 1.3 etabs (paquete basico)

| Campo | Detalle |
|-------|---------|
| **PyPI** | https://pypi.org/project/etabs/ |
| **Estado** | Paquete simple/minimal |

Paquete basico disponible en PyPI. Menos documentado que los anteriores.

---

### 1.4 comtypes (la base de todo COM)

| Campo | Detalle |
|-------|---------|
| **Nombre** | comtypes |
| **PyPI** | https://pypi.org/project/comtypes/ |
| **Version recomendada** | 1.1.7 (estable para ETABS) |
| **Install** | `pip install comtypes` |
| **Licencia** | MIT |

**Que hace**: Biblioteca Python para COM automation en Windows. Es la **base fundamental** de casi toda la automatizacion ETABS/SAP2000 con Python. Provee:
- `comtypes.client.GetActiveObject()` -- conectar a instancia activa
- `comtypes.client.CreateObject()` -- crear nueva instancia
- Type library generation automatica (carpeta `comtypes.gen/`)

**ADVERTENCIA (de nuestra experiencia)**:
- Version 1.1.7 es la mas estable para ETABS v19
- Limpiar `comtypes.gen/` antes de reconectar si hay errores de binding
- `CreateObject()` puede lanzar instancias INVISIBLES
- `GetActiveObject()` falla si ETABS no esta abierto

---

### 1.5 Sap2000py

| Campo | Detalle |
|-------|---------|
| **Nombre** | Sap2000py |
| **PyPI** | https://pypi.org/project/Sap2000py/ |
| **Version** | 0.1.6 (8 abril 2025) |
| **Autor** | Lingyun Gou |
| **Python** | >= 3.9 |
| **Licencia** | GPL |
| **OS** | Solo Windows |
| **Install** | `pip install Sap2000py` |

**Que hace**: Interface Python para SAP2000 API. Incluye demos de puente continuo. Estado: Beta. La API SAP2000 es practicamente identica a la de ETABS (misma familia CSI OAPI), asi que patrones de codigo son transferibles.

---

### 1.6 sap2000 (kandluis)

| Campo | Detalle |
|-------|---------|
| **PyPI** | https://pypi.org/project/sap2000/ |
| **GitHub** | https://github.com/kandluis/sap2000 |

Wrapper Python para SAP2000 con modulo `elements.py` para manipulacion de elementos estructurales.

---

### 1.7 ak_sap

| Campo | Detalle |
|-------|---------|
| **GitHub** | https://github.com/rpakishore/ak_sap |
| **Autor** | Arun Kishore |
| **Licencia** | GPLv3 |
| **Install** | Via GitHub (no en PyPI) |

**Que hace**: Wrapper Python completo para SAP2000. Permite generar, analizar y extraer modelos estructurales complejos. Features:
- Attach a modelo existente o crear nuevo
- Control de visibilidad de ventana SAP2000
- Modulos: Model (control global), Object (puntos, frames)
- Modal analysis y response spectrum setup

**Codigo ejemplo**:
```python
from ak_sap import debug, Sap2000Wrapper
# Attach to existing or create new model
```

---

### 1.8 openseespy

| Campo | Detalle |
|-------|---------|
| **Nombre** | openseespy |
| **PyPI** | https://pypi.org/project/openseespy/ |
| **Docs** | https://openseespydoc.readthedocs.io/ |
| **Install** | `pip install openseespy` |
| **Plataformas** | Windows, Linux, Mac |

**Que hace**: Interprete Python para OpenSees (framework de analisis no-lineal de estructuras). Meta-package que instala el paquete correcto para tu OS. Desde 2018 integra Python como interprete junto a TCL.

**Paquetes complementarios**:
- `opensees` -- https://pypi.org/project/opensees/ (version alternativa)
- `opseestools` -- Streamline workflows, integra Pandas/NumPy/joblib
- `opstool` -- Pre/post-procesamiento y visualizacion avanzada

---

### 1.9 Otros paquetes de ingenieria estructural

| Paquete | PyPI | Descripcion |
|---------|------|-------------|
| **PyNiteFEA** | https://pypi.org/project/PyNiteFEA/ | FEA 3D elastico de vigas, marcos y armaduras |
| **anastruct** | https://pypi.org/project/anastruct/ | Analisis 2D de marcos y armaduras (FEM) con no-linealidad |
| **pycivil** | https://pypi.org/project/pycivil/ | Libreria para ingenieros estructurales, independiente de software comercial |
| **strupy** | https://pypi.org/project/strupy/ | Paquete de diseno estructural |
| **PyCBA** | (PyPI) | Analisis elastico lineal rapido de configuraciones de vigas |

---

## PARTE 2 -- Tutoriales y Blog Posts

### 2.1 EngineeringSkills.com -- Introduccion a ETABS Python API

| Campo | Detalle |
|-------|---------|
| **Titulo** | An Introduction to the ETABS Python API |
| **URL** | https://www.engineeringskills.com/posts/an-introduction-to-the-etabs-python-api |
| **Autor** | Hakan Keskin |

**Contenido**:
- Lanzar y conectar a modelo ETABS existente via Python
- Correr analisis estructural programaticamente
- Extraer resultados de analisis (fuerzas internas columnas/vigas bajo multiples combos)
- Automatizar tareas repetitivas

**Patron de conexion mostrado**:
```python
import comtypes.client
try:
    EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
except (OSError, comtypes.COMError):
    print("No running instance found")
    sys.exit(-1)
SapModel = EtabsObject.SapModel
```

---

### 2.2 Stru.ai Blog -- Serie completa ETABS API

Stru.ai tiene la coleccion mas extensa de tutoriales ETABS+Python. Articulos clave:

| Titulo | URL | Tema |
|--------|-----|------|
| ETABS API Beginner Guide 2025 | https://stru.ai/blog/etabs-api-beginner-guide | Setup, COM, primer script |
| Master the ETABS API 2025 | https://stru.ai/blog/etabs-api-automation-2025 | Automatizacion avanzada |
| Automate ETABS Analysis with Python | https://stru.ai/blog/automate-etabs-analysis-python | Correr analisis, extraer resultados |
| Automate ETABS Post-Processing | https://stru.ai/blog/etabs-post-processing-automation | Post-proceso, reportes |
| Automate Structural Design Tasks | https://stru.ai/blog/automate-structural-design-python-etabs | Workflow diseno |
| Master ETABS Seismic Analysis Automation | https://stru.ai/blog/etabs-seismic-automation | Espectro, drift, masa modal |
| Mastering ETABS Seismic Automation | https://stru.ai/blog/automate-etabs-seismic-python | Analisis sismico completo |
| Automate Steel Connection Design | https://stru.ai/blog/automate-steel-connection-etabs | Conexiones acero |
| Automate ETABS Post-Processing (How To) | https://stru.ai/blog/automate-etabs-post-processing | Paso a paso |
| SAP2000 Python API Automation | https://stru.ai/blog/automate-sap2000-with-python | SAP2000 (misma API) |

**Conceptos clave cubiertos**:
- COM interface via comtypes
- SapModel como objeto central
- APIs: Model, FrameObj, AreaObj, PropFrame, Results
- Workflow: Connect -> Access Model -> Request Results -> Process Data -> Export
- Response spectrum automation (evitar input manual)
- Story drift extraction y verificacion contra limites de codigo
- Mass participation modal (>= 90%)
- Reduccion de errores en 60%, productividad 2-3x

**Datos utiles**:
- `SapModel.Results.StoryForces` para fuerzas de piso
- `SapModel.SetPresentUnits(x)` para cambiar unidades
- Verificar drift: Display > Show Tables > Analysis Results > Story Drifts

---

### 2.3 Hakan Keskin -- Serie Medium (ETABS + SAP2000)

Hakan Keskin es probablemente el autor mas prolifico de contenido ETABS+Python. Sus articulos:

| Titulo | URL |
|--------|-----|
| CSI API Tool: Python Integration with ETABS, SAP2000, and SAFE | https://hakan-keskin.medium.com/csi-api-tool-python-integration-with-etabs-sap2000-and-safe-516f60a19e6c |
| Extracting Story Drifts and Joint Displacements in ETABS | https://hakan-keskin.medium.com/extracting-story-drifts-and-joint-displacements-in-etabs-with-python-6b886aac89ba |
| Extracting Modal Analysis Results and Base Reactions | https://hakan-keskin.medium.com/extracting-modal-analysis-results-and-base-reactions-in-etabs-with-python-af12da00ca5f |
| Extracting Element Forces, Base Reactions, and 3D Geometry | https://hakan-keskin.medium.com/extracting-element-forces-base-reactions-and-3d-geometry-from-etabs-with-python-cd1e41696d78 |
| Pushover Analysis: Extracting and Filtering Hinge Results | https://hakan-keskin.medium.com/pushover-analysis-in-etabs-with-python-extracting-and-filtering-hinge-results-bd7b3ed64f20 |
| Time History Function Definition in ETABS Using API | https://hakan-keskin.medium.com/time-history-function-definition-in-etabs-using-the-api-d9e0a7b2ac28 |
| Automating SAP2000 Analysis with Python & CSI OAPI | https://hakan-keskin.medium.com/automating-structural-analysis-in-sap2000-with-python-csi-oapi-530d1da7f3bd |
| SAP2000: Extracting Internal Forces for Load Cases | https://hakan-keskin.medium.com/automating-sap2000-analysis-with-python-extracting-selected-elements-internal-forces-for-load-13fe8477e157 |
| AI Assistant Integration in ETABS API Tool | https://hakan-keskin.medium.com/enhancing-structural-engineering-workflows-with-ai-integrating-an-offline-ai-assistant-in-etabs-e35be2be7317 |

**CSI API Tool (su proyecto principal)**:
- App desktop con PyQt5
- GUI con stacked layouts y tab containers
- Soporta ETABS, SAP2000, SAFE en un solo entorno modular
- Backend comtypes para COM
- Reciente: chat AI offline integrado para scripting assistance

---

### 2.4 NeutralAXIS -- Getting Started ETABS API

| Campo | Detalle |
|-------|---------|
| **URL Intro** | https://neutralaxis.github.io/ETABS/ETABS%20API/Introduction/ |
| **URL Getting Started** | https://neutralaxis.github.io/ETABS/ETABS%20API/Getting_Started/ |
| **URL Units** | https://neutralaxis.github.io/ETABS/ETABS%20API/Set_or_Change_Units/ |

**Contenido**:
- 3 opciones de conexion:
  1. Automatic Launch (Helper crea ETABS automaticamente)
  2. Launch from specific path
  3. Connect to running instance
- Troubleshooting `ModuleNotFoundError: No module named 'comtypes.client'`
- Configuracion de unidades via API

---

### 2.5 Re-Tug (Austin Guter) -- Database Tables y Diaphragm Slicer

| Titulo | URL |
|--------|-----|
| ETABs API - More Examples (Database Tables) | https://re-tug.com/post/etabs-api-more-examples-database-tables/18 |
| Diaphragm Slicer - ETABs API | https://re-tug.com/post/diaphragm-slicer-etabs-api/8 |
| SAP2000 API Example | https://www.re-tug.com/post/sap2000-api-example/61 |

**GitHub**: https://github.com/retug/ETABs

**Patrones de codigo clave**:
```python
# Listar todas las tablas disponibles
SapModel.DatabaseTables.GetAvailableTables(NumberTables, TableKey, TableName, ImportType)

# Get/Set load cases para display
SapModel.DatabaseTables.GetLoadCasesSelectedForDisplay()
SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay()

# Cambiar unidades de resultados
SapModel.SetPresentUnits(x)
```

---

### 2.6 VIKTOR.ai -- Platform + Tutoriales

| Titulo | URL |
|--------|-----|
| How to use Python to automate SAP2000 | https://www.viktor.ai/blog/174/python-to-automate-sap2000 |
| 6 Ways to improve SAP2000 and ETABS workflows | https://www.viktor.ai/blog/175/6-ways-to-improve-sap2000-etabs-workflows |
| Integrate ETABS and SAP2000 Tutorial | https://docs.viktor.ai/docs/tutorials/integrate-etabs-sap2000/ |
| Automate frame section creation with Python and Excel | https://www.viktor.ai/blog/180/automate-frame-section-creation-in-sap-2000-using-python-and-excel |
| Export and Visualize ETABS Model Results | https://www.viktor.ai/blog/179/easily-export-and-visualize-etabs-model-results |
| Automate ETABS Post-Processing with AI and Python | https://www.viktor.ai/blog/200/etabs-model-post-processing-ai-python |
| ETABS/SAP2000 Software Integration Docs | https://docs.viktor.ai/docs/create-apps/software-integrations/etabs-and-sap2000/ |

**Que es VIKTOR**: Plataforma low-code para crear web apps con Python. Tiene wrapper propio para CSI API que simplifica extraccion de resultados de tablas.

**Requisitos**: `pip install pywin32 comtypes`

**Enfoque**: Aplicaciones parametricas -- defines dimensiones, materiales, secciones, cargas como parametros y la app genera el modelo automaticamente.

---

### 2.7 Fabriccio Livia Saenz -- LinkedIn (Modelacion Parametrica)

| Campo | Detalle |
|-------|---------|
| **Titulo** | Etabs Automation: Building Models with Python |
| **URL** | https://www.linkedin.com/pulse/etabs-automation-building-models-python-fabriccio-livia-saenz-rsxwe |
| **Fecha** | 9 marzo 2024 |

**Contenido**: Tutorial paso a paso para crear modelo de edificio de 50 pisos:
- Piso 1: h=4m, pisos tipo: h=3m
- 3 ejes verticales (A,B,C) x 3 horizontales (1,2,3) a 3.5m
- Conexion a ETABS, config modelo, grids, frames, columnas, losas

---

### 2.8 PythonForStructuralEngineers.com -- Curso ETABS Automation

| Campo | Detalle |
|-------|---------|
| **URL** | https://pythonforstructuralengineers.com/etabs-automation/ |
| **Tipo** | Curso pago |

**Contenido**: Curso completo "ETABS AUTOMATION WITH PYTHON". Ensena a controlar ETABS con scripts simples, extraer/procesar datos, actualizar modelos, escribir scripts reutilizables cross-project.

**Instructor**: Ingeniero estructural con experiencia en Ramboll High Rise, BIG (Bjarke Ingels Group), City Wave Milan, the Orb at Burning Man.

---

### 2.9 Kinson.io -- Plugin ETABS/SAP2000

| Campo | Detalle |
|-------|---------|
| **URL** | https://kinson.io/posts/etabs-plugin-quickstart |
| **GitHub** | https://github.com/jchatkinson/ETABS-plugin-starter-kit |
| **Autor** | Jeremy Atkinson |

**Contenido**: Starter kit para crear plugins compilados para ETABS/SAP2000 usando CSI oAPI. Boilerplate listo para clonar. Clase `cPlugin` con `Main()` que recibe `cSapModel` y `cPluginCallback`.

---

### 2.10 CSI America -- Documentacion Oficial

| Campo | Detalle |
|-------|---------|
| **Developer Page** | https://www.csiamerica.com/developer |
| **API Page** | https://www.csiamerica.com/application-programming-interface |
| **OAPI Wiki** | https://wiki.csiamerica.com/display/kb/OAPI |
| **Python Example** | http://docs.csiamerica.com/help-files/common-api(from-sap-and-csibridge)/Example_Code/Example_7_(Python).htm |
| **ETABS API 2016 Python** | http://docs.csiamerica.com/help-files/etabs-api-2016/html/28e07341-b3ce-4425-aa5d-6abc0b37dd19.htm |

**Contenido**:
- API disponible para: ETABS, SAP2000, CSiBridge, SAFE
- Lenguajes soportados: VBA, VB.NET, C#, C++, Visual Fortran, Python, MATLAB
- Help file: `CSI_OAPI_Documentation.chm` (en directorio de instalacion SAP2000)
- Ejemplo Python 7: Basado en problema de verificacion Example 1-001, crea modelo desde cero, corre analisis, extrae resultados, compara con valores manuales
- Requiere Python 3.4+ y comtypes

**GitHub oficial examples**: https://github.com/jantozor/CSiAPIExamples
- Ejemplos para cada lenguaje
- Cubre ETABS, SAP2000, CSiBridge, SAFE
- Simples y didacticos para entender el workflow

---

### 2.10 Udemy -- Curso ETABS/SAP2000 OAPI (turco)

| Campo | Detalle |
|-------|---------|
| **URL** | https://www.udemy.com/course/python-ile-sfrdan-etabs-sap2000-oapi/ |
| **Titulo** | Python ile Sifirdan ETABS/SAP2000 OAPI |

Curso pago en Udemy cubriendo OAPI desde cero con Python.

---

## PARTE 3 -- GitHub Repositories Relevantes

### 3.1 Repositorios especificos ETABS

| Repo | URL | Descripcion |
|------|-----|-------------|
| **Etabs-API-Python** (danielogg92) | https://github.com/danielogg92/Etabs-API-Python | Funciones faciles para CSI ETABS API. `Main.py`, `Etabs_Get_Functions.py`, `Etabs_Set_Functions.py`. Enfoque Australian Standards. |
| **ETABS-Ninja** (mihdicaballero) | https://github.com/mihdicaballero/ETABS-Ninja | Coleccion de scripts: extraccion de propiedades, fuerzas, desplazamientos, reacciones. Genera presentaciones/reportes/graficos. |
| **etabs_api** (ebrahimraeyat) | https://github.com/ebrahimraeyat/etabs_api | API para ETABS 2018+ y SAFE. Modulos frame_obj, area, database. Base del paquete PyPI etabs-api. |
| **ETABs** (retug) | https://github.com/retug/ETABs | Scripts para Database Tables, time history. Blog companion. |
| **etabs_python_modelling** (mtavares51) | https://github.com/mtavares51/etabs_python_modelling | Modelacion parametrica de estructuras con ETABS API y Python. |
| **CSi-API** (pichosan) | https://github.com/pichosan/CSi-API | ETABS & SAP2000 scripts. |
| **CSiAPIExamples** (jantozor) | https://github.com/jantozor/CSiAPIExamples | Ejemplos oficiales multi-lenguaje para ETABS, SAP2000, CSiBridge, SAFE. |
| **ETABS-plugin-starter-kit** (jchatkinson) | https://github.com/jchatkinson/ETABS-plugin-starter-kit | Boilerplate para plugins compilados. |
| **SAP2000-python-optimization** (marco-rosso-m) | https://github.com/marco-rosso-m/SAP2000-python-for-structural-optimization | Optimizacion estructural con SAP2000 + pymoo (genetic algorithm). |

### 3.2 GitHub Topic: `etabs`

URL: https://github.com/topics/etabs -- Pagina central con todos los repos taggeados.

---

## PARTE 4 -- Foros (Eng-Tips & Stack Overflow)

### 4.1 Eng-Tips -- Threads ETABS API

Stack Overflow tiene muy poco contenido sobre ETABS API. **Eng-Tips es el foro principal** para discusiones tecnicas.

| Titulo | URL | Tema clave |
|--------|-----|------------|
| Error when getting Python to attach to ETABS | https://www.eng-tips.com/threads/error-when-getting-python-to-attach-to-etabs.477451/ | comtypes version issues, AttributeError |
| ETABS v18 API - Cannot attach python with etabs | https://www.eng-tips.com/threads/etabs-v18-api-cannot-attach-python-with-etabs.477710/ | Fix: cambiar de PyCharm a Anaconda, limpiar comtypes.gen |
| ETABs API - FrameObj.GetSection | https://www.eng-tips.com/threads/etabs-api-frameobj-getsection.477453/ | Obtener propiedades de seccion |
| ETABS API - GetGridSys_2 | https://www.eng-tips.com/threads/etabs-api-getgridsys_2.478021/ | Dibujar grids via API |
| Etabs API with Python (student) | https://www.eng-tips.com/threads/etabs-api-with-python.492251/ | Asignar cargas a area objects |
| ETABs API Troubles - Section Cut Definition | https://www.eng-tips.com/threads/etabs-api-troubles-section-cut-definition.502839/ | Codigo que funcionaba en v19 no funciona en v20 |
| ETABS API add new mass source | https://www.eng-tips.com/threads/etabs-api-add-new-mass-source.521909/ | MassSource via API |
| ETABS API Python "Analysis Result" | https://www.eng-tips.com/threads/etabs-api-python-quot-analysis-result-quot.514827/ | Extraccion de resultados |
| ETABS API - extract concrete frame quantities | https://www.eng-tips.com/threads/etabs-api-need-some-help-for-extract-concrete-frame-quantties-volume.468589/ | Volumenes de hormigon |
| ETABS (22) API Section Cut Forces | https://www.eng-tips.com/threads/etabs-22-api-section-cut-forces.526157/ | Section cuts en v22 |
| SAP2000 OAPI | https://www.eng-tips.com/threads/sap2000-oapi.516723/ | Discusion general SAP2000 API |

### 4.2 Soluciones y patrones clave de los foros

**Problema: comtypes version incompatible**
- Solucion: Usar comtypes 1.1.7. Versiones anteriores (1.1.2) requerian modificar `__init__.py`
- comtypes 1.1.8+ puede funcionar pero verificar

**Problema: No se puede conectar a ETABS**
- Solucion 1: Verificar ETABS esta abierto y con modelo cargado
- Solucion 2: Limpiar `comtypes.gen/` y reconectar
- Solucion 3: Cambiar IDE (PyCharm -> Anaconda/VS Code)
- Solucion 4: Verificar que el ProgID sea correcto para tu version

**Problema: Codigo funciona en v19 pero no en v20+**
- Causa: Cambios en database table definitions entre versiones
- Solucion: Verificar nombres de tablas con `GetAvailableTables()`

**Problema: Mass Source via API**
- Documentacion limitada pero el metodo `SetMassSource_1` esta documentado en la CHM

---

## PARTE 5 -- Patrones de Codigo Fundamentales

### 5.1 Conexion a ETABS (3 metodos)

**Metodo 1: GetActiveObject (RECOMENDADO)**
```python
import comtypes.client
import sys

try:
    EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
except (OSError, comtypes.COMError):
    print("No running instance of the program found.")
    sys.exit(-1)

SapModel = EtabsObject.SapModel
```

**Metodo 2: Try-Except con fallback**
```python
import comtypes.client

try:
    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
except:
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")

SapModel = myETABSObject.SapModel
```

**Metodo 3: Helper + QueryInterface (nueva instancia)**
```python
import comtypes.client

helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
EtabsObject.ApplicationStart()
SapModel = EtabsObject.SapModel
```

### 5.2 Conexion a SAP2000
```python
import comtypes.client

helper = comtypes.client.CreateObject('SAP2000v1.Helper')
helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
mySapObject = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
mySapObject.ApplicationStart()
SapModel = mySapObject.SapModel
```

### 5.3 Extraer resultados
```python
# Story forces
SapModel.Results.StoryForces(...)

# Database tables
NumberTables = 0
TableKey = []
TableName = []
ImportType = []
SapModel.DatabaseTables.GetAvailableTables(NumberTables, TableKey, TableName, ImportType)

# Load cases for display
SapModel.DatabaseTables.GetLoadCasesSelectedForDisplay()
SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(...)
```

### 5.4 Flujo tipico de automatizacion
```
1. Connect (GetActiveObject o CreateObject)
2. Access Model (SapModel)
3. Unlock model (SapModel.SetModelIsLocked(False))
4. Modify/Create (grids, materials, sections, elements, loads)
5. Run Analysis (SapModel.Analyze.RunAnalysis())
6. Extract Results (SapModel.Results.*)
7. Process Data (pandas, numpy)
8. Export (Excel, CSV, plots)
```

---

## PARTE 6 -- Best Practices y Lecciones

### De los tutoriales
1. **Siempre usar try-except** para conexion COM
2. **Preferir GetActiveObject** sobre CreateObject para evitar instancias fantasma
3. **Unlock model** antes de modificar: `SapModel.SetModelIsLocked(False)`
4. **Verificar unidades** con `SapModel.SetPresentUnits()` antes de extraer resultados
5. **comtypes 1.1.7** es la version mas estable para ETABS
6. **Limpiar comtypes.gen/** si hay errores de binding inconsistente
7. **Database Tables API** es la forma mas flexible de extraer resultados

### De nuestra experiencia (taller scripts)
8. **`CreateObject()` puede crear instancia INVISIBLE** -- forzar `obj.Visible=True`
9. **Prioridad conexion**: GetActiveObject > Helper.GetObject > CreateObject (visible)
10. **COM GC**: mantener helper/obj/model en variables globales del modulo
11. **File.Save() via COM puede producir .edb CORRUPTO** si ETABS abrio sin UI
12. **Separar pipeline en sesiones COM independientes** si la sesion muere
13. **AutoMesh size** debe ser <= vano minimo (ej: 0.4m para vano 0.425m)
14. **get_story_data()** falla en v19 pero no es critico -- no abortar

---

## PARTE 7 -- Resumen para Nuestro Taller

### Que paquetes instalar
```bash
pip install comtypes          # BASE - COM automation (ya lo tenemos)
pip install etabs-api         # OPCIONAL - wrapper alto nivel sobre comtypes
pip install pytabs            # ALTERNATIVA - wrapper .NET (requiere pythonnet)
```

### Que NO necesitamos
- openseespy (analisis no-lineal standalone, no ETABS)
- Sap2000py / ak_sap (SAP2000, no ETABS)
- VIKTOR (plataforma web, overkill para nuestro caso)

### Recursos mas utiles para nuestro pipeline
1. **Documentacion oficial CSI** -- CHM en directorio de instalacion ETABS
2. **GitHub CSiAPIExamples** -- ejemplos oficiales multi-lenguaje
3. **Hakan Keskin Medium** -- articulos con codigo real y aplicacion practica
4. **NeutralAXIS Getting Started** -- si necesitamos troubleshootear conexion
5. **Re-Tug Database Tables** -- para extraer resultados via DatabaseTables API
6. **Eng-Tips threads** -- troubleshooting especifico por version

### Proximos pasos sugeridos
- Revisar `etabs-api` de ebrahimraeyat para ver si simplifica nuestro pipeline actual
- Probar `pytabs` (Mitchell Tesch) si queremos cambiar de COM a .NET binding
- Consultar CSI CHM para firmas exactas de `FuncRS.SetFromFile` y `MassSource`

---

## Sources

### PyPI Packages
- [pytabs](https://pypi.org/project/pytabs/)
- [etabs-api](https://pypi.org/project/etabs-api/)
- [etabs](https://pypi.org/project/etabs/)
- [comtypes](https://pypi.org/project/comtypes/)
- [openseespy](https://pypi.org/project/openseespy/)
- [Sap2000py](https://pypi.org/project/Sap2000py/)
- [sap2000](https://pypi.org/project/sap2000/)
- [anastruct](https://pypi.org/project/anastruct/)
- [PyNiteFEA](https://pypi.org/project/PyNiteFEA/)

### Tutorials & Blogs
- [EngineeringSkills - ETABS Python API Introduction](https://www.engineeringskills.com/posts/an-introduction-to-the-etabs-python-api)
- [Stru.ai - ETABS API Beginner Guide 2025](https://stru.ai/blog/etabs-api-beginner-guide)
- [Stru.ai - Master ETABS API 2025](https://stru.ai/blog/etabs-api-automation-2025)
- [Stru.ai - Automate ETABS Analysis](https://stru.ai/blog/automate-etabs-analysis-python)
- [Stru.ai - ETABS Post-Processing Automation](https://stru.ai/blog/etabs-post-processing-automation)
- [Stru.ai - ETABS Seismic Automation](https://stru.ai/blog/etabs-seismic-automation)
- [Hakan Keskin - CSI API Tool](https://hakan-keskin.medium.com/csi-api-tool-python-integration-with-etabs-sap2000-and-safe-516f60a19e6c)
- [Hakan Keskin - Story Drifts](https://hakan-keskin.medium.com/extracting-story-drifts-and-joint-displacements-in-etabs-with-python-6b886aac89ba)
- [Hakan Keskin - Modal Analysis](https://hakan-keskin.medium.com/extracting-modal-analysis-results-and-base-reactions-in-etabs-with-python-af12da00ca5f)
- [Hakan Keskin - Pushover](https://hakan-keskin.medium.com/pushover-analysis-in-etabs-with-python-extracting-and-filtering-hinge-results-bd7b3ed64f20)
- [NeutralAXIS - Getting Started](https://neutralaxis.github.io/ETABS/ETABS%20API/Getting_Started/)
- [Re-Tug - Database Tables](https://re-tug.com/post/etabs-api-more-examples-database-tables/18)
- [VIKTOR.ai - ETABS/SAP2000 Integration](https://docs.viktor.ai/docs/tutorials/integrate-etabs-sap2000/)
- [PythonForStructuralEngineers - ETABS Automation](https://pythonforstructuralengineers.com/etabs-automation/)
- [Fabriccio Livia - LinkedIn Article](https://www.linkedin.com/pulse/etabs-automation-building-models-python-fabriccio-livia-saenz-rsxwe)
- [Kinson.io - ETABS Plugin Quickstart](https://kinson.io/posts/etabs-plugin-quickstart)
- [CSI America - Developer](https://www.csiamerica.com/developer)
- [CSI Official Python Example](http://docs.csiamerica.com/help-files/common-api(from-sap-and-csibridge)/Example_Code/Example_7_(Python).htm)

### GitHub Repositories
- [danielogg92/Etabs-API-Python](https://github.com/danielogg92/Etabs-API-Python)
- [ebrahimraeyat/etabs_api](https://github.com/ebrahimraeyat/etabs_api)
- [mitchell-tesch/pytabs](https://github.com/mitchell-tesch/pytabs)
- [mitchell-tesch/CSiPy](https://github.com/mitchell-tesch/CSiPy)
- [mihdicaballero/ETABS-Ninja](https://github.com/mihdicaballero/ETABS-Ninja)
- [retug/ETABs](https://github.com/retug/ETABs)
- [jantozor/CSiAPIExamples](https://github.com/jantozor/CSiAPIExamples)
- [rpakishore/ak_sap](https://github.com/rpakishore/ak_sap)
- [jchatkinson/ETABS-plugin-starter-kit](https://github.com/jchatkinson/ETABS-plugin-starter-kit)
- [mtavares51/etabs_python_modelling](https://github.com/mtavares51/etabs_python_modelling)
- [pichosan/CSi-API](https://github.com/pichosan/CSi-API)
- [marco-rosso-m/SAP2000-python-for-structural-optimization](https://github.com/marco-rosso-m/SAP2000-python-for-structural-optimization)

### Forums
- [Eng-Tips - Error attaching Python to ETABS](https://www.eng-tips.com/threads/error-when-getting-python-to-attach-to-etabs.477451/)
- [Eng-Tips - ETABS v18 Cannot attach Python](https://www.eng-tips.com/threads/etabs-v18-api-cannot-attach-python-with-etabs.477710/)
- [Eng-Tips - FrameObj.GetSection](https://www.eng-tips.com/threads/etabs-api-frameobj-getsection.477453/)
- [Eng-Tips - Section Cut Definition](https://www.eng-tips.com/threads/etabs-api-troubles-section-cut-definition.502839/)
- [Eng-Tips - Mass Source](https://www.eng-tips.com/threads/etabs-api-add-new-mass-source.521909/)
- [Eng-Tips - Section Cut Forces v22](https://www.eng-tips.com/threads/etabs-22-api-section-cut-forces.526157/)
- [Eng-Tips - SAP2000 OAPI](https://www.eng-tips.com/threads/sap2000-oapi.516723/)
