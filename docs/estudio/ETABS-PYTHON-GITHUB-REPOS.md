# ETABS + Python Automation -- Repos GitHub Verificados

**Investigacion realizada**: 20 marzo 2026
**Fuente**: GitHub API (busquedas: "etabs python", "etabs comtypes", "pyetabs", "etabs automation", "csi etabs python", "SapModel comtypes")
**Total encontrado**: ~50 repos, 8 significativos con codigo real

---

## Resumen de Repos Encontrados

| # | Repo | Stars | Updated | Descripcion |
|---|------|-------|---------|-------------|
| 1 | **danielogg92/Etabs-API-Python** | 67 | 2026-01 | Funciones wrapper para CSI ETABS API |
| 2 | **mitchell-tesch/CSiPy** (pytabs) | 38 | 2025-12 | Wrapper Python completo para CSi .NET API |
| 3 | **youandvern/ETABS_building_drift_check** | 21 | 2026-02 | Verificacion drift + torsion con PyQt5 GUI |
| 4 | **retug/ETABs** | 19 | 2026-01 | Scripts ETABS API: diaphragm slicer, DB tables |
| 5 | **mihdicaballero/ETABS-Ninja** | 14 | 2025-12 | Coleccion funciones Python para ETABS API |
| 6 | **kaka4348/PYEtabs** | 2 | 2023-09 | Wrapper basico |
| 7 | **seybaskan/ETABS-TBDY2018-Automation** | 1 | 2026-02 | Verificaciones TBDY 2018 (norma turca) |
| 8 | **Kodestruct/Kodestruct.ETABS** | 7 | 2025-03 | C# - Dynamo + ETABS 2016 (no Python) |

---

## 1. danielogg92/Etabs-API-Python (67 stars, MIT)
**URL**: https://github.com/danielogg92/Etabs-API-Python
**Archivos**: Main.py, Etabs_Get_Functions.py, Etabs_Set_Functions.py, Database_Tables.py
**Enfoque**: Australia (AS3600), funciones wrapper limpias

### 1.1 Conexion a ETABS -- DOS METODOS

```python
# Fuente: danielogg92/Etabs-API-Python/Main.py

# METODO 1: GetActiveObject (ETABS ya abierto)
import comtypes.client
import sys

def connect_to_etabs():
    try:
        EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
    SapModel = EtabsObject.SapModel
    return SapModel, EtabsObject

# METODO 2: Helper + GetObject (ETABS v2019+)
def connect_to_etabs_2019():
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    try:
        myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
    SapModel = myETABSObject.SapModel
    return SapModel, myETABSObject, helper
```

### 1.2 Story Data

```python
# Fuente: danielogg92/Etabs-API-Python/Main.py
def get_story_data(SapModel):
    story_in = SapModel.Story.GetStories()
    nos_stories = story_in[0]
    story_nms = story_in[1]
    story_eles = story_in[2]
    story_hgts = story_in[3]
    is_master_story = story_in[4]
    similar_to_story = story_in[5]
    splice_above = story_in[6]
    splice_height = story_in[7]
    story_data = []
    for i in range(len(story_nms)):
        j = -1 - i  # reversa para orden descendente
        story_data.append([story_nms[j], round(story_hgts[j],3),
                           round(story_eles[j],3), is_master_story[j],
                           similar_to_story[j], splice_above[j], splice_height[j]])
    return story_data
```

### 1.3 Unidades

```python
# Fuente: danielogg92/Etabs-API-Python/Main.py
def set_etabs_units(SapModel, length="mm", force="N"):
    if length == "mm" and force == "N":
        SapModel.SetPresentUnits(9)      # N_mm_C
    elif length == "mm" and force == "kN":
        SapModel.SetPresentUnits(5)      # kN_mm_C
    elif length == "m" and force == "N":
        SapModel.SetPresentUnits(10)     # N_m_C
    elif length == "m" and force == "kN":
        SapModel.SetPresentUnits(6)      # kN_m_C
```

### 1.4 Obtener TODOS los Frames

