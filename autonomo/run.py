"""
Agente Autónomo — ETABS Edificio 1
Orquestador que lanza Claude Code CLI por feature,
maneja rate limits, espera y retoma automáticamente.

Uso:
    python autonomo/run.py              # Inicia o retoma
    python autonomo/run.py --status     # Ver estado
    python autonomo/run.py --reset      # Reiniciar progreso
    python autonomo/run.py --skip R01   # Saltar feature
    python autonomo/run.py --only R01   # Ejecutar solo una
"""

import json
import subprocess
import sys
import time
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════

PROJECT_DIR = Path(r"C:\Seba\1° Sem. 2026 - UCN")
AUTONOMO_DIR = PROJECT_DIR / "autonomo"
FEATURES_FILE = AUTONOMO_DIR / "features.json"
PROGRESS_FILE = AUTONOMO_DIR / "progress.json"
CONTEXT_FILE = AUTONOMO_DIR / "context.md"
TASK_FILE = AUTONOMO_DIR / "current_task.md"
LOGS_DIR = AUTONOMO_DIR / "logs"

# Modelo por defecto (features pueden overridear)
DEFAULT_MODEL = "opus"
DEFAULT_MAX_TURNS = 80

# Rate limit: cuánto esperar (segundos)
# Claude Code Max plan: ~5h entre resets
RATE_LIMIT_WAIT_SECONDS = 5 * 3600 + 120  # 5h + 2min de margen
RETRY_WAIT_SECONDS = 30
MAX_RETRIES_PER_FEATURE = 3

# Timeout por feature (segundos) — 2 horas máximo
FEATURE_TIMEOUT = 2 * 3600

# Patrones que indican rate limit en la salida de claude
RATE_LIMIT_PATTERNS = [
    r"rate.?limit",
    r"usage.?limit",
    r"too many requests",
    r"429",
    r"quota",
    r"capacity",
    r"overloaded",
    r"billing",
    r"wait.*minutes",
    r"try again",
    r"exceeded.*limit",
    r"hit your limit",
    r"hit.+limit",
    r"resets?\s+\d{1,2}\s*(am|pm)",
]

# ═══════════════════════════════════════════════════════════
# GESTIÓN DE ESTADO
# ═══════════════════════════════════════════════════════════

def load_features():
    with open(FEATURES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["features"]

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "completed": [],
        "failed": [],
        "skipped": [],
        "current": None,
        "started_at": None,
        "last_run": None,
        "total_claude_runs": 0,
        "rate_limit_waits": 0,
    }

