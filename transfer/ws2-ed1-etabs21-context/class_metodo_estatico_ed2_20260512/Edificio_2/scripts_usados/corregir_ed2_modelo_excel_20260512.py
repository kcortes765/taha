from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import sys
import time
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


THIS = Path(__file__).resolve()
CLASS_ROOT = THIS.parents[1]
HECRAS2 = CLASS_ROOT.parents[1]
PROG2 = HECRAS2 / "prog2"
COMMON = PROG2 / "_common"
sys.path.insert(0, str(COMMON))

from ws2_etabs_oapi import (  # noqa: E402
    TONF_M_C,
    RunLog,
    check_ret,
    connect_etabs21,
    current_model_path,
    export_table_csv,
    get_etabs_processes,
    get_frame_property,
    get_name_list,
    guarded_run_analysis,
    set_mass_source_from_loads,
    unlock_model,
)


STAMP = time.strftime("%Y%m%d_%H%M%S")

ED2_ROOT = CLASS_ROOT / "Edificio_2"
MODEL_DIR = ED2_ROOT / "models"
EXCEL_DIR = ED2_ROOT / "excel"
RESULTS_DIR = ED2_ROOT / "results"
REPORTS_DIR = ED2_ROOT / "reports"
BACKUP_DIR = ED2_ROOT / "backups"

BASE_MODEL = MODEL_DIR / "ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.EDB"
CORRECTED_MODEL = MODEL_DIR / f"ED2_CLASE_METODO_ESTATICO_CORREGIDO_{STAMP}.EDB"
EXTERNAL_EXCEL_TEMPLATE = Path(r"C:\Users\Civil\Downloads\ED2_METODO_ESTATICO_MANUAL_EXCEL_CORREGIDO_LISTO.xlsx")
FALLBACK_EXCEL_TEMPLATE = EXCEL_DIR / "ED2_METODO_ESTATICO_MANUAL_EXCEL_20260512.xlsx"
CORRECTED_EXCEL = EXCEL_DIR / "ED2_METODO_ESTATICO_MANUAL_EXCEL_CORREGIDO_20260512.xlsx"
DOWNLOADS_EXCEL_COPY = Path(r"C:\Users\Civil\Downloads\ED2_METODO_ESTATICO_MANUAL_EXCEL_CORREGIDO_WS2_20260512.xlsx")

LOG = REPORTS_DIR / f"CORRECCION_ED2_MODELO_EXCEL_{STAMP}.log"
REPORT = REPORTS_DIR / f"CORRECCION_ED2_MODELO_EXCEL_{STAMP}.md"
JSON_REPORT = REPORTS_DIR / f"CORRECCION_ED2_MODELO_EXCEL_{STAMP}.json"

BEAM_SECTIONS = {"V50x70G25", "V45x70G25"}
COLUMN_SECTIONS = {"C70x70G25", "C65x65G25"}
STORIES = ["Story1", "Story2", "Story3", "Story4", "Story5"]
ELEVATIONS = {"Story1": 3.5, "Story2": 6.5, "Story3": 9.5, "Story4": 12.5, "Story5": 15.5}

AO_G = 0.40
S_SOIL = 1.05
T_PRIME = 0.45
N_SOIL = 1.40
R_FACTOR = 7.0
I_FACTOR = 1.0
H_TOTAL = 15.5
B_X = 32.5
B_Y = 32.5

NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ET.register_namespace("", NS["main"])