```python
# Fuente: danielogg92/Etabs-API-Python/Etabs_Get_Functions.py
def get_all_frames(SapModel):
    frame_objs = SapModel.FrameObj.GetAllFrames()
    frames = []
    for i in range(frame_objs[0]):
        frames.append([
            frame_objs[1][i],   # frameNm
            frame_objs[2][i],   # prop
            frame_objs[3][i],   # story
            frame_objs[4][i],   # pt1
            frame_objs[5][i],   # pt2
            frame_objs[6][i],   # x1
            frame_objs[7][i],   # y1
            frame_objs[8][i],   # z1
            frame_objs[9][i],   # x2
            frame_objs[10][i],  # y2
            frame_objs[11][i],  # z2
            frame_objs[12][i],  # rot
            frame_objs[13][i],  # offX1
            frame_objs[14][i],  # offY1
            frame_objs[15][i],  # offZ1
            frame_objs[16][i],  # offX2
            frame_objs[17][i],  # offY2
            frame_objs[18][i],  # offZ2
            frame_objs[19][i],  # cardPt
        ])
    return frames
```

### 1.5 Obtener Materiales (Concreto y Acero con propiedades)

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
            mat_conc_prop = SapModel.PropMaterial.GetOConcrete_1(mat_name)
            conc_fc = mat_conc_prop[0]
            materials[mat_name] = {'mat_name': mat_name, 'mat_type': mat_type, 'fc': conc_fc}
        elif mat_type == 'Steel':
            mat_steel_prop = SapModel.PropMaterial.GetOSteel_1(mat_name)
            steel_fy = mat_steel_prop[0]
            steel_fu = mat_steel_prop[1]
            materials[mat_name] = {'mat_name': mat_name, 'mat_type': mat_type,
                                   'fy': steel_fy, 'fu': steel_fu}
        else:
            materials[mat_name] = {'mat_name': mat_name, 'mat_type': mat_type}
    return materials
```

### 1.6 Crear Materiales (Concreto australiano como ejemplo)

```python
# Fuente: danielogg92/Etabs-API-Python/Etabs_Set_Functions.py
def add_australia_conc_materials(SapModel, delete_existing=False):
    conc_grade = [25, 32, 40, 50, 65, 80, 100]
    for grade in conc_grade:
        conc_nm = "CONC-" + str(grade)
        SapModel.PropMaterial.AddMaterial(conc_nm, 2, "User", "AS3600",
                                         str(grade) + 'MPa', UserName=conc_nm)
        # Propiedades del concreto
        SapModel.PropMaterial.SetOConcrete(conc_nm, grade,
            False,   # isLightweight
            0.0,     # fcsFact
            2,       # SSType (Mander)
            4,       # SSHysType (Takeda)
            0.003,   # strainAtFc
            0.0035)  # strainAtUlt
        # Propiedades isotropicas
        conc_E = {25:26700, 32:30100, 40:32800, 50:34800,
                  65:37400, 80:39600, 100:42200}
        SapModel.PropMaterial.SetMPIsotropic(conc_nm, conc_E[grade], 0.2, 10e-6)
        SapModel.PropMaterial.SetWeightAndMass(conc_nm, 1, 24.6e-6)
```

### 1.7 Database Tables

```python
# Fuente: danielogg92/Etabs-API-Python/Database_Tables.py
def get_all_db_tables(SapModel):
    """import types: 0=not importable, 1=importable, 2=interactive unlocked, 3=interactive always"""
    table_data = SapModel.DatabaseTables.GetAllTables()
    all_tables = {}
    for i in range(table_data[0]):
        table_key = table_data[1][i]
        all_tables[table_key] = {
            'table_name': table_data[2][i],
            'import_type': table_data[3][i],
            'is_empty': table_data[4][i]
        }
    return all_tables

def get_spandrel_design(SapModel):
    """Ejemplo: leer tabla de diseno de spandrels AS3600"""
    table_key = 'Shear Wall Spandrel Design Summary - AS 3600-2018'
    spandrel_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName='')
    FieldsKeysIncluded = spandrel_db[2]
    NosFields = len(FieldsKeysIncluded)
    NumberRecords = spandrel_db[3]
    TableData = spandrel_db[4]
    spandrels = {}
    for i in range(NumberRecords):
        Story = TableData[i*NosFields + 0]
        Spandrel = TableData[i*NosFields + 1]
        # ... extraer cada campo por indice ...
    return spandrels
