---
name: update-claude-md
description: Audit and update CLAUDE.md against the actual codebase state. Corrects stale info, adds missing info, and culls dead info. Returns structured findings and writes an audit artifact.
---

# Update CLAUDE.md

Audit the project's `CLAUDE.md` against the actual codebase. Make direct edits where confident; flag ambiguous items for the user.

---

## Step 1 — Snapshot the codebase state

Gather ground truth before auditing. Run these in parallel:

1. **Directory structure** — Glob to map top-level and key nested directories:
   ```
   Glob: src/**/*
   Glob: specs/*
   Glob: human-tasks/*
   ```

2. **Schema files** — Read all files in the DB schema directory (e.g. `src/lib/db/schema/`) to know every table/model.

3. **Environment variables** — Read the env validation file (e.g. `src/lib/config.ts`) and `.env.example` to get the canonical list of env vars.

4. **Package.json scripts** — Read `package.json` to get the actual `scripts` block and `dependencies`/`devDependencies`.

5. **API routes** — Glob for route files (`src/app/api/**/route.ts`) to know every endpoint.

6. **Middleware / auth** — Read middleware or proxy files to understand route protection.

7. **Recent git history** — Run `git log --oneline -30` to see what's been built recently.

---

## Step 2 — Audit CLAUDE.md

Read the project's `CLAUDE.md` (repo root). Compare every claim against the Step 1 snapshot.

### 2a — Project Overview
- Does the "Currently implements Specs X-Y" claim match reality? Check which specs have corresponding code.
- Does the technology list match `package.json`?

### 2b — Common Commands
- Does every listed command exist in `package.json` scripts?
- Are there important scripts missing from the list?
- Is "No test framework is configured yet" still true? Check for vitest, jest, or similar.

### 2c — Architecture sections
For each subsection (Route Groups, API Pattern, Database, Storage, Auth, etc.):
- **Schema listing**: Compare listed files against actual files in the schema directory. Add missing ones.
- **Route groups**: Compare listed groups against actual `src/app/` directory structure.
- **Directories mentioned**: Verify paths still exist and aren't stale.
- **Patterns described**: Check if new patterns have emerged.

### 2d — Environment
- Compare listed env vars against the actual validation schema. Add missing required vars, remove deleted ones.

### 2e — Missing sections
Look for important new directories or patterns not covered anywhere in CLAUDE.md:
- New `src/lib/` modules (AI, hooks, services)
- New `src/hooks/` custom hooks
- New infrastructure (queue, cache, external API clients)

### Actions
- **Edit directly**: Factual corrections (file lists, env vars, spec numbers, command names).
- **Flag for user**: Subjective descriptions, architectural philosophy, or anything ambiguous.

Use the Edit tool to update CLAUDE.md. Keep the existing style and structure.

---

## Step 3 — Write audit artifact

Write a JSON file to `audit_log/` in the repo root:

```json
{
  "skill": "update-claude-md",
  "timestamp": "<ISO 8601>",
  "findings": [
    { "section": "<section name>", "action": "updated|flagged|no_change", "detail": "<one line>" }
  ],
  "flags": [
    "<anything requiring human review>"
  ]
}
```

File name: `audit_log/update-claude-md-<timestamp>.json`

Create the `audit_log/` directory if it doesn't exist.

---

## Step 4 — Return findings

Output the findings as a structured block for the caller to read:

```
## CLAUDE.md Audit
- **Updated**: [list each change, one line each]
- **Needs human review**: [anything ambiguous or credential-related]
```

---

## Edge cases

- **No CLAUDE.md**: Tell the user there's no CLAUDE.md and offer to create one.
- **No schema directory**: Skip schema file checks, note it in findings.
- **Large codebase**: Focus on sections already in CLAUDE.md; don't audit what isn't there.
- **Ambiguity**: Flag for the user rather than making a wrong edit. Accuracy over completeness.
