#!/usr/bin/env python3
"""
Better README — Audit Script v3
Dual-track scoring: auto-detects Skill Repository vs General Project.
Benchmarked against real high-star repos in both categories.

Usage:
  python3 readme_audit.py --path ./README.md
  python3 readme_audit.py --path ./README.md --json
  python3 readme_audit.py --path ./README.md --track skill
  python3 readme_audit.py --path ./README.md --track general
  python3 readme_audit.py --detect /path/to/project
"""

import argparse
import json
import os
import re
import sys


# ═══════════════════════════════════════════════════════════════
# Track Detection
# ═══════════════════════════════════════════════════════════════

def detect_track(content, project_dir=None):
    """Auto-detect: is this a skill repository or a general project?"""
    skill_signals = 0

    # Content signals
    lower = content.lower()
    if 'skill' in lower and ('sk.md' in lower or 'skill.md' in lower or 'SKILL.md' in content):
        skill_signals += 3
    if 'clawhub' in lower:
        skill_signals += 2
    if 'agent skill' in lower or 'agent-skills' in lower or 'agentskills' in lower:
        skill_signals += 2
    if 'activate_skill' in lower or 'install-skills' in lower:
        skill_signals += 2
    if re.search(r'\bclaude code\b|\bcodex\b|\bgemini cli\b|\bopenclaw\b|\bcursor\b.*agent', lower):
        skill_signals += 1

    # Directory signals
    if project_dir and os.path.isdir(project_dir):
        files = set(os.listdir(project_dir))
        if 'SKILL.md' in files:
            skill_signals += 5
        if any('skill' in f.lower() for f in files):
            skill_signals += 1

    return 'skill' if skill_signals >= 3 else 'general'


# ═══════════════════════════════════════════════════════════════
# Shared Helpers
# ═══════════════════════════════════════════════════════════════

def parse_sections(content):
    """Extract sections by markdown headers."""
    sections = {}
    current_header = None
    current_body = []
    for line in content.split('\n'):
        header_match = re.match(r'^(#{1,4})\s+(.+)', line)
        if header_match:
            if current_header:
                sections[current_header] = '\n'.join(current_body)
            current_header = header_match.group(2)
            current_body = []
        elif current_header:
            current_body.append(line)
    if current_header:
        sections[current_header] = '\n'.join(current_body)
    return sections


def count_badges(content):
    """Count badges using multiple patterns."""
    search_area = content[:2000]
    badge_url_patterns = [
        r'img\.shields\.io',
        r'github\.com/[^/\s]+/[^/\s]+/(actions|workflows)/[^\s]*badge',
        r'www\.bestpractices\.dev',
        r'insights\.linuxfoundation\.org',
        r'badge\.fury\.io',
        r'coveralls\.io',
        r'codecov\.io',
        r'opencollect\.com',
    ]
    # Standard markdown badges: [![label](url)](link)
    badge_markdown = re.findall(
        r'\[?!\[[^\]]*\]\([^)]*(?:' + '|'.join(badge_url_patterns) + r')[^)]*\)',
        search_area
    )
    count = len(badge_markdown)
    # Also check reference-style badges: [![label][shield]][url]
    ref_badges = re.findall(r'\[!\[[^\]]*\]\[[^\]]+\]\]', search_area)
    count += len(ref_badges)
    return count


def get_grade(score):
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 50: return "D"
    return "F"


# ═══════════════════════════════════════════════════════════════
# TRACK A: Skill Repository Scoring
# ═══════════════════════════════════════════════════════════════

def skill_score_scope(content, sections):
    """Clear scope & skill count (18 pts)."""
    score = 0
    # Look for numbers + "skills"
    count_match = re.search(r'(\d+)\s*[\w]*\s*(?:skills?|plugins?|agents?)', content[:500], re.IGNORECASE)
    if count_match:
        score += 8
    # Categories/domains listed
    domains = re.findall(r'(?:engineering|devops|marketing|security|compliance|productivity|research|finance|automation|data|frontend|backend|full.stack|mobile|cli|api)', content[:1000], re.IGNORECASE)
    if len(set(d.lower() for d in domains)) >= 3:
        score += 6
    elif len(set(d.lower() for d in domains)) >= 1:
        score += 3
    # "production-ready" or similar quality signal
    if re.search(r'production.ready|battle.tested|tested|enterprise|industrial', content[:500], re.IGNORECASE):
        score += 4
    return min(score, 18)


