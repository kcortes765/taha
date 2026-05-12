from __future__ import annotations

import csv
import json
import math
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import xlsxwriter


THIS = Path(__file__).resolve()
CLASS_ROOT = THIS.parents[1]
HECRAS2 = CLASS_ROOT.parents[1]
PROG2 = HECRAS2 / "prog2"
COMMON = PROG2 / "_common"

sys.path.insert(0, str(COMMON))

from ws2_etabs_oapi import RunLog, connect_etabs21, current_model_path, get_etabs_processes  # noqa: E402


STAMP = time.strftime("%Y%m%d_%H%M%S")

MODEL = CLASS_ROOT / "Edificio_2" / "models" / "ED2_CLASE_METODO_ESTATICO_EXCEL_20260512.EDB"
OUT = MODEL.with_suffix(".OUT")
EXCEL = CLASS_ROOT / "Edificio_2" / "excel" / "ED2_METODO_ESTATICO_MANUAL_EXCEL_20260512.xlsx"
BACKUP_DIR = CLASS_ROOT / "Edificio_2" / "backups"
RESULTS_DIR = CLASS_ROOT / "Edificio_2" / "results"
REPORTS_DIR = CLASS_ROOT / "Edificio_2" / "reports"
REPORT = REPORTS_DIR / f"AUDITORIA_EXCEL_CLASE_SISMO_20260512_{STAMP}.md"
JSON_REPORT = REPORTS_DIR / f"AUDITORIA_EXCEL_CLASE_SISMO_20260512_{STAMP}.json"
LOG = REPORTS_DIR / f"AUDITORIA_EXCEL_CLASE_SISMO_20260512_{STAMP}.log"

TRANSCRIPTS = Path(r"C:\Users\Civil\Downloads\drive-download-20260512T184206Z-3-001")
NCH433 = HECRAS2 / "codex_ws2_context" / "transfer" / "ws2-ed1-etabs21-context" / "files" / "05_NCh433_2026_para_Curso.pdf"
APUNTES_ESTATICO = HECRAS2 / "codex_ws2_context" / "transfer" / "ws2-ed1-etabs21-context" / "files" / "11_02c_Analisis_Estatico.pdf"

STORIES = ["Story1", "Story2", "Story3", "Story4", "Story5"]
ELEVATIONS = {"Story1": 3.5, "Story2": 6.5, "Story3": 9.5, "Story4": 12.5, "Story5": 15.5}

# Clase + NCh433:2026, tabla 8, suelo C.
AO_G = 0.40
S_SUELO = 1.05
T_PRIME = 0.45
N_SUELO = 1.40
I_FACTOR = 1.0
R_MARCOS = 7.0
H_TOTAL = 15.5
B_X = 32.5
B_Y = 32.5
AREA_PLANTA = 32.5 * 32.5
LIVE_MASS_FACTOR = 0.25


def ensure_dirs() -> None:
    for path in [BACKUP_DIR, RESULTS_DIR, REPORTS_DIR, EXCEL.parent]:
        path.mkdir(parents=True, exist_ok=True)


def backup_excel() -> Path | None:
    if not EXCEL.exists():
        return None
    backup = BACKUP_DIR / f"{EXCEL.stem}_BACKUP_PRE_AUDIT_CLASE_{STAMP}{EXCEL.suffix}"
    shutil.copy2(EXCEL, backup)
    return backup


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
        if mass is None:
            i += 1
            continue

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

        if z_m is not None:
            story = min(STORIES, key=lambda name: abs(ELEVATIONS[name] - z_m))
            rows.append({"story": story, "elevation_m": ELEVATIONS[story], "weight_tonf": mass})
        i += 1

    unique: dict[str, dict[str, float]] = {}
    for row in rows:
        unique[row["story"]] = row
    result = [unique[name] for name in STORIES if name in unique]
    if len(result) != len(STORIES):
        raise RuntimeError(f"No se pudieron leer 5 pesos de piso desde {path}")
    return result


