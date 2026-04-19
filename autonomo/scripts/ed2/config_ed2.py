"""
config_ed2.py - Configuracion y conexion COM para pipeline ETABS 21
Edificio 2: 5 pisos de marcos HA, Antofagasta - Taller ADSE UCN 1S-2026

Este modulo centraliza:
  - Conexion COM robusta a ETABS 21 (comtypes)
  - Datos completos del edificio (grilla, pisos, materiales, secciones)
  - Geometria de columnas, vigas y losas (marcos, sin muros)
  - Parametros sismicos NCh433/DS61
  - Funciones helper (connect, disconnect, verify, formulas)

Firmas COM verificadas contra:
  - autonomo/research/com_signatures.md (R03)
  - docs.csiamerica.com API 2016
  - Repos: danielogg92, ebrahimraeyat, mihdicaballero, mtavares51

Uso:
  >>> from config_ed2 import connect, disconnect, get_model
  >>> model = connect()
  >>> # ... operaciones ETABS ...
  >>> disconnect()

Fuente datos: Enunciado Taller ADSE 1S-2026 pags 8-13, Prof. Music
              autonomo/research/ed2_datos_enunciado.md (datos verificados)
Normas: NCh433 Mod 2009, DS61, DS60, ACI318-08, NCh3171, NCh1537

# =====================================================================
# Template: autonomo/scripts/config.py (Ed.1)
# Adaptado para Edificio 2 — Marcos HA, 5 pisos, planta regular 32.5x32.5m
# =====================================================================
"""

import os
import sys
import math
import time
import shutil
import logging

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
log = logging.getLogger("etabs_config_ed2")
if not log.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    log.addHandler(_h)
    log.setLevel(logging.INFO)

# ===================================================================
# SECCION 1: CONSTANTES ETABS (eUnits, eMatType, etc.)
# Fuente: com_signatures.md / etabs_api_reference.md
# ===================================================================

# eUnits — sistema de unidades del modelo
UNITS_TONF_M_C = 12          # Tonf, m, C — unidades del proyecto
UNITS_KGF_M_C = 8            # kgf, m, C (etabs_api_reference.md §21.1)
UNITS_KN_M_C = 6             # kN, m, C

# eMatType — tipos de material
MAT_STEEL = 1
MAT_CONCRETE = 2
MAT_NODESIGN = 3
MAT_ALUMINUM = 4
MAT_COLDFORMED = 5
MAT_REBAR = 6
MAT_TENDON = 7

# eLoadPatternType — tipos de patron de carga (etabs_api_reference.md §21.3)
LTYPE_DEAD = 1
LTYPE_SUPERDEAD = 2
LTYPE_LIVE = 3
LTYPE_REDUCELIVE = 4
LTYPE_QUAKE = 5
LTYPE_WIND = 6
LTYPE_SNOW = 7
LTYPE_OTHER = 8
LTYPE_ROOFLIVE = 11          # LiveRoof=11, NOT 12 (12=Notional)

# eShellType — com_signatures.md §4.1
SHELL_THIN = 1               # ShellThin (Kirchhoff, sin corte transversal)
SHELL_THICK = 2              # ShellThick (Mindlin-Reissner, CON corte transversal)
SHELL_MEMBRANE = 3           # Solo membrana (sin flexion)
SHELL_SHELL = 5              # Shell generico
SHELL_LAYERED = 6            # Layered/compuesto

# eSlabType
SLAB_SLAB = 0
SLAB_DROP = 1
SLAB_STIFF = 2
SLAB_RIBBED = 3
SLAB_WAFFLE = 4

# Cardinal Points (para vigas) — CSI ETABS convention
# 1=BottomLeft, 2=BottomCenter, 3=BottomRight, 4=MiddleLeft,
# 5=MiddleCenter, 6=MiddleRight, 7=TopLeft, 8=TopCenter,
# 9=TopRight, 10=Centroid, 11=ShearCenter
CP_BOTTOM_LEFT = 1
CP_BOTTOM_CENTER = 2        # Vigas invertidas (Ed.1)
CP_BOTTOM_RIGHT = 3
CP_TOP_CENTER = 8
CP_CENTROID = 10             # Vigas normales (Ed.2)

# ProgID COM — ETABS 21 target
ETABS_PROGID = "CSI.ETABS.API.ETABSObject"
# Helper ProgIDs to try in order (v1 works for v18-v22+, v17 is legacy fallback)
HELPER_PROGIDS = ["ETABSv1.Helper", "ETABSv17.Helper"]
HELPER_PROGID = "ETABSv1.Helper"   # Primary — works for ETABS v18-v22+

# Environment overrides for console execution / pipeline orchestration
ENV_CREATE_IF_MISSING = "ED2_ETABS_CREATE_IF_MISSING"
ENV_MODEL_PATH = "ED2_ETABS_MODEL_PATH"
ENV_FORCE_MODEL_OPEN = "ED2_ETABS_FORCE_MODEL_OPEN"
ENV_RUNTIME_ROOT = "ED2_RUNTIME_ROOT"

# Runtime objetivo para este paquete
EXPECTED_ETABS_MAJOR = 21
ALLOW_OTHER_ETABS_MAJOR = False

# Soft error mode legacy. En ETABS 21 el paquete trabaja en modo estricto:
# ret != 0 => falla, salvo que una llamada use soft=True explicitamente.
# Se conserva el fallback legacy solo para versiones antiguas si se habilitan.
SOFT_ERRORS = False

# ===================================================================
# SECCION 2: GRILLA — 6 ejes X (numericos) + 6 ejes Y (literales)
# Planta REGULAR cuadrada 32.5 x 32.5 m
# 5 vanos x 6.5 m en cada direccion
# Fuente: Enunciado Taller pag 8 (planta tipo Ed.2)
# ===================================================================

GRID_X = {
    '1': 0.0,
    '2': 6.5,
    '3': 13.0,
    '4': 19.5,
    '5': 26.0,
    '6': 32.5,
}

