"""
package_transfer_ed2.py - Empaqueta evidencia portable Ed.2 WS <-> local.

Genera en `transfer/`:
- manifest JSON con rutas, presencia de archivos y checksums
- zip con `results/`, modelo `.edb` mas reciente y log del pipeline mas reciente

Uso:
  python package_transfer_ed2.py
  python package_transfer_ed2.py --tag preliminar_ws
"""

import argparse
import hashlib
import json
import os
import sys
import zipfile
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import MODELS_DIR, RESULTS_DIR, RUNTIME_ROOT, SCRIPT_DIR, TRANSFER_DIR
from ed2_static_official import REQUIRED_RESULT_FILES, ensure_transfer_dir


def is_under_root(path: str, root: str) -> bool:
    try:
        return os.path.commonpath([os.path.abspath(path), os.path.abspath(root)]) == os.path.abspath(root)
    except ValueError:
        return False


def latest_file(directory: str, suffix: str):
    if not os.path.isdir(directory):
        return None
    candidates = [
        os.path.join(directory, name)
        for name in os.listdir(directory)
        if name.lower().endswith(suffix.lower())
    ]
    if not candidates:
        return None
    return max(candidates, key=os.path.getmtime)


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files():
    files = []

    if os.path.isdir(RESULTS_DIR):
        for root, _, names in os.walk(RESULTS_DIR):
            for name in sorted(names):
                files.append(os.path.join(root, name))

    latest_model = latest_file(MODELS_DIR, ".edb")
    if latest_model:
        files.append(latest_model)

    latest_log = latest_file(SCRIPT_DIR, ".log")
    if latest_log:
        files.append(latest_log)

    return files, latest_model, latest_log


def build_manifest(files, latest_model, latest_log):
    missing_required = [
        name for name in REQUIRED_RESULT_FILES if not os.path.exists(os.path.join(RESULTS_DIR, name))
    ]
    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "runtime_root": RUNTIME_ROOT,
        "script_dir": SCRIPT_DIR,
        "results_dir": RESULTS_DIR,
        "models_dir": MODELS_DIR,
        "latest_model": latest_model or "",
        "latest_pipeline_log": latest_log or "",
        "required_results_missing": missing_required,
        "files": [
            {
                "path": path,
                "relative_to_runtime_root": os.path.relpath(path, RUNTIME_ROOT)
                if is_under_root(path, RUNTIME_ROOT)
                else os.path.basename(path),
                "size_bytes": os.path.getsize(path),
                "sha256": sha256(path),
            }
            for path in files
        ],
    }


def write_zip(zip_path: str, files, manifest_path: str):
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            if is_under_root(path, RUNTIME_ROOT):
                arcname = os.path.relpath(path, RUNTIME_ROOT)
            else:
                arcname = os.path.basename(path)
            zf.write(path, arcname)
        zf.write(manifest_path, os.path.basename(manifest_path))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="ws_export", help="Tag short for manifest/zip names")
    args = parser.parse_args()

    ensure_transfer_dir()
    files, latest_model, latest_log = collect_files()
    if not files:
        print("No hay archivos para empaquetar. Corre el pipeline o genera resultados primero.")
        return 1

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_tag = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in args.tag)
    manifest_path = os.path.join(TRANSFER_DIR, f"ed2_transfer_manifest_{safe_tag}_{stamp}.json")
    zip_path = os.path.join(TRANSFER_DIR, f"ed2_transfer_{safe_tag}_{stamp}.zip")

    manifest = build_manifest(files, latest_model, latest_log)
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)

    write_zip(zip_path, files, manifest_path)

    print(f"Manifest: {manifest_path}")
    print(f"Zip:      {zip_path}")
    print(f"Files:    {len(files)}")
    print(f"Missing required results: {len(manifest['required_results_missing'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
