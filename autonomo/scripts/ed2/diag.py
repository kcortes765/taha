r"""
diag.py - Diagnostico COM para ETABS 21 en WS UCN
Corre ANTES de ejecutar el pipeline. Verifica:
  1. Python version
  2. comtypes instalado
  3. ETABS corriendo y accesible via COM (tries multiple methods)
  4. Modelo abierto, unidades, version
  5. Archivos del pipeline presentes

Uso:
  python diag.py
  python diag.py --create-if-missing
  python diag.py --model C:\ruta\Edificio2_parte1_oficial.edb
"""
import sys
import os
import importlib
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from config_ed2 import (
    ENV_CREATE_IF_MISSING,
    ENV_FORCE_MODEL_OPEN,
    ENV_MODEL_PATH,
    MODELS_DIR,
    RESULTS_DIR,
    RUNTIME_ROOT,
    TRANSFER_DIR,
    connect,
)


parser = argparse.ArgumentParser()
parser.add_argument("--create-if-missing", action="store_true", help="Launch ETABS if no running instance is found")
parser.add_argument("--model", help="Open/force this .edb after connecting")
args = parser.parse_args()

if args.create_if_missing:
    os.environ[ENV_CREATE_IF_MISSING] = "1"
if args.model:
    os.environ[ENV_MODEL_PATH] = os.path.abspath(args.model)
    os.environ[ENV_FORCE_MODEL_OPEN] = "1"

print("=" * 60)
print("  DIAGNOSTICO COM - ETABS 21 - Edificio 2")
print("=" * 60)
print()
print(f"Runtime root: {RUNTIME_ROOT}")
print(f"Models dir:   {MODELS_DIR}")
print(f"Results dir:  {RESULTS_DIR}")
print(f"Transfer dir: {TRANSFER_DIR}")
print()

# --- 1. Python ---
print(f"[1] Python: {sys.version}")
print(f"    Arch: {sys.maxsize > 2**32 and '64-bit' or '32-bit'}")
print(f"    Path: {sys.executable}")
ok_python = sys.version_info >= (3, 7)
print(f"    {'PASS' if ok_python else 'FAIL: necesita Python 3.7+'}")
print()

# --- 2. comtypes ---
try:
    import comtypes
    import comtypes.client
    print(f"[2] comtypes: {comtypes.__version__}")

    # Limpiar gen stale
    gen_path = os.path.join(os.path.dirname(comtypes.__file__), "gen")
    if os.path.exists(gen_path):
        import shutil
        try:
            shutil.rmtree(gen_path)
            os.makedirs(gen_path)
            with open(os.path.join(gen_path, "__init__.py"), "w") as f:
                f.write("")
            print("    comtypes.gen limpiado (stale cache)")
        except Exception as e:
            print(f"    WARNING: no se pudo limpiar comtypes.gen: {e}")
    print("    PASS")
except ImportError:
    print("[2] comtypes: NO INSTALADO")
    print("    Instalar: pip install comtypes")
    sys.exit(1)
print()

# --- 3. Conectar a ETABS ---
print("[3] Conectando a ETABS...")

sap_model = None
detected_major = 0

try:
    sap_model = connect(
        create_if_missing=args.create_if_missing,
        model_path=args.model,
        force_open_model=bool(args.model),
    )
    print("    PASS")
except Exception as e:
    print()
    print("    FAIL: No se pudo conectar a ETABS")
    print(f"    Detalle: {e}")
    print("    Asegurate de:")
    print("    1. ETABS 21 esta ABIERTO")
    print("    2. Hay un modelo abierto (File > New Model > Blank)")
    print("       o usa --create-if-missing")
    print("    3. Python es del mismo bitness que ETABS (64-bit)")
    sys.exit(1)

print()

