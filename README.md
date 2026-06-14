# 📝 Better README

**English** | **[中文](README.zh-CN.md)**

Audit, generate, and optimize project README files with quality scoring, template matching, and multilingual support. Works with any project type — libraries, CLI tools, web apps, agent skills, and datasets.

**The problem:** Most README files are written as an afterthought. No "why" section, no visual demo, 10-step setup guides nobody finishes. Better README fixes this — score your existing README, get a template tailored to your project type, and generate bilingual docs in one pass.

## Install

```bash
# ClawHub
clawhub install better-readme

# Or from source
git clone https://github.com/Thomaszhou22/better-readme.git
cp -r better-readme ~/.openclaw/skills/
```

Requires Python 3.8+. No other dependencies.

## Quick Start

```bash
# Score your existing README
python3 scripts/readme_audit.py --path ./README.md

# Detect project type (recommends a template)
python3 scripts/readme_audit.py --detect /path/to/project

# JSON output for CI/CD
python3 scripts/readme_audit.py --path ./README.md --json
```

Or just tell your AI agent: **"Check my README"** — it'll handle the rest.

## How It Works

```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
  │  1. Classify │────▶│  2. Score    │────▶│  3. Generate     │
  │  What type?  │     │  How good?   │     │  Fix + bilingual │
  └──────────────┘     └──────────────┘     └──────────────────┘
         ▲                                         │
         │        Agent fills template             │
         └─────────────────────────────────────────┘
                   Re-score to verify
```

### Step 1: Classify

Automatically detects your project type:

| Signal | Type | Template |
|--------|------|----------|
| `main`/`exports` in package.json | Library/SDK | API-first |
| `bin` field, CLI framework | CLI Tool | Demo-first |
| React/Vue + deploy target | App/Product | Screenshot-first |
| `SKILL.md` exists | Agent Skill | Trigger-first |
| `.csv`/`.json` dataset | Data/Resource | Schema-first |

### Step 2: Score

9-dimension scoring (100 points):

| Dimension | Max | What it checks |
|-----------|-----|----------------|
| First impression | 15 | H1 + tagline + visual in first 10 lines |
| Problem statement | 10 | "Why" section explaining the pain |
| Quick start | 20 | Install + run in ≤3 commands |
| Visual demo | 10 | Screenshot, GIF, or video |
| Feature clarity | 10 | Scannable feature list/table |
| Usage / API docs | 10 | 2+ code examples |
| Badges & metadata | 5 | License, version, CI badges |
| Community & links | 10 | Contributing, Issues, Discussions |
| Pre-publish readiness | 10 | TOC, roadmap, changelog |

### Step 3: Generate

- Pick the matching template from `references/templates.md`
- Scan your project for real data (name, install command, license, features)
- Fill the template — no placeholder text
- Generate both `README.md` (English) and `README.zh-CN.md` (Chinese)
- Language toggle at the top

### Step 4: Pre-Publish Checklist

Run through `references/pre-publish-checklist.md`:

- 🔴 **Critical**: README, install, license, GitHub About, topics
- 🟡 **Important**: Screenshot, "Why" section, contributing, issues template
- 🟢 **Nice to have**: Badges, changelog, discussions, funding

## Template Types

| Type | Hero Element | Focus | Install Example |
|------|-------------|-------|-----------------|
| 📦 Library/SDK | Code snippet | API + examples | `npm install` |
| 🔧 CLI Tool | Demo GIF | Commands table | `brew install` |
| 🚀 App/Product | Screenshot | Features + live demo | Deploy button |
| 🧩 Agent Skill | Trigger condition | Workflow + compat | `clawhub install` |
| 📊 Data/Resource | Stats card | Schema + sample | Direct download |

## Agent Integration

Tell your agent any of these:
- *"Write a README for this project"*
- *"Score my README"*
- *"My README sucks, fix it"*

The agent will:
1. Detect project type
2. Run the audit script
3. Load the matching template
4. Scan your codebase for real data
5. Generate bilingual READMEs
6. Run the pre-publish checklist

## Files

```
better-readme/
├── SKILL.md                          # Trigger conditions + workflow
├── scripts/
│   └── readme_audit.py               # README scorer + project detector
├── references/
│   ├── templates.md                  # 5 project-type templates
│   ├── scoring-rubric.md             # Full scoring criteria
│   └── pre-publish-checklist.md      # GitHub launch checklist
└── README.md
```

## Compatibility

- ✅ OpenClaw
- ✅ Claude Code
- ✅ Cursor / Codex CLI / Gemini CLI
- ✅ Any platform using SKILL.md format

## License

MIT © 2026 Thomas Zhou
