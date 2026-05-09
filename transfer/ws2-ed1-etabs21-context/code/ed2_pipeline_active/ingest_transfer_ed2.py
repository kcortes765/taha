"""
ingest_transfer_ed2.py - Importa evidencia Ed.2 desde un zip WS -> local.

Uso:
  python ingest_transfer_ed2.py --zip C:\ruta\ed2_transfer_preliminar_ws.zip
  python ingest_transfer_ed2.py --zip C:\ruta\ed2_transfer_preliminar_ws.zip --target-root C:\ruta\destino

Comportamiento:
- crea backup de `results/`, `models/` y logs previos si existen
- extrae contenido del zip al target root
- valida presencia de manifest
"""

import argparse
import os
import shutil
import sys
import zipfile
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import RUNTIME_ROOT, TRANSFER_DIR


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def backup_existing(target_root: str) -> str:
    backup_root = ensure_dir(os.path.join(target_root, "transfer", "import_backups"))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(backup_root, stamp)
    os.makedirs(backup_dir, exist_ok=True)

    for name in ["results", "models"]:
        src = os.path.join(target_root, name)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(backup_dir, name))

    for name in os.listdir(target_root):
        if name.lower().startswith("pipeline_ed2_") and name.lower().endswith(".log"):
            shutil.copy2(os.path.join(target_root, name), os.path.join(backup_dir, name))

    return backup_dir


def extract_zip(zip_path: str, target_root: str):
    manifest_names = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        manifest_names = [name for name in zf.namelist() if "manifest" in os.path.basename(name).lower()]
        zf.extractall(target_root)
    return manifest_names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True, help="Zip generado por package_transfer_ed2.py")
    parser.add_argument("--target-root", default=RUNTIME_ROOT, help="Runtime root destino")
    args = parser.parse_args()

    zip_path = os.path.abspath(args.zip)
    target_root = os.path.abspath(args.target_root)

    if not os.path.isfile(zip_path):
        print(f"Zip no encontrado: {zip_path}")
        return 1

    ensure_dir(target_root)
    backup_dir = backup_existing(target_root)
    manifest_names = extract_zip(zip_path, target_root)

    print(f"Imported zip: {zip_path}")
    print(f"Target root:  {target_root}")
    print(f"Backup dir:   {backup_dir}")
    if manifest_names:
        print("Manifest(s):")
        for name in manifest_names:
            print(f"  - {name}")
    else:
        print("WARNING: el zip no traia manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