GRID_Y = {
    'A': 0.0,
    'B': 6.5,
    'C': 13.0,
    'D': 19.5,
    'E': 26.0,
    'F': 32.5,
}

# Listas ordenadas
GRID_X_NAMES = list(GRID_X.keys())
GRID_X_VALS = list(GRID_X.values())
GRID_Y_NAMES = list(GRID_Y.keys())
GRID_Y_VALS = list(GRID_Y.values())

N_LINES_X = len(GRID_X)   # 6
N_LINES_Y = len(GRID_Y)   # 6

# Dimensiones en planta
LX_PLANTA = max(GRID_X.values()) - min(GRID_X.values())  # 32.5 m
LY_PLANTA = max(GRID_Y.values()) - min(GRID_Y.values())  # 32.5 m
AREA_PLANTA = LX_PLANTA * LY_PLANTA                       # 1056.25 m2

# Espaciamiento uniforme
GRID_SPACING = 6.5           # m (uniforme en ambas direcciones)

# ===================================================================
# SECCION 3: PISOS — 5 pisos, base empotrada
# Piso 1: h=3.50m, Pisos 2-5: h=3.00m
# H total = 3.50 + 4*3.00 = 15.50 m
# Fuente: Enunciado Taller pag 8
# ===================================================================

N_STORIES = 5
STORY_HEIGHT_1 = 3.50       # Piso 1 (m)
STORY_HEIGHT_TYP = 3.00     # Pisos 2-5 (m)

STORY_HEIGHTS = [STORY_HEIGHT_1] + [STORY_HEIGHT_TYP] * (N_STORIES - 1)
STORY_NAMES = [f"Story{i}" for i in range(1, N_STORIES + 1)]

# Elevaciones acumuladas desde la base
STORY_ELEVATIONS = []
_elev = 0.0
for _h in STORY_HEIGHTS:
    _elev += _h
    STORY_ELEVATIONS.append(round(_elev, 3))
# STORY_ELEVATIONS = [3.5, 6.5, 9.5, 12.5, 15.5]

H_TOTAL = STORY_ELEVATIONS[-1]  # 15.50 m

# ===================================================================
# SECCION 4: MATERIALES
# Unidades de trabajo: Tonf, m, C (eUnits=12)
# Factor de conversion: 1 MPa = 101.937 tonf/m2
# Fuente: Enunciado pag 10 (materiales) + pag 13 (Es, gamma_acero)
# ===================================================================

MPA_TO_TONF_M2 = 101.937    # 1 MPa = 10^6 N/m2 / 9806.65 N/tonf

# --- Hormigon G25 ---
MAT_CONC_NAME = "G25"
FC_MPA = 25.0                                      # f'c = 25 MPa
FC_TONF_M2 = FC_MPA * MPA_TO_TONF_M2              # 2,548.4 tonf/m2
EC_MPA = 4700.0 * math.sqrt(FC_MPA)               # 23,500 MPa
EC_TONF_M2 = EC_MPA * MPA_TO_TONF_M2              # 2,395,520 tonf/m2
POISSON_CONC = 0.20
ALPHA_THERMAL_CONC = 1.0e-05                       # /C
GAMMA_CONC = 2.50                                  # tonf/m3 (incluye armaduras)
# Parametros no lineales hormigon (SetOConcrete_1)
CONC_STRAIN_FC = 0.002       # Deformacion en f'c (ACI 318 standard, G25)
CONC_STRAIN_ULT = 0.005      # Deformacion ultima
CONC_FINAL_SLOPE = -0.1      # Pendiente post-pico

# --- Acero de refuerzo A630-420H ---
MAT_REBAR_NAME = "A630-420H"
FY_MPA = 420.0                                     # fy = 420 MPa
FY_TONF_M2 = FY_MPA * MPA_TO_TONF_M2             # 42,813.5 tonf/m2
FU_MPA = 630.0                                     # fu = 630 MPa
FU_TONF_M2 = FU_MPA * MPA_TO_TONF_M2             # 64,220.3 tonf/m2
ES_MPA = 210000.0                                  # Es = 210,000 MPa (enunciado p.13)
ES_TONF_M2 = ES_MPA * MPA_TO_TONF_M2             # 21,406,770 tonf/m2
POISSON_STEEL = 0.30
ALPHA_THERMAL_STEEL = 1.17e-05                     # /C
GAMMA_STEEL = 7.85                                 # tonf/m3 (enunciado p.13)
# Parametros no lineales acero (SetORebar_1)
EFY_MPA = FY_MPA * 1.10                           # Expected fy (fye = fy × 1.1, Guia Ed.2)
EFU_MPA = FU_MPA * 1.10                           # Expected fu (fue = fu × 1.1, Guia Ed.2)
EFY_TONF_M2 = EFY_MPA * MPA_TO_TONF_M2
EFU_TONF_M2 = EFU_MPA * MPA_TO_TONF_M2
REBAR_STRAIN_HARD = 0.01      # Deformacion inicio endurecimiento
REBAR_STRAIN_ULT = 0.09       # Deformacion ultima
REBAR_FINAL_SLOPE = -0.1

# ===================================================================
# SECCION 5: SECCIONES (frames y areas)
# 2 grupos por piso: P1-P2 (inferior) y P3-P5 (superior)
# Fuente: Enunciado Taller pag 9
# ===================================================================

# --- Columnas (Rectangulares) ---
COL_70_NAME = "C70x70G25"
COL_70_B = 0.70               # m (T2 en ETABS)
COL_70_H = 0.70               # m (T3 en ETABS)

COL_65_NAME = "C65x65G25"
COL_65_B = 0.65               # m
COL_65_H = 0.65               # m

# --- Vigas NORMALES (NO invertidas — diferencia clave con Ed.1) ---
VIGA_50_NAME = "V50x70G25"
VIGA_50_B = 0.50              # Ancho (m) — T2 en ETABS
VIGA_50_H = 0.70              # Peralte (m) — T3 en ETABS

