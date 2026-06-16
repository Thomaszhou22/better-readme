---
name: better-readme
version: 1.1.0
description: "Use when the user asks to create, improve, fix, or audit a README.md file, score their README, document an open source project, or set up new project docs. Provides 8-dimension 0-100 quality scoring, 5-type template matrix (Library, CLI, App, Skill, Data), and pre-publish checklist. Do NOT use for API docs, wikis, inline code comments, or general technical writing."
---

# Better README

Create, audit, and optimize project README files with **8-dimension quality scoring (0–100)**, 5-type template matching (Library, CLI, App, Skill, Data), and pre-publish readiness checks.

**Key differentiator:** The 0–100 audit score evaluates READMEs across 8 dimensions — first impression, problem statement, quick start, visual demo, feature clarity, API docs, badges, and community. Nothing else on ClawHub does this.

## Activation Triggers

- "write/improve/fix my README"
- "create a README for this project"
- "score/check my README"
- "my README is bad"
- "I need a README template"
- "document my open source project"
- Setting up a new open-source project
- Preparing a GitHub launch

## Workflow

### Phase 0: Onboarding (first use only)

When this skill is activated for the first time (no prior onboarding record):

1. Briefly introduce what this skill can do (score, improve, create READMEs)
2. Ask the user: _"Want me to evaluate the READMEs of your existing repos?"_
3. If yes:
   - Fetch the user's public GitHub repo list
   - Let the user pick which repos to evaluate (or evaluate all)
   - Run Phase 2 (Score) on each selected repo's README
   - Summarize scores and highlight the weakest ones
   - Offer to improve the lowest-scoring READMEs
4. If no, skip ahead to the normal workflow
5. Record that onboarding is complete (do not repeat)

### Phase 1: Classify

Identify the project type by scanning the codebase:

| Signal | Project Type |
|--------|-------------|
| `package.json` with `main`/`exports`, no UI | **Library/SDK** |
| `bin/` field, CLI framework (commander, click, clap) | **CLI Tool** |
| React/Vue/HTML, deploy target (Vercel/Netlify) | **App/Product** |
| `SKILL.md` exists, `skills/` directory | **Agent Skill** |
| `.csv`/`.json`/`.parquet` dataset, no src/ | **Data/Resource** |

If ambiguous, ask the user.

### Phase 2: Score (if README exists)

Run the audit script:

```bash
python3 scripts/readme_audit.py --path /path/to/README.md
```

This produces a 0–100 score across 8 dimensions. See `references/scoring-rubric.md` for criteria.

If score < 70, recommend a full rewrite using the appropriate template.

### Phase 3: Generate

1. Load the matching template from `references/templates.md`
2. Scan the project for real data:
   - Project name, description from `package.json` / `pyproject.toml` / `Cargo.toml`
   - Install command (detect package manager)
   - License file
   - Key features (scan source for main entry points)
   - Badge URLs (CI, coverage, npm/PyPI)
3. Fill the template with real data
4. Generate `README.md` in **English** by default
5. Print a preview for the user to review
6. Ask the user if they need additional language versions (e.g., Chinese)

### Phase 4: Pre-Publish Checklist

Run through `references/pre-publish-checklist.md` and report:

- ✅ Passed items
- ⚠️ Warnings (nice to have)
- ❌ Missing critical items

## Template Selection Guide

| Type | Hero | Focus | Install |
|------|------|-------|---------|
| **Library/SDK** | Code snippet | API reference | `npm install` / `pip install` |
| **CLI Tool** | Demo GIF/terminal | Commands table | `brew install` / `cargo install` |
| **App/Product** | Screenshot/hero image | Features + live demo | Deploy button |
| **Agent Skill** | What it triggers on | Workflow + compatibility | `clawhub install` |
| **Data/Resource** | Stats card | Schema + sample data | Direct download |

## Quality Standards (Non-Negotiable)

1. **30-second rule**: User must understand what this does after one scroll
2. **≤3 install steps**: If setup needs 10 steps, nobody finishes
3. **Real examples**: Not `your-api-key-here` — actual working snippets
4. **No dead links**: Every link must resolve
5. **Mobile readable**: No wide tables without horizontal scroll handling

## Scoring Dimensions

| Dimension | Max Points | Quick Check |
|-----------|-----------|-------------|
| First impression (hero/title/tagline) | 15 | H1 + one-line description in first 5 lines |
| Problem statement | 10 | "Why" section explaining what pain this solves |
| Quick start | 20 | Install + run in ≤3 commands |
| Visual demo | 10 | Screenshot, GIF, or video present |
| Feature clarity | 10 | Feature list or "what it does" section |
| API/Usage docs | 10 | Code examples for main use cases |
| Badges & metadata | 5 | License, version, CI status |
| Community & links | 10 | Contributing guide, link to issues, discussions |
| Pre-publish readiness | 10 | Topics, description, social preview configured |

See `references/scoring-rubric.md` for full criteria.

## Language Support

Default to generating an **English-only** README.

After generation, ask the user: _"Do you need a README in another language (e.g., Chinese, Japanese, etc.)?"_

Only generate additional language versions if the user requests it. Keep each language version in a separate file (e.g., `README.zh-CN.md`) with a language toggle at the top:

```markdown
**English** | **[中文](README.zh-CN.md)**
```

## Audit Script Usage

```bash
# Score a single README
python3 scripts/readme_audit.py --path ./README.md

# Score and output JSON
python3 scripts/readme_audit.py --path ./README.md --json

# Recommend a template type based on project structure
python3 scripts/readme_audit.py --detect /path/to/project
```