def skill_score_platforms(content):
    """Platform compatibility (15 pts)."""
    score = 0
    lower = content.lower()
    platforms = []
    platform_map = {
        'claude code': ['claude code', 'claude-code', 'claude/skills'],
        'codex': ['codex', 'openai codex'],
        'gemini': ['gemini cli', 'gemini'],
        'openclaw': ['openclaw', 'clawhub', 'clawd'],
        'cursor': ['cursor'],
        'aider': ['aider'],
        'windsurf': ['windsurf'],
        'kilo code': ['kilo code'],
        'opencode': ['opencode'],
        'augment': ['augment'],
        'antigravity': ['antigravity'],
        'mistral': ['mistral vibe', 'mistral'],
        'hermes': ['hermes agent', 'hermes'],
    }
    for name, patterns in platform_map.items():
        if any(p in lower for p in patterns):
            platforms.append(name)

    if len(platforms) >= 5:
        score = 15
    elif len(platforms) >= 3:
        score = 12
    elif len(platforms) >= 1:
        score = 8
    return score


def skill_score_quick_install(content, sections):
    """Quick install (20 pts)."""
    score = 0
    # One-liner patterns
    one_liners = re.findall(
        r'[`|]?(clawhub\s+install|npx\s+[\w@.-]+|npm\s+install|sh -c|curl\s+\S+.*\|.*sh)',
        content, re.IGNORECASE
    )
    standard_installs = re.findall(
        r'`?(git clone|pip install|brew install|cargo install)\s+[\w@./-]+',
        content, re.IGNORECASE
    )
    install_in_code = re.findall(
        r'```(?:bash|sh|shell|zsh)?\n.*?(clawhub|npx|npm install|git clone|sh -c|scripts/install).*?```',
        content, re.DOTALL | re.IGNORECASE
    )

    if one_liners:
        score += 15
        if install_in_code:
            score += 5
    elif standard_installs or install_in_code:
        score += 10
        for header, body in sections.items():
            if any(w in header.lower() for w in ['install', 'setup', 'getting started', 'quick']):
                score += 5
                break
    return min(score, 20)


def skill_score_catalog(content, sections):
    """Skill catalog / index (15 pts)."""
    score = 0
    # Table of skills
    skill_table = re.findall(r'\|.*`[a-z][\w-]*`.*\|', content, re.IGNORECASE)
    # Bullet list of skills
    skill_bullets = re.findall(r'^[-*]\s+`?\*\*?[\w][\w\s-]*`?\**\s*[—–:-]', content, re.MULTILINE)
    # Category headers with skills under them
    skill_names = re.findall(r'`([\w-]+)`\s*(?:skill|agent|plugin)', content, re.IGNORECASE)

    total_listed = len(skill_table) + len(skill_bullets) + len(skill_names)
    if total_listed >= 10:
        score = 15
    elif total_listed >= 5:
        score = 12
    elif total_listed >= 1:
        score = 8
    return score


def skill_score_usage(content, sections):
    """Usage example (12 pts)."""
    score = 0
    code_blocks = re.findall(r'```\w*\n.*?```', content, re.DOTALL)
    # Skill activation patterns
    activate_patterns = re.findall(r'activate_skill|activate|trigger|use\s+(?:the\s+)?skill', content, re.IGNORECASE)
    # Example output shown
    has_output = bool(re.search(r'```(?:output|result|json|text)\n', content, re.IGNORECASE))

    if code_blocks and activate_patterns:
        score = 12
    elif code_blocks and len(code_blocks) >= 2:
        score = 8
    elif code_blocks:
        score = 5
    return min(score, 12)


def skill_score_structure(content, sections):
    """Structure & ToC (10 pts)."""
    score = 0
    toc_patterns = [
        r'##\s*table of contents',
        r'##\s*目录',
        r'<details>\s*\n\s*<summary>.*(?:table of contents|目录)',
        r'\[.*\]\(#.*\).*\n.*\[.*\]\(#.*\)',
        r'<ol>\s*\n\s*<li>',
    ]
    for pattern in toc_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            score += 6
            break
    h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
    if h2_count >= 5:
        score += 4
    elif h2_count >= 3:
        score += 2
    return min(score, 10)


def skill_score_badges(content):
    """Badges & metadata (5 pts)."""
    count = count_badges(content)
    if count >= 2: return 5
    if count >= 1: return 3
    return 0


