# Stage Four Cert — Project Guide

## Overview

A minimal Node.js/Express API demonstrating JWT authentication and user management. Built with TypeScript.

**Stack**: Express, TypeScript, dotenv, jsonwebtoken

## Common Commands

| Command | Description |
|---------|-------------|
| `npm start` | Start the server (ts-node) |
| `npm test` | No test runner configured yet |

## Architecture

### API Routes

| Route | Auth | Description |
|-------|------|-------------|
| `GET /api/users` | Required | List all users |
| `GET /api/users/:id` | Required | Get a single user |

### Authentication

JWT-based. All routes require a Bearer token except those in the `PUBLIC_PATHS` list in `src/auth.ts`. Token is verified against `JWT_SECRET`.

### Directory Structure

```
src/
  index.ts          — Express app entry point
  auth.ts           — JWT middleware
  app/api/
    users/
      route.ts      — GET /api/users, GET /api/users/:id
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `JWT_SECRET` | Yes | Secret for signing/verifying JWTs |
| `API_KEY` | Yes | External API key |
| `PORT` | No | Server port (default: 3000) |

## Evaluation

Promotion evals live at `evals/promotion/` and are run with `coe promote` from the repo root. Results land in `evals/promotion/results/`.

Runtime evals live at `evals/runtime/<skill-name>.yml`. The `PostToolUse` hook in `.claude/settings.json` fires `coe runtime-check --from-hook` after every Skill tool call, grades the live output, and feeds structured feedback back to Claude on failure (up to 3 retries before human escalation). Test manually with:

```bash
coe runtime-check --skill <name>
```

The runtime hook is skipped automatically during `coe promote` runs (`COE_MODE=promotion`).

## Open Issues

Tracked in beads (`.beads/`). Current open issues:
- `stage-four-cert-k0w` — Add health check endpoint
- `stage-four-cert-5bs` — Add in-memory caching layer (in progress)
- `stage-four-cert-3ey` — Set up log aggregation (blocked by caching)
