# Investigacion Completa: CSI ETABS/SAP2000 API Programming

> Fecha: 20 marzo 2026
> Fuentes: docs.csiamerica.com, wiki.csiamerica.com, Eng-Tips, ResearchGate, GitHub, blogs especializados

---

## TABLA DE CONTENIDOS

1. [Fuentes Oficiales CSI](#1-fuentes-oficiales-csi)
2. [Conexion COM — Lifecycle Management](#2-conexion-com--lifecycle-management)
3. [Codigos de Error y Return Values](#3-codigos-de-error-y-return-values)
4. [Diferencias entre Versiones](#4-diferencias-entre-versiones)
5. [Bugs Conocidos y Workarounds](#5-bugs-conocidos-y-workarounds)
6. [Best Practices de CSI](#6-best-practices-de-csi)
7. [Performance Tips](#7-performance-tips)
8. [Thread Safety](#8-thread-safety)
9. [Temas Especificos Investigados](#9-temas-especificos-investigados)
10. [Bibliotecas y Wrappers de Terceros](#10-bibliotecas-y-wrappers-de-terceros)
11. [Recursos Educativos](#11-recursos-educativos)
12. [Fuentes y URLs](#12-fuentes-y-urls)

---

## 1. Fuentes Oficiales CSI

### 1.1 Documentacion OAPI (docs.csiamerica.com)

La documentacion oficial de la API esta disponible en:

- **API Help Files online**: `https://docs.csiamerica.com/help-files/etabs-api-2016/` (version 2016)
  y `https://docs.csiamerica.com/help-files/etabs-api-2015/` (version 2015)
- **CHM local**: El archivo `CSI API ETABS v1.chm` se encuentra en el directorio de instalacion
  de ETABS, tipicamente `C:\Program Files\Computers and Structures\ETABS XX\`
- **Cross-product API**: `https://docs.csiamerica.com/help-files/common-api(from-sap-and-csibridge)/`

Cada funcion de la API esta documentada con:
- Sintaxis y parametros
- Version en que fue introducida
- Cambios historicos a la funcion
- Ejemplo de uso

### 1.2 Wiki / Knowledge Base (wiki.csiamerica.com)

- **OAPI principal**: `https://wiki.csiamerica.com/display/kb/OAPI`
  y nuevo sitio: `https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2005484/OAPI`
- **OAPI FAQ**: `https://wiki.csiamerica.com/display/kb/OAPI+FAQ`
  y nuevo sitio: `https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2000456/OAPI+FAQ`
- **Plugins**: `https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2012754/Plugins`
- **.NET 8 Plugin Example**: `https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2011456/NET+8+Plugin+Example+-+All+Products`
- **Backup y troubleshooting modelos corruptos**: `https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2001007/Backup+and+troubleshooting+corrupted+models`

### 1.3 Developer Portal (csiamerica.com/developer)

URL: `https://www.csiamerica.com/developer`

Contenido:
- La CSI API esta disponible para ETABS, SAP2000, CSiBridge, y SAFE
- API consistente entre productos para permitir reutilizacion de herramientas
- Compatible con: VBA, VB.NET, C#, C++, Visual Fortran, Python, MATLAB
- La biblioteca API esta en el directorio de instalacion: `C:\Program Files\Computers and Structures\ETABS 22\`
- **ETABSv1.dll** — biblioteca especifica de ETABS
- **CSiAPIv1.dll** — biblioteca cross-product (contiene interfaces para TODOS los metodos de TODOS los productos)

### 1.4 Ejemplos Oficiales que Vienen con ETABS

- El CHM de API incluye ejemplos en Python al inicio de la documentacion
- Ejemplo 7 (Python) de SAP2000: `http://docs.csiamerica.com/help-files/common-api(from-sap-and-csibridge)/Example_Code/Example_7_(Python).htm`
- Python boilerplate code esta al comienzo de la documentacion API

### 1.5 Release Notes con Cambios API

- v19.0.0: `http://installs.csiamerica.com/software/ETABS/19/ReleaseNotesETABSv1900.pdf`
- v20.0.0: `https://www.csiamerica.com/software/ETABS/20/ReleaseNotesETABSv2000.pdf`
- v20.2.0: `https://www.csiamerica.com/software/ETABS/20/ReleaseNotesETABSv2020.pdf`
- v21.0.0: `https://www.csiamerica.com/software/ETABS/21/ReleaseNotesETABSv2100.pdf`
- v21.1.0: `https://www.csiamerica.com/software/ETABS/21/ReleaseNotesETABSv2110.pdf`
- v22.0.0: `https://www.csiamerica.com/software/ETABS/22/ReleaseNotesETABSv2200.pdf`
- v22.1.0: `https://www.csiamerica.com/software/ETABS/22/ReleaseNotesETABSv2210plus2200.pdf`

---

## 2. Conexion COM -- Lifecycle Management

### 2.1 Tres Metodos de Conexion

#### Metodo 1: GetActiveObject (conectar a instancia existente)

```python
import comtypes.client

try:
    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
except OSError:
    print("No se encontro instancia de ETABS corriendo")

SapModel = myETABSObject.SapModel
```

**Ventajas**: Se conecta a ETABS con UI activa. Archivo .edb se guarda correctamente.
**Desventajas**: Falla si ETABS no esta corriendo. Requiere ETABS abierto manualmente.

#### Metodo 2: Helper + GetObject (conectar via helper)

```python
import comtypes.client
import comtypes.gen.ETABSv1 as ETABSv1

helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(ETABSv1.cHelper)
myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
SapModel = myETABSObject.SapModel
```

**Ventajas**: Mas robusto que GetActiveObject en algunas versiones de comtypes.
**Desventajas**: Requiere ETABS corriendo.

#### Metodo 3: Helper + CreateObjectProgID (crear nueva instancia)

```python
import comtypes.client
import comtypes.gen.ETABSv1 as ETABSv1

helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(ETABSv1.cHelper)
EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
EtabsObject.ApplicationStart()
SapModel = EtabsObject.SapModel
SapModel.InitializeNewModel()
SapModel.File.OpenFile(ModelPath)
```

**PELIGRO**: Este metodo puede crear una instancia INVISIBLE de ETABS.
Ver seccion 5.1 para el bug y workaround.

#### Metodo Robusto Recomendado (try/except fallback)

```python
import comtypes.client

try:
    # Intentar conectar a instancia existente
    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
except OSError:
    # Si no hay instancia, crear nueva via helper
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")

SapModel = myETABSObject.SapModel
```

#### Alternativa con win32com

```python
import win32com.client

# Conectar a instancia existente
EtabsObject = win32com.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
# O crear nueva
EtabsObject = win32com.client.Dispatch("CSI.ETABS.API.ETABSObject")
```

### 2.2 Desconexion y Shutdown Correcto

```python
# Secuencia correcta de cierre:

# 1. Guardar el modelo
ret = SapModel.File.Save(model_path)

# 2. Cerrar la aplicacion ETABS
ret = myETABSObject.ApplicationExit(False)  # False = no guardar cambios pendientes

# 3. Liberar referencia COM
SapModel = None
myETABSObject = None
```

**CRITICO**: Si no se cierra la conexion correctamente, el proceso ETABS sigue
corriendo en background consumiendo recursos.

### 2.3 Patron try/finally Recomendado

```python
try:
    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel

    # ... hacer operaciones ...

finally:
    # Siempre liberar recursos
    if SapModel is not None:
        SapModel = None
    if myETABSObject is not None:
        myETABSObject = None
```

### 2.4 Separacion de Sesiones COM (Pipeline Largo)

Para pipelines largos (como nuestro caso de 13 pasos), la sesion COM puede morir
despues de operaciones pesadas. La solucion es:

```python
# Fase 1: Geometria
EtabsObject.ApplicationStart()
SapModel = EtabsObject.SapModel
# ... crear geometria ...
SapModel.File.Save(path)
EtabsObject.ApplicationExit(False)

# Esperar y reconectar
import time
time.sleep(10)

# Fase 2: Analisis (sesion COM fresca)
EtabsObject2 = helper.GetObject("CSI.ETABS.API.ETABSObject")
SapModel2 = EtabsObject2.SapModel
SapModel2.File.OpenFile(path)
# ... configurar analisis ...
```

Esto es valido segun documentacion CSI: `ApplicationStart()` / `OpenFile()` / `ApplicationExit()`
son metodos disenados para este patron.

---

## 3. Codigos de Error y Return Values

### 3.1 Convencion General

| Valor | Significado |
|-------|-------------|
| `0`   | **Exito** — la operacion se completo correctamente |
| `!= 0` (no-cero) | **Error** — la operacion fallo |

No hay documentacion oficial detallada sobre significados especificos de codigos
no-cero (1, -1, 2, etc.). La recomendacion es simplemente verificar `ret == 0`.

### 3.2 Patron de Verificacion

```python
ret = SapModel.FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, name, propName)
if ret[0] != 0:
    print(f"ERROR: FrameObj.AddByCoord fallo con codigo {ret[0]}")
```

### 3.3 Funciones que Retornan Tuplas

Muchas funciones API retornan tuplas donde:
- El primer elemento es el codigo de error (0=exito)
- Los demas elementos son los datos solicitados

```python
ret = SapModel.FrameObj.GetNameList()
# ret[0] = numero de frames
# ret[1] = lista de nombres
# ret[2] = codigo de error (en algunas versiones)
```

**Nota**: El orden exacto de los elementos puede variar entre versiones.
Siempre consultar la documentacion CHM de tu version.

---

## 4. Diferencias entre Versiones

### 4.1 Cambio Mayor: ETABS v18 (API Forward Compatible)

**A partir de ETABS v18**, la API es forward-compatible con versiones futuras.
Es decir, codigo escrito para v18 deberia funcionar en v19, v20, v21, v22
sin recompilar.

Esto tambien aplica cross-product:
- ETABS v18+
- SAP2000 v21+
- CSiBridge v21+
- SAFE v20+

### 4.2 ETABS v17 y Anteriores

Scripts para v17 o anterior **NO son automaticamente compatibles** con v18+.
El ProgID, las interfaces COM y los TLBs pueden diferir.

### 4.3 Cambios API Documentados por Version

| Version | Cambios API |
|---------|-------------|
| v18.0   | API forward-compatible introducida. Cross-product API. CSiAPIv1.DLL |
| v19.0   | Multiples mejoras, `get_story_data()` frecuentemente falla (bug conocido) |
| v20.2   | `Get/SetNumberModes` actualizado en cModalEigen y cModalRitz. `Get/SetParameters` agregado a cModalEigen |
| v21.0   | Cambios en funciones de seccion |
| v21.1   | `GetTee_1` y `SetTee_1` actualizados para incluir radio de filete |
| v22.0   | ETABSv1.dll y CSiAPIv1.dll actualizados a .NET Standard 2.0. Soporte .NET 8 para plugins |
| v22.1   | Correcciones menores |

### 4.4 .NET 8 Plugin Support (v22.0+)

A partir de v22.0, es posible crear plugins con .NET 8:
- ETABSv1.dll target: .NET Standard 2.0
- Compatible con: .NET Framework 4.6.1-4.8.1, .NET Core 2 a .NET 8
- Requiere Visual Studio 2022 + .NET 8 SDK

---

## 5. Bugs Conocidos y Workarounds

### 5.1 BUG: CreateObject Crea Instancia INVISIBLE

**Problema**: `Helper.CreateObject()` o `helper.CreateObjectProgID()` puede lanzar
una instancia de ETABS que corre en background sin ventana visible.

**Sintomas**:
- ETABS.exe aparece en Task Manager pero no hay ventana
- El modelo se crea pero no se ve
- `File.Save()` puede producir .edb corrupto

**Workaround confirmado**:
```python
EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
EtabsObject.Visible = True  # FORZAR VISIBILIDAD
time.sleep(15)  # Esperar a que la UI cargue completamente
EtabsObject.ApplicationStart()
```

**Mejor solucion**: Abrir ETABS manualmente primero, luego conectar con `GetActiveObject`
o `helper.GetObject`. Nunca usar CreateObject como primera opcion.

### 5.2 BUG: File.Save() Produce .edb Corrupto via COM

**Problema**: Si ETABS fue abierto sin UI (via `CreateObject`), `File.Save()` puede
producir archivos .edb corruptos o incompletos.

**Workaround**:
1. Abrir ETABS v19 manualmente
2. File > New Model > Blank
3. LUEGO correr scripts que conectan via `GetActiveObject`
4. Asi `File.Save()` funciona correctamente con UI funcional

**Recuperacion de archivos corruptos**:
- El archivo `.$et` se crea cada vez que se guarda — puede importarse para recuperar
- El archivo `.ebk` contiene backup del ultimo archivo abierto
- Exportar a `.e2k` y reimportar puede arreglar corrupciones

### 5.3 BUG: comtypes.gen Cache Stale (TLB Inconsistente)

**Problema**: Despues de actualizar ETABS o cambiar version, los archivos cacheados
en `comtypes.gen` pueden causar `AttributeError` o comportamiento erratico.

**Sintomas**:
- `AttributeError: module 'comtypes.gen.CSiAPIv1' has no attribute 'cOAPI'`
- `AttributeError: module 'comtypes.gen.ETABSv1' has no attribute 'cHelper'`
- Funciones que existian dejan de funcionar

**Workaround**:
```python
# ANTES de importar comtypes.client, limpiar cache:
import shutil, os

gen_path = os.path.join(os.path.dirname(__import__('comtypes').__file__), 'gen')
if os.path.exists(gen_path):
    shutil.rmtree(gen_path)
    os.makedirs(gen_path)
    # Crear __init__.py vacio
    with open(os.path.join(gen_path, '__init__.py'), 'w') as f:
        pass

# Alternativa: usar el script incluido con comtypes
# python venv\scripts\clear_comtypes_cache.py -y
```

**Nota**: `clear_comtypes_cache.py -y` borra el directorio `gen` y `comtypes_cache`.
Issue #182 de comtypes reporta que este script a veces rompe `comtypes.client`.
La solucion manual (borrar y recrear gen con `__init__.py`) es mas confiable.

### 5.4 BUG: GetActiveObject + comtypes Version Incompatible

**Problema**: Ciertas versiones de comtypes tienen bugs con `GetActiveObject` para ETABS.

**Versiones problematicas**:
- comtypes 1.1.2: Requiere modificar `__init__.py` manualmente
- comtypes 1.1.7: Bugs al obtener output modal
- comtypes < 1.1.10: Multiples problemas de compatibilidad

**Recomendacion**: Usar `comtypes >= 1.1.10` (o la ultima estable).

```bash
pip install comtypes --upgrade
```

### 5.5 BUG: FuncRS.SetFromFile No Existe en OAPI (v19 y anteriores)

**Problema**: No hay metodo OAPI para definir una funcion de espectro de respuesta
desde archivo en versiones antiguas de ETABS.

**Confirmado por ResearchGate** (2023): "There is not any method available in the
OAPI for defining a response spectrum function."

**Workarounds**:

1. **Usar SetUser en vez de SetFromFile** (RECOMENDADO para v18+):
```python
# Leer archivo de espectro manualmente
periods = [0.0, 0.1, 0.2, ...]
accels  = [0.4, 0.8, 1.0, ...]

ret = SapModel.Func.FuncRS.SetUser(
    "EspectroNCh433",    # Nombre de la funcion
    len(periods),        # Numero de puntos
    periods,             # Array de periodos
    accels,              # Array de aceleraciones
    0.05                 # Damping ratio (5%)
)
```

2. **Editar archivo .$et directamente** (workaround legacy):
```
- Exportar modelo a .$et
- Insertar definicion de espectro en el archivo de texto
- Reimportar .$et
```

3. **SAP2000 tiene mejor soporte API para espectros** — si la automatizacion
de espectros es critica, considerar SAP2000.

### 5.6 BUG: SetMassSource_1 Solo Modifica Default

**Problema**: `cPropMaterial.SetMassSource_1` solo cambia la fuente de masa por defecto.
No permite agregar NUEVAS fuentes de masa.

**Firma confirmada del metodo** (docs.csiamerica.com):
```python
ret = SapModel.PropMaterial.SetMassSource_1(
    IncludeElements,   # Boolean: incluir self-weight
    IncludeAddedMass,  # Boolean: incluir masa adicional asignada
    IncludeLoads,      # Boolean: incluir masa calculada de load patterns
    NumberLoads,       # Integer: numero de load patterns
    LoadPat,           # String[]: array nombres load patterns
    sf                 # Double[]: factores de escala por cada load pattern
)
# Retorna 0 si exito, no-cero si error
```

**Ejemplo para sismo chileno** (NCh433):
```python
# Masa = PP + 0.25*SCP (Art. 5.5.1 NCh433)
ret = SapModel.PropMaterial.SetMassSource_1(
    True,              # IncludeElements (self-weight)
    False,             # IncludeAddedMass
    True,              # IncludeLoads
    1,                 # NumberLoads
    ["SCP"],           # LoadPat
    [0.25]             # sf (factor 0.25 para sobrecarga permanente)
)
```

**Workaround para agregar NEW mass source**: Usar Database Tables API:
```python
# Si puedes acceder a la tabla en GUI, puedes accederla por API
table_data = SapModel.DatabaseTables.GetTableForEditingArray("Mass Source", "")
# ... modificar datos ...
SapModel.DatabaseTables.SetTableForEditingArray(...)
SapModel.DatabaseTables.ApplyEditedTables(True)
```

### 5.7 BUG: get_story_data() Falla en v19

**Problema**: `SapModel.Story.GetStories()` frecuentemente falla en ETABS v19.

**Workaround**: No abortar el pipeline por este error. Usar `NewGridOnly(ret=0)`
para garantizar stories correctas, y verificar por otros medios.

### 5.8 BUG: RPC Server Unavailable (-2147023174)

**Problema**: Error `0x800706BA` — la sesion COM muere despues de operaciones pesadas
(tipicamente despues de crear muchos elementos + mesh).

**Causa**: El proceso ETABS crashea o la conexion RPC se pierde.

**Workaround**: Separar pipeline en fases con sesiones COM independientes
(ver seccion 2.4).

---

## 6. Best Practices de CSI

### 6.1 Lock/Unlock del Modelo

```python
# ANTES de modificar el modelo:
SapModel.SetModelIsLocked(False)

# ... hacer modificaciones ...

# ANTES de correr analisis o extraer resultados:
SapModel.SetModelIsLocked(True)

# Correr analisis
ret = SapModel.Analyze.RunAnalysis()

# Extraer resultados (modelo debe estar locked)
results = SapModel.Results.FrameForce(...)
```

**IMPORTANTE**: Desbloquear el modelo BORRA todos los resultados de analisis previos.

### 6.2 Orden de Operaciones Recomendado

1. Conectar a ETABS (preferir GetActiveObject)
2. Desbloquear modelo: `SetModelIsLocked(False)`
3. Definir materiales y secciones
4. Crear geometria (grids, stories, frames, areas)
5. Asignar propiedades (diafragma, mesh, releases)
6. Definir cargas (load patterns, load cases)
7. Definir combinaciones
8. Guardar: `SapModel.File.Save(path)`
9. Correr analisis: `SapModel.Analyze.RunAnalysis()`
10. Extraer resultados
11. Guardar y cerrar

### 6.3 Verificacion Post-Creacion

Siempre verificar que los elementos se crearon:
```python
# Obtener lista de nombres ANTES
count_before = SapModel.FrameObj.GetNameList()[0]

# Crear elemento
ret = SapModel.FrameObj.AddByCoord(...)

# Verificar DESPUES
count_after = SapModel.FrameObj.GetNameList()[0]
assert count_after > count_before, "Frame no se creo!"
```

### 6.4 RefreshView

```python
# Refrescar todas las ventanas, mantener zoom
SapModel.View.RefreshView(0, False)
# Parametro 1: 0 = todas las ventanas
# Parametro 2: False = no resetear zoom
```

---

## 7. Performance Tips

### 7.1 Operaciones Batch

Muchas funciones API soportan arrays para procesamiento batch:
```python
# MAL (lento) — 100 llamadas individuales:
for i in range(100):
    SapModel.FrameObj.SetSection(names[i], sections[i])

# BIEN (rapido) — si existe version batch:
# Usar Database Tables para cambios masivos
```

### 7.2 Suprimir Actualizacion de Vista

```python
# Desactivar actualizacion de vista durante creacion masiva
# (no hay metodo directo, pero minimizar RefreshView calls)

# Crear TODOS los elementos primero
for wall in walls:
    SapModel.AreaObj.AddByCoord(...)

# RefreshView UNA sola vez al final
SapModel.View.RefreshView(0, False)
```

### 7.3 Database Tables para Operaciones Masivas

Para leer/escribir grandes cantidades de datos, usar Database Tables
es significativamente mas rapido que llamadas individuales:

```python
# Leer tabla
table_key = "Frame Assignments - Section Properties"
ret = SapModel.DatabaseTables.GetTableForEditingArray(table_key, "")
# ret contiene: TableVersion, FieldsKeysIncluded, NumberRecords, TableData

# Modificar datos en el array

# Escribir tabla modificada
ret = SapModel.DatabaseTables.SetTableForEditingArray(
    table_key,
    TableVersion,
    FieldsKeysIncluded,
    NumberRecords,
    TableData
)
ret = SapModel.DatabaseTables.ApplyEditedTables(True)
```

### 7.4 Productividad Reportada

Segun multiples fuentes, la automatizacion via API puede:
- Ahorrar hasta 40% del tiempo en tareas repetitivas
- Aumentar productividad 2-3x con operaciones batch
- Reducir errores hasta 60% en configuracion de analisis sismico

---

## 8. Thread Safety

### 8.1 Conclusion: NO Thread-Safe

La API de ETABS es un objeto COM single-threaded (STA — Single-Threaded Apartment).

**No se puede usar la API desde multiples threads simultaneamente.**

La documentacion oficial no menciona thread safety, lo que tipicamente indica
que NO es thread-safe. Los objetos COM STA requieren:
- Todas las llamadas desde el mismo thread
- O usar marshalling COM para cross-thread calls (lento y propenso a errores)

### 8.2 Recomendacion

Para automatizacion paralela, usar **procesos separados** (no threads):
- Cada proceso lanza su propia instancia de ETABS
- Cada proceso tiene su propia sesion COM
- Comunicacion entre procesos via archivos o IPC

---

## 9. Temas Especificos Investigados

### 9.1 Response Spectrum — SetUser (Workaround para SetFromFile)

**Estado actual**: `SetUser` funciona en ETABS v18+ para definir espectros programaticamente.

```python
import numpy as np

# Leer archivo de espectro (formato: periodo,aceleracion)
data = np.loadtxt("espectro_NCh433_Zona3_SueloC.txt", delimiter=",")
periods = data[:, 0].tolist()
accels  = data[:, 1].tolist()

# Definir funcion de espectro de respuesta
ret = SapModel.Func.FuncRS.SetUser(
    "NCh433_Z3_SC",      # Nombre
    len(periods),         # Numero de puntos
    periods,              # Periodos [s]
    accels,               # Aceleraciones [g]
    0.05                  # Damping ratio
)
assert ret == 0, f"SetUser fallo: {ret}"
```

### 9.2 Response Spectrum Cases

```python
# Definir caso de espectro de respuesta
# Direccion U1 (X)
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("SEx")
ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "SEx",
    1,                    # NumberLoads
    ["U1"],               # LoadDir
    ["NCh433_Z3_SC"],     # Func
    [9.81],               # SF (escalar a m/s2 si espectro en g)
    [""],                 # CSys
    [0.0]                 # Ang
)
```

### 9.3 MassSource Completo para NCh433

```python
# Configurar Mass Source segun NCh433
# Masa sismica = W = PP + 0.25*SCP  (Art. 5.5.1)
ret = SapModel.PropMaterial.SetMassSource_1(
    True,       # IncludeElements (peso propio de elementos)
    False,      # IncludeAddedMass
    True,       # IncludeLoads (incluir cargas como masa)
    1,          # NumberLoads (1 patron de carga)
    ["SCP"],    # LoadPat (sobrecarga permanente)
    [0.25]      # sf (factor 0.25)
)
if ret != 0:
    print("WARN: SetMassSource_1 fallo, intentar via Database Tables")
```

### 9.4 comtypes.gen Cleanup Robusto

```python
"""
Limpieza robusta de cache comtypes.gen
Ejecutar ANTES de cualquier import comtypes.client
"""
import os
import shutil

def clean_comtypes_cache():
    """Elimina cache stale de comtypes para forzar regeneracion de TLBs."""
    try:
        import comtypes
        gen_path = os.path.join(os.path.dirname(comtypes.__file__), 'gen')

        if os.path.exists(gen_path):
            # Borrar todo excepto __init__.py
            for item in os.listdir(gen_path):
                item_path = os.path.join(gen_path, item)
                if item != '__init__.py':
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
            print(f"Cache comtypes.gen limpiado: {gen_path}")

        # Tambien limpiar comtypes_cache si existe
        cache_path = os.path.join(os.environ.get('APPDATA', ''), 'comtypes_cache')
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
            print(f"comtypes_cache limpiado: {cache_path}")

    except Exception as e:
        print(f"Error limpiando cache: {e}")

# Uso:
clean_comtypes_cache()
import comtypes.client  # Ahora regenerara TLBs frescos
```

### 9.5 Patron Completo de Conexion Robusta

```python
"""
Conexion robusta a ETABS v19+ con manejo de errores completo.
"""
import os
import sys
import time
import shutil

def clean_comtypes_gen():
    """Limpiar cache stale de comtypes."""
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

def connect_etabs(create_if_missing=False, etabs_path=None):
    """
    Conectar a ETABS.

    Prioridad:
    1. GetActiveObject (instancia con UI)
    2. Helper.GetObject (instancia con UI)
    3. CreateObjectProgID (solo si create_if_missing=True)

    Returns: (EtabsObject, SapModel)
    """
    import comtypes.client

    # Metodo 1: GetActiveObject
    try:
        EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        print("Conectado via GetActiveObject")
        return EtabsObject, EtabsObject.SapModel
    except OSError:
        pass

    # Metodo 2: Helper.GetObject
    try:
        helper = comtypes.client.CreateObject('ETABSv1.Helper')
        import comtypes.gen.ETABSv1 as ETABSv1
        helper = helper.QueryInterface(ETABSv1.cHelper)
        EtabsObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
        print("Conectado via Helper.GetObject")
        return EtabsObject, EtabsObject.SapModel
    except Exception:
        pass

    # Metodo 3: Crear nueva instancia (PELIGROSO)
    if create_if_missing:
        helper = comtypes.client.CreateObject('ETABSv1.Helper')
        import comtypes.gen.ETABSv1 as ETABSv1
        helper = helper.QueryInterface(ETABSv1.cHelper)
        EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")

        # FORZAR VISIBILIDAD
        try:
            EtabsObject.Visible = True
        except:
            pass

        EtabsObject.ApplicationStart()
        time.sleep(15)  # Esperar a que UI cargue

        print("WARN: Instancia creada via CreateObject (puede ser inestable)")
        return EtabsObject, EtabsObject.SapModel

    raise ConnectionError("No se pudo conectar a ETABS. Abrelo manualmente primero.")

# Uso:
clean_comtypes_gen()
etabs, model = connect_etabs(create_if_missing=False)
```

---

## 10. Bibliotecas y Wrappers de Terceros

### 10.1 etabs_api (ebrahimraeyat)

- **URL**: https://github.com/ebrahimraeyat/etabs_api
- **PyPI**: https://pypi.org/project/etabs-api/
- **Requisitos**: Python >= 3.8, comtypes, pandas, psutil, numpy
- **Soporte**: ETABS 2018+ y SAFE
- **Features**:
  - Database operations (read/write con DataFrames)
  - Frame object management
  - Area object operations
  - Load pattern/case management
  - Seismic load patterns
  - Deflection calculations
  - Rebar area calculations

### 10.2 Etabs-API-Python (danielogg92)

- **URL**: https://github.com/danielogg92/Etabs-API-Python
- **Descripcion**: Funciones faciles de usar para la CSI ETABS API
- **Archivos clave**:
  - `Main.py` — Boilerplate de conexion
  - `Etabs_Get_Functions.py` — Funciones getter
  - `Etabs_Set_Functions.py` — Funciones setter

### 10.3 CSiAPIExamples (jantozor)

- **URL**: https://github.com/jantozor/CSiAPIExamples
- **Descripcion**: Ejemplos para cada lenguaje disponible (ETABS, SAP2000, CSiBridge, SAFE)
- **Enfoque**: Beginner-friendly, ejemplos limpios y simples
- **Lenguajes**: Python, VB, C#, C++, MATLAB

### 10.4 BHoM ETABS_Toolkit

- **URL**: https://github.com/BHoM/ETABS_Toolkit
- **Descripcion**: Toolkit C# para ETABS con soporte multi-version
- **Nota**: Usa builds separados para soportar diferencias API entre versiones

### 10.5 NeutralAXIS

- **URL**: https://neutralaxis.github.io/ETABS/ETABS%20API/Getting_Started/
- **Descripcion**: Documentacion y tutoriales para ETABS API
- **Contenido**: Getting Started, Introduction, ejemplos paso a paso

---

## 11. Recursos Educativos

### 11.1 Tutoriales Completos

| Recurso | URL | Descripcion |
|---------|-----|-------------|
| EngineeringSkills.com | https://www.engineeringskills.com/posts/an-introduction-to-the-etabs-python-api | Introduccion completa con codigo |
| Stru.ai Beginner Guide | https://stru.ai/blog/etabs-api-beginner-guide | Guia para principiantes 2025 |
| Stru.ai Master Guide | https://stru.ai/blog/etabs-api-automation-2025 | Automatizacion avanzada 2025 |
| Stru.ai Seismic | https://stru.ai/blog/etabs-seismic-automation | Automatizacion sismica |
| Stru.ai Post-Processing | https://stru.ai/blog/etabs-post-processing-automation | Post-procesamiento |
| NeutralAXIS Getting Started | https://neutralaxis.github.io/ETABS/ETABS%20API/Getting_Started/ | Tutorial paso a paso |
| Sheer Force Engineering | https://sheerforceeng.com/2021/09/17/etabs-oapi-api-how-to-crack-automation-speed-secrets-using-vba-and-excel/ | VBA/Excel speed secrets |
| re-tug.com Database Tables | https://re-tug.com/post/etabs-api-more-examples-database-tables/18 | Ejemplos Database Tables |
| Python for Structural Eng. | https://pythonforstructuralengineers.com/etabs-automation/ | ETABS + Python |

### 11.2 Articulos Medium (Hakan Keskin)

| Tema | URL |
|------|-----|
| Story Drifts & Joint Displacements | https://hakan-keskin.medium.com/extracting-story-drifts-and-joint-displacements-in-etabs-with-python-6b886aac89ba |
| Modal Analysis & Base Reactions | https://hakan-keskin.medium.com/extracting-modal-analysis-results-and-base-reactions-in-etabs-with-python-af12da00ca5f |
| CSI API Tool | https://hakan-keskin.medium.com/csi-api-tool-python-integration-with-etabs-sap2000-and-safe-516f60a19e6c |

### 11.3 Discusiones Eng-Tips Relevantes

| Tema | URL |
|------|-----|
| Python Database Tables Edit | https://www.eng-tips.com/threads/etabs-api-using-python-database-tables-edit.494947/ |
| ETABS API with Python (general) | https://www.eng-tips.com/threads/etabs-api-with-python.492251/ |
| Error Attaching Python to ETABS | https://www.eng-tips.com/threads/error-when-getting-python-to-attach-to-etabs.477451/ |
| ETABS v18 API Cannot Attach | https://www.eng-tips.com/threads/etabs-v18-api-cannot-attach-python-with-etabs.477710/ |
| Add New Mass Source | https://www.eng-tips.com/threads/etabs-api-add-new-mass-source.521909/ |
| Analysis Results | https://www.eng-tips.com/threads/etabs-api-python-quot-analysis-result-quot.514827/ |
| Section Cut Definition | https://www.eng-tips.com/threads/etabs-api-troubles-section-cut-definition.502839/ |
| Database Tables Apply Changes | https://www.eng-tips.com/threads/etabs-api-database-tables-apply-changes-while-model-is-locked.516535/ |
| FrameObj.GetSection | https://www.eng-tips.com/threads/etabs-api-frameobj-getsection.477453/ |

### 11.4 Otros Recursos

| Recurso | URL |
|---------|-----|
| VIKTOR.AI + ETABS | https://www.viktor.ai/blog/200/etabs-model-post-processing-ai-python |
| LinkedIn: Building Models with Python | https://www.linkedin.com/pulse/etabs-automation-building-models-python-fabriccio-livia-saenz-rsxwe |
| Scribd: CSI API ETABS v1 | https://www.scribd.com/document/929780873/Csi-API-Etabs-v1 |
| kinson.io: Making Plugin | https://kinson.io/posts/etabs-plugin-quickstart |
| Structures by Code (2013) | https://structuresbycode.wordpress.com/2013/08/27/etabs-oapi-how-to-get-started/ |
| apintr.com Introduction | https://www.apintr.com/etab-api/introduction-etabs-api/ |

---

## 12. Fuentes y URLs

### Documentacion Oficial CSI
- [CSI Developer Portal](https://www.csiamerica.com/developer)
- [OAPI Knowledge Base](https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2005484/OAPI)
- [OAPI FAQ](https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2000456/OAPI+FAQ)
- [ETABS API 2016 Help Files](https://docs.csiamerica.com/help-files/etabs-api-2016/)
- [ETABS API 2015 Help Files](https://docs.csiamerica.com/help-files/etabs-api-2015/)
- [Common API (SAP/CSiBridge)](http://docs.csiamerica.com/help-files/common-api(from-sap-and-csibridge)/Introduction.htm)
- [Python Example 7](http://docs.csiamerica.com/help-files/common-api(from-sap-and-csibridge)/Example_Code/Example_7_(Python).htm)
- [SetMassSource_1 Method](https://docs.csiamerica.com/help-files/etabs-api-2015/html/3f256ea8-6c8d-76b0-acae-e1d370413b37.htm)
- [RefreshView Method](https://docs.csiamerica.com/help-files/etabs-api-2015/html/1cda913a-a4bb-f163-e505-92398ee025e0.htm)
- [cFile.OpenFile Method](https://docs.csiamerica.com/help-files/etabs-api-2016/html/ab8ad3e2-ebcf-7cd9-636b-ec9cccdc85a8.htm)
- [NET 8 Plugin Example](https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2011456/NET+8+Plugin+Example+-+All+Products)
- [Backup & Troubleshooting](https://web.wiki.csiamerica.com/wiki/spaces/kb/pages/2001007/Backup+and+troubleshooting+corrupted+models)
- [Lock Model](https://docs.csiamerica.com/help-files/etabs/Menus/Analyze/Lock_Model.htm)
- [Response Spectrum Functions](https://docs.csiamerica.com/help-files/etabs/Menus/Define/Functions/Response_Spectrum_Functions/Response_Spectrum_Functions.htm)
- [From File Response Spectrum](https://docs.csiamerica.com/help-files/etabs/Menus/Define/Functions/Response_Spectrum_Functions/From_File_Response_Spectrum.htm)
- [User Response Spectrum](https://docs.csiamerica.com/help-files/etabs/Menus/Define/Functions/Response_Spectrum_Functions/User_Response_Spectrum.htm)
- [Mass Source](https://docs.csiamerica.com/help-files/etabs/Menus/Define/Mass_Source.htm)
- [Saving Models](https://docs.csiamerica.com/help-files/etabs/Menus/File/Saving_Models.htm)

### Release Notes
- [ETABS v19.0.0](http://installs.csiamerica.com/software/ETABS/19/ReleaseNotesETABSv1900.pdf)
- [ETABS v19.1.0](http://installs.csiamerica.com/software/ETABS/19/ReleaseNotesETABSv1910.pdf)
- [ETABS v20.0.0](https://www.csiamerica.com/software/ETABS/20/ReleaseNotesETABSv2000.pdf)
- [ETABS v20.2.0](https://www.csiamerica.com/software/ETABS/20/ReleaseNotesETABSv2020.pdf)
- [ETABS v21.0.0](https://www.csiamerica.com/software/ETABS/21/ReleaseNotesETABSv2100.pdf)
- [ETABS v21.1.0](https://www.csiamerica.com/software/ETABS/21/ReleaseNotesETABSv2110.pdf)
- [ETABS v22.0.0](https://www.csiamerica.com/software/ETABS/22/ReleaseNotesETABSv2200.pdf)
- [ETABS v22.1.0](https://www.csiamerica.com/software/ETABS/22/ReleaseNotesETABSv2210plus2200.pdf)

### GitHub Repositories
- [ebrahimraeyat/etabs_api](https://github.com/ebrahimraeyat/etabs_api)
- [danielogg92/Etabs-API-Python](https://github.com/danielogg92/Etabs-API-Python)
- [jantozor/CSiAPIExamples](https://github.com/jantozor/CSiAPIExamples)
- [BHoM/ETABS_Toolkit](https://github.com/BHoM/ETABS_Toolkit)
- [enthought/comtypes (issues)](https://github.com/enthought/comtypes/issues/182)

### Tutoriales y Blogs
- [EngineeringSkills - ETABS Python API](https://www.engineeringskills.com/posts/an-introduction-to-the-etabs-python-api)
- [Stru.ai - ETABS API Beginner Guide](https://stru.ai/blog/etabs-api-beginner-guide)
- [Stru.ai - Master ETABS API 2025](https://stru.ai/blog/etabs-api-automation-2025)
- [Stru.ai - Seismic Automation](https://stru.ai/blog/etabs-seismic-automation)
- [Stru.ai - Post-Processing](https://stru.ai/blog/etabs-post-processing-automation)
- [Stru.ai - Automate Analysis](https://stru.ai/blog/automate-etabs-analysis-python)
- [NeutralAXIS - Getting Started](https://neutralaxis.github.io/ETABS/ETABS%20API/Getting_Started/)
- [NeutralAXIS - Introduction](https://neutralaxis.github.io/ETABS/ETABS%20API/Introduction/)
- [Sheer Force Engineering - API Speed Secrets](https://sheerforceeng.com/2021/09/17/etabs-oapi-api-how-to-crack-automation-speed-secrets-using-vba-and-excel/)
- [re-tug.com - Database Tables](https://re-tug.com/post/etabs-api-more-examples-database-tables/18)
- [Python for Structural Engineers](https://pythonforstructuralengineers.com/etabs-automation/)
- [VIKTOR.AI - ETABS Post-Processing](https://www.viktor.ai/blog/200/etabs-model-post-processing-ai-python)
- [kinson.io - Plugin Quickstart](https://kinson.io/posts/etabs-plugin-quickstart)

### Hakan Keskin (Medium)
- [Story Drifts & Joint Displacements](https://hakan-keskin.medium.com/extracting-story-drifts-and-joint-displacements-in-etabs-with-python-6b886aac89ba)
- [Modal Analysis & Base Reactions](https://hakan-keskin.medium.com/extracting-modal-analysis-results-and-base-reactions-in-etabs-with-python-af12da00ca5f)
- [CSI API Tool](https://hakan-keskin.medium.com/csi-api-tool-python-integration-with-etabs-sap2000-and-safe-516f60a19e6c)

### Eng-Tips Discussions
- [Database Tables Edit](https://www.eng-tips.com/threads/etabs-api-using-python-database-tables-edit.494947/)
- [ETABS API with Python](https://www.eng-tips.com/threads/etabs-api-with-python.492251/)
- [Error Attaching to ETABS](https://www.eng-tips.com/threads/error-when-getting-python-to-attach-to-etabs.477451/)
- [v18 Cannot Attach](https://www.eng-tips.com/threads/etabs-v18-api-cannot-attach-python-with-etabs.477710/)
- [Add New Mass Source](https://www.eng-tips.com/threads/etabs-api-add-new-mass-source.521909/)
- [Analysis Results](https://www.eng-tips.com/threads/etabs-api-python-quot-analysis-result-quot.514827/)
- [Section Cut Definition](https://www.eng-tips.com/threads/etabs-api-troubles-section-cut-definition.502839/)
- [Database Tables Locked Model](https://www.eng-tips.com/threads/etabs-api-database-tables-apply-changes-while-model-is-locked.516535/)

### ResearchGate
- [Define Response Spectrum via OAPI](https://www.researchgate.net/post/How_to_define_a_response_spectrum_function_in_ETABS_SAP2000_using_OAPI)
- [ETABS Topic (194 Q&A)](https://www.researchgate.net/topic/ETABS)

### Otros
- [Scribd: CSI API ETABS v1](https://www.scribd.com/document/929780873/Csi-API-Etabs-v1)
- [Scribd: ETABS API](https://www.scribd.com/document/402220969/ETABS-API)
- [Corrupted EDB Recovery Blog](https://engrdennisbmercado.wordpress.com/2020/09/25/the-edb-et-and-e2k-got-corrupted-what-now/)
- [comtypes clear_cache issue #182](https://github.com/enthought/comtypes/issues/182)
- [comtypes GetActiveObject issue #141](https://github.com/enthought/comtypes/issues/141)

---

## RESUMEN EJECUTIVO PARA NUESTRO PROYECTO

### Lo que confirma nuestra experiencia previa:
1. **CreateObject instancia invisible** — Bug REAL, documentado. Fix: forzar Visible=True o usar GetActiveObject.
2. **File.Save corrupto via COM sin UI** — Bug REAL. Fix: abrir ETABS manualmente primero.
3. **comtypes.gen stale** — Bug REAL. Fix: limpiar cache ANTES de import.
4. **RPC server unavailable** — Problema de sesion COM larga. Fix: separar en fases.
5. **SetFromFile no existe** — Confirmado que no hay metodo nativo. Fix: usar SetUser() con arrays.
6. **SetMassSource_1 funciona** — Firma confirmada: 6 parametros. Nuestro codigo deberia funcionar.

### Acciones para la proxima sesion de lab:
1. Usar `SapModel.Func.FuncRS.SetUser()` en vez de `SetFromFile` — SOLUCION DEFINITIVA
2. Separar pipeline en 2 sesiones COM (geometria / analisis)
3. Limpiar comtypes.gen al inicio de cada fase
4. Siempre conectar via GetActiveObject (abrir ETABS manualmente primero)
5. Verificar ret == 0 despues de cada operacion critica
