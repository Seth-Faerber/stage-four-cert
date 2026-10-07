#!/bin/bash
# Reset docs to State A (out of sync with codebase) for a clean eval run.
# Preserves audit_log.jsonl and audit_log/ artifacts from prior runs.
set -e

git checkout HEAD -- CLAUDE.md human-tasks/ .beads/

echo "Reset complete: CLAUDE.md, human-tasks/, and .beads/ restored to State A (out of sync)"