```

---

## 2. mitchell-tesch/CSiPy (pytabs) (38 stars, MIT)
**URL**: https://github.com/mitchell-tesch/CSiPy
**Arquitectura**: Wrapper OOP completo, usa .NET API (no comtypes COM directo), pythonnet
**Archivos clave**: src/pytabs/model.py, 30+ modulos de interfaces

### 2.1 Conexion (wrapper sofisticado con .NET)

```python
# Fuente: mitchell-tesch/CSiPy/src/pytabs/model.py
from .etabs_config import etabs, pytabs_config
from .error_handle import handle, EtabsError

class EtabsModel:
    def __init__(self, attach_to_instance=True, specific_etabs=False,
                 specific_etabs_path='', model_path='', remote_computer=''):
        helper = etabs.cHelper(etabs.Helper())

        if attach_to_instance:
            try:
                if remote_computer:
                    self.etabs_object = etabs.cOAPI(
                        helper.GetObjectHost(remote_computer, 'CSI.ETABS.API.ETABSObject'))
                else:
                    self.etabs_object = etabs.cOAPI(
                        helper.GetObject('CSI.ETABS.API.ETABSObject'))
                self.active = True
            except Exception as e:
                raise EtabsError(-1, 'No running instance ETABS found')
        else:
            if specific_etabs:
                self.etabs_object = etabs.cOAPI(
                    helper.CreateObject(str(specific_etabs_path)))
            else:
                self.etabs_object = etabs.cOAPI(
                    helper.CreateObjectProgID('CSI.ETABS.API.ETABSObject'))
            self.etabs_object.ApplicationStart()
            self.active = True

        if self.active:
            self.sap_model = etabs.cSapModel(self.etabs_object.SapModel)
            self.file = etabs.cFile(self.sap_model.File)
            # Inicializar TODAS las interfaces como atributos
            self.analyse = Analyse(self.sap_model)
            self.analysis_results = AnalysisResults(self.sap_model)
            self.area_obj = AreaObj(self.sap_model)
            self.combo = Combo(self.sap_model)
            self.database_tables = DatabaseTables(self.sap_model)
            self.frame_obj = FrameObj(self.sap_model)
            self.load_cases = LoadCases(self.sap_model)
            self.load_patterns = LoadPatterns(self.sap_model)
            self.story = Story(self.sap_model)
            # ... 20+ interfaces mas ...

    def exit_application(self):
        self.etabs_object.ApplicationExit(False)
        self.sap_model = None
        self.active = False

    def open_model(self, model_path):
        handle(self.file.OpenFile(str(model_path)))
        self.model_open = True

    def set_present_units(self, units):
        handle(self.sap_model.SetPresentUnits(units))
```

**NOTA IMPORTANTE**: CSiPy soporta **computador remoto** via `GetObjectHost` y `CreateObjectHost`.
Tiene 30+ interfaces separadas (AreaObj, FrameObj, Combo, LoadPatterns, etc).

---

## 3. youandvern/ETABS_building_drift_check (21 stars)
**URL**: https://github.com/youandvern/ETABS_building_drift_check
**Enfoque**: GUI PyQt5 para verificar drift y torsion automaticamente
**Incluye**: Modelo .EDB de prueba

### 3.1 Clase EtabsModel completa (abrir, analizar, resultados)

```python
# Fuente: youandvern/ETABS_building_drift_check/APItest.py
class EtabsModel:
    def __init__(self, modelpath,
                 etabspath="C:/Program Files/Computers and Structures/ETABS 17/ETABS.exe",
                 existinstance=False, specprogpath=False):

        self.AttachToInstance = existinstance
        self.ProgramPath = etabspath
        self.FullPath = modelpath

        if self.AttachToInstance:
            # Conectar a instancia existente
            self.myETABSObject = comtypes.client.GetActiveObject(
                "CSI.ETABS.API.ETABSObject")
        else:
            # Crear nueva instancia
            self.helper = comtypes.client.CreateObject('ETABSv17.Helper')
            self.helper = self.helper.QueryInterface(comtypes.gen.ETABSv17.cHelper)
            if self.SpecifyPath:
                self.myETABSObject = self.helper.CreateObject(self.ProgramPath)
            else:
                self.myETABSObject = self.helper.CreateObjectProgID(
                    "CSI.ETABS.API.ETABSObject")
            self.myETABSObject.ApplicationStart()

        # Inicializar modelo
        self.SapModel = self.myETABSObject.SapModel
        self.SapModel.InitializeNewModel()
        self.SapModel.File.OpenFile(self.FullPath)

        # Correr analisis
        self.SapModel.Analyze.RunAnalysis()

        # Obtener combos de drift
        [self.NumberCombo, self.ComboNames, ret] = \
            self.SapModel.RespCombo.GetNameList(0, [])
        self.DriftCombos = [c for c in self.ComboNames if "drift" in c.lower()]