VIGA_45_NAME = "V45x70G25"
VIGA_45_B = 0.45              # m
VIGA_45_H = 0.70              # m

# Cardinal point para vigas normales: Top Center (vigas convencionales cuelgan bajo losa)
# Guia Ed.2 Fase 5.2: CP=8 (Top Center) + StiffnessTransforms=True
# NOTA: Ed.1 usa CP=2 (BottomCenter, vigas invertidas)
VIGA_CARDINAL_POINT = CP_TOP_CENTER   # 8 — vigas convencionales (cara superior al nivel de losa)

# --- Losa maciza ---
LOSA_NAME = "L17G25"
LOSA_ESP = 0.17                # Espesor (m) — uniforme todos los pisos

# --- Asignacion de secciones por piso ---
# {story_index (1-based): (col_name, viga_name)}
SECTIONS_BY_STORY = {
    1: (COL_70_NAME, VIGA_50_NAME),
    2: (COL_70_NAME, VIGA_50_NAME),
    3: (COL_65_NAME, VIGA_45_NAME),
    4: (COL_65_NAME, VIGA_45_NAME),
    5: (COL_65_NAME, VIGA_45_NAME),
}

# --- Property Modifiers ACI318 ---

# Columnas: I2=I3=0.70 (ACI318 Table 6.6.3.1.1(a))
# [A, As2, As3, J, I22, I33, M, W]
COL_MODIFIERS = [1.0, 1.0, 1.0, 1.0, 0.70, 0.70, 1.0, 1.0]

# Vigas: I2=I3=0.35, J=0 (practica chilena — anular rigidez torsional)
# [A, As2, As3, J, I22, I33, M, W]
VIGA_MODIFIERS = [1.0, 1.0, 1.0, 0.0, 0.35, 0.35, 1.0, 1.0]

# Losas: inercia a flexion al 25% (practica chilena)
# [f11, f22, f12, m11, m22, m12, v13, v23, Mass, Weight]
LOSA_MODIFIERS = [1.0, 1.0, 1.0, 0.25, 0.25, 0.25, 1.0, 1.0, 1.0, 1.0]

# AutoMesh para losas
AUTOMESH_SIZE = 1.00           # m

# Rigid-zone factor (cachos rigidos) — Enunciado pag 9
RZF = 0.75

# ===================================================================
# SECCION 6: GEOMETRIA DE MARCOS
# Ed.2 NO tiene muros — solo columnas + vigas
# 36 columnas por piso (6x6 grilla)
# 60 vigas por piso (30 dir X + 30 dir Y)
# 25 losas por piso (5x5 paneles)
# ===================================================================

# Intersecciones de grilla: 36 nodos por piso
COLUMN_POSITIONS = []
for y_name in GRID_Y_NAMES:
    for x_name in GRID_X_NAMES:
        COLUMN_POSITIONS.append((GRID_X[x_name], GRID_Y[y_name]))
N_COLUMNS_PER_STORY = len(COLUMN_POSITIONS)   # 36

# Vigas direccion X: 6 filas (ejes A-F) x 5 vanos = 30 vigas
VIGAS_DIR_X = []
for y_name in GRID_Y_NAMES:
    y = GRID_Y[y_name]
    for i in range(len(GRID_X_NAMES) - 1):
        x_ini = GRID_X[GRID_X_NAMES[i]]
        x_fin = GRID_X[GRID_X_NAMES[i + 1]]
        VIGAS_DIR_X.append((y, x_ini, x_fin))

# Vigas direccion Y: 6 columnas (ejes 1-6) x 5 vanos = 30 vigas
VIGAS_DIR_Y = []
for x_name in GRID_X_NAMES:
    x = GRID_X[x_name]
    for i in range(len(GRID_Y_NAMES) - 1):
        y_ini = GRID_Y[GRID_Y_NAMES[i]]
        y_fin = GRID_Y[GRID_Y_NAMES[i + 1]]
        VIGAS_DIR_Y.append((x, y_ini, y_fin))

N_VIGAS_X_PER_STORY = len(VIGAS_DIR_X)   # 30
N_VIGAS_Y_PER_STORY = len(VIGAS_DIR_Y)   # 30
N_VIGAS_PER_STORY = N_VIGAS_X_PER_STORY + N_VIGAS_Y_PER_STORY  # 60

# Paneles de losa: 5x5 = 25 por piso (sin shaft, sin huecos)
SLAB_PANELS = []
for i in range(len(GRID_X_NAMES) - 1):
    for j in range(len(GRID_Y_NAMES) - 1):
        x0 = GRID_X[GRID_X_NAMES[i]]
        x1 = GRID_X[GRID_X_NAMES[i + 1]]
        y0 = GRID_Y[GRID_Y_NAMES[j]]
        y1 = GRID_Y[GRID_Y_NAMES[j + 1]]
        SLAB_PANELS.append((x0, y0, x1, y1))

N_SLABS_PER_STORY = len(SLAB_PANELS)   # 25
AREA_LOSA_PANEL = GRID_SPACING * GRID_SPACING  # 42.25 m2
AREA_LOSA_PISO = N_SLABS_PER_STORY * AREA_LOSA_PANEL  # 1056.25 m2

# Conteo total de elementos
N_COLUMNS_TOTAL = N_COLUMNS_PER_STORY * N_STORIES     # 180
N_VIGAS_TOTAL = N_VIGAS_PER_STORY * N_STORIES          # 300
N_SLABS_TOTAL = N_SLABS_PER_STORY * N_STORIES          # 125

# ===================================================================
# SECCION 7: CARGAS
# Unidades: tonf/m2 (para ETABS en Tonf_m_C)
# Fuente: Enunciado Taller pag 9
# Ed.2 NO distingue oficina/pasillo — carga UNIFORME en toda la planta
# ===================================================================

