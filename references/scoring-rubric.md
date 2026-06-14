# Scoring Rubric (v3 — Dual-Track: Skill Repos + General Projects)

> Benchmarked against:
> **General high-star repos:** freeCodeCamp (400k⭐), Oh My Zsh (175k⭐), shadcn/ui (75k⭐), VS Code (170k⭐)
> **High-star skill repos:** alirezarezvani/claude-skills (5.2k⭐), openclaw/agent-skills, agent-skills-hub (790+ skills), pskoett/self-improving (461k installs), steipete/github (190k installs)
> **Official spec:** openclaw/skill-creator (the authoritative SKILL.md standard)

---

## Critical Insight: Two Different Worlds

Skill repositories have different README conventions than general projects:

| Aspect | General Projects | Skill Repositories |
|--------|-----------------|-------------------|
| Audience | End users / developers | AI agents + developers |
| Key file | README.md | SKILL.md (README is secondary) |
| Install | npm / curl / brew | `clawhub install` / git clone + symlink |
| Social proof | Stars / Discord | Installs / stars on ClawHub |
| Hero visual | Logo / screenshot | Optional (SKILL.md frontmatter matters more) |
| Best README reference | Oh My Zsh, shadcn | alirezarezvani/claude-skills, agent-skills-hub |

**The audit auto-detects which track to use.**

---

## Track A: Skill Repository README (100 pts)

For repos that contain SKILL.md files or are agent skill collections.

### 1. Clear Scope & Skill Count (18 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 18 | States exactly how many skills + what domains covered | alirezarezvani: "345 production-ready skills...engineering, DevOps, marketing, compliance" |
| 12 | Lists skills or categories but no count | openclaw/agent-skills: lists 5 skills with descriptions |
| 6 | Vague description of what's included | |
| 0 | No indication of what skills are in the repo | |

**Why 18 pts:** The #1 thing a skill repo visitor needs to know is "what's in here and how much?"

### 2. Platform Compatibility (15 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 15 | Explicitly lists which agent platforms are supported | alirezarezvani: "Claude Code · Codex · Gemini CLI · OpenClaw · Cursor · 9 more" |
| 10 | Mentions platform support but not exhaustive | agent-skills-hub: "Claude Code, Gemini, Cursor, Kiro, Codex..." |
| 5 | Implies single-platform only | |
| 0 | No platform info | |

**Why 15 pts:** Skill compatibility determines if the visitor can actually use it. This is unique to skill repos.

### 3. Quick Install (20 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 20 | Single copy-paste command (`clawhub install`, `npx`, one-liner) | agent-skills-hub: `npx agent-skills-hub --claude`; `clawhub install X` |
| 15 | 2-3 clear steps (clone + install script) | openclaw/agent-skills: `git clone ... && scripts/install-skills` |
| 10 | Clone instructions only, no automated installer | |
| 5 | Partial, requires reading docs | |
| 0 | No install instructions | |

**Why 20 pts:** Same as general projects — if they can't try it in 60 seconds, they bounce.

### 4. Skill Catalog / Index (15 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 15 | Full table or list of skills with names + one-line descriptions | alirezarezvani: full category breakdown; openclaw/agent-skills: bulleted list with descriptions |
| 10 | Partial list or only category headers | |
| 5 | Mention of skills but no catalog | |
| 0 | No indication of individual skills | |

**Why 15 pts:** Skill repos with catalogs get 3x more installs (ClawHub data pattern).

### 5. Structure & ToC (10 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 10 | Clear ToC (collapsible or inline) + logical section headers | agent-skills-hub: full `<details>` ToC; alirezarezvani: category headers |
| 6 | Clear sections (`##`) but no ToC | |
| 3 | Minimal structure | |
| 0 | Wall of text | |

### 6. Usage Example (12 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 12 | Code example showing a skill being activated/used + expected output | alirezarezvani: `> activate_skill(name="senior-architect")` |
| 8 | Install + activate steps but no output shown | |
| 4 | Inline code only | |
| 0 | No usage example | |

**Why 12 pts:** For skill repos, "how do I actually trigger this?" is the #2 question after "what's in here?"

### 7. Badges & Metadata (5 pts)