def skill_score_community(content, sections):
    """Contributing & community (5 pts)."""
    score = 0
    lower = content.lower()
    if any(w in lower for w in ['contributing', 'contribute', 'pull request', '贡献']):
        score += 3
    if any(w in lower for w in ['issues', 'bug report', 'feedback', '问题反馈']):
        score += 2
    return min(score, 5)


# ═══════════════════════════════════════════════════════════════
# TRACK B: General Project Scoring
# ═══════════════════════════════════════════════════════════════

def general_score_hero_visual(content, lines):
    """Hero visual (18 pts)."""
    score = 0
    first_15 = "\n".join(lines[:15])
    images = re.findall(r'!\[.*?\]\(.*?\)', first_15)
    html_imgs = re.findall(r'<img\s', first_15)
    html_picture = re.findall(r'<picture\s', first_15)
    total_visuals = len(images) + len(html_imgs) + len(html_picture)
    if total_visuals >= 1:
        first_5 = "\n".join(lines[:5])
        early = bool(re.search(r'!\[.*?\]\(.*?\)', first_5) or re.search(r'<img\s', first_5) or re.search(r'<picture\s', first_5))
        score = 18 if early else 12
    if score == 0:
        if re.search(r'[╔╗╚╝║═┌┐└┘│─]{5,}', first_15):
            score = 6
    return min(score, 18)


def general_score_tagline(content, lines):
    """Tagline & personality (12 pts)."""
    score = 0
    first_20 = "\n".join(lines[:20])
    h1_match = re.search(r'^#\s+(.+)', first_20, re.MULTILINE)
    if h1_match:
        score += 4
    h1_end = h1_match.end() if h1_match else 0
    after_h1 = first_20[h1_end:].strip()
    text_lines = []
    for line in after_h1.split('\n'):
        line = line.strip()
        if line and not line.startswith('[![') and not line.startswith('![') \
           and not line.startswith('<img') and not line.startswith('<picture') \
           and not line.startswith('<div') and not line.startswith('<p') \
           and not line.startswith('<hr') and not line.startswith('---'):
            text_lines.append(line)
            if len(text_lines) >= 3:
                break
    tagline = ' '.join(text_lines)
    personality_words = [
        'not ', 'but you', 'feel like', 'money back', 'talk of the town',
        'amazing', 'magic', 'beautiful', 'simplest', 'powerful',
        'will not', "won't", 'trust me', "let's", 'actually',
        'start here', 'make it', 'supercharge', 'effortless',
        'boring', 'try again', 'sound', 'sort of',
    ]
    corporate_words = [
        'comprehensive', 'leverage', 'utilize', 'facilitate',
        'robust solution', 'cutting-edge', 'state-of-the-art platform',
    ]
    personality_score = sum(1 for w in personality_words if w in tagline.lower())
    corporate_penalty = sum(1 for w in corporate_words if w in tagline.lower())
    if len(tagline) > 20:
        score += 4
    if personality_score >= 1 and corporate_penalty == 0:
        score += 4
    elif personality_score >= 1:
        score += 2
    elif len(tagline) > 20 and corporate_penalty == 0:
        score += 2
    elif corporate_penalty > 0:
        score -= 2
    return max(0, min(score, 12))


def general_score_quick_start(content, sections):
    """Quick start (20 pts)."""
    score = 0
    one_liners = re.findall(
        r'[`|]\s*(sh -c|curl\s+\S+.*\|.*sh|wget.*\|.*sh|fetch.*\|.*sh|npx\s+[\w@.-]+)',
        content, re.IGNORECASE
    )
    standard_installs = re.findall(
        r'`?(npm install|npm i |pip install|pip3 install|brew install|cargo install|apt install|apt-get install|yarn add|yarn global|go install|git clone)\s+[\w@./-]+`?',
        content, re.IGNORECASE
    )
    install_in_code = re.findall(
        r'```(?:bash|sh|shell|zsh)?\n.*?(npm install|pip install|brew install|cargo install|git clone|sh -c|curl|apt install|yarn add|npx).*?```',
        content, re.DOTALL | re.IGNORECASE
    )
    if one_liners:
        score += 15
        if install_in_code or standard_installs:
            score += 5
    elif standard_installs or install_in_code:
        score += 10
        for header in sections:
            if any(w in header.lower() for w in ['install', 'setup', 'getting started', 'quick start', 'basic']):
                score += 5
                break
    return min(score, 20)


