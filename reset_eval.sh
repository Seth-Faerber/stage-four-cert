#!/bin/bash
# Reset to State B (code implemented, issues still open) for update-beads eval.
# Preserves audit_log.jsonl and audit_log/ artifacts from prior runs.
set -e

git checkout HEAD -- CLAUDE.md human-tasks/ .beads/

# interactions.jsonl is restored by git checkout above (may have stale entries).
# Truncate it so the eval's file_contains checks start from a clean baseline.
truncate -s 0 .beads/interactions.jsonl

# Dolt is gitignored — force all three issues to open regardless of prior runs.
bd reopen stage-four-cert-k0w stage-four-cert-5bs stage-four-cert-3ey

echo "Reset complete: k0w, 5bs, 3ey reopened to open state (State B)"