# --- 4. Verificar modelo ---
print("[4] Verificando modelo...")
try:
    print("    SapModel: PASS")

    # Version
    etabs_version = "unknown"
    try:
        ver = sap_model.GetVersion()
        if isinstance(ver, (tuple, list)) and len(ver) >= 2:
            etabs_version = str(ver[0])
            print(f"    Version: {ver[0]} (build {ver[1]})")
            # Parse major version
            parts = etabs_version.split('.')
            major = int(parts[0]) if parts[0].isdigit() else 0
            detected_major = major
            if major == 21:
                print(f"    Version check: v21 detected — OK")
            elif major > 21:
                print(f"    Version check: v{major} detected — revisar compatibilidad, paquete endurecido para v21")
            elif major >= 19:
                print(f"    Version check: FAIL — se detectó v{major}, pero este flujo Ed.2 está cerrado para ETABS 21")
            else:
                print(f"    Version check: FAIL — v{major} no soportado para este flujo")
        else:
            print(f"    Version: {ver}")
    except Exception as e:
        print(f"    Version: no disponible ({e})")

    # Unidades actuales
    try:
        units = sap_model.GetPresentUnits()
        if isinstance(units, (tuple, list)):
            units = units[0]
        units_map = {1: "lb,in,F", 2: "lb,ft,F", 3: "kip,in,F", 4: "kip,ft,F",
                     5: "kN,mm,C", 6: "kN,m,C", 7: "kgf,mm,C", 8: "kgf,m,C",
                     9: "N,mm,C", 10: "N,m,C", 11: "Tonf,mm,C", 12: "Tonf,m,C",
                     13: "kN,cm,C", 14: "kgf,cm,C", 15: "N,cm,C", 16: "Tonf,cm,C"}
        print(f"    Unidades: {units_map.get(units, units)} (code={units})")
    except Exception as e:
        print(f"    Unidades: no disponible ({e})")

    # Nombre archivo
    try:
        fname = sap_model.GetModelFilename()
        if isinstance(fname, (tuple, list)):
            fname = fname[0]
        if fname:
            print(f"    Archivo: {fname}")
        else:
            print("    Archivo: (modelo sin guardar)")
    except Exception:
        print("    Archivo: (no disponible)")

    # Test basico: obtener numero de pisos
    try:
        ret = sap_model.Story.GetStories_2()
        if isinstance(ret, (tuple, list)) and len(ret) > 1:
            n_stories = ret[0] if isinstance(ret[0], int) else len(ret) - 1
            print(f"    Stories: {n_stories}")
        else:
            print(f"    Stories: {ret}")
    except Exception as e:
        # GetStories_2 may not exist in all versions — try GetStories
        try:
            ret = sap_model.Story.GetStories()
            if isinstance(ret, (tuple, list)) and len(ret) > 0:
                print(f"    Stories: {ret[0]} (via GetStories)")
            else:
                print(f"    Stories: {ret}")
        except Exception as e2:
            print(f"    Stories: no disponible ({e}; fallback: {e2})")

    # Test: Diaphragm availability
    try:
        diap = sap_model.Diaphragm
        if diap is not None:
            print("    Diaphragm API: PASS (available)")
        else:
            print("    Diaphragm API: None (v19 known issue — implicit creation used)")
    except Exception as e:
        print(f"    Diaphragm API: not available ({e})")

    print("    PASS")
except Exception as e:
    print(f"    FAIL: {e}")
    sys.exit(1)
print()

# --- 5. Archivos del pipeline ---
print("[5] Archivos del pipeline...")
required = [
    "config_ed2.py",
    "01_init_model_ed2.py",
    "02_materials_sections_ed2.py",
    "03_columns_ed2.py",
    "04_beams_ed2.py",
    "05_slabs_ed2.py",
    "06_assignments_ed2.py",
    "07_loads_ed2.py",
    "08_seismic_ed2.py",
    "09_torsion_ed2.py",
    "10_combinations_ed2.py",
    "11_run_analysis_ed2.py",
    "12_extract_results_ed2.py",
    "run_pipeline_ed2.py",
]

missing = []
for f in required:
    path = os.path.join(SCRIPT_DIR, f)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    status = f"PASS ({size:,} bytes)" if exists else "FAIL"
    if not exists:
        missing.append(f)
    print(f"    {f}: {status}")

# Espectro — check same dir first, then parent
espectro_paths = [
    os.path.join(SCRIPT_DIR, "espectro_elastico_Z3SC.txt"),
    os.path.join(SCRIPT_DIR, "..", "espectro_elastico_Z3SC.txt"),
]
espectro_found = False
for ep in espectro_paths:
    if os.path.exists(ep):
        print(f"    espectro: PASS ({os.path.abspath(ep)})")
        espectro_found = True
        break
if not espectro_found:
    print("    espectro: FAIL - copiar espectro_elastico_Z3SC.txt a esta carpeta")
    missing.append("espectro_elastico_Z3SC.txt")

print()

# --- Resumen ---
print("=" * 60)
n_pass = 0
n_fail = 0

checks = [
    ("Python >= 3.7", ok_python),
    ("comtypes installed", True),  # would have exited above
    ("ETABS connected", sap_model is not None),
    ("SapModel accessible", sap_model is not None),
    ("ETABS 21 detected", detected_major == 21),
    ("All scripts present", len(missing) == 0),
]

for name, passed in checks:
    status = "PASS" if passed else "FAIL"
    if passed:
        n_pass += 1
    else:
        n_fail += 1
    print(f"  [{status}] {name}")

print()
if n_fail == 0:
    print(f"  DIAGNOSTICO: ALL {n_pass} CHECKS PASSED — LISTO PARA CORRER")
    print()
    print("  Siguiente paso:")
    print("    python run_pipeline_ed2.py --phase 1")
    print()
    print("  O paso a paso:")
    print("    python 01_init_model_ed2.py")
    print("    python 02_materials_sections_ed2.py")
    print("    python 03_columns_ed2.py")
    print("    ...")
else:
    print(f"  DIAGNOSTICO: {n_fail} CHECKS FAILED")
    if missing:
        print(f"  Archivos faltantes: {', '.join(missing)}")
    if etabs_obj is None:
        print("  ETABS no conectado")
print("=" * 60)