def general_score_problem_value(content, sections):
    """Problem & value proposition (12 pts)."""
    score = 0
    lower = content.lower()
    first_1000 = content[:1000].lower()
    problem_found = False
    for header in sections:
        if any(w in header.lower() for w in ['why', 'problem', 'motivation', '痛点', '为什么']):
            if len(sections[header].strip()) > 30:
                score += 4
                problem_found = True
                break
    if not problem_found:
        if any(w in first_1000 for w in ['because', 'struggle', 'frustrat', 'tired of', 'pain', 'difficult', 'hard to']):
            score += 3
    value_patterns = [r'help(ed|s)?\s+\d+', r'\d+[\d,]*\s+(people|users|developers|stars|downloads)', r'(millions|thousands)\s+(of|people|users)']
    for p in value_patterns:
        if re.search(p, lower):
            score += 4
            break
    else:
        if any(w in first_1000 for w in ['for developers', 'for teams', 'for beginners', 'for you', 'who want']):
            score += 2
    if re.search(r'\d+[kKmM]?\+?\s*(stars|downloads|users|install|people|developers)', lower):
        score += 4
    return min(score, 12)


def general_score_toc(content, sections):
    """ToC & structure (10 pts)."""
    score = 0
    toc_patterns = [
        r'##\s*table of contents', r'##\s*目录',
        r'<details>\s*\n\s*<summary>.*table of contents', r'<details>\s*\n\s*<summary>.*目录',
        r'\[.*\]\(#.*\).*\n.*\[.*\]\(#.*\)', r'<ol>\s*\n\s*<li>',
    ]
    for p in toc_patterns:
        if re.search(p, content, re.IGNORECASE):
            score += 6
            break
    h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
    if h2_count >= 5: score += 4
    elif h2_count >= 3: score += 2
    return min(score, 10)


def general_score_social(content, sections):
    """Social proof & community (12 pts)."""
    score = 0
    lower = content.lower()
    if any(w in lower for w in ['discord', 'slack', 'gitter', 'telegram', '社区', 'matrix']): score += 4
    if any(w in lower for w in ['contributing', 'contribute', 'pull request', '贡献', 'pr welcome']): score += 3
    if any(w in lower for w in ['issues', 'bug report', 'feedback', '问题反馈', 'report']): score += 2
    if any(w in lower for w in ['twitter.com', 'x.com', '@', 'mastodon', 'weibo']): score += 3
    return min(score, 12)


def general_score_badges(content):
    """Badges (6 pts)."""
    count = count_badges(content)
    if count >= 3: return 6
    if count >= 1: return 4
    return 0


def general_score_usage(content, sections):
    """Usage examples (10 pts)."""
    score = 0
    code_blocks = re.findall(r'```\w*\n.*?```', content, re.DOTALL)
    docs_links = re.findall(r'\[.*?\]\(https?://.*?(docs|documentation|guide|tutorial).*?\)', content, re.IGNORECASE)
    if not docs_links:
        docs_links = re.findall(r'docs\.\S+|documentation\S+', content)
    if len(code_blocks) >= 4: score = 10
    elif len(code_blocks) >= 2: score = 7
    elif len(code_blocks) >= 1: score = 5
    if docs_links and score < 10: score += 2
    if score == 0:
        inline = re.findall(r'`[^`\n]{10,}`', content)
        if len(inline) >= 3: score = 4
        elif len(inline) >= 1: score = 2
    return min(score, 10)


# ═══════════════════════════════════════════════════════════════
# Audit Orchestration
# ═══════════════════════════════════════════════════════════════

def audit_readme(filepath, track=None, project_dir=None):
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}", "score": 0}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    sections = parse_sections(content)

    if track is None:
        track = detect_track(content, project_dir or os.path.dirname(filepath))

    if track == 'skill':
        dims = {
            'scope_count': skill_score_scope(content, sections),
            'platforms': skill_score_platforms(content),
            'quick_install': skill_score_quick_install(content, sections),
            'catalog': skill_score_catalog(content, sections),
            'structure_toc': skill_score_structure(content, sections),
            'usage_example': skill_score_usage(content, sections),
            'badges': skill_score_badges(content),
            'community': skill_score_community(content, sections),
        }
        maxes = {
            'scope_count': 18, 'platforms': 15, 'quick_install': 20,
            'catalog': 15, 'structure_toc': 10, 'usage_example': 12,
            'badges': 5, 'community': 5,
        }
    else:
        dims = {
            'hero_visual': general_score_hero_visual(content, lines),
            'tagline_personality': general_score_tagline(content, lines),
            'quick_start': general_score_quick_start(content, sections),
            'problem_value': general_score_problem_value(content, sections),
            'toc_structure': general_score_toc(content, sections),
            'social_proof': general_score_social(content, sections),
            'badges': general_score_badges(content),
            'usage_examples': general_score_usage(content, sections),
        }
        maxes = {
            'hero_visual': 18, 'tagline_personality': 12, 'quick_start': 20,
            'problem_value': 12, 'toc_structure': 10, 'social_proof': 12,
            'badges': 6, 'usage_examples': 10,
        }

    total = sum(dims.values())
    return {
        "score": total,
        "grade": get_grade(total),
        "track": track,
        "dimensions": dims,
        "max_per_dimension": maxes,
    }


