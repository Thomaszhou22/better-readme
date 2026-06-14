# README Templates

Five project types, each optimized for its audience.

---

## Template 1: Library / SDK

```markdown
# 📦 {Name}

{One-line description — what it does, not what it IS}

[![npm version](badge)](link) [![License](badge)](link) [![CI](badge)](link)

## Why

{2-3 sentences: what pain does this solve? Who is it for?}

## Install

```bash
npm install {name}
# or
pip install {name}
```

## Quick Start

```{lang}
import {name} from '{name}'

const result = {name}.doThing()
console.log(result)
```

## Features

- ✅ Feature one — short description
- ✅ Feature two — short description
- ✅ Feature three — short description

## API

### `doThing(options)`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `foo` | `string` | `''` | Does foo |

Returns: `Promise<Result>`

## Examples

- [Basic usage](examples/basic.ts)
- [Advanced](examples/advanced.ts)

## Compatibility

- Node.js 18+
- TypeScript 5+

## Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT © {Year} {Author}
```

---

## Template 2: CLI Tool

```markdown
# 🔧 {Name}

{One-line description}

![Demo]({demo.gif})

## Install

```bash
npm install -g {name}
# or
brew install {name}
```

## Usage

```bash
{name} --flag value
```

### Commands

| Command | Description |
|---------|-------------|
| `init` | Set up configuration |
| `run` | Execute the main task |
| `status` | Show current status |

## Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | `./out` | Output directory |
| `--verbose` | `-v` | `false` | Verbose logging |

## Examples

```bash
# Basic usage
{name} run -o ./results

# With config file
{name} run --config .myconfig.json
```

## Configuration

{Brief config explanation or link to docs}

## Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT © {Year} {Author}
```

---

## Template 3: App / Product

```markdown
# {Name} 🚀

{One-line tagline}

![{App Screenshot}]({screenshot.png})

**[Live Demo](demo-url)** • **[Documentation](docs-url)**

## The Problem

{2-4 sentences: What pain exists? Why did you build this?}

## Features

🎯 **Feature One** — How it helps

📊 **Feature Two** — How it helps

🔗 **Feature Three** — How it helps

## Quick Start

```bash
git clone https://github.com/{user}/{repo}.git
cd {repo}
npm install
npm run dev
```

Open `http://localhost:5173` 🎉

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Tailwind |
| Backend | Supabase |
| Deploy | Vercel |

## Roadmap

- [x] Core feature
- [ ] Next feature
- [ ] Future feature

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT © {Year} {Author}
```

---

## Template 4: Agent Skill

```markdown
# 🧩 {Name}

{One-line description}

## Install

```bash
clawhub install {slug}
# or
cp -r {name}/ ~/.openclaw/skills/
```

## What It Does

{2-3 sentences on what the skill handles for the agent}

## How It Triggers

The skill activates when:
- User says: "{trigger phrase 1}"
- User says: "{trigger phrase 2}"
- Context matches: {scenario}

## Workflow

1. **Step 1** — What happens first
2. **Step 2** — What happens next
3. **Step 3** — Final output

## Compatibility

- ✅ OpenClaw
- ✅ Claude Code
- ✅ Cursor / Codex CLI / Gemini CLI

## Configuration

{Any config options, or "Zero configuration — works out of the box."}

## Files

```
{name}/
├── SKILL.md          # Trigger + workflow
├── scripts/          # Automation
└── references/       # Patterns / templates
```

## License

MIT © {Year} {Author}
```

---

## Template 5: Data / Resource

```markdown
# 📊 {Name}

{One-line description}

![Stats]({stats-badge.png})

## What's Inside

- **{N}** records
- **{N}** fields per record
- Updated {frequency}

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `name` | string | Display name |
| `value` | number | Metric value |

## Sample

```json
{
  "id": "001",
  "name": "Example",
  "value": 42
}
```

## Download

- [CSV]({link})
- [JSON]({link})
- [Parquet]({link})

## Usage

```python
import pandas as pd
df = pd.read_csv('{name}.csv')
```

## License

{License} © {Year} {Author}
```

---

## Common Elements (All Templates)

### Language Toggle (top of file)

```markdown
**English** | **[中文](README.zh-CN.md)**
```

### Badge URLs

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![npm version](https://img.shields.io/npm/v/{name}.svg)](https://npmjs.com/package/{name})
[![CI](https://github.com/{user}/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/{user}/{repo}/actions)
```

### "Why" Section Formula

> {Target user} struggles with {pain point}. {Existing solutions} are {gap}.
> {Name} solves this by {approach}.

### Feature Bullet Formula

> **{Emoji} {Feature name}** — {Benefit}, not just {technical description}
