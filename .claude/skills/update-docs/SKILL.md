---
name: update-docs
description: Audit and update CLAUDE.md, beads issues, and human-tasks against the actual codebase state. Coordinates the update-claude-md, update-beads, and update-human-tasks skills in sequence and aggregates findings into an audit log.
---

# Update Docs

Coordinate a full documentation audit across CLAUDE.md, beads issues, and human-tasks checklists. This skill orchestrates three sub-skills in sequence and aggregates their results.

> **Non-interactive shell rule**: every `bd` command must be prefixed with `source ~/.zshrc &&` so `BEADS_DIR` is set.

---

## Step 1 — Snapshot the codebase state

Gather ground truth before invoking sub-skills. Run these in parallel:

1. **Directory structure** — Glob `src/**/*`, `specs/*`, `human-tasks/*`
2. **Package.json** — Read `package.json` for scripts and dependencies
3. **API routes** — Glob `src/app/api/**/route.ts`
4. **Environment vars** — Read `.env.example` and any env validation file
5. **Recent git history** — `git log --oneline -30`

This snapshot is available as shared context for interpreting sub-skill output.

---

## Step 2 — Run update-claude-md

Read `~/.claude/skills/update-claude-md/SKILL.md` and execute every step in it using `read_file`, `write_file`, `run_command`, and `list_directory`. Do not use the Skill tool. Complete all steps through writing the audit artifact before proceeding.

Capture its structured findings for Step 5.

---

## Step 3 — Run update-beads

Read `~/.claude/skills/update-beads/SKILL.md` and execute every step in it using `read_file`, `write_file`, `run_command`, and `list_directory`. Do not use the Skill tool. Complete all steps — including running `bd close` for each confirmed issue and writing the audit artifact — before proceeding.

Capture its structured findings for Step 5.

---

## Step 4 — Run update-human-tasks

Read `~/.claude/skills/update-human-tasks/SKILL.md` and execute every step in it using `read_file`, `write_file`, `run_command`, and `list_directory`. Do not use the Skill tool. Complete all steps through writing the audit artifact before proceeding.

Capture its structured findings for Step 5.

---

## Step 5 — Aggregate findings and write audit log

Read the three JSON artifacts written by the sub-skills from `audit_log/`. Append a single aggregated entry to `audit_log.jsonl` in the repo root:

```json
{
  "run_id": "<UUID or timestamp>",
  "timestamp": "<ISO 8601>",
  "skills_invoked": ["update-claude-md", "update-beads", "update-human-tasks"],
  "claude_md": { "<contents of update-claude-md artifact>" },
  "beads": { "<contents of update-beads artifact>" },
  "human_tasks": { "<contents of update-human-tasks artifact>" }
}
```

Create `audit_log.jsonl` if it doesn't exist. Append (don't overwrite) so successive runs accumulate.

---

## Step 6 — Present findings

Output a structured summary combining all three sub-skill outputs. Use these section headers verbatim — the `## Beads Audit` block must appear exactly as shown:

```
## Documentation Audit Summary

### CLAUDE.md
- **Updated**: [list each change made, one line each]
- **Needs human review**: [anything ambiguous]

---

## Beads Audit

**Closed**
- [issue ID — title: one-line rationale, or `- none`]

**Flagged**
- [issue ID — title: reason, or `- none`]

**Orphaned work**
- [recent commit with no open issue, or `- none`]

Audit written to: audit_log/update-beads-<timestamp>.json

---

### Human-Tasks
- **Updated**: [items checked off or added]
- **Needs human review**: [items requiring human verification]
- **Skipped**: (if no human-tasks directory)
```

Keep it concise. Don't repeat full issue descriptions — just IDs, titles, and one-line rationale.

---

## Edge cases

- **A sub-skill fails**: Note the failure in the summary. Continue with the remaining sub-skills rather than halting.
- **No CLAUDE.md**: The update-claude-md skill handles this and will report it.
- **No open beads issues**: The update-beads skill handles this and will report it.
- **No human-tasks directory**: The update-human-tasks skill handles this and will report it.