# ═══════════════════════════════════════════════════════════════
# Project Type Detection (for --detect)
# ═══════════════════════════════════════════════════════════════

def detect_project_type(project_dir):
    if not os.path.isdir(project_dir):
        return {"type": "unknown", "reason": "directory not found"}
    files = set(os.listdir(project_dir))
    if 'SKILL.md' in files:
        return {"type": "agent-skill", "reason": "SKILL.md found"}
    data_files = [f for f in files if f.endswith(('.csv', '.parquet'))]
    if data_files and not any(f in files for f in ['package.json', 'pyproject.toml', 'Cargo.toml', 'src', 'lib']):
        return {"type": "data-resource", "reason": f"data files found: {data_files[:3]}"}
    pkg_json = os.path.join(project_dir, 'package.json')
    if os.path.exists(pkg_json):
        try:
            with open(pkg_json) as f:
                pkg = json.load(f)
            if bool(pkg.get('bin')):
                return {"type": "cli-tool", "reason": "package.json has 'bin' field"}
            deps = pkg.get('dependencies', {})
            if any(k in deps for k in ['react', 'vue', 'svelte', 'solid-js', 'next', 'vite', 'astro']):
                return {"type": "app-product", "reason": "UI framework detected"}
            if pkg.get('main') or pkg.get('exports'):
                return {"type": "library-sdk", "reason": "package.json has 'main'/'exports'"}
        except Exception:
            pass
    if os.path.exists(os.path.join(project_dir, 'pyproject.toml')):
        return {"type": "library-sdk", "reason": "pyproject.toml found"}
    if any(f.endswith(('.html', '.jsx', '.tsx')) for f in files):
        return {"type": "app-product", "reason": "UI files detected"}
    return {"type": "unknown", "reason": "no strong signals found"}


# ═══════════════════════════════════════════════════════════════
# Report Generation
# ═══════════════════════════════════════════════════════════════

