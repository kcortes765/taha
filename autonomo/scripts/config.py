"""
config.py - Configuracion y conexion COM para pipeline ETABS v19
Edificio 1: 20 pisos de muros HA, Antofagasta - Taller ADSE UCN 1S-2026

Este modulo centraliza:
  - Conexion COM robusta a ETABS v19 (comtypes)
  - Datos completos del edificio (grilla, pisos, materiales, secciones)
  - Geometria de muros, vigas y losas
  - Parametros sismicos NCh433/DS61
  - Funciones helper (connect, disconnect, verify, formulas)

Firmas COM verificadas contra:
  - docs.csiamerica.com API 2016
  - Repos: danielogg92, ebrahimraeyat, mihdicaballero, mtavares51
  - Eng-Tips threads 516841, 477551
  - Investigacion R01/R02/R03 del proyecto

Uso:
  >>> from config import connect, disconnect, SapModel
  >>> model = connect()
  >>> # ... operaciones ETABS ...
  >>> disconnect()

Fuente datos: Enunciado Taller ADSE 1S-2026, Prof. Music
Normas: NCh433 Mod 2009, DS61, DS60, ACI318-08, NCh3171, NCh1537
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
log = logging.getLogger("etabs_config")
if not log.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    log.addHandler(_h)
    log.setLevel(logging.INFO)

# ===================================================================
# SECCION 1: CONSTANTES ETABS (eUnits, eMatType, etc.)
# ===================================================================

# eUnits — sistema de unidades del modelo
UNITS_TONF_M_C = 12          # Tonf, m, C — unidades del proyecto
UNITS_KGF_M_C = 15           # kgf, m, C
UNITS_KN_M_C = 6             # kN, m, C

# eMatType — tipos de material
MAT_STEEL = 1
MAT_CONCRETE = 2
MAT_NODESIGN = 3
MAT_ALUMINUM = 4
MAT_COLDFORMED = 5
MAT_REBAR = 6
MAT_TENDON = 7

# eLoadPatternType — tipos de patron de carga
LTYPE_DEAD = 1
LTYPE_SUPERDEAD = 2
LTYPE_LIVE = 3
LTYPE_REDUCELIVE = 4
LTYPE_QUAKE = 5
LTYPE_WIND = 6
LTYPE_ROOFLIVE = 12

# eWallPropType
WALL_SPECIFIED = 0

# eShellType
SHELL_THIN = 1
SHELL_THICK = 2
SHELL_MEMBRANE = 3
SHELL_LAYERED = 5

# eSlabType
SLAB_SLAB = 0
SLAB_DROP = 1
SLAB_STIFF = 2
SLAB_RIBBED = 3
SLAB_WAFFLE = 4

# Cardinal Points (para vigas)
CP_BOTTOM_LEFT = 1
CP_BOTTOM_CENTER = 2        # Vigas invertidas
CP_BOTTOM_RIGHT = 3
CP_CENTROID = 8
CP_TOP_CENTER = 11

# ProgID COM
ETABS_PROGID = "CSI.ETABS.API.ETABSObject"
HELPER_PROGID = "ETABSv1.Helper"   # Universal para ETABS v18-v22+

# ===================================================================
# SECCION 2: GRILLA — 17 ejes X (numerados) + 6 ejes Y (letrados)
# Fuente: Enunciado Taller pag 2 (planta tipo) y pag 6 (elevaciones)
# ===================================================================

GRID_X = {
    '1':  0.000,
    '2':  3.125,
    '3':  3.825,
    '4':  9.295,
    '5':  9.895,
    '6':  15.465,
    '7':  16.015,
    '8':  18.565,
    '9':  18.990,
    '10': 21.665,
    '11': 24.990,
    '12': 26.315,
    '13': 27.834,
    '14': 32.435,
    '15': 34.005,
    '16': 37.130,
    '17': 38.505,
}

GRID_Y = {
    'A': 0.000,
    'B': 0.701,
    'C': 6.446,
    'D': 7.996,
    'E': 10.716,
    'F': 13.821,
}

# Listas ordenadas
GRID_X_NAMES = list(GRID_X.keys())
GRID_X_VALS = list(GRID_X.values())
GRID_Y_NAMES = list(GRID_Y.keys())
GRID_Y_VALS = list(GRID_Y.values())

N_LINES_X = len(GRID_X)   # 17
N_LINES_Y = len(GRID_Y)   # 6

# Dimensiones en planta
LX_PLANTA = max(GRID_X.values()) - min(GRID_X.values())  # 38.505 m
LY_PLANTA = max(GRID_Y.values()) - min(GRID_Y.values())  # 13.821 m
AREA_ENVOLVENTE = LX_PLANTA * LY_PLANTA                   # 532.2 m2

# ===================================================================
# SECCION 3: PISOS — 20 pisos, base empotrada
# Piso 1: h=3.40m, Pisos 2-20: h=2.60m
# H total = 3.40 + 19*2.60 = 52.80 m
# ===================================================================

N_STORIES = 20
STORY_HEIGHT_1 = 3.40       # Piso 1 (m)
STORY_HEIGHT_TYP = 2.60     # Pisos 2-20 (m)

STORY_HEIGHTS = [STORY_HEIGHT_1] + [STORY_HEIGHT_TYP] * (N_STORIES - 1)
STORY_NAMES = [f"Story{i}" for i in range(1, N_STORIES + 1)]

# Elevaciones acumuladas desde la base
STORY_ELEVATIONS = []
_elev = 0.0
for _h in STORY_HEIGHTS:
    _elev += _h
    STORY_ELEVATIONS.append(round(_elev, 3))
# STORY_ELEVATIONS = [3.4, 6.0, 8.6, ..., 52.8]

H_TOTAL = STORY_ELEVATIONS[-1]  # 52.80 m

# ===================================================================
# SECCION 4: MATERIALES
# Unidades de trabajo: Tonf, m, C (eUnits=12)
# Factor de conversion: 1 MPa = 101.937 tonf/m2
# ===================================================================

MPA_TO_TONF_M2 = 101.937    # 1 MPa = 10^6 N/m2 / 9806.65 N/tonf

# --- Hormigon G30 ---
MAT_CONC_NAME = "G30"
FC_MPA = 30.0                                      # f'c = 30 MPa
FC_TONF_M2 = FC_MPA * MPA_TO_TONF_M2              # ~3058.1 tonf/m2
EC_MPA = 4700.0 * math.sqrt(FC_MPA)               # 25,742.96 MPa
EC_TONF_M2 = EC_MPA * MPA_TO_TONF_M2              # ~2,624,270 tonf/m2
POISSON_CONC = 0.20
ALPHA_THERMAL_CONC = 1.0e-05                       # /C
GAMMA_CONC = 2.50                                  # tonf/m3 (incluye armaduras)
# Parametros no lineales hormigon (SetOConcrete_1)
CONC_STRAIN_FC = 0.002216     # Deformacion en f'c (Mander)
CONC_STRAIN_ULT = 0.005       # Deformacion ultima
CONC_FINAL_SLOPE = -0.1       # Pendiente post-pico

# --- Acero de refuerzo A630-420H ---
MAT_REBAR_NAME = "A630-420H"
FY_MPA = 420.0                                     # fy = 420 MPa
FY_TONF_M2 = FY_MPA * MPA_TO_TONF_M2             # ~42,813.5 tonf/m2
FU_MPA = 630.0                                     # fu = 630 MPa
FU_TONF_M2 = FU_MPA * MPA_TO_TONF_M2             # ~64,220.3 tonf/m2
ES_MPA = 200000.0                                  # Es = 200,000 MPa
ES_TONF_M2 = ES_MPA * MPA_TO_TONF_M2             # ~20,387,400 tonf/m2
POISSON_STEEL = 0.30
ALPHA_THERMAL_STEEL = 1.17e-05                     # /C
GAMMA_STEEL = 7.85                                 # tonf/m3
# Parametros no lineales acero (SetORebar_1)
EFY_MPA = FY_MPA * 1.17                           # Expected fy (factor Ry=1.17)
EFU_MPA = FU_MPA * 1.08                           # Expected fu
EFY_TONF_M2 = EFY_MPA * MPA_TO_TONF_M2
EFU_TONF_M2 = EFU_MPA * MPA_TO_TONF_M2
REBAR_STRAIN_HARD = 0.01      # Deformacion inicio endurecimiento
REBAR_STRAIN_ULT = 0.09       # Deformacion ultima
REBAR_FINAL_SLOPE = -0.1

# ===================================================================
# SECCION 5: SECCIONES (frames y areas)
# ===================================================================

# Vigas invertidas 20/60 cm
VIGA_NAME = "VI20x60G30"
VIGA_B = 0.20                  # Ancho (m) — T2 en ETABS
VIGA_H = 0.60                  # Peralte (m) — T3 en ETABS
VIGA_CARDINAL_POINT = CP_BOTTOM_CENTER   # Punto 2: vigas invertidas

# Muros de hormigon armado
MURO_30_NAME = "MHA30G30"
MURO_30_ESP = 0.30             # Espesor (m)
MURO_20_NAME = "MHA20G30"
MURO_20_ESP = 0.20             # Espesor (m)

# Losa maciza
LOSA_NAME = "Losa15G30"
LOSA_ESP = 0.15                # Espesor (m)

# Modifiers para vigas: J=0 (practica chilena — anular rigidez torsional)
# [A, As2, As3, J, I22, I33, M, W]
VIGA_MODIFIERS = [1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0]

# Modifiers para losas: inercia a flexion al 25% (practica chilena)
# [f11, f22, f12, m11, m22, m12, v13, v23, Mass, Weight]
LOSA_MODIFIERS = [1.0, 1.0, 1.0, 0.25, 0.25, 0.25, 1.0, 1.0, 1.0, 1.0]

# AutoMesh para muros y losas
AUTOMESH_SIZE = 1.00           # m (guia UI: 1.0m — consistente con practica Lafontaine)

# ===================================================================
# SECCION 6: MUROS — Posiciones verificadas contra planos
# Cada tupla: (eje, x_fijo, y_ini, y_fin, espesor) para dir Y
#             (eje, y_fijo, x_ini, x_fin, espesor) para dir X
# ===================================================================

# --- MUROS DIRECCION Y (verticales en planta, corren en dir Y) ---
# Regla general: Ejes 1,3,4,5,7,12,13,14,16,17 -> 30cm. Resto -> 20cm.
# Los muros NO cruzan el pasillo central (entre C y D)

MUROS_DIR_Y = [
    # (eje, x, y_ini, y_fin, espesor)
    ('1',  GRID_X['1'],  GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
    ('2',  GRID_X['2'],  GRID_Y['A'], GRID_Y['B'], MURO_20_ESP),
    ('2',  GRID_X['2'],  GRID_Y['D'], GRID_Y['F'], MURO_20_ESP),
    ('3',  GRID_X['3'],  GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
    ('3',  GRID_X['3'],  GRID_Y['D'], GRID_Y['F'], MURO_30_ESP),
    ('4',  GRID_X['4'],  GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
    ('4',  GRID_X['4'],  GRID_Y['D'], GRID_Y['F'], MURO_30_ESP),
    ('5',  GRID_X['5'],  GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
    ('5',  GRID_X['5'],  GRID_Y['D'], GRID_Y['F'], MURO_30_ESP),
    ('6',  GRID_X['6'],  GRID_Y['D'], GRID_Y['F'], MURO_20_ESP),
    ('7',  GRID_X['7'],  GRID_Y['D'], GRID_Y['F'], MURO_30_ESP),
    ('8',  GRID_X['8'],  GRID_Y['A'], GRID_Y['B'], MURO_20_ESP),
    ('9',  GRID_X['9'],  GRID_Y['A'], GRID_Y['B'], MURO_20_ESP),
    ('10', GRID_X['10'], GRID_Y['A'], GRID_Y['B'], MURO_20_ESP),
    ('10', GRID_X['10'], GRID_Y['D'], GRID_Y['F'], MURO_20_ESP),
    ('11', GRID_X['11'], GRID_Y['D'], GRID_Y['F'], MURO_20_ESP),
    ('12', GRID_X['12'], GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
    ('12', GRID_X['12'], GRID_Y['D'], GRID_Y['F'], MURO_30_ESP),
    ('13', GRID_X['13'], GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
    ('13', GRID_X['13'], GRID_Y['D'], GRID_Y['F'], MURO_30_ESP),
    ('14', GRID_X['14'], GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
    ('14', GRID_X['14'], GRID_Y['D'], GRID_Y['F'], MURO_30_ESP),
    ('15', GRID_X['15'], GRID_Y['D'], GRID_Y['F'], MURO_20_ESP),
    ('16', GRID_X['16'], GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
    ('16', GRID_X['16'], GRID_Y['D'], GRID_Y['F'], MURO_30_ESP),
    ('17', GRID_X['17'], GRID_Y['A'], GRID_Y['C'], MURO_30_ESP),
]

# --- MUROS DIRECCION X (horizontales en planta, corren en dir X) ---
# Eje C: entre ejes 3-6 y 10-14 son 30cm. Resto 20cm.
# Fuente: Elevacion Eje C y Eje D (Enunciado pag 6)

MUROS_DIR_X = [
    # (eje, y, x_ini, x_fin, espesor)
    # Eje A: stubs cortos
    ('A', GRID_Y['A'], GRID_X['2'],  GRID_X['3'],  MURO_20_ESP),
    ('A', GRID_Y['A'], GRID_X['4'],  GRID_X['5'],  MURO_20_ESP),
    ('A', GRID_Y['A'], GRID_X['8'],  GRID_X['9'],  MURO_20_ESP),
    ('A', GRID_Y['A'], GRID_X['12'], GRID_X['13'], MURO_20_ESP),
    ('A', GRID_Y['A'], GRID_X['16'], GRID_X['17'], MURO_20_ESP),

    # Eje C: machones principales — 8 segmentos
    ('C', GRID_Y['C'], GRID_X['1'],  GRID_X['3'],  MURO_20_ESP),
    ('C', GRID_Y['C'], GRID_X['3'],  GRID_X['4'],  MURO_30_ESP),
    ('C', GRID_Y['C'], GRID_X['5'],  GRID_X['6'],  MURO_30_ESP),
    ('C', GRID_Y['C'], GRID_X['7'],  GRID_X['8'],  MURO_20_ESP),
    ('C', GRID_Y['C'], GRID_X['10'], GRID_X['11'], MURO_30_ESP),
    ('C', GRID_Y['C'], GRID_X['11'], GRID_X['12'], MURO_30_ESP),
    ('C', GRID_Y['C'], GRID_X['13'], GRID_X['14'], MURO_30_ESP),
    ('C', GRID_Y['C'], GRID_X['14'], GRID_X['17'], MURO_20_ESP),

    # Eje D: 5 machones
    ('D', GRID_Y['D'], GRID_X['2'],  GRID_X['3'],  MURO_20_ESP),
    ('D', GRID_Y['D'], GRID_X['4'],  GRID_X['5'],  MURO_20_ESP),
    ('D', GRID_Y['D'], GRID_X['10'], GRID_X['11'], MURO_20_ESP),
    ('D', GRID_Y['D'], GRID_X['12'], GRID_X['13'], MURO_20_ESP),
    ('D', GRID_Y['D'], GRID_X['14'], GRID_X['15'], MURO_20_ESP),

    # Eje E: stubs superiores pasillo
    ('E', GRID_Y['E'], GRID_X['2'],  GRID_X['3'],  MURO_20_ESP),
    ('E', GRID_Y['E'], GRID_X['4'],  GRID_X['5'],  MURO_20_ESP),
    ('E', GRID_Y['E'], GRID_X['10'], GRID_X['11'], MURO_20_ESP),
    ('E', GRID_Y['E'], GRID_X['14'], GRID_X['15'], MURO_20_ESP),

    # Eje F: muro centrado en eje 10 (L=7.70m por enunciado pag 3)
    ('F', GRID_Y['F'], GRID_X['10'] - 4.25, GRID_X['10'] + 3.45, MURO_20_ESP),
]

# Totales para verificacion
N_MUROS_DIR_Y = len(MUROS_DIR_Y)   # 26 segmentos
N_MUROS_DIR_X = len(MUROS_DIR_X)   # 23 segmentos

# ===================================================================
# SECCION 7: VIGAS — Posiciones desde planta tipo (Enunciado pag 2)
# Todas VI20x60G30, vigas invertidas (Cardinal Point 2)
# Tupla: (y_fijo, x_ini, x_fin)
# ===================================================================

VIGAS_EJE_A = [
    (GRID_Y['A'], GRID_X['1'],  GRID_X['2']),
    (GRID_Y['A'], GRID_X['3'],  GRID_X['4']),
    (GRID_Y['A'], GRID_X['5'],  GRID_X['6']),
    (GRID_Y['A'], GRID_X['7'],  GRID_X['8']),
    (GRID_Y['A'], GRID_X['9'],  GRID_X['10']),
    (GRID_Y['A'], GRID_X['10'], GRID_X['11']),
    (GRID_Y['A'], GRID_X['11'], GRID_X['12']),
    (GRID_Y['A'], GRID_X['13'], GRID_X['14']),
    (GRID_Y['A'], GRID_X['14'], GRID_X['15']),
    (GRID_Y['A'], GRID_X['15'], GRID_X['16']),
]

VIGAS_EJE_F = [
    (GRID_Y['F'], GRID_X['2'],  GRID_X['3']),
    (GRID_Y['F'], GRID_X['3'],  GRID_X['4']),
    (GRID_Y['F'], GRID_X['5'],  GRID_X['6']),
    (GRID_Y['F'], GRID_X['6'],  GRID_X['7']),
    (GRID_Y['F'], GRID_X['11'], GRID_X['12']),
    (GRID_Y['F'], GRID_X['12'], GRID_X['13']),
    (GRID_Y['F'], GRID_X['13'], GRID_X['14']),
    (GRID_Y['F'], GRID_X['15'], GRID_X['16']),
]

VIGAS_EJE_B = [
    (GRID_Y['B'], GRID_X['1'],  GRID_X['2']),
    (GRID_Y['B'], GRID_X['3'],  GRID_X['4']),
    (GRID_Y['B'], GRID_X['5'],  GRID_X['6']),
    (GRID_Y['B'], GRID_X['6'],  GRID_X['7']),
    (GRID_Y['B'], GRID_X['7'],  GRID_X['8']),
    (GRID_Y['B'], GRID_X['9'],  GRID_X['10']),
    (GRID_Y['B'], GRID_X['10'], GRID_X['11']),
    (GRID_Y['B'], GRID_X['11'], GRID_X['12']),
    (GRID_Y['B'], GRID_X['13'], GRID_X['14']),
    (GRID_Y['B'], GRID_X['14'], GRID_X['15']),
    (GRID_Y['B'], GRID_X['15'], GRID_X['16']),
    (GRID_Y['B'], GRID_X['16'], GRID_X['17']),
]

VIGAS = VIGAS_EJE_A + VIGAS_EJE_F + VIGAS_EJE_B
N_VIGAS = len(VIGAS)   # 30 por piso

# ===================================================================
# SECCION 8: LOSAS — Huella real (no envolvente)
# Excluye: shaft ascensor (ejes 9-11, C-D), zona acceso (ejes 1-3, A-B)
# Fuente: Enunciado pag 2 y 4
# ===================================================================

def _rect_axes(x_ini, x_fin, y_ini, y_fin):
    """Convierte nombres de eje a coordenadas (x0, y0, x1, y1)."""
    return (GRID_X[x_ini], GRID_Y[y_ini], GRID_X[x_fin], GRID_Y[y_fin])


SLAB_PANELS_FLOOR = [
    _rect_axes('3',  '6',  'A', 'B'),   # Sur poniente
    _rect_axes('7',  '8',  'A', 'B'),   # Sur centro
    _rect_axes('9',  '16', 'A', 'B'),   # Sur oriente
    _rect_axes('3',  '17', 'B', 'C'),   # Franja central sur
    _rect_axes('3',  '9',  'C', 'D'),   # Pasillo poniente (sin shaft)
    _rect_axes('11', '17', 'C', 'D'),   # Pasillo oriente (sin shaft)
    _rect_axes('3',  '17', 'D', 'F'),   # Franja central norte
]

SLAB_PANELS_ROOF = [
    _rect_axes('3',  '16', 'A', 'B'),   # Techo sur (sin 16-17)
    _rect_axes('3',  '17', 'B', 'C'),   # Techo franja sur
    _rect_axes('3',  '9',  'C', 'D'),   # Techo pasillo pon.
    _rect_axes('11', '17', 'C', 'D'),   # Techo pasillo ori.
    _rect_axes('3',  '17', 'D', 'F'),   # Techo franja norte
]


def _rect_area(panel):
    """Area de un panel rectangular (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = panel
    return abs((x1 - x0) * (y1 - y0))


def _rect_centroid(panel):
    """Centroide de un panel rectangular."""
    x0, y0, x1, y1 = panel
    return ((x0 + x1) / 2.0, (y0 + y1) / 2.0)


def _panels_area(panels):
    """Area total de una lista de paneles."""
    return sum(_rect_area(p) for p in panels)


def _panels_centroid(panels):
    """Centroide ponderado de una lista de paneles."""
    total = _panels_area(panels)
    if total <= 0:
        return (0.0, 0.0)
    sx, sy = 0.0, 0.0
    for p in panels:
        a = _rect_area(p)
        cx, cy = _rect_centroid(p)
        sx += a * cx
        sy += a * cy
    return (sx / total, sy / total)


# Areas calculadas
AREA_PISO_TIPO = _panels_area(SLAB_PANELS_FLOOR)    # ~468 m2
AREA_TECHO = _panels_area(SLAB_PANELS_ROOF)
AREA_TOTAL_NIVELES = AREA_PISO_TIPO * (N_STORIES - 1) + AREA_TECHO
AREA_PLANTA = AREA_TOTAL_NIVELES / N_STORIES

# Centroides
CM_X, CM_Y = _panels_centroid(SLAB_PANELS_FLOOR)
CM_X_TECHO, CM_Y_TECHO = _panels_centroid(SLAB_PANELS_ROOF)

# ===================================================================
# SECCION 9: CARGAS
# Unidades: tonf/m2 (para ETABS en Tonf_m_C)
# Fuente: Enunciado Taller + NCh1537
# ===================================================================

# Patrones de carga y su tipo ETABS
LOAD_PATTERNS = {
    # nombre: (eLoadPatternType, SelfWeightMultiplier)
    'PP':   (LTYPE_DEAD,      1.0),     # Peso propio (SWM=1)
    'TERP': (LTYPE_SUPERDEAD, 0.0),     # Terminaciones pisos
    'TERT': (LTYPE_SUPERDEAD, 0.0),     # Terminaciones techo
    'SCP':  (LTYPE_LIVE,      0.0),     # Sobrecarga pisos
    'SCT':  (LTYPE_ROOFLIVE,  0.0),     # Sobrecarga techo
}

# Valores de carga en tonf/m2 (cargas se aplican negativas = gravedad)
TERP_PISO = 0.140       # 140 kgf/m2 = 0.140 tonf/m2
TERT_TECHO = 0.100       # 100 kgf/m2
SCP_OFICINA = 0.250      # 250 kgf/m2 (oficinas)
SCP_PASILLO = 0.500      # 500 kgf/m2 (pasillos comunes)
SCT_TECHO = 0.100        # 100 kgf/m2

# Mass Source: NCh433 requiere PP + TERP + TERT + 0.25*SCP
# TERT SF=1.0 (terminaciones techo son carga permanente, contribuyen a masa)
MASS_SOURCE_PATTERNS = {
    'PP':   1.0,
    'TERP': 1.0,
    'TERT': 1.0,
    'SCP':  0.25,
}

# ===================================================================
# SECCION 10: PARAMETROS SISMICOS
# NCh433 Mod 2009 + DS61
# Caso: Zona 3, Suelo C, Oficina (Cat. II), Muros HA
# ===================================================================

ZONA_SISMICA = 3
AO_G = 0.40                  # Ao/g — NCh433 Tabla 6.2, Zona 3
AO_MS2 = AO_G * 9.81         # Ao en m/s2 = 3.924
SUELO = 'C'
CATEGORIA = 'II'              # Oficinas
I_FACTOR = 1.0                # NCh433 Tabla 6.1, Cat II
G_ACCEL = 9.81                # m/s2

# Parametros de suelo — DS61 Tabla 12.3
S_SUELO = 1.05
TO_SUELO = 0.40               # s
T_PRIME = 0.45                 # s (T')
N_SUELO = 1.40
P_SUELO = 1.60

# Sistema estructural — NCh433 Tabla 5.1 (Muros HA)
R_MUROS = 7                   # Factor de modificacion de respuesta
RO_MUROS = 11                 # Factor de sobreresistencia

# Torsion accidental — NCh433 Art. 6.3.3
EA_X = 0.05 * LX_PLANTA       # Excentricidad accidental dir X (para SY)
EA_Y = 0.05 * LY_PLANTA       # Excentricidad accidental dir Y (para SX)

# Espectro: archivo generado por calc_espectro.py
SPECTRUM_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "espectro_elastico_Z3SC.txt")
SPECTRUM_DAMPING = 0.05        # 5%
SPECTRUM_SF = G_ACCEL          # 9.81 — convierte Sa/g a m/s2

