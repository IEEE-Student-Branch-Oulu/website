# IEEE SB Oulu — Website

Monorepo for the IEEE Student Branch Oulu website. The frontend is a Nuxt 4 / Vue 3 SPA; the backend is a Python service (in progress). Git quality gates are enforced at the repo root via Husky + commitlint + pre-commit.

---

## Repository layout

```
website-main/
├── frontend/          # Nuxt 4 app (Vue 3, Tailwind CSS, TypeScript)
├── backend/           # FastAPI + PostgreSQL service — see backend/README.md
├── docs/adr/          # Architecture Decision Records (the "why" behind choices)
├── .husky/            # Git hooks (pre-commit, commit-msg, pre-push)
├── .pre-commit-config.yaml
├── commitlint.config.mjs
└── package.json       # Root — only husky + commitlint live here
```

Stack-specific quick-starts: [`frontend/`](./frontend/) and [`backend/README.md`](./backend/README.md).
Decision records: [`docs/adr/`](./docs/adr/).

---

## Prerequisites

| Tool | Minimum version | Purpose |
|------|----------------|---------|
| **Node.js** | 20 LTS | Frontend + root tooling |
| **npm** | 10+ (ships with Node 20) | Package management |
| **Python** | 3.11+ | Backend + pre-commit runtime |
| **pip** | any recent | Installing pre-commit |
| **pre-commit** | 3.x | File-level hooks (ESLint, Prettier, Ruff, gitleaks…) |
| **git** | 2.x | Required by Husky hooks |

Install pre-commit (if not already present):

```bash
pip install pre-commit
# or, if you use pipx:
pipx install pre-commit
```

---

## First-time setup

Run every step in order. Steps 1–2 install the root tooling; steps 3–4 set up the frontend; step 5 wires up all git hooks.

### 1. Install root dependencies (Husky + commitlint)

From the repo root:

```bash
npm install
```

This also runs `husky` automatically via the `prepare` script, which creates the `.husky/_/` bootstrap files.

### 2. Install pre-commit hooks

```bash
pre-commit install
```

This registers the hooks defined in `.pre-commit-config.yaml` into `.git/hooks/`. You only need to do this once per clone.

### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

`npm install` triggers a `postinstall` script that runs `nuxt prepare`, which generates `.nuxt/` (type declarations, ESLint config, etc.). **Do not skip this** — TypeScript and ESLint both depend on generated files in `.nuxt/`.

### 4. Install Playwright browsers (for e2e tests)

```bash
cd frontend
npx playwright install --with-deps chromium
```

This downloads the Chromium binary that Playwright uses. Only Chromium is configured; `--with-deps` installs the required system libraries on Linux.

### 5. Verify the hook chain

Make a trivial commit from the root to confirm everything is wired up:

```bash
git add .
git commit -m "chore: verify hook setup"
```