```

### 3.2 Resultados de Drift

```python
# Fuente: youandvern/ETABS_building_drift_check/APItest.py
def story_drift_results(self, dlimit=0.01):
    self.StoryDrifts = []
    for dcombo in self.DriftCombos:
        self.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        self.SapModel.Results.Setup.SetComboSelectedForOutput(dcombo)

        NumberResults = 0
        Stories = []; LoadCases = []; StepTypes = []; StepNums = []
        Directions = []; Drifts = []; Labels = []
        Xs = []; Ys = []; Zs = []

        [NumberResults, Stories, LoadCases, StepTypes, StepNums,
         Directions, Drifts, Labels, Xs, Ys, Zs, ret] = \
            self.SapModel.Results.StoryDrifts(
                NumberResults, Stories, LoadCases, StepTypes, StepNums,
                Directions, Drifts, Labels, Xs, Ys, Zs)

        for i in range(NumberResults):
            self.StoryDrifts.append((
                Stories[i], LoadCases[i], Directions[i],
                Drifts[i], Drifts[i] / dlimit))

    labels = ['Story', 'Combo', 'Direction', 'Drift', 'DCR(Drift/Limit)']
    df = pd.DataFrame.from_records(self.StoryDrifts, columns=labels)
    return df.sort_values(by=['Drift'], ascending=False)
```

### 3.3 Verificacion de Torsion (JointDrifts)

```python
# Fuente: youandvern/ETABS_building_drift_check/APItest.py
def story_torsion_check(self):
    self.JointDisplacements = []
    for dcombo in self.DriftCombos:
        self.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        self.SapModel.Results.Setup.SetComboSelectedForOutput(dcombo)

        [NumberResults, Stories, Label, Names, LoadCases,
         StepType, StepNum, DispX, DispY, DriftX, DriftY, ret] = \
            self.SapModel.Results.JointDrifts(
                0, [], '', '', [], [], [], [], [], [], [])

        for i in range(NumberResults):
            self.JointDisplacements.append((
                Label[i], Stories[i], LoadCases[i], DispX[i], DispY[i]))

    jdf = pd.DataFrame.from_records(self.JointDisplacements,
                                     columns=['label','Story','Combo','DispX','DispY'])
    # Calcular ratio torsion: max/avg por piso y combo
    for dcombo in self.DriftCombos:
        for story in jdf.Story.unique():
            temp_df = jdf[(jdf['Story'] == story) & (jdf['Combo'] == dcombo)]
            averaged = abs(temp_df['DispX'].mean())
            maximumd = temp_df['DispX'].abs().max()
            ratiod = maximumd / averaged
            # Si avg(Y) > avg(X), cambiar direccion
```

---

## 4. retug/ETABs (19 stars, MIT)
**URL**: https://github.com/retug/ETABs
**Enfoque**: Diaphragm slicer tool + Database Tables
**Nota**: Trabaja con ETABSv19, comtypes v1.1.7

### 4.1 Conexion y Section Cuts automaticos

```python
# Fuente: retug/ETABs/01-Diaphragm Slicer/section_cut_tool.py
import comtypes.client
import numpy as np

