"""
run_pipeline.py — Master script: execute entire ETABS pipeline for Edificio 1.

Orchestrates all 12 pipeline scripts in order, split into 2 COM phases
to avoid session crashes (lesson learned from previous attempts):

  PHASE 1 — Geometry (scripts 01–07):
    01_init_model        Initialize model, grid, stories
    02_materials_sections Define G30, A630-420H, VI20x60, MHA30/20, Losa15
    03_walls              Create all walls (dir Y + dir X), 20 stories
    04_beams              Create all beams (vigas invertidas), 20 stories
    05_slabs              Create all slabs (floor + roof panels), 20 stories
    06_assignments        Diaphragm D1, AutoMesh 0.4m, base restraints
    07_loads              Load patterns PP/TERP/TERT/SCP/SCT + gravity loads

  ** CHECKPOINT: Save .edb + restart COM session **

  PHASE 2 — Analysis (scripts 08–12):
    08_seismic            Response spectrum, mass source, P-Delta
    09_torsion            Torsion accidental (3 methods available)
    10_combinations       Load combinations C1–C11 (NCh3171)
    11_run_analysis       Run analysis + validate (weight, T1, drift, Qbase)
    12_extract_results    Extract all results to console/CSV/markdown

Features:
  --dry-run       Print execution plan without running anything
  --from N        Resume from step N (1-12)
  --to N          Stop after step N (1-12)
  --phase 1|2     Run only phase 1 or phase 2
  --no-checkpoint Skip the checkpoint pause between phases
  --log FILE      Write log to file (default: pipeline_YYYYMMDD_HHMMSS.log)

COM session management:
  Each script is run as a subprocess (python script.py) to ensure clean
  COM state. Between phases, the user is prompted to verify ETABS is stable.
  This is the proven approach from lab testing (5 mar 2026).

Prerequisites:
  - ETABS v19 open manually (File > New Model > Blank)
  - comtypes installed (pip install comtypes)
  - All scripts (01-12) + config.py in the same directory
  - For --from > 1: model must be in the correct state

Usage:
  python run_pipeline.py                  # Full pipeline
  python run_pipeline.py --dry-run        # Preview only
  python run_pipeline.py --from 8         # Resume from seismic (phase 2)
  python run_pipeline.py --phase 1        # Geometry only
  python run_pipeline.py --from 3 --to 5  # Only walls, beams, slabs

Sources: Taller ADSE UCN 1S-2026, Prof. Music
Normas: NCh433 Mod 2009, DS61, DS60, ACI318-08, NCh3171, NCh1537
"""

import os
import sys
import time
import argparse
import subprocess
import logging
from datetime import datetime


# ===================================================================
# CONSTANTS
# ===================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Pipeline steps in execution order
# (step_number, script_filename, short_description, phase)
PIPELINE_STEPS = [
    (1,  "01_init_model.py",          "Initialize model, grid, stories",         1),
    (2,  "02_materials_sections.py",  "Define materials and sections",           1),
    (3,  "03_walls.py",               "Create walls (dir Y + dir X, 20 pisos)", 1),
    (4,  "04_beams.py",               "Create beams (vigas invertidas)",         1),
    (5,  "05_slabs.py",               "Create slabs (floor + roof panels)",      1),
    (6,  "06_assignments.py",         "Diaphragm D1, AutoMesh, restraints",      1),
    (7,  "07_loads.py",               "Load patterns + gravity loads",           1),
    (8,  "08_seismic.py",             "Response spectrum, mass source, P-Delta", 2),
    (9,  "09_torsion.py",             "Torsion accidental cases",                2),
    (10, "10_combinations.py",        "Load combinations C1-C11 (NCh3171)",      2),
    (11, "11_run_analysis.py",        "Run analysis + validation",               2),
    (12, "12_extract_results.py",     "Extract results to CSV/markdown",         2),
]

PHASE_NAMES = {
    1: "GEOMETRY (model creation)",
    2: "ANALYSIS (seismic + results)",
}

# Phase boundary: checkpoint happens AFTER this step
PHASE_1_LAST_STEP = 7