You should see the hooks run in sequence (see the [Git hooks](#git-hooks) section for what each one does). If any hook fails, fix the reported issue before continuing.

---

## Running the frontend locally

```bash
cd frontend
npm run dev
```

The dev server starts at **http://localhost:3000** with Nuxt Devtools enabled. Hot module replacement is active — no manual restarts needed for `.vue`, `.ts`, or `.css` changes.

Other useful commands:

```bash
npm run build          # Production build (outputs to .output/)
npm run preview        # Preview the production build locally
npm run typecheck      # Run vue-tsc for a full TypeScript check
```

---

## Linting and formatting

All linting and formatting is run automatically on staged files at commit time (see [Git hooks](#git-hooks)), but you can run them manually at any time:

```bash
# From frontend/
npm run lint           # ESLint — report only
npm run lint:fix       # ESLint — auto-fix
npm run format         # Prettier — write all files
npm run format:check   # Prettier — report only (used in CI)
```

**ESLint** is configured via `frontend/eslint.config.mjs`, which extends the auto-generated Nuxt ESLint config (`.nuxt/eslint.config.mjs`). Stylistic rules are disabled in favour of Prettier.

**Prettier** options (`frontend/.prettierrc`):
- No semicolons
- Single quotes
- 2-space indent
- Trailing commas (ES5)
- 100-character print width
- `prettier-plugin-tailwindcss` sorts Tailwind class names automatically

---

## Testing

### Unit tests (Vitest)

```bash
cd frontend
npm run test            # Watch mode
npm run test:run        # Single run (used by pre-commit hook)
npm run test:coverage   # Run with v8 coverage report
```

Tests live in `frontend/tests/unit/`. The Vitest environment is set to `nuxt` with `happy-dom`, so Vue components render correctly without a real browser. Coverage thresholds are enforced at **70% lines / 70% functions** — the run fails if you drop below.

### End-to-end tests (Playwright)

```bash
cd frontend
npm run test:e2e        # Headless Chromium
npm run test:e2e:ui     # Playwright UI (interactive, great for debugging)
```

Tests live in `frontend/tests/e2e/`. Playwright automatically starts the Nuxt dev server on port 3000 before running tests (configured in `playwright.config.ts`). If you already have a dev server running, Playwright reuses it (this behaviour is disabled in CI).

---

## Git hooks

The project uses two separate but complementary hook systems that both run on `git commit`:

| System | Config | Scope |
|--------|--------|-------|
| **Husky** | `.husky/` | Orchestrates multi-step frontend checks and commitlint |
| **pre-commit** | `.pre-commit-config.yaml` | File-level checks on staged files |

### `pre-commit` hook (Husky)

Runs on every `git commit`. Steps in order:

1. `npm install` in `frontend/` — ensures deps are up to date
2. `lint-staged` — runs ESLint + Prettier on staged `.js/.ts/.vue` files and Prettier on staged `.json/.md/.css` files
3. `npm run typecheck` — full TypeScript check via `vue-tsc`
4. `npm run test:run` — all Vitest unit tests

If any step fails the commit is aborted.

### `commit-msg` hook (via pre-commit / Husky)

Runs `commitlint` to validate the commit message format. Messages must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <subject>
```

Allowed types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `style`, `ci`, `perf`

Rules:
- Subject must be **lower-case**
- Header line must be **≤ 72 characters**

Examples:

```
feat: add events listing page
fix: correct nav link on mobile
chore: update dependencies
```

### `pre-push` hook (Husky)

Runs before `git push`. Executes the full Playwright e2e suite:

```
npm --prefix frontend run test:e2e
```

This is slower than the pre-commit checks (~30–120 s depending on your machine). Push is blocked if any e2e test fails.

### pre-commit framework hooks (`.pre-commit-config.yaml`)

These run on staged files in parallel with (or just before) the Husky hooks, depending on your git version. They cover:

| Hook | What it checks |
|------|---------------|
| `trailing-whitespace` | No trailing spaces |
| `end-of-file-fixer` | Files end with a newline |
| `check-merge-conflict` | No leftover conflict markers |
| `check-yaml` / `check-json` / `check-toml` | Valid syntax |
| `check-added-large-files` | No files > 500 KB |
| `mixed-line-ending` | Forces LF line endings |
| `gitleaks` | Scans for secrets / credentials |
| `eslint` (local) | ESLint on staged frontend files |
| `prettier` (local) | Prettier on staged frontend files |
| `ruff` | Lints + auto-fixes staged Python files |
| `ruff-format` | Formats staged Python files |
| `mypy` | Static type-checks staged Python files |

To run all pre-commit hooks manually against every file in the repo:

```bash
pre-commit run --all-files
```

To run a single hook (e.g. gitleaks):

```bash
pre-commit run gitleaks --all-files
```

---

## Skipping hooks (emergency only)

If you genuinely need to bypass a hook for a one-off reason:

```bash
# Skip Husky hooks
HUSKY=0 git commit -m "..."

# Skip pre-commit framework hooks
git commit --no-verify -m "..."
```

Avoid doing this on the `main` branch. Both hooks exist for good reasons and CI will catch anything that slips through locally.

---

## Editor setup

The project ships an `.editorconfig` at the root that sets indent style and line endings. Most editors pick this up automatically.

For VS Code, install the following extensions for the best experience:

- **Volar** (Vue - Official) — Vue 3 / Nuxt language support
- **ESLint** — in-editor linting
- **Prettier** — in-editor formatting (set as default formatter for `.vue`, `.ts`, `.js`)
- **Tailwind CSS IntelliSense** — class name autocomplete

Add to your VS Code workspace settings (`frontend/.vscode/settings.json` if you create one):

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

---

## Common issues

**`nuxt prepare` errors on `npm install`**
Delete `.nuxt/` and re-run `npm install` inside `frontend/`. The generated files can get stale after a Nuxt version bump.

**`pre-commit: command not found`**
Install pre-commit with `pip install pre-commit` and re-run `pre-commit install`.

**Playwright fails with "browser not found"**
Run `npx playwright install --with-deps chromium` from `frontend/`.

**commitlint rejects your message**
Check that your message starts with one of the allowed types (`feat:`, `fix:`, etc.) and that the subject is lower-case with no trailing period.

**`gitleaks` blocks a commit**
A secret or credential was detected in a staged file. Remove it, rotate the credential if it was real, and recommit. If it is a false positive, add an inline `gitleaks:allow` comment or a `.gitleaksignore` entry.