# Patrones de carga y su tipo ETABS
LOAD_PATTERNS = {
    # nombre: (eLoadPatternType, SelfWeightMultiplier)
    'PP':   (LTYPE_DEAD,      1.0),     # Peso propio (SWM=1)
    'TERP': (LTYPE_SUPERDEAD, 0.0),     # Terminaciones pisos tipo (P1-P4)
    'TERT': (LTYPE_SUPERDEAD, 0.0),     # Terminaciones techo (P5)
    'SCP':  (LTYPE_LIVE,      0.0),     # Sobrecarga pisos tipo (P1-P4)
    'SCT':  (LTYPE_ROOFLIVE,  0.0),     # Sobrecarga techo (P5)
}

# Valores de carga en tonf/m2
TERP_PISO = 0.140       # 140 kgf/m2 = 0.140 tonf/m2 (pisos 1-4)
TERT_TECHO = 0.100      # 100 kgf/m2 = 0.100 tonf/m2 (piso 5)
SCP_PISO = 0.300        # 300 kgf/m2 = 0.300 tonf/m2 (pisos 1-4, uniforme)
SCT_TECHO = 0.100       # 100 kgf/m2 = 0.100 tonf/m2 (piso 5)

LOADS_AREA = {
    'TERP': TERP_PISO,
    'TERT': TERT_TECHO,
    'SCP': SCP_PISO,
    'SCT': SCT_TECHO,
}

# Mass Source oficial Ed.2 Parte 1:
# PP + TERP + TERT + 0.25*SCP + 0.25*SCT
MASS_SOURCE_PATTERNS = {
    'PP':   1.0,
    'TERP': 1.0,
    'TERT': 1.0,
    'SCP':  0.25,
    'SCT':  0.25,
}

# ===================================================================
# SECCION 8: PARAMETROS SISMICOS
# NCh433 Mod 2009 + DS61
# Caso: Zona 3, Suelo C, Oficina (Cat. II), Marcos Especiales HA
# Fuente: Enunciado pag 8 + NCh433 Tabla 5.1
# ===================================================================

ZONA_SISMICA = 3
AO_G = 0.40                  # Ao/g — NCh433 Tabla 6.2, Zona 3
AO_MS2 = AO_G * 9.81         # Ao en m/s2 = 3.924
SUELO = 'C'
CATEGORIA = 'II'              # Oficinas
I_FACTOR = 1.0                # NCh433 Tabla 6.1, Cat II
G_ACCEL = 9.81                # m/s2

# Parametros de suelo — DS61 Tabla 12.3, Suelo C
S_SUELO = 1.05
TO_SUELO = 0.40               # s
T_PRIME = 0.45                 # s (T')
N_SUELO = 1.40
P_SUELO = 1.60

# Sistema estructural — NCh433 Tabla 5.1 (Marcos Especiales HA)
R_MARCOS = 7                  # Factor de modificacion de respuesta
RO_MARCOS = 11                # Factor de sobreresistencia

# Torsion accidental — NCh433 Art. 6.3.4 (DINAMICO)
# ea = +-0.10 * bk (CONSTANTE para analisis dinamico)
# Planta cuadrada: bx = by = 32.5 m => ea_x = ea_y = 3.25 m
EA_X = 0.10 * LX_PLANTA       # 3.25 m
EA_Y = 0.10 * LY_PLANTA       # 3.25 m

# Torsion accidental estatica — NCh433 Art. 6.2.8
# ea_k = 0.10 * bk * (Zk / H)  (variable por piso)
EA_STATIC_X = {}
EA_STATIC_Y = {}
for i, elev in enumerate(STORY_ELEVATIONS):
    story = STORY_NAMES[i]
    EA_STATIC_X[story] = 0.10 * LY_PLANTA * (elev / H_TOTAL)
    EA_STATIC_Y[story] = 0.10 * LX_PLANTA * (elev / H_TOTAL)
# Para Ed.2 LX = LY = 32.5 m, pero se dejan separados para respetar la
# semantica normativa: si el sismo actua en X, la excentricidad accidental
# se toma perpendicular a X, y viceversa.
EA_STATIC = dict(EA_STATIC_X)

# Espectro: mismo archivo que Ed.1 (Zona 3, Suelo C)
# Try same directory first, then parent directory as fallback
_spectrum_dir = os.path.dirname(os.path.abspath(__file__))
_spectrum_same = os.path.join(_spectrum_dir, "espectro_elastico_Z3SC.txt")
_spectrum_parent = os.path.join(_spectrum_dir, "..", "espectro_elastico_Z3SC.txt")
SPECTRUM_FILE = _spectrum_same if os.path.exists(_spectrum_same) else _spectrum_parent
SPECTRUM_DAMPING = 0.05        # 5%
SPECTRUM_SF = G_ACCEL          # 9.81 — convierte Sa/g a m/s2

# Diafragma
DIAPHRAGM_RIGID_NAME = "D1"

# Combinaciones NCh3171 expandidas para el flujo estatico oficial.
# D = PP + TERP + TERT (todas las cargas permanentes)
# L = SCP, Lr = SCT
# Ed.2 Parte 1 exige considerar signo del sismo principal y de la torsion
# accidental, por lo que C4-C7 se expanden a 16 variantes.
COMBINATIONS = {
    'C1': [(1.4, 'PP'), (1.4, 'TERP'), (1.4, 'TERT')],
    'C2': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.6, 'SCP'), (0.5, 'SCT')],
    'C3': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (1.6, 'SCT')],
    'C4_XP_TP': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (1.4, 'EX'), (1.4, 'TEX')],
    'C4_XP_TN': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (1.4, 'EX'), (-1.4, 'TEX')],
    'C4_XN_TP': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (-1.4, 'EX'), (1.4, 'TEX')],
    'C4_XN_TN': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (-1.4, 'EX'), (-1.4, 'TEX')],
    'C5_XP_TP': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (1.4, 'EX'), (1.4, 'TEX')],
    'C5_XP_TN': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (1.4, 'EX'), (-1.4, 'TEX')],
    'C5_XN_TP': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (-1.4, 'EX'), (1.4, 'TEX')],
    'C5_XN_TN': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (-1.4, 'EX'), (-1.4, 'TEX')],
    'C6_YP_TP': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (1.4, 'EY'), (1.4, 'TEY')],
    'C6_YP_TN': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (1.4, 'EY'), (-1.4, 'TEY')],
    'C6_YN_TP': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (-1.4, 'EY'), (1.4, 'TEY')],
    'C6_YN_TN': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (-1.4, 'EY'), (-1.4, 'TEY')],
    'C7_YP_TP': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (1.4, 'EY'), (1.4, 'TEY')],
    'C7_YP_TN': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (1.4, 'EY'), (-1.4, 'TEY')],
    'C7_YN_TP': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (-1.4, 'EY'), (1.4, 'TEY')],
    'C7_YN_TN': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (-1.4, 'EY'), (-1.4, 'TEY')],
}