def ensure_dirs() -> None:
    for path in [MODEL_DIR, EXCEL_DIR, RESULTS_DIR, REPORTS_DIR, BACKUP_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def timestamped_backup(path: Path, tag: str) -> Path | None:
    if not path.exists():
        return None
    backup = BACKUP_DIR / f"{path.stem}_BACKUP_{tag}_{STAMP}{path.suffix}"
    shutil.copy2(path, backup)
    return backup


def remove_model_companions(model_path: Path) -> list[str]:
    """Remove stale ETABS companion/result files for a new working basename.

    ETABS can throw miOpen when an EDB basename has inconsistent analysis side
    files. The script uses a unique basename, but this keeps reruns clean if the
    same timestamped file somehow already exists.
    """
    removed: list[str] = []
    for path in model_path.parent.glob(model_path.stem + ".*"):
        if path.resolve() == model_path.resolve():
            continue
        try:
            path.unlink()
            removed.append(str(path))
        except FileNotFoundError:
            pass
    return removed


def set_run_modal_only(sap: Any, log: RunLog) -> None:
    try:
        ret = sap.Analyze.SetRunCaseFlag("", False, True)
        log.write(f"Analyze.SetRunCaseFlag(all false) ret={ret}")
    except Exception as exc:
        log.write(f"Analyze.SetRunCaseFlag(all false) failed: {exc!r}")
    try:
        ret = sap.Analyze.SetRunCaseFlag("Modal", True, False)
        log.write(f"Analyze.SetRunCaseFlag(Modal true) ret={ret}")
    except Exception as exc:
        log.write(f"Analyze.SetRunCaseFlag(Modal true) failed: {exc!r}")


def correct_frame_offsets(sap: Any, log: RunLog) -> dict[str, Any]:
    unlock_model(sap)
    sap.SetPresentUnits(TONF_M_C)
    frames = get_name_list(sap.FrameObj)
    data = {
        "total_frames": len(frames),
        "beams_rz_075": 0,
        "columns_rz_removed": 0,
        "other_skipped": 0,
        "failed": [],
    }
    for frame in frames:
        try:
            section = get_frame_property(sap, frame)
        except Exception as exc:
            data["failed"].append({"frame": frame, "error": f"GetSection {exc!r}"})
            continue
        try:
            if section in BEAM_SECTIONS:
                ret = sap.FrameObj.SetEndLengthOffset(frame, True, 0.0, 0.0, 0.75, 0)
                if check_ret(ret, f"SetEndLengthOffset beam {frame}", soft=True):
                    data["beams_rz_075"] += 1
                else:
                    data["failed"].append({"frame": frame, "section": section, "ret": repr(ret)})
            elif section in COLUMN_SECTIONS:
                try:
                    ret = sap.FrameObj.SetEndLengthOffset(frame, False, 0.0, 0.0, 0.0, 0)
                except TypeError:
                    ret = sap.FrameObj.SetEndLengthOffset(frame, False, 0.0, 0.0, 0.0)
                if check_ret(ret, f"SetEndLengthOffset column {frame}", soft=True):
                    data["columns_rz_removed"] += 1
                else:
                    data["failed"].append({"frame": frame, "section": section, "ret": repr(ret)})
            else:
                data["other_skipped"] += 1
        except Exception as exc:
            data["failed"].append({"frame": frame, "section": section, "error": repr(exc)})
    log.write(
        "Rigid end zones: "
        f"beams_rz_075={data['beams_rz_075']}, "
        f"columns_rz_removed={data['columns_rz_removed']}, "
        f"failed={len(data['failed'])}"
    )
    return data


def correct_mass_source(sap: Any, log: RunLog) -> dict[str, Any]:
    unlock_model(sap)
    patterns = ["PP", "TERP", "TERT", "SCP", "SCT"]
    factors = [1.0, 1.0, 1.0, 0.25, 0.0]
    ok = set_mass_source_from_loads(
        sap,
        patterns,
        factors,
        include_element_self_mass=False,
        log=log,
    )
    if not ok:
        raise RuntimeError("No se pudo actualizar Mass Source a PP+TERP+TERT+0.25SCP+0SCT.")
    return {"patterns": patterns, "factors": factors, "include_element_self_mass": False}


def select_modal_output(sap: Any, log: RunLog) -> None:
    try:
        sap.Results.Setup.DeselectAllCasesAndCombosForOutput()
        sap.Results.Setup.SetCaseSelectedForOutput("Modal")
    except Exception as exc:
        log.write(f"Results setup for Modal failed: {exc!r}")


def get_modal_rows(sap: Any) -> list[dict[str, float]]:
    res = sap.Results.ModalParticipatingMassRatios()
    if not isinstance(res, (tuple, list)) or len(res) < 18 or int(res[0]) <= 0:
        raise RuntimeError(f"ModalParticipatingMassRatios returned unexpected data: {res!r}")
    n = int(res[0])
    periods = list(res[4])
    ux = list(res[5])
    uy = list(res[6])
    sum_ux = list(res[8])
    sum_uy = list(res[9])
    rz = list(res[13])
    sum_rz = list(res[16])
    rows = []
    for idx in range(n):
        rows.append(
            {
                "mode": idx + 1,
                "period": float(periods[idx]),
                "UX": float(ux[idx]),
                "UY": float(uy[idx]),
                "RZ": float(rz[idx]),
                "SumUX": float(sum_ux[idx]),
                "SumUY": float(sum_uy[idx]),
                "SumRZ": float(sum_rz[idx]),
            }
        )
    return rows


def parse_story_weights_from_out(path: Path) -> list[dict[str, float]]:
    text = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    number_re = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:E[+-]?\d+)?", flags=re.I)
    rows: list[dict[str, float]] = []
    i = 0
    while i < len(text):
        if "TRANSLATIONAL MASS AND MASS MOMENTS OF INERTIA" not in text[i]:
            i += 1
            continue
        mass = None
        for j in range(i + 1, min(i + 8, len(text))):
            if any(token in text[j] for token in ("U1", "U2", "U3", "R1", "R2", "R3", "GLOBAL")):
                continue
            vals = number_re.findall(text[j])
            if len(vals) >= 6:
                mass = float(vals[0])
                break
        z_m = None
        for j in range(i + 1, min(i + 20, len(text))):
            if "CENTER OF MASS" not in text[j]:
                continue
            for k in range(j + 1, min(j + 8, len(text))):
                if not text[k].strip().startswith("Z"):
                    continue
                vals = number_re.findall(text[k])
                if len(vals) >= 3:
                    z_m = float(vals[2]) / 1000.0
                    break
            break
        if mass is not None and z_m is not None:
            story = min(STORIES, key=lambda name: abs(ELEVATIONS[name] - z_m))
            rows.append({"story": story, "elevation_m": ELEVATIONS[story], "weight_tonf": mass})
        i += 1
    unique = {row["story"]: row for row in rows}
    result = [unique[name] for name in STORIES if name in unique]
    if len(result) != len(STORIES):
        raise RuntimeError(f"No se pudieron leer 5 pesos de piso desde {path}")
    return result


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def compute_static_values(story_rows: list[dict[str, float]], modal_rows: list[dict[str, float]]) -> dict[str, Any]:
    tx = max(modal_rows, key=lambda row: row["UX"])
    ty = max(modal_rows, key=lambda row: row["UY"])
    tz = max(modal_rows, key=lambda row: row["RZ"])
    p_total = sum(row["weight_tonf"] for row in story_rows)
    c_min = AO_G * S_SOIL / 6.0
    c_max = 0.35 * AO_G * S_SOIL

    def c_raw(t: float) -> float:
        return 2.75 * S_SOIL * AO_G / R_FACTOR * (T_PRIME / t) ** N_SOIL

    cx_raw = c_raw(tx["period"])
    cy_raw = c_raw(ty["period"])
    cx = max(c_min, min(cx_raw, c_max))
    cy = max(c_min, min(cy_raw, c_max))
    qx = cx * I_FACTOR * p_total
    qy = cy * I_FACTOR * p_total

    dist = []
    previous_z = 0.0
    for row in story_rows:
        z = row["elevation_m"]
        ak = math.sqrt(max(0.0, 1.0 - previous_z / H_TOTAL)) - math.sqrt(max(0.0, 1.0 - z / H_TOTAL))
        dist.append({**row, "z_prev": previous_z, "Ak": ak, "AkPk": ak * row["weight_tonf"]})
        previous_z = z
    denom = sum(row["AkPk"] for row in dist)
    for row in dist:
        fx = qx * row["AkPk"] / denom
        fy = qy * row["AkPk"] / denom
        ex = 0.10 * B_Y * row["elevation_m"] / H_TOTAL
        ey = 0.10 * B_X * row["elevation_m"] / H_TOTAL
        row.update(
            {
                "Fx": fx,
                "Fy": fy,
                "eX": ex,
                "eY": ey,
                "MtX": fx * ex,
                "MtY": fy * ey,
            }
        )
    for idx, row in enumerate(dist):
        row["Vx"] = sum(item["Fx"] for item in dist[idx:])
        row["Vy"] = sum(item["Fy"] for item in dist[idx:])
    return {
        "tx_mode": tx,
        "ty_mode": ty,
        "tz_mode": tz,
        "p_total": p_total,
        "c_min": c_min,
        "c_max": c_max,
        "cx_raw": cx_raw,
        "cy_raw": cy_raw,
        "cx": cx,
        "cy": cy,
        "qx": qx,
        "qy": qy,
        "dist": dist,
        "sum_fx_error": sum(row["Fx"] for row in dist) - qx,
        "sum_fy_error": sum(row["Fy"] for row in dist) - qy,
    }