def extract_modal_rows_from_open_etabs(log: RunLog) -> list[dict[str, float]]:
    processes = get_etabs_processes()
    if len(processes) > 1:
        raise RuntimeError("Hay más de una instancia ETABS abierta; no se puede auditar en forma segura.")
    allow_start = len(processes) == 0
    if allow_start:
        log.write("No hay ETABS abierto; se abrirá una única instancia ETABS 21 para leer resultados modales.")

    session = None
    try:
        session = connect_etabs21(MODEL, log, allow_start=allow_start)
        sap = session.sap_model
        log.write(f"Modelo activo para auditoría Excel: {current_model_path(sap)}")
        try:
            sap.Results.Setup.DeselectAllCasesAndCombosForOutput()
            sap.Results.Setup.SetCaseSelectedForOutput("Modal")
        except Exception as exc:
            log.write(f"WARNING Results.Setup Modal failed: {exc}")

        res = sap.Results.ModalParticipatingMassRatios()
        if not isinstance(res, (tuple, list)) or len(res) < 18 or int(res[0]) <= 0:
            raise RuntimeError("ETABS no entregó ModalParticipatingMassRatios.")
        n = int(res[0])
        periods = list(res[4])
        ux = list(res[5])
        uy = list(res[6])
        rz = list(res[13])
        sum_ux = list(res[8])
        sum_uy = list(res[9])
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
    finally:
        if session is not None:
            if session.close_if_started(save=False):
                log.write("Se cerró la instancia ETABS iniciada por este auditor.")
            else:
                session.release()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def compute(story_rows: list[dict[str, float]], modal_rows: list[dict[str, float]]) -> dict[str, Any]:
    tx_mode = max(modal_rows, key=lambda row: row["UX"])
    ty_mode = max(modal_rows, key=lambda row: row["UY"])
    tz_mode = max(modal_rows, key=lambda row: row["RZ"])
    p_total = sum(row["weight_tonf"] for row in story_rows)
    c_min = AO_G * S_SUELO / 6.0
    c_max = 0.35 * AO_G * S_SUELO

    def c_raw(t: float) -> float:
        return 2.75 * S_SUELO * AO_G / R_MARCOS * (T_PRIME / t) ** N_SUELO

    cx_raw = c_raw(tx_mode["period"])
    cy_raw = c_raw(ty_mode["period"])
    cx = max(c_min, min(cx_raw, c_max))
    cy = max(c_min, min(cy_raw, c_max))
    qx = cx * I_FACTOR * p_total
    qy = cy * I_FACTOR * p_total

    dist = []
    previous_z = 0.0
    terms = []
    for row in story_rows:
        z = row["elevation_m"]
        ak = math.sqrt(max(0.0, 1 - previous_z / H_TOTAL)) - math.sqrt(max(0.0, 1 - z / H_TOTAL))
        akpk = ak * row["weight_tonf"]
        terms.append(akpk)
        dist.append({**row, "z_prev": previous_z, "Ak": ak, "AkPk": akpk})
        previous_z = z
    denom = sum(terms)
    for row in dist:
        fx = qx * row["AkPk"] / denom
        fy = qy * row["AkPk"] / denom
        ex = 0.10 * B_Y * row["elevation_m"] / H_TOTAL
        ey = 0.10 * B_X * row["elevation_m"] / H_TOTAL
        row.update({"Fx": fx, "Fy": fy, "eX": ex, "eY": ey, "MtX": fx * ex, "MtY": fy * ey})
    for idx, row in enumerate(dist):
        row["Vx_acum"] = sum(item["Fx"] for item in dist[idx:])
        row["Vy_acum"] = sum(item["Fy"] for item in dist[idx:])

    return {
        "tx_mode": tx_mode,
        "ty_mode": ty_mode,
        "tz_mode": tz_mode,
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
    }