def save_progress(progress):
    progress["last_run"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def get_next_feature(features, progress):
    done = set(progress["completed"] + progress["failed"] + progress["skipped"])
    for feat in features:
        if feat["id"] not in done:
            return feat
    return None

# ═══════════════════════════════════════════════════════════
# RATE LIMIT
# ═══════════════════════════════════════════════════════════

def detect_rate_limit(output):
    """Detecta si la salida de Claude indica rate limit."""
    text = output.lower()
    for pattern in RATE_LIMIT_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

def extract_wait_time(output):
    """Intenta extraer tiempo de espera de la salida de Claude."""
    # Buscar "resets Xam/pm" (formato Claude Max)
    m = re.search(r"resets?\s+(\d{1,2})\s*(am|pm)", output.lower())
    if m:
        hour = int(m.group(1))
        ampm = m.group(2)
        if ampm == "pm" and hour != 12:
            hour += 12
        if ampm == "am" and hour == 12:
            hour = 0
        from datetime import datetime, timedelta
        now = datetime.now()
        reset_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        if reset_time <= now:
            reset_time += timedelta(days=1)
        wait = (reset_time - now).total_seconds() + 120  # +2min margen
        return int(wait)

    # Buscar patrones como "try again in 5 hours" o "wait 300 minutes"
    m = re.search(r"(\d+)\s*hour", output.lower())
    if m:
        return int(m.group(1)) * 3600

    m = re.search(r"(\d+)\s*minute", output.lower())
    if m:
        return int(m.group(1)) * 60

    # Si no encuentra tiempo específico, usar default
    return RATE_LIMIT_WAIT_SECONDS

def wait_for_reset(wait_seconds):
    """Espera con countdown visual hasta que se reseteen los créditos."""
    reset_time = datetime.now() + timedelta(seconds=wait_seconds)

    print(f"\n{'='*60}")
    print(f"  RATE LIMIT DETECTADO")
    print(f"  Esperando hasta: {reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
    hours = wait_seconds // 3600
    mins = (wait_seconds % 3600) // 60
    print(f"  Tiempo: {hours}h {mins}m")
    print(f"{'='*60}\n")

    try:
        while datetime.now() < reset_time:
            remaining = (reset_time - datetime.now()).total_seconds()
            h = int(remaining // 3600)
            m = int((remaining % 3600) // 60)
            s = int(remaining % 60)
            print(f"\r  Faltan: {h:02d}:{m:02d}:{s:02d}  ", end="", flush=True)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\n  Interrumpido por usuario durante espera.")
        print("  Ejecuta de nuevo para retomar.\n")
        sys.exit(0)

    print(f"\n\n  Tiempo cumplido. Retomando en 30 segundos...\n")
    time.sleep(30)

# ═══════════════════════════════════════════════════════════
# PROMPT Y EJECUCIÓN
# ═══════════════════════════════════════════════════════════

def write_task_file(feature, progress, features):
    """Escribe el archivo de tarea que Claude leerá."""
    completed = progress["completed"]
    total = len(features)
    done = len(completed)

    completed_list = "\n".join(f"- {fid}" for fid in completed) if completed else "(ninguna)"

    task_content = f"""# Tarea Actual — Agente Autónomo ETABS

## Progreso: {done}/{total} features completadas

## Feature actual: {feature['id']} — {feature['name']}
**Fase**: {feature.get('phase', 'general')}

## Descripción de la tarea
{feature['description']}

## Outputs esperados
{chr(10).join(f'- {o}' for o in feature.get('outputs', ['(no especificado)']))}

## Features ya completadas
{completed_list}

## Instrucciones obligatorias
1. Lee `autonomo/context.md` PRIMERO para el contexto completo del proyecto
2. Ejecuta la tarea descrita arriba con máximo rigor y exhaustividad
3. Si necesitas investigar en internet, hazlo (web search, web fetch)
4. Escribe los resultados en los archivos indicados en "Outputs esperados"
5. Al terminar, escribe un resumen breve en `autonomo/logs/feature_{feature['id']}.md`
6. NO modifiques autonomo/progress.json — el orquestador lo gestiona

## Reglas
- Español para explicaciones, inglés para código/ETABS
- Para scripts API: Python + comtypes, compatible ETABS v19 (CSI OAPI)
- No inventar funciones de API — usar solo las documentadas
- Verificar contra las normas originales cuando corresponda
- Ser exhaustivo: esta es una tarea crítica
"""
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        f.write(task_content)

def run_claude(feature):
    """Ejecuta Claude Code CLI para una feature."""
    model = feature.get("model", DEFAULT_MODEL)
    max_turns = feature.get("max_turns", DEFAULT_MAX_TURNS)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"raw_{feature['id']}_{timestamp}.log"

    # Prompt corto que referencia el archivo de tarea
    prompt = (
        "Lee el archivo autonomo/current_task.md y ejecuta la tarea descrita. "
        "Lee también autonomo/context.md para el contexto del proyecto. "
        "Sé exhaustivo y riguroso."
    )

    cmd = [
        "claude",
        "-p", prompt,
        "--model", model,
        "--max-turns", str(max_turns),
        "--output-format", "text",
    ]

    print(f"  claude -p (model={model}, max_turns={max_turns})")
    print(f"  Log: {log_file.name}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(PROJECT_DIR),
            timeout=FEATURE_TIMEOUT,
        )

        output = (result.stdout or "") + "\n" + (result.stderr or "")

        # Guardar log crudo
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"Feature: {feature['id']} — {feature['name']}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Model: {model}\n")
            f.write(f"Exit code: {result.returncode}\n")
            f.write(f"{'='*60}\n\n")
            f.write("=== STDOUT ===\n")
            f.write(result.stdout or "(vacío)")
            f.write("\n\n=== STDERR ===\n")
            f.write(result.stderr or "(vacío)")

        is_rate_limited = detect_rate_limit(output)
        wait_time = extract_wait_time(output) if is_rate_limited else 0

        return {
            "success": result.returncode == 0 and not is_rate_limited,
            "output": output,
            "rate_limited": is_rate_limited,
            "wait_time": wait_time,
            "exit_code": result.returncode,
            "log_file": str(log_file),
        }

    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT ({FEATURE_TIMEOUT//3600}h)")
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"TIMEOUT after {FEATURE_TIMEOUT}s\n")
        return {
            "success": False,
            "output": "TIMEOUT",
            "rate_limited": False,
            "wait_time": 0,
            "exit_code": -1,
            "log_file": str(log_file),
        }

    except FileNotFoundError:
        print("  ERROR: 'claude' no encontrado en PATH")
        print("  Asegúrate de tener Claude Code CLI instalado")
        sys.exit(1)

    except Exception as e:
        print(f"  ERROR: {e}")
        return {
            "success": False,
            "output": str(e),
            "rate_limited": False,
            "wait_time": 0,
            "exit_code": -1,
            "log_file": str(log_file),
        }

# ═══════════════════════════════════════════════════════════
# APOS — ACTUALIZACIÓN DE ESTADO
# ═══════════════════════════════════════════════════════════

def update_apos(progress, features):
    """Actualiza archivos APOS con el estado actual."""
    apos_dir = PROJECT_DIR / ".apos"
    apos_dir.mkdir(exist_ok=True)

    completed = len(progress["completed"])
    failed = len(progress.get("failed", []))
    total = len(features)
    pct = 100 * completed // total if total > 0 else 0

    # STATUS.md
    status_lines = [
        "# STATUS — Agente Autónomo ETABS",
        f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"## Progreso: {completed}/{total} ({pct}%)",
        "",
        "### Completadas",
    ]
    for fid in progress["completed"]:
        status_lines.append(f"- {fid}")
    if not progress["completed"]:
        status_lines.append("(ninguna)")

    status_lines.append("")
    status_lines.append("### Pendientes")
    for f in features:
        if f["id"] not in progress["completed"] and f["id"] not in progress.get("failed", []):
            status_lines.append(f"- {f['id']}: {f['name']}")

    if failed > 0:
        status_lines.append("")
        status_lines.append("### Fallidas")
        for fid in progress["failed"]:
            status_lines.append(f"- {fid}")

    status_lines.append("")
    status_lines.append(f"### Stats")
    status_lines.append(f"- Ejecuciones Claude: {progress.get('total_claude_runs', 0)}")
    status_lines.append(f"- Esperas rate limit: {progress.get('rate_limit_waits', 0)}")

    with open(apos_dir / "STATUS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(status_lines))

# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def print_status(features, progress):
    """Muestra estado actual."""
    completed = len(progress["completed"])
    failed = len(progress.get("failed", []))
    skipped = len(progress.get("skipped", []))
    total = len(features)
    pending = total - completed - failed - skipped

    print(f"\n  Features:     {total}")
    print(f"  Completadas:  {completed}")
    print(f"  Fallidas:     {failed}")
    print(f"  Saltadas:     {skipped}")
    print(f"  Pendientes:   {pending}")
    print(f"  Runs Claude:  {progress.get('total_claude_runs', 0)}")
    print(f"  Rate limits:  {progress.get('rate_limit_waits', 0)}")

    if progress.get("started_at"):
        started = datetime.fromisoformat(progress["started_at"])
        elapsed = datetime.now() - started
        print(f"  Tiempo total: {elapsed}")

    if progress.get("current"):
        print(f"  Último/actual: {progress['current']}")
    print()

def handle_args(features, progress):
    """Procesa argumentos de línea de comandos."""
    args = sys.argv[1:]

    if "--status" in args:
        print_status(features, progress)
        sys.exit(0)

    if "--reset" in args:
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
        print("  Progreso reseteado.\n")
        sys.exit(0)

    if "--skip" in args:
        idx = args.index("--skip")
        if idx + 1 < len(args):
            skip_id = args[idx + 1]
            if skip_id not in progress.get("skipped", []):
                progress.setdefault("skipped", []).append(skip_id)
                save_progress(progress)
            print(f"  Feature {skip_id} marcada como saltada.\n")
            sys.exit(0)

    if "--only" in args:
        idx = args.index("--only")
        if idx + 1 < len(args):
            return args[idx + 1]

    return None

# ═══════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════

def main():
    print(
        "\n"
        "  +==========================================+\n"
        "  |  AGENTE AUTONOMO - ETABS Edificio 1     |\n"
        "  |  Orquestador v1.0                       |\n"
        "  +==========================================+\n"
    )

    # Verificar archivos necesarios
    if not FEATURES_FILE.exists():
        print(f"  ERROR: No existe {FEATURES_FILE}")
        print("  Ejecuta primero la configuración del proyecto.\n")
        sys.exit(1)

    if not CONTEXT_FILE.exists():
        print(f"  ERROR: No existe {CONTEXT_FILE}")
        sys.exit(1)

    # Cargar estado
    features = load_features()
    progress = load_progress()

    # CLI args
    only_feature = handle_args(features, progress)

    # Primera ejecución
    if not progress.get("started_at"):
        progress["started_at"] = datetime.now().isoformat()
        save_progress(progress)

    # Estado inicial
    print_status(features, progress)

    # Si --only, buscar esa feature específica
    if only_feature:
        target = None
        for f in features:
            if f["id"] == only_feature:
                target = f
                break
        if not target:
            print(f"  ERROR: Feature '{only_feature}' no encontrada.\n")
            sys.exit(1)
        features_to_run = [target]
    else:
        features_to_run = None  # usar get_next_feature

    total = len(features)

    while True:
        # Obtener siguiente feature
        if features_to_run:
            if not features_to_run:
                break
            feature = features_to_run.pop(0)
        else:
            feature = get_next_feature(features, progress)

        if not feature:
            print("\n  TODAS LAS FEATURES COMPLETADAS\n")
            break

        done = len(progress["completed"])
        print(f"\n{'='*60}")
        print(f"  [{done+1}/{total}] {feature['id']} — {feature['name']}")
        print(f"  Fase: {feature.get('phase', '?')}")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # Escribir tarea para Claude
        write_task_file(feature, progress, features)
        progress["current"] = feature["id"]
        save_progress(progress)

        # Loop de reintentos
        retries = 0
        success = False

        while retries < MAX_RETRIES_PER_FEATURE:
            progress["total_claude_runs"] = progress.get("total_claude_runs", 0) + 1
            save_progress(progress)

            result = run_claude(feature)

            if result["rate_limited"]:
                progress["rate_limit_waits"] = progress.get("rate_limit_waits", 0) + 1
                save_progress(progress)
                wait_for_reset(result["wait_time"] or RATE_LIMIT_WAIT_SECONDS)
                retries += 1
                continue

            if result["success"]:
                print(f"\n  COMPLETADA: {feature['id']}")
                progress["completed"].append(feature["id"])
                progress["current"] = None
                save_progress(progress)
                update_apos(progress, features)
                success = True
                break
            else:
                retries += 1
                print(f"  Intento {retries}/{MAX_RETRIES_PER_FEATURE} fallido")
                print(f"  Exit code: {result['exit_code']}")
                if retries < MAX_RETRIES_PER_FEATURE:
                    print(f"  Reintentando en {RETRY_WAIT_SECONDS}s...")
                    time.sleep(RETRY_WAIT_SECONDS)

        if not success:
            print(f"\n  FALLIDA: {feature['id']} ({MAX_RETRIES_PER_FEATURE} intentos)")
            progress.setdefault("failed", []).append(feature["id"])
            progress["current"] = None
            save_progress(progress)
            update_apos(progress, features)

    # Resumen final
    elapsed = "?"
    if progress.get("started_at"):
        started = datetime.fromisoformat(progress["started_at"])
        elapsed = str(datetime.now() - started).split(".")[0]

    print(f"\n{'='*60}")
    print(f"  RESUMEN FINAL")
    print(f"  Completadas:  {len(progress['completed'])}/{total}")
    print(f"  Fallidas:     {len(progress.get('failed', []))}")
    print(f"  Runs Claude:  {progress.get('total_claude_runs', 0)}")
    print(f"  Rate limits:  {progress.get('rate_limit_waits', 0)}")
    print(f"  Tiempo total: {elapsed}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrumpido. Ejecuta de nuevo para retomar.\n")
        sys.exit(0)