def workbook_sheet_paths(zf: zipfile.ZipFile) -> dict[str, str]:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
    result: dict[str, str] = {}
    for sheet in wb.findall("main:sheets/main:sheet", NS):
        rid = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        target = rid_to_target[rid].lstrip("/")
        path = target if target.startswith("xl/") else "xl/" + target
        result[sheet.attrib["name"]] = path
    return result


def col_to_num(col: str) -> int:
    value = 0
    for ch in col:
        value = value * 26 + ord(ch.upper()) - ord("A") + 1
    return value


def ensure_cell(ws: ET.Element, ref: str) -> ET.Element:
    sheet_data = ws.find("main:sheetData", NS)
    if sheet_data is None:
        sheet_data = ET.SubElement(ws, f"{{{NS['main']}}}sheetData")
    row_num = int(re.findall(r"\d+", ref)[0])
    col = re.findall(r"[A-Z]+", ref)[0]
    row = None
    for candidate in sheet_data.findall("main:row", NS):
        if int(candidate.attrib.get("r", "0")) == row_num:
            row = candidate
            break
    if row is None:
        row = ET.Element(f"{{{NS['main']}}}row", {"r": str(row_num)})
        rows = sheet_data.findall("main:row", NS)
        inserted = False
        for idx, candidate in enumerate(rows):
            if int(candidate.attrib.get("r", "0")) > row_num:
                sheet_data.insert(idx, row)
                inserted = True
                break
        if not inserted:
            sheet_data.append(row)
    cell = None
    for candidate in row.findall("main:c", NS):
        if candidate.attrib.get("r") == ref:
            cell = candidate
            break
    if cell is None:
        cell = ET.Element(f"{{{NS['main']}}}c", {"r": ref})
        target_col = col_to_num(col)
        cells = row.findall("main:c", NS)
        inserted = False
        for idx, candidate in enumerate(cells):
            cand_col = re.findall(r"[A-Z]+", candidate.attrib.get("r", "A"))[0]
            if col_to_num(cand_col) > target_col:
                row.insert(idx, cell)
                inserted = True
                break
        if not inserted:
            row.append(cell)
    return cell


