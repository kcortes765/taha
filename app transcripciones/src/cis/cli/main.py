from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from cis.orchestration.pipeline_daily import run_daily_pipeline
from cis.orchestration.pipeline_pre_exam import run_pre_exam
from cis.orchestration.pipeline_weekly import run_weekly_review


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cis", description="Course Intelligence System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    daily = subparsers.add_parser("daily-run", help="Run the daily ingest pipeline.")
    daily.add_argument("--course", dest="course_id", default=None)

    weekly = subparsers.add_parser("weekly-review", help="Generate a weekly review.")
    weekly.add_argument("--course", dest="course_id", required=True)

    pre_exam = subparsers.add_parser("pre-exam", help="Generate a pre-exam review.")
    pre_exam.add_argument("--course", dest="course_id", required=True)

    ui = subparsers.add_parser("ui", help="Launch the Streamlit dashboard.")
    ui.add_argument("--port", type=int, default=8501)

    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "daily-run":
        result = run_daily_pipeline(course_id=args.course_id)
        print(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return 0

    if args.command == "weekly-review":
        print(run_weekly_review(args.course_id))
        return 0

    if args.command == "pre-exam":
        print(run_pre_exam(args.course_id))
        return 0

    if args.command == "ui":
        app_path = Path(__file__).resolve().parents[1] / "ui" / "app.py"
        project_root = Path(__file__).resolve().parents[3]
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.port", str(args.port)],
            cwd=str(project_root),
            check=False,
        )
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
