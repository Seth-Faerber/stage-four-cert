---
name: update-beads
description: Audit beads issues against the actual codebase state. Closes completed issues, flags ambiguous ones, and notes orphaned work. Returns structured findings and writes an audit artifact.
---

# Update Beads

Audit open beads issues against the actual codebase. Close completed issues; flag ambiguous ones.

> **Non-interactive shell rule**: every `bd` command must be prefixed with `source ~/.zshrc &&` so `BEADS_DIR` is set.

---

## Required output format

Your final response (Step 5) **must** use these section headers verbatim. All three sections are required — write `- none` if a section has no entries. Do not rename or reword the headers.

```
## Beads Audit

**Closed**
- <id> — <title>: <one-line rationale>

**Flagged**
- <id> — <title>: <reason>

**Orphaned work**
- <commit or description>

Audit written to: audit_log/update-beads-<timestamp>.json
```

---

## Example

**Issues found (Step 1):**
- `myapp-4xr` — Add GET /health endpoint (open, P2)
- `myapp-9kz` — Add in-memory cache module (open, P2)
- `myapp-2mn` — Configure log aggregation (open, P3, blocked)

Recent commits: `feat: health + cache`, `chore: update readme`

**Issue myapp-4xr:**
`bd show myapp-4xr` → wants `GET /api/health` returning `{status: ok}`.
`read_file: src/api/health.ts` → exists, returns `{status: "ok"}`.
Work is done → run immediately:
```bash
source ~/.zshrc && bd close myapp-4xr --reason="Implemented — src/api/health.ts returns {status: ok}"
```

**Issue myapp-9kz:**
`bd show myapp-9kz` → wants in-memory cache with TTL.
`read_file: src/cache.ts` → exists, uses `node-cache` with TTL config.
`run_command: grep node-cache package.json` → found in dependencies.
Work is done → run immediately:
```bash
source ~/.zshrc && bd close myapp-9kz --reason="Implemented — src/cache.ts uses node-cache"
```

**Issue myapp-2mn:**
`bd show myapp-2mn` → wants structured log aggregation to external sink.
`run_command: grep -r "winston\|pino\|bunyan" src/` → no results.
Work is not done → leave alone.

**Orphaned work (Step 3):** `feat: health + cache` → accounted for by myapp-4xr and myapp-9kz. None orphaned.

**Artifact (Step 4):** Written to `audit_log/update-beads-2024-01-15T10:30:00Z.json`

**Output (Step 5):**

## Beads Audit

**Closed**
- myapp-4xr — Add GET /health endpoint: Implemented — src/api/health.ts returns {status: ok}
- myapp-9kz — Add in-memory cache module: Implemented — src/cache.ts uses node-cache

**Flagged**
- none

**Orphaned work**
- none

Audit written to: audit_log/update-beads-2024-01-15T10:30:00Z.json

---

## Overview

All five steps must complete before returning results:

1. Get current issues
2. Cross-reference with codebase
3. Check for orphaned work
4. Write audit artifact to `audit_log/`
5. Return findings

---

## Step 1 — Get current issues

Run in parallel:

```bash
source ~/.zshrc && bd list --status=open
source ~/.zshrc && bd list --status=in_progress
git log --oneline -20
```

---

## Step 2 — Cross-reference with codebase

For each open/in-progress issue:

1. Read the issue: `source ~/.zshrc && bd show <id>`
2. Search the codebase for the work described (files, routes, functions, dependencies).
3. Decide:
   - **Work exists in the codebase** → close it immediately, before checking the next issue:
     ```bash
     source ~/.zshrc && bd close <id> --reason="Implemented — <one-line evidence>"
     ```
   - **Work does not exist** → leave it alone.
   - **Uncertain** → flag it; do not close.

**Evidence bar**: presence of the described artifact (file, route, module, dependency) is sufficient to close. Do not check whether it is actively called, imported, or wired up elsewhere — that is out of scope.

Close each confirmed issue as you go. Do not batch closes at the end.

---

## Step 3 — Check for orphaned work

Note any recent commits from `git log` that have no corresponding open issue. Do not create retroactive issues.

---

## Step 4 — Write audit artifact

Write `audit_log/update-beads-<timestamp>.json` (create `audit_log/` if needed):

```json
{
  "skill": "update-beads",
  "timestamp": "<ISO 8601>",
  "closed": [
    { "id": "<issue id>", "title": "<title>", "reason": "<close reason>" }
  ],
  "flags": [
    { "id": "<issue id>", "title": "<title>", "reason": "<why flagged>" }
  ],
  "orphaned_work": [
    "<commit or description>"
  ]
}
```

---

## Step 5 — Return findings

Use the required output format from the top of this skill. Include the artifact path on the last line.

---

## Edge cases

- **No open issues**: Skip Steps 2–3; write `- none` in all sections.
- **`bd` not available**: Report the error and stop.
- **Ambiguity**: Flag rather than close; do not close if uncertain.

---

## Make sure

Before finishing, confirm every step was completed:

- [ ] Step 1: Ran `bd list --status=open`, `bd list --status=in_progress`, and `git log`
- [ ] Step 2: Reviewed each issue and ran `bd close` immediately for each completed one
- [ ] Step 3: Checked recent git history for orphaned work
- [ ] Step 4: Wrote the JSON audit artifact to `audit_log/update-beads-<timestamp>.json`
- [ ] Step 5: Returned findings using the exact format from the top of this skill