def set_number_cell(ws: ET.Element, ref: str, value: float | int) -> None:
    cell = ensure_cell(ws, ref)
    cell.attrib.pop("t", None)
    for child in list(cell):
        if child.tag.endswith("}is"):
            cell.remove(child)
    v = cell.find("main:v", NS)
    if v is None:
        v = ET.SubElement(cell, f"{{{NS['main']}}}v")
    v.text = f"{float(value):.15g}"


def set_text_cell(ws: ET.Element, ref: str, value: str) -> None:
    cell = ensure_cell(ws, ref)
    cell.attrib["t"] = "inlineStr"
    for child in list(cell):
        cell.remove(child)
    is_el = ET.SubElement(cell, f"{{{NS['main']}}}is")
    t_el = ET.SubElement(is_el, f"{{{NS['main']}}}t")
    t_el.text = value


def set_full_recalc(xml_bytes: bytes) -> bytes:
    root = ET.fromstring(xml_bytes)
    calc_pr = root.find("main:calcPr", NS)
    if calc_pr is None:
        calc_pr = ET.SubElement(root, f"{{{NS['main']}}}calcPr")
    calc_pr.attrib["calcMode"] = "auto"
    calc_pr.attrib["fullCalcOnLoad"] = "1"
    calc_pr.attrib["forceFullCalc"] = "1"
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_excel_template(story_rows: list[dict[str, float]], modal_rows: list[dict[str, float]], calc: dict[str, Any]) -> None:
    template = EXTERNAL_EXCEL_TEMPLATE if EXTERNAL_EXCEL_TEMPLATE.exists() else FALLBACK_EXCEL_TEMPLATE
    if not template.exists():
        raise FileNotFoundError("No existe plantilla Excel externa ni plantilla local.")
    timestamped_backup(CORRECTED_EXCEL, "PRE_CORRECCION")
    shutil.copy2(template, CORRECTED_EXCEL)

    temp_path = CORRECTED_EXCEL.with_suffix(".tmp.xlsx")
    with zipfile.ZipFile(CORRECTED_EXCEL, "r") as zin, zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        sheet_paths = workbook_sheet_paths(zin)
        patched: dict[str, bytes] = {}

        inputs = ET.fromstring(zin.read(sheet_paths["01_Inputs"]))
        set_number_cell(inputs, "B12", calc["tx_mode"]["period"])
        set_number_cell(inputs, "B13", calc["ty_mode"]["period"])
        set_number_cell(inputs, "B15", 0.0)
        set_number_cell(inputs, "B16", calc["tz_mode"]["period"])
        set_number_cell(inputs, "B17", calc["tx_mode"]["mode"])
        set_number_cell(inputs, "B18", calc["ty_mode"]["mode"])
        set_number_cell(inputs, "B19", calc["tz_mode"]["mode"])
        set_text_cell(inputs, "D12", f"Modelo corregido: modo {calc['tx_mode']['mode']} con mayor UX={calc['tx_mode']['UX']:.6f}.")
        set_text_cell(inputs, "D13", f"Modelo corregido: modo {calc['ty_mode']['mode']} con mayor UY={calc['ty_mode']['UY']:.6f}.")
        set_text_cell(inputs, "D15", "Clase sismo 14: SCT no entra a la masa sismica; permanece como carga gravitacional.")
        patched[sheet_paths["01_Inputs"]] = ET.tostring(inputs, encoding="utf-8", xml_declaration=True)

        datos = ET.fromstring(zin.read(sheet_paths["02_Datos_ETABS"]))
        for idx, row in enumerate(story_rows, start=4):
            set_number_cell(datos, f"B{idx}", row["elevation_m"])
            set_number_cell(datos, f"C{idx}", row["weight_tonf"])
        for idx, row in enumerate(modal_rows, start=4):
            set_number_cell(datos, f"E{idx}", row["mode"])
            set_number_cell(datos, f"F{idx}", row["period"])
            set_number_cell(datos, f"G{idx}", row["UX"])
            set_number_cell(datos, f"H{idx}", row["UY"])
            set_number_cell(datos, f"I{idx}", row["RZ"])
            set_number_cell(datos, f"J{idx}", row["SumUX"])
            set_number_cell(datos, f"K{idx}", row["SumUY"])
            set_number_cell(datos, f"L{idx}", row["SumRZ"])
        patched[sheet_paths["02_Datos_ETABS"]] = ET.tostring(datos, encoding="utf-8", xml_declaration=True)

        readme = ET.fromstring(zin.read(sheet_paths["00_LEEME"]))
        set_text_cell(readme, "C4", f"Actualizado desde modelo corregido WS2: {CORRECTED_MODEL.name}.")
        set_text_cell(readme, "C5", "SCT=0 en masa sismica del modelo ETABS corregido; SCT sigue en cargas gravitacionales.")
        patched[sheet_paths["00_LEEME"]] = ET.tostring(readme, encoding="utf-8", xml_declaration=True)

        for item in zin.infolist():
            if item.filename == "xl/calcChain.xml":
                continue
            if item.filename == "xl/workbook.xml":
                zout.writestr(item, set_full_recalc(zin.read(item.filename)))
            elif item.filename in patched:
                zout.writestr(item, patched[item.filename])
            else:
                zout.writestr(item, zin.read(item.filename))
    os.replace(temp_path, CORRECTED_EXCEL)
    shutil.copy2(CORRECTED_EXCEL, DOWNLOADS_EXCEL_COPY)