ProgramPath = r"C:\Program Files\Computers and Structures\ETABS 19\ETABS.exe"
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
SapModel = ETABSObject.SapModel
SapModel.SetPresentUnits(4)  # kip, ft, F
SapModel.SetModelIsLocked(False)  # DESBLOQUEAR para crear section cuts
```

### 4.2 Leer Areas seleccionadas + obtener puntos

```python
# Fuente: retug/ETABs/01-Diaphragm Slicer/section_cut_tool.py
areas = SapModel.SelectObj.GetSelected()
area_obj = []
for type_obj, beam_num in zip(areas[1], areas[2]):
    if type_obj == 5:   # 5 = Area object
        area_obj.append(beam_num)

AreaInfo = []
PointData = []
for area in area_obj:
    AreaInfo.append(SapModel.AreaObj.GetPoints(area))
    pts = SapModel.AreaObj.GetPoints(area)[1]
    for pnt in pts:
        PointData.append(SapModel.PointObj.GetCoordCartesian(pnt)[0:3])
```

### 4.3 Crear Section Cuts via Database Tables

```python
# Fuente: retug/ETABs/01-Diaphragm Slicer/section_cut_tool.py
TableKey = 'Section Cut Definitions'
TableVersion = 1
FieldsKeysIncluded = [
    'Name', 'Defined By', 'Group', 'Result Type', 'Result Location',
    'Location X', 'Location Y', 'Location Z',
    'Rotation About Z', 'Rotation About Y', 'Rotation About X',
    'Axis Angle', 'Element Side',
    'Number of Quads', 'Quad Number', 'Point Number',
    'Quad X', 'Quad Y', 'Quad Z', 'GUID'
]
NumberRecords = len(flat_etabs_data)

SapModel.DatabaseTables.SetTableForEditingArray(
    TableKey, TableVersion, FieldsKeysIncluded, NumberRecords, mega_data)
SapModel.DatabaseTables.ApplyEditedTables(FillImport=True)
```

### 4.4 Obtener resultados de Section Cut

```python
# Fuente: retug/ETABs/01-Diaphragm Slicer/section_cut_tool.py
SapModel.Analyze.RunAnalysis()
SapModel.SetPresentUnits(4)
SapModel.Results.Setup.SetCaseSelectedForOutput("EQY+")

test_cut = SapModel.Results.SectionCutAnalysis(
    NumberResults, SCut, LoadCase, StepType, StepNum,
    F1, F2, F3, M1, M2, M3)

shear = test_cut[6]    # F1 = corte
moment = test_cut[10]  # M3 = momento
```

---

## 5. mihdicaballero/ETABS-Ninja (14 stars, MIT)
**URL**: https://github.com/mihdicaballero/ETABS-Ninja
**Enfoque**: Verificacion drift/torsion con graficos matplotlib, norma argentina
**Arquitectura**: Paquete Python con interface.py, get_functions.py, get_database.py, settings.py

### 5.1 Conexion via Helper.GetObject

```python
# Fuente: mihdicaballero/ETABS-Ninja/etabsninja/interface.py
import comtypes.client
import sys

# Helper se crea a nivel de modulo (global)
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

def connect_to_etabs():
    try:
        EtabsObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
    SapModel = EtabsObject.SapModel
    return SapModel, EtabsObject

def disconnect_from_etabs(etabs_object, sapmodel, close=False):
    if close:
        etabs_object.ApplicationExit(False)
    sapmodel = None
    etabs_object = None
```

### 5.2 Database Tables a DataFrame (patron generico)

```python
# Fuente: mihdicaballero/ETABS-Ninja/etabsninja/get_database.py
import pandas as pd

class DatabaseTables:
    def __init__(self, SapModel=None, etabs=None):
        self.SapModel = SapModel if SapModel else etabs.SapModel

    @staticmethod
    def reshape_data_to_df(table, cols=None):
        FieldsKeysIncluded = table[2]
        table_data = table[4]
        n = len(FieldsKeysIncluded)
        data = [list(table_data[i:i+n]) for i in range(0, len(table_data), n)]
        df = pd.DataFrame(data, columns=FieldsKeysIncluded)
        if cols is not None:
            df = df[cols]
        return df

    def table_exist(self, table_key):
        all_table = self.SapModel.DatabaseTables.GetAvailableTables()[1]
        return table_key in all_table

    def read_table(self, table_key):
        if not self.table_exist(table_key):
            return None
        return self.SapModel.DatabaseTables.GetTableForDisplayArray(
            table_key, [], table_key, 0, [], 0, [])