# Valores esperados de validacion (orden de magnitud)
PESO_ESPERADO_TONF = AREA_PLANTA * N_STORIES * 1.0   # ~5281 tonf (1 tonf/m2 regla)
DRIFT_LIMITE_CM = 0.002        # NCh433 5.9.2
DRIFT_LIMITE_PUNTO = 0.001     # NCh433 5.9.3 exceso sobre CM

# ===================================================================
# SECCION 9: FORMULAS SISMICAS VERIFICADAS
# ===================================================================

def calc_alpha(T, To=TO_SUELO, p=P_SUELO):
    """Factor de amplificacion espectral — NCh433 Art. 6.3.5.2, Ec. (9).

    alpha(T) = [1 + 4.5*(T/To)^p] / [1 + (T/To)^3]
    """
    if T <= 0:
        return 1.0
    ratio = T / To
    return (1.0 + 4.5 * ratio**p) / (1.0 + ratio**3)


def calc_Sa_g(T, S=S_SUELO, Ao=AO_G, To=TO_SUELO, p=P_SUELO):
    """Pseudo-aceleracion espectral en unidades de g.

    Sa/g = S * Ao * alpha(T)
    """
    return S * Ao * calc_alpha(T, To, p)


def calc_R_star(T_star, Ro=RO_MARCOS, To=TO_SUELO):
    """Factor de reduccion espectral R* — NCh433 Art. 6.3.5.3, Ec. (10).

    R* = 1 + T* / (0.10*To + T*/Ro)

    Formula general (aplica a marcos y muros).
    """
    if T_star <= 0:
        return 1.0
    denom = 0.10 * To + T_star / Ro
    return 1.0 + T_star / denom


def calc_C(T_star, S=S_SUELO, Ao=AO_G, R=R_MARCOS, Tp=T_PRIME,
           n=N_SUELO, g=G_ACCEL):
    """Coeficiente sismico C — NCh433 Art. 6.2.3.1, Ec. (2).

    C = 2.75 * S * (Ao/g) * (T'/T*)^n / R
    """
    if T_star <= 0:
        return 0.0
    return 2.75 * S * Ao * g / (g * R) * (Tp / T_star) ** n


def calc_Cmin(I=I_FACTOR, S=S_SUELO, Ao=AO_G, g=G_ACCEL):
    """Coeficiente sismico minimo — NCh433 Art. 6.3.7.

    Cmin = (Ao/g) * S / 6 = 0.4 * 1.05 / 6 = 0.070
    """
    return Ao * S * g / (6.0 * g)


def calc_Cmax(S=S_SUELO, Ao=AO_G, R=R_MARCOS, g=G_ACCEL):
    """Coeficiente sismico maximo — NCh433 Art. 6.2.3.1.

    Cmax = 0.35 * S * (Ao/g) = 0.35 * 1.05 * 0.4 = 0.147

    NOTA: Para marcos puros (q = V_muros/V_total = 0), NO aplica
    reduccion de Cmax (f = 1.25 - 0.5*q = 1.25, pero f > 1 => f = 1).
    """
    return 0.35 * S * Ao * g / g


# ===================================================================
# SECCION 10: CONEXION COM — ETABS 21
# Patron robusto: GetActiveObject -> Helper.GetObject -> CreateObject
# Identico a Ed.1 (autonomo/scripts/config.py)
# ===================================================================

# Variables globales COM — MANTENER para evitar garbage collection
_helper = None
_etabs_obj = None
_sap_model = None
_etabs_major = 0
_etabs_version = "unknown"


def clean_comtypes_gen():
    """Limpiar cache stale de comtypes ANTES de import comtypes.client.

    CRITICO: Si hay TLBs desactualizados en comtypes/gen/, la conexion
    puede fallar silenciosamente o generar bindings incompatibles.
    """
    try:
        import comtypes
        gen_path = os.path.join(os.path.dirname(comtypes.__file__), 'gen')
        if not os.path.exists(gen_path):
            return
        for item in os.listdir(gen_path):
            if item == '__init__.py':
                continue
            path = os.path.join(gen_path, item)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except OSError:
                pass
        log.info("comtypes.gen limpiado")
    except ImportError:
        log.warning("comtypes no instalado — pip install comtypes")
        raise


def _get_etabs_version(sap_model):
    """Get ETABS version string safely. Returns (major, minor, full_string)."""
    try:
        ver = sap_model.GetVersion()
        if isinstance(ver, (tuple, list)) and len(ver) >= 2:
            full = str(ver[0])
            # Parse major version number (e.g., "19.1.0" -> 19)
            parts = full.split('.')
            major = int(parts[0]) if parts[0].isdigit() else 0
            return major, full
        return 0, str(ver)
    except Exception:
        return 0, "unknown"