# Model save path for checkpoint
MODELS_DIR = os.path.join(SCRIPT_DIR, "models")
CHECKPOINT_FILENAME = "Edificio1_checkpoint_phase1.edb"


# ===================================================================
# LOGGING SETUP
# ===================================================================

def setup_logging(log_file=None):
    """Configure logging to console and optionally to file.

    Args:
        log_file: Path to log file. If None, auto-generates timestamped name.

    Returns:
        Logger instance
    """
    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.DEBUG)

    # Console handler — INFO level
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "[%(asctime)s] %(message)s", datefmt="%H:%M:%S"
    ))
    logger.addHandler(console)

    # File handler — DEBUG level (captures everything)
    if log_file is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(SCRIPT_DIR, f"pipeline_{ts}.log")

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(fh)

    logger.info(f"Log file: {log_file}")
    return logger


# ===================================================================
# PIPELINE EXECUTION
# ===================================================================

def verify_scripts_exist(steps):
    """Check that all required script files exist before starting.

    Args:
        steps: List of (step_num, filename, description, phase) tuples

    Returns:
        List of missing files (empty if all OK)
    """
    missing = []
    for step_num, filename, desc, phase in steps:
        path = os.path.join(SCRIPT_DIR, filename)
        if not os.path.isfile(path):
            missing.append((step_num, filename))
    return missing


def run_step(step_num, filename, description, phase, log, dry_run=False):
    """Execute a single pipeline step as a subprocess.

    Each script is run in its own Python process to ensure clean COM state.
    This prevents stale COM references from accumulating and crashing ETABS.

    Args:
        step_num: Step number (1-12)
        filename: Script filename
        description: Human-readable description
        phase: Phase number (1 or 2)
        log: Logger instance
        dry_run: If True, only print what would be done

    Returns:
        dict with keys: step, filename, success, elapsed, returncode, error
    """
    script_path = os.path.join(SCRIPT_DIR, filename)
    result = {
        "step": step_num,
        "filename": filename,
        "success": False,
        "elapsed": 0.0,
        "returncode": None,
        "error": None,
    }

    log.info("")
    log.info("-" * 60)
    log.info(f"STEP {step_num:02d}/{len(PIPELINE_STEPS):02d} "
             f"[Phase {phase}] — {description}")
    log.info(f"  Script: {filename}")
    log.info("-" * 60)

    if dry_run:
        log.info("  [DRY RUN] Would execute: python %s", filename)
        result["success"] = True
        return result

    t_start = time.time()

    try:
        # Run script as subprocess with same Python interpreter
        # Working directory = script directory (so config.py imports work)
        proc = subprocess.run(
            [sys.executable, script_path],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes max per step
        )

        result["returncode"] = proc.returncode
        result["elapsed"] = time.time() - t_start

        # Log stdout (each script already uses logging to stdout)
        if proc.stdout:
            for line in proc.stdout.strip().split("\n"):
                log.debug("  [stdout] %s", line)
            # Show last few lines in console for progress
            stdout_lines = proc.stdout.strip().split("\n")
            # Print summary lines (typically the last SUMMARY block)
            summary_started = False
            for line in stdout_lines:
                if "SUMMARY" in line or "Ready for" in line:
                    summary_started = True
                if summary_started:
                    log.info("  %s", line)

        # Log stderr
        if proc.stderr:
            for line in proc.stderr.strip().split("\n"):
                log.debug("  [stderr] %s", line)

        if proc.returncode == 0:
            result["success"] = True
            log.info(f"  OK — completed in {result['elapsed']:.1f}s")
        else:
            result["error"] = f"Exit code {proc.returncode}"
            log.error(f"  FAILED — exit code {proc.returncode} "
                      f"after {result['elapsed']:.1f}s")
            # Show last 10 lines of stdout for debugging
            if proc.stdout:
                log.error("  Last output lines:")
                for line in stdout_lines[-10:]:
                    log.error("    %s", line)
            if proc.stderr:
                stderr_lines = proc.stderr.strip().split("\n")
                log.error("  Stderr (last 10 lines):")
                for line in stderr_lines[-10:]:
                    log.error("    %s", line)

    except subprocess.TimeoutExpired:
        result["elapsed"] = time.time() - t_start
        result["error"] = "TIMEOUT (>600s)"
        log.error(f"  TIMEOUT — step exceeded 10 minutes, killed")

    except Exception as e:
        result["elapsed"] = time.time() - t_start
        result["error"] = str(e)
        log.error(f"  EXCEPTION: {e}")

    return result


