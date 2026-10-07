"""
Test harness for stage-four-cert evals.
Wraps coe with a reset step so each run starts from State A (stale docs).

Usage:
    python scripts/run_eval.py                      # Run all evals (20 runs each)
    python scripts/run_eval.py update-docs-eval     # Run one specific eval
    python scripts/run_eval.py --runs 5             # Override run count

The reset step (reset_eval.sh) restores CLAUDE.md, human-tasks/, and .beads/
to the State A commit before each full eval suite, ensuring repeatable conditions.
"""
import subprocess
import sys
import os
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def reset_state() -> None:
    """Restore docs to State A (stale) via git checkout."""
    result = subprocess.run(
        ["bash", str(REPO_ROOT / "reset_eval.sh")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Reset failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(result.stdout.strip())


def run_coe(eval_file: str | None = None, runs: int = 20) -> int:
    """Run coe test, optionally for a specific eval file."""
    cmd = ["coe", "test"]
    if eval_file:
        cmd.append(eval_file)
    cmd += ["--runs", str(runs)]

    result = subprocess.run(cmd, cwd=REPO_ROOT)
    return result.returncode


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 4 cert eval harness")
    parser.add_argument(
        "eval_file",
        nargs="?",
        help="Specific eval file to run (e.g. update-docs-eval). Omit to run all.",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=20,
        help="Number of eval runs per file (default: 20)",
    )
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Skip the reset step (use current doc state)",
    )
    args = parser.parse_args()

    if not args.no_reset:
        print("==> Resetting docs to State A...")
        reset_state()

    print(f"==> Running evals ({args.runs} runs each)...")
    rc = run_coe(args.eval_file, args.runs)
    sys.exit(rc)


if __name__ == "__main__":
    main()
