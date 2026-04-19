"""
run_pipeline_ed2.py - Orquestador oficial Ed.2 Parte 1.

Mantiene el contrato de uso:
- python run_pipeline_ed2.py
- python run_pipeline_ed2.py --phase 1
- python run_pipeline_ed2.py --phase 2
- python run_pipeline_ed2.py --from N --to M
- python run_pipeline_ed2.py --dry-run
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import datetime


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_STEPS = [
    (1, "01_init_model_ed2.py", "Initialize model, grid 6x6, 5 stories", 1),
    (2, "02_materials_sections_ed2.py", "Define materials and sections", 1),
    (3, "03_columns_ed2.py", "Create columns (70x70 / 65x65)", 1),
    (4, "04_beams_ed2.py", "Create beams (50x70 / 45x70)", 1),
    (5, "05_slabs_ed2.py", "Create slabs (17cm, 5 pisos)", 1),
    (6, "06_assignments_ed2.py", "Diaphragm D1, AutoMesh, restraints", 1),
    (7, "07_loads_ed2.py", "Load patterns + gravity loads", 1),
    (8, "08_seismic_ed2.py", "Mass source + modal auxiliar oficial", 2),
    (9, "09_torsion_ed2.py", "Casos estaticos EX/EY/TEX/TEY", 2),
    (10, "10_combinations_ed2.py", "Combinaciones oficiales C1-C7", 2),
    (11, "11_run_analysis_ed2.py", "Run analysis oficial", 2),
    (12, "12_extract_results_ed2.py", "Extract official results", 2),
]
PHASE_NAMES = {1: "GEOMETRY", 2: "ANALYSIS"}
PHASE_1_LAST_STEP = 7


def resolve_model_arg(model_arg):
    if not model_arg:
        return None
    if os.path.isabs(model_arg):
        return os.path.abspath(model_arg)
    runtime_root = str(os.getenv("ED2_RUNTIME_ROOT", "")).strip()
    if runtime_root:
        return os.path.abspath(os.path.join(runtime_root, model_arg))
    return os.path.abspath(model_arg)


def setup_logging(log_file=None):
    logger = logging.getLogger("pipeline_ed2")
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(console)

    if log_file is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(SCRIPT_DIR, f"pipeline_ed2_{stamp}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    logger.addHandler(file_handler)

    logger.info(f"Log file: {log_file}")
    return logger


def format_elapsed(seconds: float) -> str:
    if seconds < 0.1:
        return "< 0.1s"
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def verify_scripts_exist(steps):
    missing = []
    for step_num, filename, _, _ in steps:
        if not os.path.isfile(os.path.join(SCRIPT_DIR, filename)):
            missing.append((step_num, filename))
    return missing


def print_plan(log, steps, start_step, end_step):
    log.info("")
    log.info("EXECUTION PLAN")
    log.info("=" * 60)
    current_phase = None
    for step_num, filename, description, phase in steps:
        if step_num < start_step or step_num > end_step:
            continue
        if phase != current_phase:
            current_phase = phase
            log.info(f"  Phase {phase}: {PHASE_NAMES[phase]}")
            log.info(f"  {'-' * 50}")
        log.info(f"    Step {step_num:02d}: {description}")
        log.info(f"      ({filename})")
    if start_step <= PHASE_1_LAST_STEP < end_step:
        log.info("  *** CHECKPOINT between Phase 1 and Phase 2 ***")
    log.info("=" * 60)


def run_step(log, step_num, filename, description, phase, dry_run=False, env_overrides=None):
    log.info("")
    log.info("-" * 60)
    log.info(f"STEP {step_num:02d}/12 [Phase {phase}] - {description}")
    log.info(f"  Script: {filename}")
    log.info("-" * 60)

    if dry_run:
        log.info(f"  [DRY RUN] Would execute: python {filename}")
        return {"step": step_num, "success": True, "elapsed": 0.0, "error": None}

    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    started = time.time()
    proc = subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, filename)],
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True,
        timeout=900,
        env=env,
    )
    elapsed = time.time() - started

    if proc.stdout:
        for line in proc.stdout.splitlines()[-20:]:
            log.info(f"  {line}")
    if proc.stderr:
        for line in proc.stderr.splitlines()[-20:]:
            log.debug(f"stderr: {line}")

    if proc.returncode != 0:
        log.error(f"  FAILED - exit code {proc.returncode}")
        return {"step": step_num, "success": False, "elapsed": elapsed, "error": f"exit {proc.returncode}"}

    log.info(f"  OK - completed in {elapsed:.1f}s")
    return {"step": step_num, "success": True, "elapsed": elapsed, "error": None}


def checkpoint(log, dry_run=False):
    log.info("")
    log.info("=" * 60)
    log.info("CHECKPOINT - Phase 1 complete, preparing Phase 2")
    log.info("=" * 60)
    log.info("1. Save the .edb in ETABS")
    log.info("2. Verify the model visually")
    log.info("3. Recommended: close/reopen ETABS before Phase 2")
    if dry_run:
        log.info("[DRY RUN] Would pause here")
        return True
    try:
        input("Press Enter to continue with Phase 2...")
        return True
    except (EOFError, KeyboardInterrupt):
        log.info("Checkpoint aborted by user")
        return False


def run_pipeline(args):
    log = setup_logging(args.log)
    log.info("=" * 60)
    log.info("ETABS PIPELINE - Edificio 2 (5p marcos HA, Antofagasta)")
    log.info("Taller ADSE UCN 1S-2026 - Prof. Music")
    log.info("=" * 60)
    log.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"Scripts: {SCRIPT_DIR}")
    log.info(f"Mode: {'DRY RUN' if args.dry_run else 'EXECUTE'}")
    log.info(f"Runtime root: {os.getenv('ED2_RUNTIME_ROOT', SCRIPT_DIR)}")
    if args.create_if_missing:
        log.info("ETABS startup: attach or create if missing")
    resolved_model = resolve_model_arg(args.model)
    if resolved_model:
        log.info(f"Target model: {resolved_model}")

    start_step = args.from_step
    end_step = args.to_step
    if args.phase == 1:
        start_step = max(start_step, 1)
        end_step = min(end_step, PHASE_1_LAST_STEP)
    elif args.phase == 2:
        start_step = max(start_step, PHASE_1_LAST_STEP + 1)
        end_step = min(end_step, len(PIPELINE_STEPS))

    selected = [step for step in PIPELINE_STEPS if start_step <= step[0] <= end_step]
    if not selected:
        log.error("No steps selected")
        return 1

    if resolved_model and start_step > 1 and not os.path.isfile(resolved_model):
        log.error(f"--model not found for step {start_step}: {resolved_model}")
        return 1

    print_plan(log, PIPELINE_STEPS, start_step, end_step)

    missing = verify_scripts_exist(selected)
    if missing:
        log.error("Missing scripts:")
        for step_num, filename in missing:
            log.error(f"  Step {step_num}: {filename}")
        return 1
    log.info("All script files verified OK")

    env_overrides = {}
    if args.create_if_missing:
        env_overrides["ED2_ETABS_CREATE_IF_MISSING"] = "1"
    if resolved_model:
        env_overrides["ED2_ETABS_MODEL_PATH"] = resolved_model
        if start_step > 1:
            env_overrides["ED2_ETABS_FORCE_MODEL_OPEN"] = "1"

    results = []
    pipeline_started = time.time()
    current_phase = None
    for step_num, filename, description, phase in selected:
        if phase != current_phase:
            current_phase = phase
            log.info("")
            log.info("=" * 60)
            log.info(f"PHASE {phase}: {PHASE_NAMES[phase]}")
            log.info("=" * 60)

        if step_num == PHASE_1_LAST_STEP + 1 and start_step <= PHASE_1_LAST_STEP and not args.no_checkpoint:
            if not checkpoint(log, args.dry_run):
                break

        result = run_step(
            log,
            step_num,
            filename,
            description,
            phase,
            args.dry_run,
            env_overrides=env_overrides,
        )
        results.append(result)
        if not result["success"] and not args.dry_run:
            log.error(f"Pipeline aborted at step {step_num}")
            log.error(f"Resume with: python run_pipeline_ed2.py --from {step_num}")
            break
        if not args.dry_run and step_num < end_step:
            time.sleep(1)

    elapsed = time.time() - pipeline_started
    ok = sum(1 for item in results if item["success"])
    failed = len(results) - ok

    log.info("")
    log.info("=" * 60)
    log.info("PIPELINE SUMMARY")
    log.info("=" * 60)
    log.info(f"Total time: {format_elapsed(elapsed)}")
    log.info(f"Succeeded: {ok} | Failed: {failed}")
    log.info("")
    log.info(f"  {'Step':>4s}  {'Status':>8s}  {'Time':>8s}  Description")
    log.info(f"  {'-'*4}  {'-'*8}  {'-'*8}  {'-'*30}")
    desc_map = {step: desc for step, _, desc, _ in PIPELINE_STEPS}
    for item in results:
        status = "OK" if item["success"] else "FAILED"
        runtime = format_elapsed(item["elapsed"]) if item["elapsed"] > 0 else "-"
        log.info(f"  {item['step']:4d}  {status:>8s}  {runtime:>8s}  {desc_map[item['step']]}")

    if failed == 0:
        if args.dry_run:
            log.info("[DRY RUN] No scripts were executed")
        else:
            log.info("PIPELINE COMPLETE - all selected steps finished")
        return 0
    return 1


def build_parser():
    parser = argparse.ArgumentParser(
        description="ETABS Pipeline - Edificio 2 (5p marcos HA, Antofagasta)",
        epilog="""