def etabs_version_check(sap_model):
    """Print ETABS version at the start of any script. Call after connect()."""
    global _etabs_major, _etabs_version
    major, full = _get_etabs_version(sap_model)
    _etabs_major = major
    _etabs_version = full
    log.info(f"ETABS version: {full} (major={major})")
    if major == EXPECTED_ETABS_MAJOR:
        log.info(f"  Running on expected ETABS v{EXPECTED_ETABS_MAJOR} — strict COM mode enabled")
    elif major >= 21:
        log.warning(
            f"  Running on ETABS v{major}. Package was hardened for v{EXPECTED_ETABS_MAJOR}; verify COM/table behavior."
        )
    elif major >= 19:
        message = (
            f"Running on ETABS v{major}. This Ed.2 package is targeted to v{EXPECTED_ETABS_MAJOR} "
            "and should not be considered validated here."
        )
        if ALLOW_OTHER_ETABS_MAJOR:
            log.warning("  " + message)
        else:
            raise RuntimeError(message)
    elif major > 0:
        message = f"Running on ETABS v{major}, unsupported for this Ed.2 package."
        if ALLOW_OTHER_ETABS_MAJOR:
            log.warning("  " + message)
        else:
            raise RuntimeError(message)
    return major


def get_runtime_etabs_info():
    return {
        "expected_major": EXPECTED_ETABS_MAJOR,
        "detected_major": _etabs_major,
        "detected_version": _etabs_version,
        "strict_ret_mode": _etabs_major >= EXPECTED_ETABS_MAJOR,
    }


def _env_flag(name: str, default: bool = False) -> bool:
    value = str(os.getenv(name, "")).strip().lower()
    if not value:
        return default
    return value in {"1", "true", "yes", "on", "si"}


def _normalize_model_path(model_path):
    if model_path is None:
        return None
    path = str(model_path).strip()
    if not path:
        return None
    return os.path.abspath(path)


def _get_current_model_path(sap_model):
    try:
        filepath = sap_model.GetModelFilename()
        if isinstance(filepath, (tuple, list)):
            filepath = filepath[0]
        filepath = str(filepath or "").strip()
    except Exception:
        filepath = ""
    if not filepath or filepath.upper() == "UNSAVED":
        return ""
    return os.path.abspath(filepath)


def _maybe_open_model_file(sap_model, model_path, force_open_model=False):
    target_path = _normalize_model_path(model_path)
    if not target_path:
        return

    if not os.path.isfile(target_path):
        message = f"Model path not found: {target_path}"
        if force_open_model:
            raise FileNotFoundError(message)
        log.warning(f"{message} — continuing with current ETABS model")
        return

    current_path = _get_current_model_path(sap_model)
    if current_path and os.path.normcase(current_path) == os.path.normcase(target_path):
        log.info(f"Modelo activo OK: {target_path}")
        return

    log.info(f"Abriendo modelo ETABS: {target_path}")
    ret = sap_model.File.OpenFile(target_path)
    check_ret(ret, f"File.OpenFile('{target_path}')")


def connect(create_if_missing=None, clean_gen=True, model_path=None, force_open_model=None):
    """Conectar a ETABS 21 via COM.

    Prioridad de conexion:
      1. GetActiveObject — requiere ETABS abierto con modelo
      2. Helper.GetObject — mas robusto en algunas versiones de comtypes
         (tries multiple Helper ProgIDs for ETABS compatibility)
      3. CreateObject — SOLO si create_if_missing=True (PELIGROSO)

    Args:
        create_if_missing: Si True, crea nueva instancia como ultimo recurso.
        clean_gen: Si True, limpia comtypes.gen antes de importar.
        model_path: Si se especifica, abre este .edb tras conectar.
        force_open_model: Si True, falla cuando model_path no existe.

    Returns:
        SapModel object (acceso a toda la API ETABS)

    Raises:
        ConnectionError: Si no se puede conectar a ETABS
        ImportError: Si comtypes no esta instalado
    """
    global _helper, _etabs_obj, _sap_model

    if create_if_missing is None:
        create_if_missing = _env_flag(ENV_CREATE_IF_MISSING, False)
    if model_path is None:
        model_path = os.getenv(ENV_MODEL_PATH, "")
    if force_open_model is None:
        force_open_model = _env_flag(ENV_FORCE_MODEL_OPEN, False)

    if clean_gen:
        clean_comtypes_gen()

    import comtypes.client

    # --- Metodo 1: GetActiveObject (RECOMENDADO) ---
    try:
        _etabs_obj = comtypes.client.GetActiveObject(ETABS_PROGID)
        _sap_model = _etabs_obj.SapModel
        log.info("Conectado via GetActiveObject")
        etabs_version_check(_sap_model)
        _maybe_open_model_file(_sap_model, model_path, force_open_model)
        return _sap_model
    except (OSError, Exception) as e:
        log.debug(f"GetActiveObject fallo: {e} — probando Helper...")

    # --- Metodo 2: Helper.GetObject (try multiple ProgIDs) ---
    for helper_progid in HELPER_PROGIDS:
        try:
            _helper = comtypes.client.CreateObject(helper_progid)
            try:
                import comtypes.gen.ETABSv1 as ETABSv1
                _helper = _helper.QueryInterface(ETABSv1.cHelper)
            except Exception:
                log.debug(f"  QueryInterface failed for {helper_progid}, using raw helper")
            _etabs_obj = _helper.GetObject(ETABS_PROGID)
            _sap_model = _etabs_obj.SapModel
            log.info(f"Conectado via Helper.GetObject ({helper_progid})")
            etabs_version_check(_sap_model)
            _maybe_open_model_file(_sap_model, model_path, force_open_model)
            return _sap_model
        except Exception as e:
            log.debug(f"Helper.GetObject ({helper_progid}) fallo: {e}")

    # --- Metodo 3: CreateObject (PELIGROSO) ---
    if create_if_missing:
        log.warning("Creando nueva instancia ETABS — puede ser invisible")
        for helper_progid in HELPER_PROGIDS:
            try:
                _helper = comtypes.client.CreateObject(helper_progid)
                try:
                    import comtypes.gen.ETABSv1 as ETABSv1
                    _helper = _helper.QueryInterface(ETABSv1.cHelper)
                except Exception:
                    pass
                _etabs_obj = _helper.CreateObjectProgID(ETABS_PROGID)
                break
            except Exception as e:
                log.debug(f"CreateObject ({helper_progid}) fallo: {e}")
                continue
        else:
            raise ConnectionError("CreateObject failed with all Helper ProgIDs")
        try:
            _etabs_obj.Visible = True
        except Exception:
            pass
        _etabs_obj.ApplicationStart()
        time.sleep(15)
        _sap_model = _etabs_obj.SapModel
        log.warning("Conectado via CreateObject — verificar que UI sea visible")
        etabs_version_check(_sap_model)
        _maybe_open_model_file(_sap_model, model_path, force_open_model)
        return _sap_model

    raise ConnectionError(
        "No se pudo conectar a ETABS.\n"
        "Asegurate de:\n"
        "  1. Abrir ETABS 21 manualmente\n"
        "  2. File > New Model > Blank (o abrir un modelo existente)\n"
        "  3. Luego ejecutar este script\n"
        "  4. O usar --create-if-missing / ED2_ETABS_CREATE_IF_MISSING=1"
    )