| Score | Criteria |
|-------|----------|
| 5 | 2+ badges (license, version, star count, skill count, CI) |
| 3 | 1 badge |
| 0 | No badges |

**Why only 5 pts:** openclaw/agent-skills has zero badges and is the official repo. Badges matter less for skills.

### 8. Contributing & Community (5 pts)

| Score | Criteria |
|-------|----------|
| 5 | Contributing guide + issues link + author info |
| 3 | Issues link or contributing guide |
| 0 | No community section |

**Why only 5 pts:** Skill repos are often solo-maintained. Community matters but isn't a dealbreaker.

---

## Track B: General Project README (100 pts)

For libraries, CLI tools, apps, and non-skill projects.

### 1. Hero Visual (18 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 18 | Logo/banner/screenshot as the FIRST element | freeCodeCamp, Oh My Zsh, shadcn/ui |
| 12 | Image present but below the fold | |
| 6 | ASCII art or table-only | |
| 0 | Pure text | |

### 2. Tagline & Personality (12 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 12 | H1 + memorable one-liner with personality | Oh My Zsh: "will not make you a 10x developer...but you may feel like one" |
| 8 | H1 + functional description | shadcn: "Start here then make it your own" |
| 4 | H1 only or vague | |
| 0 | No title | |

### 3. Quick Start (20 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 20 | Single copy-paste command to install + run | Oh My Zsh: `sh -c "$(curl ...)"` |
| 15 | ≤3 steps, clearly marked | |
| 10 | 4-6 steps | |
| 5 | Partial setup | |
| 0 | No install section | |

### 4. Problem & Value Proposition (12 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 12 | Clear who/what/why + proof of scale | freeCodeCamp: "helped 100,000+ people get first dev job" |
| 8 | Value stated, audience implied | |
| 4 | Feature dump, no context | |
| 0 | Jumps to install with zero context | |

### 5. Table of Contents & Structure (10 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 10 | Visible ToC (collapsible or inline) | freeCodeCamp: full ToC; Oh My Zsh: collapsible |
| 6 | Clear sections, no ToC | |
| 3 | Unstructured | |
| 0 | Wall of text | |

### 6. Social Proof & Community (12 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 12 | Discord/chat + badges + contributor stats | Oh My Zsh: Discord + 5 social badges |
| 8 | Contributing guide + Issues link | |
| 4 | Issues link only | |
| 0 | No community section | |

### 7. Badges & Metadata (6 pts)

| Score | Criteria |
|-------|----------|
| 6 | 3+ badges (CI, license, Discord, downloads) |
| 4 | 1-2 badges |
| 0 | No badges |

### 8. Usage Examples (10 pts)

| Score | Criteria | Real Example |
|-------|----------|-------------|
| 10 | 2+ copy-paste code examples + link to docs | Anthropic Cookbook: recipe table |
| 7 | One basic example | |
| 3 | Inline code only | |
| 0 | No examples | |

---

## Grade Bands (Same for Both Tracks)

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | 🚀 Top-tier — matches best-in-class patterns |
| 80-89 | B | ✅ Great — minor polish needed |
| 70-79 | C | 🟡 Solid — a few key improvements will level it up |
| 50-69 | D | 🟠 Needs significant work |
| <50 | F | 🔴 Start from template |

---

## Benchmarked Scores (Real Data)

### Skill Repos
| Repo | Score | Grade | Notes |
|------|-------|-------|-------|
| alirezarezvani/claude-skills (5.2k⭐) | 85 | B | Excellent catalog, platform list, badges |
| agent-skills-hub (790+ skills) | 78 | C | Good ToC + badges, weak tagline |
| openclaw/agent-skills | 67 | D | Clean but too minimal — no badges, no community |

### General Projects
| Repo | Score | Grade | Notes |
|------|-------|-------|-------|
| Oh My Zsh (175k⭐) | 92 | A | Gold standard for personality + one-liner install |
| freeCodeCamp (400k⭐) | 88 | B | Strong ToC + stats, could use more personality |
| shadcn/ui (75k⭐) | 72 | C | Minimal but effective — proves minimalism works IF essentials are perfect |