```

### 5.3 Story Drifts via Database Tables (alternativa a Results API)

```python
# Fuente: mihdicaballero/ETABS-Ninja/etabsninja/get_functions.py
class Results:
    def __init__(self, SapModel):
        self._SapModel = SapModel
        self._settings = Settings()
        self._LoadCaseList = self._settings.LoadCaseList

    def StoryDriftsForStories(self):
        self._SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(self._LoadCaseList)
        TableName = "Story Drifts"
        TableFields = self._SapModel.DatabaseTables.GetAllFieldsInTable(TableName)[2]
        JointDrifts = self._SapModel.DatabaseTables.GetTableForDisplayArray(
            TableName, TableFields, "All")[4]
        TableFieldsIncluded = self._SapModel.DatabaseTables.GetTableForDisplayArray(
            TableName, TableFields, "All")[2]

        NumColumns = len(TableFieldsIncluded)
        joint_drifts_array = [JointDrifts[i:i+NumColumns]
                              for i in range(0, len(JointDrifts), NumColumns)]
        df = pd.DataFrame(joint_drifts_array, columns=TableFieldsIncluded)
        df[['Drift']] = df[['Drift']].astype(float)
        df = df.groupby(['Story','Direction'])[['Drift']].agg(['max'])
        # ... pivotear y graficar ...
        return df
```

### 5.4 Crear secciones de columnas

```python
# Fuente: mihdicaballero/ETABS-Ninja/etabsninja/set_functions.py
def create_circular_section(sapmodel, concrete_material, longitudinal_material,
                            tie_material, section_diameter, clear_cover,
                            num_longitudinal_bars, longitudinal_bar_diameter,
                            tie_bar_diameter, tie_spacing):
    section_name = f"Circular-D{section_diameter}-{concrete_material}"
    sapmodel.PropFrame.SetCircle(section_name, concrete_material, section_diameter)
    ret = sapmodel.FrameObj.SetRebarColumn(
        section_name, longitudinal_material, tie_material,
        2,    # pattern
        1,    # confine type
        clear_cover, num_longitudinal_bars, 0, 0,
        longitudinal_bar_diameter, tie_bar_diameter, tie_spacing,
        0, 0, False)
```

### 5.5 Settings (configuracion por proyecto)

```python
# Fuente: mihdicaballero/ETABS-Ninja/etabsninja/settings.py
class Settings:
    def __init__(self):
        self.LoadCaseList = ["W Service"]
        self.max_InterstoryDrift = 1/400
        self.JointsGroupName = "Nodos"
        self.max_BuildingDrift = 1/400
```

---

## Patrones Comunes Identificados

### A. Conexion COM -- 3 Variantes encontradas en repos reales

| Variante | Repos que la usan | Codigo |
|----------|-------------------|--------|
| **GetActiveObject** | danielogg92 (metodo 1), youandvern | `comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")` |
| **Helper.GetObject** | danielogg92 (metodo 2), mihdicaballero, retug | `helper.GetObject("CSI.ETABS.API.ETABSObject")` |
| **Helper.CreateObject** | youandvern, CSiPy | `helper.CreateObject(ProgramPath)` |

**Consenso**: Todos los repos usan `comtypes.client` (no pythonnet) excepto CSiPy que usa .NET API via pythonnet.

### B. ProgID por version de ETABS

| ProgID | Version |
|--------|---------|
| `ETABSv17.Helper` | ETABS 17 |
| `ETABSv1.Helper` | ETABS 18, 19, 20, 21+ (universal) |
| `CSI.ETABS.API.ETABSObject` | Todas las versiones |

### C. Unidades -- Constantes usadas en repos reales

| Valor | Unidades | Repo que lo usa |
|-------|----------|-----------------|
| 3 | kip_in_F | mihdicaballero |
| 4 | kip_ft_F | retug |
| 5 | kN_mm_C | danielogg92 |
| 6 | kN_m_C | danielogg92 |
| 9 | N_mm_C | danielogg92 |
| 10 | N_m_C | danielogg92 |