# Diafragma
DIAPHRAGM_RIGID_NAME = "D1"
DIAPHRAGM_SEMI_NAME = "D1_Semi"

# Combinaciones NCh3171 (11 combos LRFD)
# Formato: {nombre: [(factor, patron), ...]}
# Nombres sismos: SDX/SDY (response spectrum cases definidos en 08_seismic.py)
COMBINATIONS = {
    'C1': [(1.4, 'PP'), (1.4, 'TERP'), (1.4, 'TERT')],
    'C2': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.6, 'SCP'), (0.5, 'SCT')],
    'C3': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.6, 'SCT'), (1.0, 'SCP')],
    'C4': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (0.5, 'SCT'), (1.4, 'SDX')],
    'C5': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (0.5, 'SCT'), (-1.4, 'SDX')],
    'C6': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (0.5, 'SCT'), (1.4, 'SDY')],
    'C7': [(1.2, 'PP'), (1.2, 'TERP'), (1.2, 'TERT'), (1.0, 'SCP'), (0.5, 'SCT'), (-1.4, 'SDY')],
    'C8': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (1.4, 'SDX')],
    'C9': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (-1.4, 'SDX')],
    'C10': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (1.4, 'SDY')],
    'C11': [(0.9, 'PP'), (0.9, 'TERP'), (0.9, 'TERT'), (-1.4, 'SDY')],
}

