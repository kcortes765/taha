"""
prepare_ws_bundle_ed2.py - Crea bundle portable para WS UCN o revision externa.

Salida:
- carpeta en `transfer/ed2_ws_bundle_<tag>/`
- zip gemelo con maximo 20 archivos dentro del bundle

El bundle queda enfocado a:
- correr Ed.2 en ETABS 21 desde consola
- empaquetar evidencia de vuelta
- validar con `verify_ed2.py`
"""

import argparse
import os
import shutil
import sys
import zipfile
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import SCRIPT_DIR, TRANSFER_DIR
from ed2_static_official import ensure_transfer_dir


BUNDLE_FILES = [
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
    "config_ed2.py",
    "diag.py",
    "run_pipeline_ed2.py",
    "ed2_static_official.py",
    "verify_ed2.py",
    "package_transfer_ed2.py",
    "espectro_elastico_Z3SC.txt",
]

README_NAME = "00_README_WS.txt"
MAX_FILES = 20


def build_readme() -> str:
    return (
        "ED2 WS UCN BUNDLE - ETABS 21\n"
        "\n"
        "Base WS esperada:\n"
        "  C:\\Users\\Civil\\Documents\\taha\n"
        "\n"
        "Uso recomendado en PowerShell:\n"
        "  cd C:\\Users\\Civil\\Documents\\taha\\ed2_ws_bundle\n"
        "  $env:ED2_RUNTIME_ROOT='C:\\Users\\Civil\\Documents\\taha'\n"
        "  python diag.py --create-if-missing\n"
        "  python run_pipeline_ed2.py --create-if-missing --model .\\models\\Edificio2_parte1_oficial.edb\n"
        "  python verify_ed2.py\n"
        "  python package_transfer_ed2.py --tag preliminar_ws\n"
        "\n"
        "Artefactos que deben volver:\n"
        "  - models\\Edificio2_parte1_oficial.edb\n"
        "  - results\\*.csv\n"
        "  - results\\*.json\n"
        "  - transfer\\ed2_transfer_*.zip\n"
        "\n"
        "Si solo quieres retomar fase 2:\n"
        "  python run_pipeline_ed2.py --phase 2 --model .\\models\\Edificio2_parte1_oficial.edb\n"
    )


def zip_dir(folder: str, zip_path: str):
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(os.listdir(folder)):
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                zf.write(path, name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="ws", help="Tag short for output folder/zip")
    args = parser.parse_args()

    ensure_transfer_dir()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_tag = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in args.tag)
    bundle_dir = os.path.join(TRANSFER_DIR, f"ed2_ws_bundle_{safe_tag}_{stamp}")
    zip_path = bundle_dir + ".zip"
    os.makedirs(bundle_dir, exist_ok=True)

    missing = []
    for name in BUNDLE_FILES:
        src = os.path.join(SCRIPT_DIR, name)
        if not os.path.isfile(src):
            missing.append(name)
            continue
        shutil.copy2(src, os.path.join(bundle_dir, name))

    readme_path = os.path.join(bundle_dir, README_NAME)
    with open(readme_path, "w", encoding="utf-8") as handle:
        handle.write(build_readme())

    if missing:
        print("Faltan archivos para el bundle:")
        for name in missing:
            print(f"  - {name}")
        return 1

    file_count = len([name for name in os.listdir(bundle_dir) if os.path.isfile(os.path.join(bundle_dir, name))])
    if file_count > MAX_FILES:
        print(f"Bundle excede el maximo de {MAX_FILES} archivos: {file_count}")
        return 1

    zip_dir(bundle_dir, zip_path)

    print(f"Bundle dir: {bundle_dir}")
    print(f"Bundle zip: {zip_path}")
    print(f"Files:      {file_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
