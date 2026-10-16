---
name: update-human-tasks
description: Audit human-tasks checklists against the actual codebase state. Checks off completed items, adds missing items, and flags items requiring human verification. Returns structured findings and writes an audit artifact.
---

# Update Human-Tasks

Audit `human-tasks/` checklists against the actual codebase. Check off items the codebase proves are done; flag items requiring human action.

---

## Step 1 — Locate and read checklists

Look for `human-tasks/` in the repo root. If it doesn't exist, skip all steps and output "No human-tasks directory found."

If it exists, read every file in the directory.

---

## Step 2 — Snapshot relevant codebase state

Gather what's needed to evaluate checklist items:

1. `.env.example` and env validation file — to evaluate infrastructure/credential items
2. `package.json` — to check dependencies and scripts
3. Glob `src/app/api/**/route.ts` — to check API endpoint items
4. Recent git history: `git log --oneline -30`

---

## Step 3 — Evaluate each checklist item

### Already-done items (`[x]`)
Verify they're still valid (e.g. "Run npm install" — is the project still npm-based?). Leave alone if valid; flag if stale.

### Incomplete items (`[ ]`)
Check if they're actually done now:

- **Infrastructure items** (API keys, accounts, credentials): Check if the corresponding env var exists in `.env.example` or validation schema. If present, the setup likely happened -- but only a human can confirm credentials are configured. **Flag these; do not check off.**
- **Verification items** (test flows, review prompts, manual checks): Check if automated tests cover them. If not, leave as incomplete -- these require human action.
- **Roadmap items** (Spec X, feature Y): Cross-reference with actual code. If the spec is fully implemented (routes, schema, UI all present), check it off.
- **Setup items** (install deps, run migrations): If the codebase shows clear evidence the step was done (deps in package.json, schema files present), check it off.

### Actions
- **Edit directly**: Check off items where the codebase proves completion. Use the Edit tool to change `[ ]` to `[x]`.
- **Add new items**: For new required env vars, new infrastructure dependencies, or new verification needs discovered in the codebase.
- **Flag for user**: Credential/account items and anything ambiguous.

---

## Step 4 — Write audit artifact

Write a JSON file to `audit_log/` in the repo root:

```json
{
  "skill": "update-human-tasks",
  "timestamp": "<ISO 8601>",
  "checked_off": [
    { "file": "<filename>", "item": "<item text>", "evidence": "<one line>" }
  ],
  "added": [
    { "file": "<filename>", "item": "<new item text>" }
  ],
  "flags": [
    { "file": "<filename>", "item": "<item text>", "reason": "<why flagged>" }
  ]
}
```

File name: `audit_log/update-human-tasks-<timestamp>.json`

Create the `audit_log/` directory if it doesn't exist.

---

## Step 5 — Return findings

Output the findings as a structured block for the caller to read:

```
## Human-Tasks Audit
- **Checked off**: [items verified done by codebase evidence]
- **Added**: [new items discovered from codebase]
- **Needs human review**: [items requiring human verification]
- **Skipped**: (if no human-tasks directory)
```

---

## Edge cases

- **No human-tasks directory**: Output "No human-tasks directory found" and stop.
- **All items already done**: Note it, write empty audit artifact.
- **Ambiguity**: Flag for the user. Don't check off items unless codebase evidence is clear.