# Valores esperados de validacion (orden de magnitud)
PESO_ESPERADO_TONF = AREA_PLANTA * N_STORIES * 1.0   # ~1 tonf/m2 regla Lafontaine
DRIFT_LIMITE = 0.002           # NCh433 limite drift CM

# ===================================================================
# SECCION 11: FORMULAS SISMICAS VERIFICADAS
# ===================================================================

def calc_alpha(T, To=TO_SUELO, p=P_SUELO):
    """Factor de amplificacion espectral — NCh433 Art. 6.3.5.2, Ec. (9).

    alpha(T) = [1 + 4.5*(T/To)^p] / [1 + (T/To)^3]

    El exponente del denominador es 3 FIJO (no depende del suelo).
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


def calc_R_star(T_star, Ro=RO_MUROS, To=TO_SUELO):
    """Factor de reduccion espectral R* — NCh433 Art. 6.3.5.3, Ec. (10).

    R* = 1 + T* / (0.10*To + T*/Ro)

    Verificada contra texto literal de NCh433 (pag 39 del PDF).
    Para T*=1.0-1.3s con Ro=11, Suelo C: R* ~ 8.6-9.2
    """
    if T_star <= 0:
        return 1.0
    denom = 0.10 * To + T_star / Ro
    return 1.0 + T_star / denom


def calc_R_star_alt(T_star, N=N_STORIES, Ro=RO_MUROS, To=TO_SUELO):
    """R* alternativo para muros — NCh433 Art. 6.3.5.4, Ec. (11).

    R* = 1 + 4*N*T* / (N*Ro*To + T*)

    Opcion CONSERVADORA (da R* menor -> fuerzas mayores).
    Solo valida para edificios de muros.
    """
    if T_star <= 0:
        return 1.0
    return 1.0 + 4.0 * N * T_star / (N * Ro * To + T_star)


def calc_C(T_star, S=S_SUELO, Ao=AO_G, R=R_MUROS, Tp=T_PRIME,
           n=N_SUELO, g=G_ACCEL):
    """Coeficiente sismico C — NCh433 Art. 6.2.3.1, Ec. (2).

    C = 2.75 * S * Ao / (g * R) * (T'/T*)^n

    Usado en metodo estatico. Resultado adimensional.
    """
    if T_star <= 0:
        return 0.0
    return 2.75 * S * Ao * g / (g * R) * (Tp / T_star) ** n


def calc_Cmin(I=I_FACTOR, S=S_SUELO, Ao=AO_G, g=G_ACCEL):
    """Coeficiente sismico minimo — NCh433 Art. 6.3.7.

    Cmin = Ao*S / (6*g)    para edificios Cat I y II
    """
    return Ao * S * g / (6.0 * g)


def calc_Cmax(S=S_SUELO, Ao=AO_G, R=R_MUROS, g=G_ACCEL):
    """Coeficiente sismico maximo — NCh433 Art. 6.2.3.1.

    Cmax = 0.35 * S * Ao / g  (para T* <= T')
    """
    return 0.35 * S * Ao * g / g


# ===================================================================
# SECCION 12: CONEXION COM — ETABS v19
# Patron robusto: GetActiveObject -> Helper.GetObject -> CreateObject
# Fuente: Investigacion R02, verificada en repos multiples
# ===================================================================

# Variables globales COM — MANTENER para evitar garbage collection
_helper = None
_etabs_obj = None
_sap_model = None


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


def connect(create_if_missing=False, clean_gen=True):
    """Conectar a ETABS v19 via COM.

    Prioridad de conexion:
      1. GetActiveObject — requiere ETABS abierto con modelo
      2. Helper.GetObject — mas robusto en algunas versiones de comtypes
      3. CreateObject — SOLO si create_if_missing=True (PELIGROSO)

    Args:
        create_if_missing: Si True, crea nueva instancia como ultimo recurso.
            ADVERTENCIA: puede crear instancia invisible. File.Save puede
            producir .edb corrupto sin UI funcional.
        clean_gen: Si True, limpia comtypes.gen antes de importar.

    Returns:
        SapModel object (acceso a toda la API ETABS)

    Raises:
        ConnectionError: Si no se puede conectar a ETABS
        ImportError: Si comtypes no esta instalado
    """
    global _helper, _etabs_obj, _sap_model

    if clean_gen:
        clean_comtypes_gen()

    import comtypes.client

    # --- Metodo 1: GetActiveObject (RECOMENDADO) ---
    try:
        _etabs_obj = comtypes.client.GetActiveObject(ETABS_PROGID)
        _sap_model = _etabs_obj.SapModel
        log.info("Conectado via GetActiveObject")
        return _sap_model
    except (OSError, comtypes.COMError):
        log.debug("GetActiveObject fallo — probando Helper...")

    # --- Metodo 2: Helper.GetObject ---
    try:
        _helper = comtypes.client.CreateObject(HELPER_PROGID)
        import comtypes.gen.ETABSv1 as ETABSv1
        _helper = _helper.QueryInterface(ETABSv1.cHelper)
        _etabs_obj = _helper.GetObject(ETABS_PROGID)
        _sap_model = _etabs_obj.SapModel
        log.info("Conectado via Helper.GetObject")
        return _sap_model
    except Exception:
        log.debug("Helper.GetObject fallo")

    # --- Metodo 3: CreateObject (PELIGROSO) ---
    if create_if_missing:
        log.warning("Creando nueva instancia ETABS — puede ser invisible")
        _helper = comtypes.client.CreateObject(HELPER_PROGID)
        import comtypes.gen.ETABSv1 as ETABSv1
        _helper = _helper.QueryInterface(ETABSv1.cHelper)
        _etabs_obj = _helper.CreateObjectProgID(ETABS_PROGID)
        try:
            _etabs_obj.Visible = True
        except Exception:
            pass
        _etabs_obj.ApplicationStart()
        time.sleep(15)
        _sap_model = _etabs_obj.SapModel
        log.warning("Conectado via CreateObject — verificar que UI sea visible")
        return _sap_model

    raise ConnectionError(
        "No se pudo conectar a ETABS.\n"
        "Asegurate de:\n"
        "  1. Abrir ETABS v19 manualmente\n"
        "  2. File > New Model > Blank (o abrir un modelo existente)\n"
        "  3. Luego ejecutar este script"
    )


def disconnect(save_path=None):
    """Desconectar de ETABS correctamente.

    Args:
        save_path: Si se proporciona, guarda el modelo antes de cerrar.
            NOTA: File.Save via COM solo funciona si ETABS tiene UI activa.
    """
    global _helper, _etabs_obj, _sap_model

    if _sap_model is not None and save_path:
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
    if _etabs_obj is not None:
        try:
            _etabs_obj.ApplicationExit(False)
            log.info("ETABS cerrado via ApplicationExit")
        except Exception:
            pass
    _etabs_obj = None
    _helper = None


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
# SECCION 13: FUNCIONES HELPER ETABS
# ===================================================================

def check_ret(ret, msg=""):
    """Verificar return value de API ETABS.

    Todas las funciones CSI OAPI retornan 0 en exito.
    Lanza RuntimeError si ret != 0.
    """
    if isinstance(ret, tuple):
        code = ret[-1] if len(ret) > 1 else ret[0]
    else:
        code = ret

    if code != 0:
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


def set_units(units=UNITS_TONF_M_C):
    """Establecer unidades del modelo."""
    model = get_model()
    ret = model.SetPresentUnits(units)
    check_ret(ret, f"SetPresentUnits({units})")


def get_section_name(espesor):
    """Dado un espesor de muro, retorna el nombre de seccion."""
    if abs(espesor - MURO_30_ESP) < 0.01:
        return MURO_30_NAME
    elif abs(espesor - MURO_20_ESP) < 0.01:
        return MURO_20_NAME
    else:
        raise ValueError(f"Espesor de muro no reconocido: {espesor}")


# ===================================================================
# SECCION 14: RUTAS DEL PROYECTO
# ===================================================================

# Directorio de este script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Directorio raiz del proyecto
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
# Donde guardar modelos ETABS
MODELS_DIR = os.path.join(SCRIPT_DIR, "models")


# ===================================================================
# MAIN — Verificacion de datos al ejecutar directamente
# ===================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("EDIFICIO 1 — Taller ADSE UCN 1S-2026")
    print("=" * 60)

    print(f"\n--- Grilla ---")
    print(f"  Ejes X: {N_LINES_X}  |  Ejes Y: {N_LINES_Y}")
    print(f"  Lx = {LX_PLANTA:.3f} m  |  Ly = {LY_PLANTA:.3f} m")
    print(f"  Area envolvente = {AREA_ENVOLVENTE:.1f} m2")

    print(f"\n--- Pisos ---")
    print(f"  N = {N_STORIES}")
    print(f"  h1 = {STORY_HEIGHT_1} m  |  h_tip = {STORY_HEIGHT_TYP} m")
    print(f"  H total = {H_TOTAL:.1f} m")
    print(f"  Elevaciones: {STORY_ELEVATIONS[0]}, {STORY_ELEVATIONS[1]}, "
          f"..., {STORY_ELEVATIONS[-1]} m")

    print(f"\n--- Materiales (en Tonf_m_C) ---")
    print(f"  G30: f'c={FC_TONF_M2:.1f} tonf/m2, Ec={EC_TONF_M2:.0f} tonf/m2, "
          f"gamma={GAMMA_CONC} tonf/m3")
    print(f"  A630-420H: fy={FY_TONF_M2:.1f}, fu={FU_TONF_M2:.1f}, "
          f"Es={ES_TONF_M2:.0f} tonf/m2")

    print(f"\n--- Secciones ---")
    print(f"  Viga: {VIGA_NAME} ({VIGA_B}x{VIGA_H}m)")
    print(f"  Muro 30: {MURO_30_NAME} (e={MURO_30_ESP}m)")
    print(f"  Muro 20: {MURO_20_NAME} (e={MURO_20_ESP}m)")
    print(f"  Losa: {LOSA_NAME} (e={LOSA_ESP}m)")

    print(f"\n--- Geometria ---")
    print(f"  Muros dir Y: {N_MUROS_DIR_Y} segmentos")
    print(f"  Muros dir X: {N_MUROS_DIR_X} segmentos")
    print(f"  Vigas: {N_VIGAS} por piso")
    print(f"  Losa pisos: {len(SLAB_PANELS_FLOOR)} paneles, "
          f"A={AREA_PISO_TIPO:.1f} m2")
    print(f"  Losa techo: {len(SLAB_PANELS_ROOF)} paneles, "
          f"A={AREA_TECHO:.1f} m2")
    print(f"  CM piso tipo: ({CM_X:.3f}, {CM_Y:.3f}) m")

    print(f"\n--- Cargas (tonf/m2) ---")
    print(f"  TERP = {TERP_PISO}  |  TERT = {TERT_TECHO}")
    print(f"  SCP oficina = {SCP_OFICINA}  |  SCP pasillo = {SCP_PASILLO}")
    print(f"  SCT = {SCT_TECHO}")

    print(f"\n--- Parametros sismicos ---")
    print(f"  Zona {ZONA_SISMICA}, Ao={AO_G}g, Suelo {SUELO}")
    print(f"  S={S_SUELO}, To={TO_SUELO}s, T'={T_PRIME}s, "
          f"n={N_SUELO}, p={P_SUELO}")
    print(f"  R={R_MUROS}, Ro={RO_MUROS}, I={I_FACTOR}")
    print(f"  EA_x = {EA_X:.3f} m  |  EA_y = {EA_Y:.3f} m")

    print(f"\n--- Formulas sismicas ---")
    for T in [0.5, 1.0, 1.3, 1.5, 2.0]:
        a = calc_alpha(T)
        R_s = calc_R_star(T)
        R_alt = calc_R_star_alt(T)
        Sa = calc_Sa_g(T)
        print(f"  T={T:.1f}s: alpha={a:.4f}, Sa/g={Sa:.4f}, "
              f"R*={R_s:.3f}, R*_alt={R_alt:.3f}")

    Cmin = calc_Cmin()
    Cmax = calc_Cmax()
    print(f"\n  Cmin = {Cmin:.5f}  |  Cmax = {Cmax:.5f}")
    print(f"  Peso esperado ~ {PESO_ESPERADO_TONF:.0f} tonf "
          f"({AREA_PLANTA:.1f} m2 x {N_STORIES} pisos x 1 tonf/m2)")

    print(f"\n--- Espectro ---")
    if os.path.exists(SPECTRUM_FILE):
        print(f"  Archivo: {SPECTRUM_FILE} [OK]")
    else:
        print(f"  Archivo: {SPECTRUM_FILE} [NO ENCONTRADO]")
        print(f"  Ejecutar: python calc_espectro.py")

    print(f"\n--- COM ---")
    try:
        import comtypes
        print(f"  comtypes v{comtypes.__version__} [OK]")
    except ImportError:
        print("  comtypes NO instalado — pip install comtypes")

    print("\n" + "=" * 60)
    print("Config OK")