def checkpoint_between_phases(log, dry_run=False):
    """Checkpoint between Phase 1 and Phase 2.

    Saves the model via a lightweight COM call, then prompts the user
    to verify ETABS is stable before continuing.

    Critical lesson (5 mar 2026): COM sessions die after heavy geometry
    creation (~1700 area objects + mesh). Separating into 2 phases with
    a fresh COM session for Phase 2 is the proven fix.
    """
    log.info("")
    log.info("=" * 60)
    log.info("CHECKPOINT — Phase 1 complete, preparing Phase 2")
    log.info("=" * 60)
    log.info("")
    log.info("Phase 1 (Geometry) is done. Before running Phase 2 (Analysis):")
    log.info("")
    log.info("  1. In ETABS: File > Save (Ctrl+S) — save the model now")
    log.info("  2. Verify the model looks correct (check a few stories)")
    log.info("  3. Optional but RECOMMENDED: close and reopen ETABS,")
    log.info("     then File > Open > the saved .edb file")
    log.info("     (This gives a fresh COM session for Phase 2)")
    log.info("")
    log.info("  WHY: COM sessions can become unstable after creating ~2000+")
    log.info("  area objects. A fresh session prevents RPC errors in Phase 2.")
    log.info("")

    if dry_run:
        log.info("  [DRY RUN] Would pause for checkpoint here")
        return True

    try:
        # Save model via subprocess (lightweight COM call)
        log.info("  Attempting to save model via COM...")
        save_script = (
            "import sys, os\n"
            "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
            "from config import connect, MODELS_DIR\n"
            "import os\n"
            "os.makedirs(MODELS_DIR, exist_ok=True)\n"
            "try:\n"
            "    m = connect(clean_gen=False)\n"
            "    p = os.path.join(MODELS_DIR, 'Edificio1_checkpoint_phase1.edb')\n"
            "    ret = m.File.Save(p)\n"
            "    print(f'Saved: {p}' if ret == 0 else f'Save returned {ret}')\n"
            "except Exception as e:\n"
            "    print(f'Save failed: {e} — save manually in ETABS')\n"
        )
        proc = subprocess.run(
            [sys.executable, "-c", save_script],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.stdout:
            log.info("  %s", proc.stdout.strip())

    except Exception as e:
        log.warning(f"  Auto-save failed: {e}")
        log.info("  Please save manually in ETABS (File > Save)")

    # Wait for user confirmation
    log.info("")
    log.info("  Press ENTER to continue with Phase 2 (Analysis)...")
    log.info("  (or Ctrl+C to abort)")

    try:
        input()
        log.info("  Continuing to Phase 2...")
        return True
    except (KeyboardInterrupt, EOFError):
        log.info("  Pipeline aborted by user at checkpoint")
        return False


def print_execution_plan(steps, from_step, to_step, log):
    """Print the execution plan before running.

    Args:
        steps: List of steps to execute
        from_step: Starting step number
        to_step: Ending step number
        log: Logger instance
    """
    log.info("")
    log.info("EXECUTION PLAN")
    log.info("=" * 60)
    current_phase = 0
    for step_num, filename, desc, phase in steps:
        if step_num < from_step or step_num > to_step:
            continue
        if phase != current_phase:
            current_phase = phase
            log.info(f"\n  Phase {phase}: {PHASE_NAMES[phase]}")
            log.info(f"  {'─' * 50}")
        marker = ">>>" if step_num == from_step and from_step > 1 else "   "
        log.info(f"  {marker} Step {step_num:02d}: {desc}")
        log.info(f"         ({filename})")

    if from_step <= PHASE_1_LAST_STEP < to_step:
        log.info(f"\n  *** CHECKPOINT between Phase 1 and Phase 2 ***")

    total = sum(1 for s in steps if from_step <= s[0] <= to_step)
    log.info(f"\n  Total steps: {total}")
    log.info("=" * 60)


def run_pipeline(args):
    """Main pipeline execution logic.

    Args:
        args: Parsed command-line arguments
    """
    # Setup logging
    log = setup_logging(args.log)

    log.info("=" * 60)
    log.info("ETABS PIPELINE — Edificio 1 (20p muros HA, Antofagasta)")
    log.info("Taller ADSE UCN 1S-2026 — Prof. Music")
    log.info("=" * 60)
    log.info(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"  Python:  {sys.executable}")
    log.info(f"  Scripts: {SCRIPT_DIR}")
    log.info(f"  Mode:    {'DRY RUN' if args.dry_run else 'EXECUTE'}")

    # Determine step range
    from_step = args.from_step
    to_step = args.to_step

    # If --phase is specified, override from/to
    if args.phase == 1:
        from_step = max(from_step, 1)
        to_step = min(to_step, PHASE_1_LAST_STEP)
    elif args.phase == 2:
        from_step = max(from_step, PHASE_1_LAST_STEP + 1)
        to_step = min(to_step, len(PIPELINE_STEPS))

    log.info(f"  Steps:   {from_step} to {to_step}")
    if from_step > 1:
        log.info(f"  RESUME:  Starting from step {from_step}")
    log.info("")

    # Filter steps to execute
    steps_to_run = [
        s for s in PIPELINE_STEPS if from_step <= s[0] <= to_step
    ]

    if not steps_to_run:
        log.error("No steps to execute in the specified range")
        return 1

    # Print execution plan
    print_execution_plan(PIPELINE_STEPS, from_step, to_step, log)

    # Verify all scripts exist
    missing = verify_scripts_exist(steps_to_run)
    if missing:
        log.error("Missing scripts:")
        for num, fname in missing:
            log.error(f"  Step {num}: {fname}")
        return 1
    log.info("  All script files verified OK")

    if args.dry_run:
        log.info("")
        log.info("[DRY RUN] Simulating execution...")

    # Execute pipeline
    results = []
    pipeline_start = time.time()
    current_phase = 0

    for step_num, filename, desc, phase in steps_to_run:
        # Phase transition header
        if phase != current_phase:
            current_phase = phase
            log.info("")
            log.info("=" * 60)
            log.info(f"PHASE {phase}: {PHASE_NAMES[phase]}")
            log.info("=" * 60)

        # Checkpoint between phases
        if (step_num == PHASE_1_LAST_STEP + 1
                and from_step <= PHASE_1_LAST_STEP
                and not args.no_checkpoint):
            if not checkpoint_between_phases(log, args.dry_run):
                log.info("Pipeline aborted at checkpoint")
                break

        # Execute step
        result = run_step(step_num, filename, desc, phase, log, args.dry_run)
        results.append(result)

        # Abort on failure (unless dry run)
        if not result["success"] and not args.dry_run:
            log.error("")
            log.error("=" * 60)
            log.error(f"PIPELINE ABORTED at step {step_num}")
            log.error(f"  Error: {result['error']}")
            log.error(f"  To resume: python run_pipeline.py --from {step_num}")
            log.error("=" * 60)
            break

        # Brief pause between steps for COM stability (2s)
        if not args.dry_run and step_num < to_step:
            time.sleep(2)

    # Pipeline summary
    pipeline_elapsed = time.time() - pipeline_start

    log.info("")
    log.info("=" * 60)
    log.info("PIPELINE SUMMARY")
    log.info("=" * 60)
    log.info(f"  Total time: {format_time(pipeline_elapsed)}")
    log.info(f"  Steps run:  {len(results)}")
    log.info("")

    # Results table
    succeeded = 0
    failed = 0
    log.info(f"  {'Step':>4s}  {'Status':>8s}  {'Time':>8s}  Description")
    log.info(f"  {'─'*4}  {'─'*8}  {'─'*8}  {'─'*30}")
    for r in results:
        status = "OK" if r["success"] else "FAILED"
        elapsed = format_time(r["elapsed"]) if r["elapsed"] > 0 else "—"
        # Find description
        desc = next(
            (s[2] for s in PIPELINE_STEPS if s[0] == r["step"]), "?"
        )
        log.info(f"  {r['step']:4d}  {status:>8s}  {elapsed:>8s}  {desc}")
        if r["success"]:
            succeeded += 1
        else:
            failed += 1

    log.info("")
    log.info(f"  Succeeded: {succeeded}  |  Failed: {failed}")

    if failed == 0 and not args.dry_run:
        log.info("")
        log.info("  PIPELINE COMPLETE — All steps executed successfully!")
        log.info("")
        log.info("  Next steps:")
        log.info("    1. Review results in autonomo/scripts/results/")
        log.info("    2. Check drift < 0.002 (NCh433)")
        log.info("    3. Verify T1 ~ 1.0-1.3s")
        log.info("    4. Confirm weight ~ 9,368 tonf (1 tonf/m2)")
    elif args.dry_run:
        log.info("")
        log.info("  [DRY RUN] No scripts were executed")
        log.info("  Remove --dry-run to run the pipeline")

    log.info("")
    log.info("=" * 60)
    log.info(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)

    return 1 if failed > 0 else 0


def format_time(seconds):
    """Format elapsed time as human-readable string.

    Args:
        seconds: Elapsed time in seconds

    Returns:
        Formatted string (e.g., "1m 23s", "45.2s", "2h 15m")
    """
    if seconds < 0.1:
        return "< 0.1s"
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m {secs:.0f}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"


# ===================================================================
# CLI
# ===================================================================

def parse_args():
    """Parse command-line arguments.

    Returns:
        Parsed args namespace
    """
    parser = argparse.ArgumentParser(
        description="ETABS Pipeline — Edificio 1 (20p muros HA, Antofagasta)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py                  Full pipeline (all 12 steps)
  python run_pipeline.py --dry-run        Preview execution plan
  python run_pipeline.py --from 8         Resume from step 8 (Phase 2)
  python run_pipeline.py --phase 1        Run geometry only (steps 1-7)
  python run_pipeline.py --from 3 --to 5  Only walls, beams, slabs
  python run_pipeline.py --no-checkpoint  Skip pause between phases

Pipeline steps:
  Phase 1 (Geometry):
    01  Initialize model       05  Create slabs
    02  Materials/sections      06  Assignments (D1, mesh)
    03  Create walls            07  Load patterns + gravity
    04  Create beams
  Phase 2 (Analysis):
    08  Response spectrum       11  Run analysis
    09  Torsion accidental      12  Extract results
    10  Load combinations
        """,
    )

    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print execution plan without running any scripts"
    )

    parser.add_argument(
        "--from", dest="from_step", type=int, default=1,
        metavar="N", choices=range(1, 13),
        help="Resume pipeline from step N (1-12, default: 1)"
    )

    parser.add_argument(
        "--to", dest="to_step", type=int, default=12,
        metavar="N", choices=range(1, 13),
        help="Stop pipeline after step N (1-12, default: 12)"
    )

    parser.add_argument(
        "--phase", type=int, default=None, choices=[1, 2],
        help="Run only phase 1 (geometry) or phase 2 (analysis)"
    )

    parser.add_argument(
        "--no-checkpoint", action="store_true",
        help="Skip the checkpoint pause between Phase 1 and Phase 2"
    )

    parser.add_argument(
        "--log", type=str, default=None, metavar="FILE",
        help="Log file path (default: auto-generated timestamped name)"
    )

    args = parser.parse_args()

    # Validate step range
    if args.from_step > args.to_step:
        parser.error(f"--from ({args.from_step}) must be <= --to ({args.to_step})")

    return args


# ===================================================================
# MAIN
# ===================================================================

if __name__ == "__main__":
    args = parse_args()
    exit_code = run_pipeline(args)
    sys.exit(exit_code)