def get_report(results):
    dims = results['dimensions']
    maxes = results['max_per_dimension']
    track = results.get('track', 'general')
    suggestions = []

    if track == 'skill':
        labels = {
            'scope_count': 'Scope & Skill Count',
            'platforms': 'Platform Compatibility',
            'quick_install': 'Quick Install',
            'catalog': 'Skill Catalog',
            'structure_toc': 'Structure & ToC',
            'usage_example': 'Usage Example',
            'badges': 'Badges',
            'community': 'Community',
        }
        tips = {
            'scope_count': 'State how many skills + what domains covered. E.g., "345 skills for engineering, DevOps, marketing..."',
            'platforms': 'List which agent platforms are supported: Claude Code, Codex, Gemini CLI, OpenClaw, Cursor, etc.',
            'quick_install': 'Provide a single command: `clawhub install X` or `npx X` or `git clone ... && ./install`',
            'catalog': 'Add a table or bullet list of all skills with one-line descriptions.',
            'structure_toc': 'Add a Table of Contents (collapsible for long READMEs). Use clear ## sections.',
            'usage_example': 'Show a skill being activated/triggered with code example + expected output.',
            'badges': 'Add 2+ badges (license, version, star count, skill count, CI).',
            'community': 'Add contributing guide + issues link.',
        }
        benchmarks = {
            'scope_count': 'alirezarezvani: "345 production-ready skills"',
            'platforms': 'alirezarezvani: "Claude Code · Codex · Gemini CLI · OpenClaw · Cursor · 9 more"',
            'quick_install': 'agent-skills-hub: `npx agent-skills-hub --claude`',
            'catalog': 'alirezarezvani: full category breakdown with skill counts',
            'structure_toc': 'agent-skills-hub: full <details> ToC with nested links',
            'usage_example': 'alirezarezvani: `> activate_skill(name="senior-architect")`',
            'badges': 'alirezarezvani: License + Skills + Agents + Personas + Stars badges',
            'community': 'openclaw/agent-skills: contributing + issues + symlinks',
        }
    else:
        labels = {
            'hero_visual': 'Hero Visual',
            'tagline_personality': 'Tagline & Personality',
            'quick_start': 'Quick Start',
            'problem_value': 'Problem & Value',
            'toc_structure': 'ToC & Structure',
            'social_proof': 'Social Proof',
            'badges': 'Badges',
            'usage_examples': 'Usage Examples',
        }
        tips = {
            'hero_visual': 'Add a logo/banner/screenshot as the FIRST element.',
            'tagline_personality': 'Add a memorable one-liner after H1. Show personality.',
            'quick_start': 'Provide a single copy-paste command to install.',
            'problem_value': 'State who it\'s for and what pain it solves. Add stats.',
            'toc_structure': 'Add a Table of Contents. Use clear ## sections.',
            'social_proof': 'Add Discord/chat link, contributing guide, social media.',
            'badges': 'Add 3+ shields.io badges (CI, license, Discord).',
            'usage_examples': 'Add 2+ copy-paste code examples + link to docs.',
        }
        benchmarks = {
            'hero_visual': 'freeCodeCamp, Oh My Zsh, shadcn all lead with a visual',
            'tagline_personality': 'Oh My Zsh: "will not make you a 10x developer..."',
            'quick_start': 'Oh My Zsh: `sh -c "$(curl ...)"`',
            'problem_value': 'freeCodeCamp: "helped 100,000+ people"',
            'toc_structure': 'freeCodeCamp + Oh My Zsh: detailed ToC',
            'social_proof': 'Oh My Zsh: Discord badge + 5 social badges',
            'badges': 'VS Code: CI + bugs + Gitter badges',
            'usage_examples': 'Anthropic Cookbook: recipe table with links',
        }

    for key in dims:
        ratio = dims[key] / maxes[key] if maxes[key] > 0 else 0
        if ratio < 0.6: status = '🔴'
        elif ratio < 1.0: status = '🟡'
        else: status = '✅'
        if ratio < 1.0:
            suggestions.append(f"  {status} {labels[key]}: {dims[key]}/{maxes[key]}")
            suggestions.append(f"     → {tips[key]}")
            suggestions.append(f"     📎 Benchmark: {benchmarks[key]}")
        else:
            suggestions.append(f"  {status} {labels[key]}: {dims[key]}/{maxes[key]}")
    return suggestions


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='📝 Better README — Dual-track audit (v3): auto-detects skill repo vs general project'
    )
    parser.add_argument('--path', help='Path to README.md file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--track', choices=['skill', 'general'], help='Force scoring track')
    parser.add_argument('--detect', help='Detect project type from directory')
    args = parser.parse_args()

    if args.detect:
        result = detect_project_type(args.detect)
        track = detect_track(open(os.path.join(args.detect, 'README.md')).read() if os.path.exists(os.path.join(args.detect, 'README.md')) else '', args.detect)
        print(f"\n🔍 Project Type Detection")
        print(f"   Directory: {args.detect}")
        print(f"   Type: {result['type']}")
        print(f"   Reason: {result['reason']}")
        print(f"   README Track: {track}")
        print()
        return

    if not args.path:
        parser.print_help()
        return

    results = audit_readme(args.path, track=args.track)

    if 'error' in results:
        print(f"❌ {results['error']}")
        return

    if args.json:
        print(json.dumps(results, indent=2))
        return

    track_label = "🧩 Skill Repository" if results['track'] == 'skill' else "🚀 General Project"
    print(f"\n📝 BETTER README — AUDIT REPORT (v3)")
    print(f"   File: {args.path}")
    print(f"   Track: {track_label} (auto-detected)")
    print(f"")
    print(f"   📊 Total Score: {results['score']}/100 ({results['grade']})")
    print(f"")

    grade_desc = {
        'A': '🚀 Top-tier — matches best-in-class patterns',
        'B': '✅ Great — minor polish needed',
        'C': '🟡 Solid — a few improvements will level it up',
        'D': '🟠 Needs significant work',
        'F': '🔴 Start from template',
    }
    print(f"   {grade_desc.get(results['grade'], '')}")
    print(f"")
    print(f"   Dimension Breakdown:")
    for s in get_report(results):
        print(s)
    print()


if __name__ == '__main__':
    main()