Examples:
  python run_pipeline_ed2.py
  python run_pipeline_ed2.py --dry-run
  python run_pipeline_ed2.py --phase 1
  python run_pipeline_ed2.py --phase 2
  python run_pipeline_ed2.py --from 8
  python run_pipeline_ed2.py --create-if-missing
  python run_pipeline_ed2.py --phase 2 --model C:\\ruta\\Edificio2_parte1_oficial.edb
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dry-run", action="store_true", help="Print execution plan without running")
    parser.add_argument("--from", dest="from_step", type=int, default=1, choices=range(1, 13), help="Resume pipeline from step N")
    parser.add_argument("--to", dest="to_step", type=int, default=12, choices=range(1, 13), help="Stop pipeline after step N")
    parser.add_argument("--phase", type=int, choices=[1, 2], help="Run only phase 1 or phase 2")
    parser.add_argument("--no-checkpoint", action="store_true", help="Skip pause between phase 1 and phase 2")
    parser.add_argument("--create-if-missing", action="store_true", help="Launch ETABS if no running instance is found")
    parser.add_argument("--model", help="Open/force this .edb after connecting")
    parser.add_argument("--log", help="Custom log file path")
    return parser


if __name__ == "__main__":
    sys.exit(run_pipeline(build_parser().parse_args()))