def disconnect(save_path=None, close_app=False):
    """Desconectar referencias COM.

    Args:
        save_path: Si se proporciona y es una ruta valida, guarda el modelo.
        close_app: Si True, tambien cierra ETABS. Por defecto solo desacopla COM
            para permitir pipelines multi-proceso sobre la misma sesion abierta.
    """
    global _helper, _etabs_obj, _sap_model, _etabs_major, _etabs_version

    if _sap_model is not None and save_path and not isinstance(save_path, bool):
        try:
            ret = _sap_model.File.Save(save_path)
            if ret == 0:
                log.info(f"Modelo guardado: {save_path}")
            else:
                log.warning(f"File.Save retorno {ret}")
        except Exception as e:
            log.error(f"Error guardando: {e}")

    # Liberar referencias COM en orden inverso
    _sap_model = None
    if _etabs_obj is not None and close_app:
        try:
            _etabs_obj.ApplicationExit(False)
            log.info("ETABS cerrado via ApplicationExit")
        except Exception:
            pass
    _etabs_obj = None
    _helper = None
    _etabs_major = 0
    _etabs_version = "unknown"


def get_model():
    """Obtener referencia al SapModel activo (sin reconectar)."""
    if _sap_model is None:
        raise RuntimeError("No conectado a ETABS — ejecutar connect() primero")
    return _sap_model


def get_etabs():
    """Obtener referencia al EtabsObject activo."""
    if _etabs_obj is None:
        raise RuntimeError("No conectado a ETABS — ejecutar connect() primero")
    return _etabs_obj


# ===================================================================
# SECCION 11: FUNCIONES HELPER ETABS
# ===================================================================

def check_ret(ret, msg="", soft=None):
    """Verificar return value de API ETABS.

    Todas las funciones CSI OAPI retornan 0 en exito.
    El flujo Ed.2 se ejecuta en modo estricto para ETABS 21.

    Args:
        ret: Return value from COM call (int, tuple, or list)
        msg: Description of the operation for error messages
        soft: If True, ret!=0 is WARNING not ERROR.
              If None, uses global SOFT_ERRORS setting.
    """
    if isinstance(ret, (tuple, list)):
        code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        code = ret

    if soft is not None:
        use_soft = soft
    else:
        use_soft = SOFT_ERRORS
        if _etabs_major >= EXPECTED_ETABS_MAJOR:
            use_soft = False

    if code != 0:
        if use_soft:
            log.warning(f"ETABS API ret={code} (non-zero): {msg}")
        else:
            raise RuntimeError(f"ETABS API fallo (ret={code}): {msg}")


def verify_model():
    """Verificar que hay un modelo activo y accesible.

    Returns:
        dict con informacion basica del modelo
    """
    model = get_model()
    info = {}

    try:
        info['units'] = model.GetPresentUnits()
    except Exception:
        info['units'] = 'ERROR'

    try:
        info['locked'] = model.GetModelIsLocked()
    except Exception:
        info['locked'] = 'ERROR'

    try:
        info['file'] = model.GetModelFilename()
    except Exception:
        info['file'] = 'UNSAVED'

    log.info(f"Modelo verificado: unidades={info['units']}, "
             f"locked={info['locked']}, file={info['file']}")
    return info


def unlock_model():
    """Desbloquear modelo para edicion (si esta locked post-analisis)."""
    model = get_model()
    try:
        model.SetModelIsLocked(False)
    except Exception:
        pass


def set_units(model_or_units=UNITS_TONF_M_C, units=None):
    """Establecer unidades del modelo.

    Soporta ambas firmas:
    - set_units()
    - set_units(UNITS_TONF_M_C)
    - set_units(SapModel, UNITS_TONF_M_C)
    """
    if units is None:
        if hasattr(model_or_units, "SetPresentUnits"):
            model = model_or_units
            target_units = UNITS_TONF_M_C
        else:
            model = get_model()
            target_units = model_or_units
    else:
        model = model_or_units
        target_units = units

    ret = model.SetPresentUnits(target_units)
    check_ret(ret, f"SetPresentUnits({target_units})")


def get_col_section(story_index):
    """Retorna nombre de seccion de columna para un piso dado (1-based)."""
    col_name, _ = SECTIONS_BY_STORY[story_index]
    return col_name


def get_viga_section(story_index):
    """Retorna nombre de seccion de viga para un piso dado (1-based)."""
    _, viga_name = SECTIONS_BY_STORY[story_index]
    return viga_name


# ===================================================================
# SECCION 12: RUTAS DEL PROYECTO
# ===================================================================

# Directorio de este script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Directorio raiz del proyecto
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))


def _resolve_runtime_root():
    candidate = str(os.getenv(ENV_RUNTIME_ROOT, "")).strip()
    if candidate:
        return os.path.abspath(candidate)
    return SCRIPT_DIR


# Directorio de trabajo efectivo para corrida local o WS UCN.
# Si ED2_RUNTIME_ROOT apunta a C:\Users\Civil\Documents\taha, todos los artefactos
# del run viven ahi sin cambiar el codigo fuente.
RUNTIME_ROOT = _resolve_runtime_root()
MODELS_DIR = os.path.join(RUNTIME_ROOT, "models")
RESULTS_DIR = os.path.join(RUNTIME_ROOT, "results")
TRANSFER_DIR = os.path.join(RUNTIME_ROOT, "transfer")
INFORME_DIR = os.path.join(RUNTIME_ROOT, "taller_ed2", "informe")