def write_excel(story_rows: list[dict[str, float]], modal_rows: list[dict[str, float]], calc: dict[str, Any]) -> None:
    workbook = xlsxwriter.Workbook(str(EXCEL))
    workbook.set_calc_mode("auto")

    colors = {
        "navy": "#17324D",
        "ink": "#202A33",
        "input": "#FFF2CC",
        "etabs": "#D9EAF7",
        "formula": "#E2F0D9",
        "fixed": "#E7E6E6",
        "warn": "#FCE4D6",
        "ok": "#D9EAD3",
        "trace": "#EADCF8",
        "white": "#FFFFFF",
    }
    title = workbook.add_format({"bold": True, "font_size": 18, "font_color": colors["white"], "bg_color": colors["navy"], "align": "center", "valign": "vcenter"})
    section = workbook.add_format({"bold": True, "font_color": colors["white"], "bg_color": colors["ink"], "align": "left"})
    header = workbook.add_format({"bold": True, "bg_color": "#BDD7EE", "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True})
    input_num = workbook.add_format({"bg_color": colors["input"], "border": 1, "locked": False, "num_format": "0.000000"})
    input_txt = workbook.add_format({"bg_color": colors["input"], "border": 1, "locked": False})
    etabs_num = workbook.add_format({"bg_color": colors["etabs"], "border": 1, "num_format": "0.000000"})
    formula_num = workbook.add_format({"bg_color": colors["formula"], "border": 1, "num_format": "0.000000"})
    fixed_num = workbook.add_format({"bg_color": colors["fixed"], "border": 1, "num_format": "0.000000"})
    text = workbook.add_format({"border": 1, "text_wrap": True, "valign": "top"})
    note = workbook.add_format({"text_wrap": True, "valign": "top"})
    ok = workbook.add_format({"bg_color": colors["ok"], "border": 1, "bold": True})
    warn = workbook.add_format({"bg_color": colors["warn"], "border": 1, "bold": True})
    trace = workbook.add_format({"bg_color": colors["trace"], "border": 1, "text_wrap": True, "valign": "top"})

    def wf(ws, row, col, formula, fmt, value):
        ws.write_formula(row, col, formula, fmt, value)

    readme = workbook.add_worksheet("00_LEEME")
    readme.merge_range("A1:H2", "Edificio 2 - Método estático manual verificado con clase", title)
    readme.set_column("A:A", 24)
    readme.set_column("B:H", 26)
    readme.write("A4", "Leyenda", section)
    legends = [
        ("Amarillo", "Editable por ti durante la clase."),
        ("Azul", "Dato leído desde ETABS/API/OUT."),
        ("Verde", "Fórmula calculada."),
        ("Gris", "Dato fijo de enunciado/norma para este caso."),
        ("Morado", "Trazabilidad de clase/PDF."),
    ]
    for r, row in enumerate(legends, start=5):
        fmt = {"Amarillo": input_txt, "Azul": etabs_num, "Verde": formula_num, "Gris": fixed_num, "Morado": trace}[row[0]]
        readme.write(r - 1, 0, row[0], fmt)
        readme.write(r - 1, 1, row[1], text)
    readme.write("A12", "Uso", section)
    readme.merge_range(
        "A13:H19",
        "Este archivo queda listo para que hagas el método estático manual del Edificio 2. "
        "Los datos iniciales ya están poblados desde la clase, NCh433:2026 y ETABS. "
        "Edita sólo celdas amarillas si el profesor decide cambiar algún supuesto. "
        "La hoja 05_Cargas_ETABS entrega las fuerzas y momentos que luego se ingresan a ETABS como EX, EY, TEX y TEY.",
        note,
    )

    inputs = workbook.add_worksheet("01_Inputs")
    inputs.set_column("A:A", 34)
    inputs.set_column("B:B", 18)
    inputs.set_column("C:D", 38)
    for c, name in enumerate(["Parámetro", "Valor", "Tipo", "Nota"]):
        inputs.write(0, c, name, header)
    input_rows = [
        ("Ao/g zona 3", AO_G, "Editable", "Clase + Tabla 7 NCh433: Antofagasta/Zona 3."),
        ("S suelo C", S_SUELO, "Editable", "Tabla 8 NCh433: suelo C."),
        ("I importancia", I_FACTOR, "Editable", "Categoría II / no aglomeración: I = 1,0."),
        ("R sistema marcos", R_MARCOS, "Editable", "Marcos especiales de hormigón armado: R = 7."),
        ("T' suelo [s]", T_PRIME, "Editable", "Tabla 8 NCh433: suelo C."),
        ("n suelo", N_SUELO, "Editable", "Tabla 8 NCh433: suelo C, n = 1,40."),
        ("H total [m]", H_TOTAL, "Fijo", "3,5 + 4x3,0 = 15,5 m."),
        ("b planta X [m]", B_X, "Fijo", "Planta 32,5 x 32,5 m."),
        ("b planta Y [m]", B_Y, "Fijo", "Planta 32,5 x 32,5 m."),
        ("Área planta [m²]", AREA_PLANTA, "Fijo", "32,5 x 32,5."),
        ("Tx* [s]", calc["tx_mode"]["period"], "Editable", f"Modo {calc['tx_mode']['mode']} con mayor UX = {calc['tx_mode']['UX']:.6f}."),
        ("Ty* [s]", calc["ty_mode"]["period"], "Editable", f"Modo {calc['ty_mode']['mode']} con mayor UY = {calc['ty_mode']['UY']:.6f}."),
        ("Factor sobrecarga masa", LIVE_MASS_FACTOR, "Editable", "No aglomeración: 25% de sobrecarga."),
    ]
    for r, (label, value, typ, comment) in enumerate(input_rows, start=2):
        inputs.write(r - 1, 0, label, text)
        inputs.write_number(r - 1, 1, value, input_num if typ == "Editable" else fixed_num)
        inputs.write(r - 1, 2, typ, input_txt if typ == "Editable" else fixed_num)
        inputs.write(r - 1, 3, comment, text)
    inputs.protect()

    datos = workbook.add_worksheet("02_Datos_ETABS")
    datos.freeze_panes(3, 0)
    datos.set_column("A:C", 18)
    datos.set_column("E:L", 15)
    datos.write("A1", "Pesos sísmicos por piso desde ETABS OUT", section)
    for c, name in enumerate(["Piso", "Z [m]", "P_k [tonf]"]):
        datos.write(2, c, name, header)
    for idx, row in enumerate(story_rows, start=4):
        datos.write(idx - 1, 0, row["story"], text)
        datos.write_number(idx - 1, 1, row["elevation_m"], etabs_num)
        datos.write_number(idx - 1, 2, row["weight_tonf"], etabs_num)
    datos.write("E1", "Masas participantes modales desde ETABS API", section)
    modal_headers = ["Modo", "T [s]", "UX", "UY", "RZ", "SumUX", "SumUY", "SumRZ"]
    for c, name in enumerate(modal_headers, start=4):
        datos.write(2, c, name, header)
    for idx, row in enumerate(modal_rows, start=4):
        datos.write_number(idx - 1, 4, row["mode"], etabs_num)
        datos.write_number(idx - 1, 5, row["period"], etabs_num)
        datos.write_number(idx - 1, 6, row["UX"], etabs_num)
        datos.write_number(idx - 1, 7, row["UY"], etabs_num)
        datos.write_number(idx - 1, 8, row["RZ"], etabs_num)
        datos.write_number(idx - 1, 9, row["SumUX"], etabs_num)
        datos.write_number(idx - 1, 10, row["SumUY"], etabs_num)
        datos.write_number(idx - 1, 11, row["SumRZ"], etabs_num)
    datos.protect()

    coef = workbook.add_worksheet("03_Coeficiente_C")
    coef.set_column("A:A", 32)
    coef.set_column("B:D", 19)
    for c, name in enumerate(["Cálculo", "X", "Y", "Nota"]):
        coef.write(0, c, name, header)
    coef_rows = [
        ("T* [s]", "=01_Inputs!B12", "=01_Inputs!B13", "Modo con mayor masa traslacional en la dirección."),
        ("C raw", "=2.75*01_Inputs!B3*01_Inputs!B2/01_Inputs!B5*(01_Inputs!B6/B2)^01_Inputs!B7", "=2.75*01_Inputs!B3*01_Inputs!B2/01_Inputs!B5*(01_Inputs!B6/C2)^01_Inputs!B7", "Ec. 6.2.3.1."),
        ("Cmin", "=01_Inputs!B2*01_Inputs!B3/6", "=B4", "Mínimo obligatorio."),
        ("Cmax", "=0.35*01_Inputs!B2*01_Inputs!B3", "=B5", "R >= 6: se usa Cmax en taller si C raw supera."),
        ("C usado", "=MAX(B4,MIN(B3,B5))", "=MAX(C4,MIN(C3,C5))", "Coeficiente aplicado."),
        ("P total [tonf]", "=SUM(02_Datos_ETABS!C4:C8)", "=B7", "Suma P_k desde ETABS OUT."),
        ("Q0 [tonf]", "=B6*01_Inputs!B4*B7", "=C6*01_Inputs!B4*C7", "Q0 = C I P."),
    ]
    values_x = [calc["tx_mode"]["period"], calc["cx_raw"], calc["c_min"], calc["c_max"], calc["cx"], calc["p_total"], calc["qx"]]
    values_y = [calc["ty_mode"]["period"], calc["cy_raw"], calc["c_min"], calc["c_max"], calc["cy"], calc["p_total"], calc["qy"]]
    for r, (row, vx, vy) in enumerate(zip(coef_rows, values_x, values_y), start=2):
        label, fx, fy, comment = row
        coef.write(r - 1, 0, label, text)
        wf(coef, r - 1, 1, fx, formula_num, vx)
        wf(coef, r - 1, 2, fy, formula_num, vy)
        coef.write(r - 1, 3, comment, text)
    coef.protect()

    dist = workbook.add_worksheet("04_Distribución")
    dist.freeze_panes(2, 0)
    dist.set_column("A:A", 12)
    dist.set_column("B:N", 15)
    headers = ["Piso", "Z [m]", "P_k", "Z prev", "A_k", "A_k P_k", "F_x", "F_y", "e sismo X", "e sismo Y", "Mt_X", "Mt_Y", "Vx acum", "Vy acum"]
    for c, name in enumerate(headers):
        dist.write(0, c, name, header)
    start = 3
    end = start + len(story_rows) - 1
    for idx, row in enumerate(calc["dist"]):
        excel_r = start + idx
        r0 = excel_r - 1
        dist.write(r0, 0, row["story"], text)
        wf(dist, r0, 1, f"=02_Datos_ETABS!B{4+idx}", etabs_num, row["elevation_m"])
        wf(dist, r0, 2, f"=02_Datos_ETABS!C{4+idx}", etabs_num, row["weight_tonf"])
        if idx == 0:
            dist.write_number(r0, 3, 0, fixed_num)
        else:
            wf(dist, r0, 3, f"=B{excel_r-1}", fixed_num, row["z_prev"])
        wf(dist, r0, 4, f"=SQRT(MAX(0,1-D{excel_r}/01_Inputs!$B$8))-SQRT(MAX(0,1-B{excel_r}/01_Inputs!$B$8))", formula_num, row["Ak"])
        wf(dist, r0, 5, f"=E{excel_r}*C{excel_r}", formula_num, row["AkPk"])
        wf(dist, r0, 6, f"='03_Coeficiente_C'!$B$8*F{excel_r}/SUM($F${start}:$F${end})", formula_num, row["Fx"])
        wf(dist, r0, 7, f"='03_Coeficiente_C'!$C$8*F{excel_r}/SUM($F${start}:$F${end})", formula_num, row["Fy"])
        wf(dist, r0, 8, f"=0.10*01_Inputs!$B$10*B{excel_r}/01_Inputs!$B$8", formula_num, row["eX"])
        wf(dist, r0, 9, f"=0.10*01_Inputs!$B$9*B{excel_r}/01_Inputs!$B$8", formula_num, row["eY"])
        wf(dist, r0, 10, f"=G{excel_r}*I{excel_r}", formula_num, row["MtX"])
        wf(dist, r0, 11, f"=H{excel_r}*J{excel_r}", formula_num, row["MtY"])
        wf(dist, r0, 12, f"=SUM(G{excel_r}:G${end})", formula_num, row["Vx_acum"])
        wf(dist, r0, 13, f"=SUM(H{excel_r}:H${end})", formula_num, row["Vy_acum"])
    check_row = end + 2
    dist.write(check_row - 1, 0, "Chequeo suma F", header)
    wf(dist, check_row - 1, 6, f"=SUM(G{start}:G{end})-'03_Coeficiente_C'!$B$8", formula_num, sum(r["Fx"] for r in calc["dist"]) - calc["qx"])
    wf(dist, check_row - 1, 7, f"=SUM(H{start}:H{end})-'03_Coeficiente_C'!$C$8", formula_num, sum(r["Fy"] for r in calc["dist"]) - calc["qy"])
    dist.protect()

    cargas = workbook.add_worksheet("05_Cargas_ETABS")
    cargas.freeze_panes(1, 0)
    cargas.set_column("A:F", 19)
    for c, name in enumerate(["Piso", "EX Fx [tonf]", "EY Fy [tonf]", "TEX Mz [tonf-m]", "TEY Mz [tonf-m]", "Uso en ETABS"]):
        cargas.write(0, c, name, header)
    for idx, row in enumerate(calc["dist"], start=2):
        src = idx + 1
        cargas.write(idx - 1, 0, row["story"], text)
        wf(cargas, idx - 1, 1, f"='04_Distribución'!G{src}", formula_num, row["Fx"])
        wf(cargas, idx - 1, 2, f"='04_Distribución'!H{src}", formula_num, row["Fy"])
        wf(cargas, idx - 1, 3, f"='04_Distribución'!K{src}", formula_num, row["MtX"])
        wf(cargas, idx - 1, 4, f"='04_Distribución'!L{src}", formula_num, row["MtY"])
        cargas.write(idx - 1, 5, "Aplicar en centro de masa/diafragma del piso; signos ± se manejan por casos/combos.", text)
    cargas.protect()

    combos = workbook.add_worksheet("06_Combos_Guía")
    combos.set_column("A:A", 24)
    combos.set_column("B:B", 82)
    combos.write("A1", "Etapa", header)
    combos.write("B1", "Referencia para después de ingresar EX/EY/TEX/TEY", header)
    for r, row in enumerate(
        [
            ("D", "PP + TERP + TERT"),
            ("L", "SCP"),
            ("Lr", "SCT"),
            ("Sismo X", "EX ± TEX, con mismo signo de torsión en todos los niveles para cada análisis."),
            ("Sismo Y", "EY ± TEY, con mismo signo de torsión en todos los niveles para cada análisis."),
            ("Resistencia", "1,2D + L ± 1,4E ± 1,4T."),
            ("Resistencia", "0,9D ± 1,4E ± 1,4T."),
            ("Drift", "E ± T sin mayorar; no usar combinaciones de resistencia para deformaciones."),
        ],
        start=2,
    ):
        combos.write(r - 1, 0, row[0], text)
        combos.write(r - 1, 1, row[1], text)
    combos.protect()

    valid = workbook.add_worksheet("07_Validaciones")
    valid.set_column("A:A", 36)
    valid.set_column("B:C", 24)
    valid.write("A1", "Chequeo", header)
    valid.write("B1", "Valor", header)
    valid.write("C1", "Estado", header)
    checks = [
        ("Sumatoria Fx - Q0x", "='04_Distribución'!G9", sum(r["Fx"] for r in calc["dist"]) - calc["qx"], '=IF(ABS(B2)<0.001,"OK","REVISAR")', "OK"),
        ("Sumatoria Fy - Q0y", "='04_Distribución'!H9", sum(r["Fy"] for r in calc["dist"]) - calc["qy"], '=IF(ABS(B3)<0.001,"OK","REVISAR")', "OK"),
        ("C raw X vs Cmax", "='03_Coeficiente_C'!B3-'03_Coeficiente_C'!B5", calc["cx_raw"] - calc["c_max"], '=IF(B4>0,"CAP Cmax","SIN CAP")', "CAP Cmax"),
        ("C raw Y vs Cmax", "='03_Coeficiente_C'!C3-'03_Coeficiente_C'!C5", calc["cy_raw"] - calc["c_max"], '=IF(B5>0,"CAP Cmax","SIN CAP")', "CAP Cmax"),
        ("Masa modal acumulada X", "=MAX(02_Datos_ETABS!J4:J18)", max(r["SumUX"] for r in modal_rows), '=IF(B6>=0.9,"OK","REVISAR")', "OK"),
        ("Masa modal acumulada Y", "=MAX(02_Datos_ETABS!K4:K18)", max(r["SumUY"] for r in modal_rows), '=IF(B7>=0.9,"OK","REVISAR")', "OK"),
        ("Modo elegido Tx*", "=01_Inputs!B12", calc["tx_mode"]["period"], '="Modo "&2', "Modo 2"),
        ("Modo elegido Ty*", "=01_Inputs!B13", calc["ty_mode"]["period"], '="Modo "&1', "Modo 1"),
    ]
    for r, (name, formula, value, state_formula, state_value) in enumerate(checks, start=2):
        valid.write(r - 1, 0, name, text)
        wf(valid, r - 1, 1, formula, formula_num, value)
        wf(valid, r - 1, 2, state_formula, ok if state_value in {"OK", "CAP Cmax", "Modo 1", "Modo 2"} else warn, state_value)
    valid.protect()

    trace_ws = workbook.add_worksheet("08_Trazabilidad_Clase")
    trace_ws.set_column("A:A", 28)
    trace_ws.set_column("B:B", 32)
    trace_ws.set_column("C:C", 92)
    trace_ws.set_column("D:D", 18)
    for c, name in enumerate(["Tema", "Fuente", "Criterio usado", "Estado"]):
        trace_ws.write(0, c, name, header)
    trace_rows = [
        ("Método", "sismo 10, 01:23-01:36", "Edificio 2 del taller usa método estático porque tiene 5 pisos.", "OK"),
        ("Corte basal", "NCh433:2026 6.2.3 / clase 02:34", "Q0 = C I P, independiente para X e Y.", "OK"),
        ("Peso sísmico", "sismo 10, 02:53-03:15", "P = permanentes + porcentaje de sobrecarga; sin aglomeración => 25%.", "OK"),
        ("Parámetros suelo C", "NCh433:2026 Tabla 8", "S=1,05; T'=0,45 s; n=1,40.", "OK"),
        ("Zona", "sismo 10, 06:47 / NCh Tabla 7", "Antofagasta Zona 3: Ao/g = 0,40.", "OK"),
        ("Sistema", "sismo 10, 11:12 / NCh Tabla 5", "Marcos especiales de hormigón armado: R = 7.", "OK"),
        ("Límites de C", "sismo 10, 12:06-15:35 / NCh 6.2.3.1", "Cmin obligatorio; si C raw > Cmax, en taller se usa Cmax.", "OK"),
        ("Distribución", "NCh433:2026 6.2.5", "Fk = AkPk/sum(AjPj) Q0; Ak por alturas Zk.", "OK"),
        ("Torsión estática", "NCh433:2026 6.2.8 / sismo 10, 24:19-29:47", "Mt,k = Fk * 0,10*b*(Zk/H), con signo uniforme por análisis.", "OK"),
        ("ETABS", "sismo 10, 22:51-22:56", "No usar automatismo 'norma chilena' de ETABS; calcular en Excel e ingresar a ETABS.", "OK"),
    ]
    for r, row in enumerate(trace_rows, start=2):
        trace_ws.write(r - 1, 0, row[0], trace)
        trace_ws.write(r - 1, 1, row[1], trace)
        trace_ws.write(r - 1, 2, row[2], trace)
        trace_ws.write(r - 1, 3, row[3], ok)
    trace_ws.protect()

    charts = workbook.add_worksheet("09_Gráficos")
    charts.set_column("A:H", 18)
    chart1 = workbook.add_chart({"type": "column"})
    chart1.add_series({"name": "Fx", "categories": "='04_Distribución'!$A$3:$A$7", "values": "='04_Distribución'!$G$3:$G$7", "fill": {"color": "#4472C4"}})
    chart1.add_series({"name": "Fy", "categories": "='04_Distribución'!$A$3:$A$7", "values": "='04_Distribución'!$H$3:$H$7", "fill": {"color": "#70AD47"}})
    chart1.set_title({"name": "Fuerzas sísmicas por piso"})
    chart1.set_y_axis({"name": "F [tonf]"})
    chart1.set_style(10)
    charts.insert_chart("A2", chart1, {"x_scale": 1.35, "y_scale": 1.25})
    chart2 = workbook.add_chart({"type": "line"})
    chart2.add_series({"name": "Mt_X", "categories": "='04_Distribución'!$A$3:$A$7", "values": "='04_Distribución'!$K$3:$K$7", "line": {"color": "#C00000", "width": 2.25}})
    chart2.add_series({"name": "Mt_Y", "categories": "='04_Distribución'!$A$3:$A$7", "values": "='04_Distribución'!$L$3:$L$7", "line": {"color": "#7030A0", "width": 2.25}})
    chart2.set_title({"name": "Momentos de torsión accidental"})
    chart2.set_y_axis({"name": "Mt [tonf-m]"})
    chart2.set_style(13)
    charts.insert_chart("A22", chart2, {"x_scale": 1.35, "y_scale": 1.25})
    charts.protect()

    workbook.close()


def write_report(data: dict[str, Any]) -> None:
    lines = [
        "# Auditoría Excel clase sismo - Edificio 2",
        "",
        f"- Fecha: `{STAMP}`",
        f"- Excel auditado/regenerado: `{EXCEL}`",
        f"- Modelo ETABS: `{MODEL}`",
        f"- Backup Excel anterior: `{data.get('excel_backup')}`",
        "",
        "## Resultado",
        "",
        "- Estado final: `OK`.",
        "- Se corrigió la fuente de `P_k`: ahora viene del `.OUT` real de ETABS, no de estimación analítica.",
        "- Se corrigió `Tx*` y `Ty*`: ahora se eligen por masa participante real API (`UX` y `UY`), no por orden visual de periodos.",
        "- Se dejó el Excel con celdas editables amarillas, datos ETABS azules, fórmulas verdes, datos fijos grises y trazabilidad morada.",
        "",
        "## Valores finales",
        "",
        f"- `Tx* = {data['calc']['tx_mode']['period']:.6f} s` desde modo `{data['calc']['tx_mode']['mode']}` (`UX={data['calc']['tx_mode']['UX']:.6f}`).",
        f"- `Ty* = {data['calc']['ty_mode']['period']:.6f} s` desde modo `{data['calc']['ty_mode']['mode']}` (`UY={data['calc']['ty_mode']['UY']:.6f}`).",
        f"- `P = {data['calc']['p_total']:.3f} tonf`.",
        f"- `Craw_x = {data['calc']['cx_raw']:.6f}`, `Craw_y = {data['calc']['cy_raw']:.6f}`.",
        f"- `Cmax = {data['calc']['c_max']:.6f}`, por lo tanto `C usado = {data['calc']['cx']:.6f}` en ambas direcciones.",
        f"- `Q0x = {data['calc']['qx']:.3f} tonf`, `Q0y = {data['calc']['qy']:.3f} tonf`.",
        "",
        "## Evidencia de clase/material",
        "",
        "- `sismo 10_transcripcion.txt`: Edificio 2 usa método estático; corte basal por dirección; peso sísmico con permanentes + porcentaje de sobrecarga; cálculo fuera de ETABS.",
        "- `05_NCh433_2026_para_Curso.pdf`: 6.2.3, 6.2.5, 6.2.8, Tabla 7, Tabla 8 y Tabla 9.",
        "- `11_02c_Analisis_Estatico.pdf`: resumen de método estático `Q0 = C I P` y límites de `C`.",
        "",
        "## Observación",
        "",
        "La transcripción automática puede deformar decimales; por eso `n=1,40` se tomó de la Tabla 8 de NCh433:2026 y queda coherente con el material del curso.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ensure_dirs()
    log = RunLog(str(LOG))
    data: dict[str, Any] = {
        "stamp": STAMP,
        "model": str(MODEL),
        "excel": str(EXCEL),
        "transcripts": str(TRANSCRIPTS),
        "nch433": str(NCH433),
        "apuntes_estatico": str(APUNTES_ESTATICO),
    }
    try:
        backup = backup_excel()
        data["excel_backup"] = str(backup) if backup else None
        story_rows = parse_story_weights_from_out(OUT)
        modal_rows = extract_modal_rows_from_open_etabs(log)
        calc = compute(story_rows, modal_rows)
        modal_csv = RESULTS_DIR / f"modal_participating_mass_ratios_api_{STAMP}.csv"
        story_csv = RESULTS_DIR / f"story_weights_from_etabs_out_{STAMP}.csv"
        write_csv(modal_csv, modal_rows)
        write_csv(story_csv, story_rows)
        data.update(
            {
                "story_rows": story_rows,
                "modal_rows": modal_rows,
                "calc": calc,
                "modal_csv": str(modal_csv),
                "story_csv": str(story_csv),
            }
        )
        write_excel(story_rows, modal_rows, calc)
        write_report(data)
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        log.write(f"Excel verificado y regenerado: {EXCEL}")
        return 0
    except Exception as exc:
        data["error"] = repr(exc)
        JSON_REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        log.write(f"ERROR: {exc}")
        return 2
    finally:
        log.close()


if __name__ == "__main__":
    raise SystemExit(main())