def verify_et_export(path: Path) -> dict[str, Any]:
    data = {
        "rz_counts": {},
        "mass_source_lines": [],
        "diaphragm_areaassign_count": None,
        "areaassign_count": None,
    }
    if not path.exists():
        data["missing"] = str(path)
        return data
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    rz_counts: dict[str, int] = {}
    for line in lines:
        m = re.search(r'LINEASSIGN\s+"[^"]+"\s+"[^"]+"\s+SECTION\s+"([^"]+)"', line)
        if m and "RIGIDZONE 0.75" in line:
            rz_counts[m.group(1)] = rz_counts.get(m.group(1), 0) + 1
    data["rz_counts"] = rz_counts
    data["mass_source_lines"] = [line.strip() for line in lines if line.strip().startswith("MASSSOURCE")]
    data["diaphragm_areaassign_count"] = sum(1 for line in lines if line.strip().startswith("AREAASSIGN") and 'DIAPH "D1"' in line)
    data["areaassign_count"] = sum(1 for line in lines if line.strip().startswith("AREAASSIGN"))
    return data


def write_report(data: dict[str, Any]) -> None:
    calc = data["calc"]
    lines = [
        "# Correccion Edificio 2 modelo + Excel",
        "",
        f"- Fecha: `{STAMP}`",
        f"- Modelo base: `{BASE_MODEL}`",
        f"- Modelo corregido: `{CORRECTED_MODEL}`",
        f"- Excel corregido: `{CORRECTED_EXCEL}`",
        f"- Copia en Descargas: `{DOWNLOADS_EXCEL_COPY}`",
        f"- Backup modelo base: `{data.get('model_backup')}`",
        f"- Backup Excel anterior: `{data.get('excel_backup')}`",
        "",
        "## Correcciones aplicadas",
        "",
        "- Rigid End Zones: `0.75` solo en vigas `V50x70G25` y `V45x70G25`.",
        "- Rigid End Zones removidos de columnas `C70x70G25` y `C65x65G25`.",
        "- Mass Source: `PP + TERP + TERT + 0.25*SCP + 0*SCT`.",
        "- Modal corrido de nuevo en una unica instancia ETABS 21.",
        "",
        "## Resultados corregidos",
        "",
        f"- `Tx* = {calc['tx_mode']['period']:.6f} s` modo `{calc['tx_mode']['mode']}` (`UX={calc['tx_mode']['UX']:.6f}`).",
        f"- `Ty* = {calc['ty_mode']['period']:.6f} s` modo `{calc['ty_mode']['mode']}` (`UY={calc['ty_mode']['UY']:.6f}`).",
        f"- `Tz* = {calc['tz_mode']['period']:.6f} s` modo `{calc['tz_mode']['mode']}` (`RZ={calc['tz_mode']['RZ']:.6f}`).",
        f"- `P = {calc['p_total']:.3f} tonf`.",
        f"- `Craw_x = {calc['cx_raw']:.6f}`, `Craw_y = {calc['cy_raw']:.6f}`.",
        f"- `C usado X = {calc['cx']:.6f}`, `C usado Y = {calc['cy']:.6f}`.",
        f"- `Q0x = {calc['qx']:.3f} tonf`, `Q0y = {calc['qy']:.3f} tonf`.",
        f"- `sum(Fx)-Q0x = {calc['sum_fx_error']:.6g}`.",
        f"- `sum(Fy)-Q0y = {calc['sum_fy_error']:.6g}`.",
        "",
        "## Evidencia",
        "",
        f"- Modal CSV: `{data['modal_csv']}`",
        f"- Pesos por piso CSV: `{data['story_csv']}`",
        f"- Tablas ETABS exportadas: `{data['exports_dir']}`",
        f"- JSON completo: `{JSON_REPORT}`",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ensure_dirs()
    log = RunLog(LOG)
    data: dict[str, Any] = {"stamp": STAMP}
    session = None
    try:
        processes = get_etabs_processes()
        log.write(f"ETABS processes before correction: {processes}")
        if len(processes) > 1:
            raise RuntimeError("Hay mas de una instancia ETABS abierta. Detengo por regla critica.")
        if not BASE_MODEL.exists():
            raise FileNotFoundError(BASE_MODEL)

        data["model_backup"] = str(timestamped_backup(BASE_MODEL, "PRE_CORRECCION")) if BASE_MODEL.exists() else None
        data["excel_backup"] = str(timestamped_backup(CORRECTED_EXCEL, "PRE_CORRECCION")) if CORRECTED_EXCEL.exists() else None
        removed = remove_model_companions(CORRECTED_MODEL)
        data["removed_stale_companions"] = removed
        shutil.copy2(BASE_MODEL, CORRECTED_MODEL)
        log.write(f"Corrected working model copied: {CORRECTED_MODEL}")

        session = connect_etabs21(CORRECTED_MODEL, log, allow_start=(len(processes) == 0))
        data["etabs"] = {
            "pid": session.pid,
            "started_by_script": session.started_by_script,
            "attach_method": session.attach_method,
            "version": session.version,
        }
        sap = session.sap_model
        log.write(f"Active model: {current_model_path(sap)}")

        data["frame_offset_edit"] = correct_frame_offsets(sap, log)
        data["mass_source_edit"] = correct_mass_source(sap, log)
        set_run_modal_only(sap, log)
        check_ret(sap.File.Save(str(CORRECTED_MODEL)), f"File.Save({CORRECTED_MODEL})")
        check_ret(guarded_run_analysis(sap, log, pid=session.pid, context="ED2 corrected modal run"), "Analyze.RunAnalysis corrected")
        select_modal_output(sap, log)
        modal_rows = get_modal_rows(sap)
        check_ret(sap.File.Save(str(CORRECTED_MODEL)), f"File.Save({CORRECTED_MODEL}) post-run")

        exports_dir = RESULTS_DIR / f"corregido_{STAMP}"
        exports_dir.mkdir(parents=True, exist_ok=True)
        for table in [
            "Modal Periods And Frequencies",
            "Modal Participating Mass Ratios",
            "Mass Source Definition",
            "Mass Summary by Story",
            "Base Reactions",
        ]:
            export_table_csv(sap, table, exports_dir / f"{table.replace(' ', '_')}_{STAMP}.csv", log)

        story_rows = parse_story_weights_from_out(CORRECTED_MODEL.with_suffix(".OUT"))
        calc = compute_static_values(story_rows, modal_rows)

        modal_csv = RESULTS_DIR / f"modal_participating_mass_ratios_corregido_{STAMP}.csv"
        story_csv = RESULTS_DIR / f"story_weights_corregido_{STAMP}.csv"
        dist_csv = RESULTS_DIR / f"ed2_static_distribution_corregido_{STAMP}.csv"
        write_csv(modal_csv, modal_rows)
        write_csv(story_csv, story_rows)
        write_csv(dist_csv, calc["dist"])

        patch_excel_template(story_rows, modal_rows, calc)

        data.update(
            {
                "corrected_model": str(CORRECTED_MODEL),
                "corrected_excel": str(CORRECTED_EXCEL),
                "downloads_excel_copy": str(DOWNLOADS_EXCEL_COPY),
                "story_rows": story_rows,
                "modal_rows": modal_rows,
                "calc": calc,
                "modal_csv": str(modal_csv),
                "story_csv": str(story_csv),
                "dist_csv": str(dist_csv),
                "exports_dir": str(exports_dir),
                "et_export_verification": verify_et_export(CORRECTED_MODEL.with_suffix(".$et")),
            }
        )
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        write_report(data)
        log.write(f"Report written: {REPORT}")
        return 0
    except Exception as exc:
        data["error"] = repr(exc)
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        log.write(f"ERROR: {exc!r}")
        return 1
    finally:
        if session is not None:
            if session.close_if_started(save=True):
                log.write("Closed ETABS instance started by this script.")
            else:
                session.release()
        log.close()


if __name__ == "__main__":
    raise SystemExit(main())