### D. Patron DatabaseTables -- GetTableForDisplayArray

Todos los repos que leen tablas usan el mismo patron:
```python
table = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName)
# table[0] = GroupName
# table[1] = TableVersion
# table[2] = FieldsKeysIncluded (lista de nombres de columnas)
# table[3] = NumberRecords
# table[4] = TableData (lista plana, reshape con n = len(fields))
```

Reshape a DataFrame:
```python
n = len(table[2])
data = [list(table[4][i:i+n]) for i in range(0, len(table[4]), n)]
df = pd.DataFrame(data, columns=table[2])
```

### E. Patron Results API -- StoryDrifts

```python
SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
SapModel.Results.Setup.SetComboSelectedForOutput(combo_name)
[NumberResults, Stories, LoadCases, StepTypes, StepNums,
 Directions, Drifts, Labels, Xs, Ys, Zs, ret] = \
    SapModel.Results.StoryDrifts(0, [], [], [], [], [], [], [], [], [], [])
```

### F. Patron Results API -- SectionCutAnalysis

```python
SapModel.Results.Setup.SetCaseSelectedForOutput("EQY+")
result = SapModel.Results.SectionCutAnalysis(
    NumberResults, SCut, LoadCase, StepType, StepNum,
    F1, F2, F3, M1, M2, M3)
# result[6] = F1 (corte), result[10] = M3 (momento)
```

---

## Utilidades Interesantes

### 1. Verificador Pass/Fail con colorama (ETABS-Ninja)
```python
# mihdicaballero/ETABS-Ninja/etabsninja/general_functions.py
from colorama import Fore, Style
def FU(element, value, comparison_value):
    DCR = value / comparison_value
    if value < comparison_value:
        msg = f"{element}: {value} < {comparison_value}. OK. {DCR*100:.0f}% DCR"
        print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")
    else:
        msg = f"{element}: {value} >= {comparison_value}. NG! {DCR*100:.0f}% DCR"
        print(f"{Fore.RED}{msg}{Style.RESET_ALL}")
```

### 2. GUI PyQt5 completa (youandvern)
- Abre modelo ETABS
- Corre analisis automaticamente
- Filtra combos con "drift" en el nombre
- Muestra tabla drift + tabla torsion lado a lado
- Exporta a Excel

### 3. Diaphragm Slicer automatico (retug)
- Selecciona areas de losa
- Genera N section cuts automaticos a lo largo del diafragma
- Obtiene corte y momento en cada seccion
- Grafica distribucion de fuerzas del diafragma

### 4. CSiPy: Wrapper completo con 30+ interfaces tipadas
- Soporte computador remoto
- Error handling centralizado
- Enumeraciones tipadas
- Open/Save/Close model

---

## Relevancia para nuestro pipeline taller-etabs

| Patron del repo | Aplicabilidad a nuestro pipeline |
|-----------------|----------------------------------|
| `ETABSv1.Helper` + `GetObject` | Ya lo usamos, confirmado correcto |
| `GetActiveObject` como fallback | Alternativa viable si Helper falla |
| `SetPresentUnits(6)` para kN_m_C | Confirma nuestro uso (Chile = kN, m) |
| DatabaseTables reshape | Mejor que Results API para drift/torsion post-analisis |
| `SetModelIsLocked(False)` antes de editar | Importante para Section Cuts |
| `ApplicationExit(False)` para cerrar | Patron confirmado en todos los repos |
| Helper a nivel de modulo (global) | ETABS-Ninja lo hace, evita problemas GC |
| `InitializeNewModel()` antes de `OpenFile` | Solo youandvern lo hace, no siempre necesario |

---

## Notas sobre versiones ETABS

- **ETABSv17.Helper**: Solo para ETABS 17 (youandvern)
- **ETABSv1.Helper**: Universal para v18+ (danielogg92 metodo 2, mihdicaballero, retug)
- **comtypes.gen.ETABSv1.cHelper**: QueryInterface necesario para acceder a metodos tipados
- **comtypes.gen.ETABSv17.cHelper**: Lo mismo pero v17
- Ningun repo usa `comtypes.gen` stale cleanup explicito (nosotros si lo necesitamos)