# ===================================================================
# MAIN — Verificacion de datos al ejecutar directamente
# ===================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("EDIFICIO 2 — Taller ADSE UCN 1S-2026")
    print("Marcos Especiales HA, 5 pisos, Antofagasta")
    print("=" * 60)

    print(f"\n--- Grilla ---")
    print(f"  Ejes X: {N_LINES_X}  |  Ejes Y: {N_LINES_Y}")
    print(f"  Espaciamiento: {GRID_SPACING} m (uniforme)")
    print(f"  Lx = {LX_PLANTA:.1f} m  |  Ly = {LY_PLANTA:.1f} m")
    print(f"  Area planta = {AREA_PLANTA:.2f} m2")

    print(f"\n--- Pisos ---")
    print(f"  N = {N_STORIES}")
    print(f"  h1 = {STORY_HEIGHT_1} m  |  h_tip = {STORY_HEIGHT_TYP} m")
    print(f"  H total = {H_TOTAL:.1f} m")
    print(f"  Elevaciones: {STORY_ELEVATIONS} m")

    print(f"\n--- Materiales (en Tonf_m_C) ---")
    print(f"  G25: f'c={FC_TONF_M2:.1f} tonf/m2, Ec={EC_TONF_M2:.0f} tonf/m2, "
          f"gamma={GAMMA_CONC} tonf/m3")
    print(f"  A630-420H: fy={FY_TONF_M2:.1f}, fu={FU_TONF_M2:.1f}, "
          f"Es={ES_TONF_M2:.0f} tonf/m2")

    print(f"\n--- Secciones ---")
    print(f"  P1-P2: Col {COL_70_NAME} ({COL_70_B}x{COL_70_H}m), "
          f"Viga {VIGA_50_NAME} ({VIGA_50_B}x{VIGA_50_H}m)")
    print(f"  P3-P5: Col {COL_65_NAME} ({COL_65_B}x{COL_65_H}m), "
          f"Viga {VIGA_45_NAME} ({VIGA_45_B}x{VIGA_45_H}m)")
    print(f"  Losa: {LOSA_NAME} (e={LOSA_ESP}m)")
    print(f"  Modifiers col: I22=I33={COL_MODIFIERS[4]}")
    print(f"  Modifiers viga: I22=I33={VIGA_MODIFIERS[4]}, J={VIGA_MODIFIERS[3]}")
    print(f"  Modifiers losa: m11=m22=m12={LOSA_MODIFIERS[3]}")
    print(f"  RZF (cachos rigidos) = {RZF}")

    print(f"\n--- Geometria ---")
    print(f"  Columnas/piso: {N_COLUMNS_PER_STORY}  |  Total: {N_COLUMNS_TOTAL}")
    print(f"  Vigas/piso: {N_VIGAS_PER_STORY} (X:{N_VIGAS_X_PER_STORY} + Y:{N_VIGAS_Y_PER_STORY})")
    print(f"  Vigas total: {N_VIGAS_TOTAL}")
    print(f"  Losas/piso: {N_SLABS_PER_STORY}  |  Total: {N_SLABS_TOTAL}")
    print(f"  Area losa/piso: {AREA_LOSA_PISO:.2f} m2")

    print(f"\n--- Cargas (tonf/m2) ---")
    print(f"  TERP = {TERP_PISO}  |  TERT = {TERT_TECHO}")
    print(f"  SCP piso = {SCP_PISO}  |  SCT techo = {SCT_TECHO}")

    print(f"\n--- Parametros sismicos ---")
    print(f"  Zona {ZONA_SISMICA}, Ao={AO_G}g, Suelo {SUELO}")
    print(f"  S={S_SUELO}, To={TO_SUELO}s, T'={T_PRIME}s, "
          f"n={N_SUELO}, p={P_SUELO}")
    print(f"  R={R_MARCOS}, Ro={RO_MARCOS}, I={I_FACTOR}")
    print(f"  EA_x = {EA_X:.3f} m  |  EA_y = {EA_Y:.3f} m")
    print(f"  Torsion estatica por piso:")
    for name, ea in EA_STATIC.items():
        print(f"    {name}: ea = {ea:.3f} m")

    print(f"\n--- Formulas sismicas ---")
    for T in [0.3, 0.5, 0.65, 1.0]:
        a = calc_alpha(T)
        R_s = calc_R_star(T)
        Sa = calc_Sa_g(T)
        C = calc_C(T)
        print(f"  T={T:.2f}s: alpha={a:.4f}, Sa/g={Sa:.4f}, "
              f"R*={R_s:.3f}, C={C:.5f}")

    Cmin = calc_Cmin()
    Cmax = calc_Cmax()
    print(f"\n  Cmin = {Cmin:.5f}  |  Cmax = {Cmax:.5f}")
    print(f"  Peso esperado ~ {PESO_ESPERADO_TONF:.0f} tonf "
          f"({AREA_PLANTA:.1f} m2 x {N_STORIES} pisos x 1 tonf/m2)")

    print(f"\n--- Espectro ---")
    spectrum_abs = os.path.abspath(SPECTRUM_FILE)
    if os.path.exists(spectrum_abs):
        print(f"  Archivo: {spectrum_abs} [OK]")
    else:
        print(f"  Archivo: {spectrum_abs} [NO ENCONTRADO]")
        print(f"  Buscar en: autonomo/scripts/espectro_elastico_Z3SC.txt")

    print(f"\n--- COM ---")
    try:
        import comtypes
        print(f"  comtypes v{comtypes.__version__} [OK]")
    except ImportError:
        print("  comtypes NO instalado — pip install comtypes")

    print("\n" + "=" * 60)
    print("Config Ed.2 OK")
