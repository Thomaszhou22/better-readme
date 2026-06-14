#!/usr/bin/env python3
"""
Better README — Audit Script
Scores a README.md file across 9 dimensions (0-100).
Also detects project type from project structure.

Usage:
  python3 readme_audit.py --path ./README.md
  python3 readme_audit.py --path ./README.md --json
  python3 readme_audit.py --detect /path/to/project
"""

import argparse
import json
import os
import re
import sys

# ── Scoring Rules ──

MAX_SCORE = 100

def score_first_impression(content, lines):
    """H1 + tagline + visual in first 10 lines (15 pts)"""
    score = 0
    first_screen = "\n".join(lines[:12])

    # H1 title
    if re.search(r'^#\s+\S+', first_screen, re.MULTILINE):
        score += 5

    # One-line description (non-empty text after H1, not just badges)
    desc_pattern = re.search(r'^#\s+.+\n+(.+)', first_screen)
    if desc_pattern:
        line = desc_pattern.group(1).strip()
        # Not just a badge line
        if line and not line.startswith('[') and not line.startswith('!') and not line.startswith('>'):
            if len(line) > 15:
                score += 5
        elif line.startswith('>') and len(line) > 20:
            # Blockquote tagline
            score += 5

    # Visual (image/GIF) in first 12 lines
    if re.search(r'!\[.*\]\(.*\)', first_screen) or re.search(r'<img ', first_screen):
        score += 5

    return min(score, 15)


def score_problem_statement(content, sections):
    """Clear 'Why' section (10 pts)"""
    score = 0
    why_section = None
    for header, body in sections.items():
        header_lower = header.lower()
        if any(w in header_lower for w in ['why', 'problem', 'motivation', '痛点', '为什么']):
            why_section = body
            break

    if why_section:
        if len(why_section.strip()) > 50:
            score = 10
        elif len(why_section.strip()) > 20:
            score = 7
    elif len(content) > 200:
        # Check if problem is explained in intro
        first_500 = content[:500].lower()
        if any(w in first_500 for w in ['because', 'problem', 'struggle', 'frustrat', 'need', 'pain']):
            score = 6

    return min(score, 10)


def score_quick_start(content, sections):
    """Install + run in ≤3 commands (20 pts)"""
    score = 0

    # Look for install section
    install_section = None
    usage_section = None
    for header, body in sections.items():
        header_lower = header.lower()
        if any(w in header_lower for w in ['install', 'setup', 'getting started', 'quick start', '安装', '快速开始']):
            install_section = body
        if any(w in header_lower for w in ['usage', 'example', 'quick start', '使用']):
            usage_section = body

    # Count code blocks in install
    if install_section:
        code_blocks = re.findall(r'```', install_section)
        if len(code_blocks) >= 2:
            score += 10
        elif len(code_blocks) >= 1:
            score += 7

        # Check for common install patterns
        if re.search(r'(npm install|pip install|brew install|cargo install|git clone|apt install|yarn add)', install_section, re.IGNORECASE):
            score += 5

    if usage_section:
        code_blocks = re.findall(r'```', usage_section)
        if len(code_blocks) >= 2:
            score += 5
        elif len(code_blocks) >= 1:
            score += 3

    # Fallback: any code block in first 100 lines
    if score == 0:
        first_100 = "\n".join(content.split('\n')[:100])
        if re.search(r'```', first_100):
            score = 5

    return min(score, 20)


def score_visual_demo(content, lines):
    """Screenshot/GIF/video present (10 pts)"""
    score = 0

    images = re.findall(r'!\[.*?\]\(.*?\)', content)
    gifs = re.findall(r'\.gif\)', content, re.IGNORECASE)
    videos = re.findall(r'<video|<iframe|youtu\.be|youtube\.com/watch', content, re.IGNORECASE)
    demos = re.findall(r'demo', content, re.IGNORECASE)

    if gifs or videos:
        score = 10
    elif len(images) >= 2:
        score = 8
    elif len(images) >= 1:
        # Check if image is meaningful (not just a badge)
        non_badge_images = [img for img in images if 'shields.io' not in img and 'badge' not in img.lower()]
        if non_badge_images:
            score = 7
        else:
            score = 3

    if score == 0 and demos:
        score = 3

    return min(score, 10)


def score_feature_clarity(content, sections):
    """Feature list/table that's scannable (10 pts)"""
    score = 0
    feature_section = None
    for header, body in sections.items():
        header_lower = header.lower()
        if any(w in header_lower for w in ['feature', 'what it does', '功能', '特性']):
            feature_section = body
            break

    if feature_section:
        # Bullet points or table = scannable
        bullets = feature_section.count('\n- ') + feature_section.count('\n* ')
        tables = feature_section.count('|')
        if bullets >= 3 or tables >= 6:
            score = 10
        elif bullets >= 1:
            score = 7
        else:
            score = 4
    else:
        # Check entire content for feature-like bullets near a "features" keyword
        feature_match = re.search(r'(?:feature|功能)(.*?)(?:\n#{1,4}|\Z)', content, re.IGNORECASE | re.DOTALL)
        if feature_match:
            block = feature_match.group(1)
            if block.count('\n- ') >= 3 or block.count('\n* ') >= 3:
                score = 7

    return min(score, 10)


def score_usage_docs(content, sections):
    """2+ code examples for main use cases (10 pts)"""
    score = 0

    # Count all code blocks (excluding install)
    code_blocks = re.findall(r'```\w*\n.*?```', content, re.DOTALL)
    total_blocks = len(code_blocks)

    # Count inline code
    inline_code = re.findall(r'`[^`\n]{5,}`', content)

    if total_blocks >= 4:
        score = 10
    elif total_blocks >= 2:
        score = 7
    elif total_blocks >= 1 and len(inline_code) >= 3:
        score = 6
    elif total_blocks >= 1:
        score = 4
    elif len(inline_code) >= 5:
        score = 3

    return min(score, 10)


def score_badges(content):
    """License + version + CI badges (5 pts)"""
    score = 0
    lower = content.lower()

    if 'shields.io' in lower or 'badge' in lower:
        if re.search(r'license', lower[:500]):
            score += 2
        if re.search(r'npm|pypi|version', lower[:500]):
            score += 2
        if re.search(r'ci|build|test|actions', lower[:500]):
            score += 1

    return min(score, 5)


def score_community(content, sections):
    """Contributing + Issues + Discussions (10 pts)"""
    score = 0
    lower = content.lower()

    if any(w in lower for w in ['contributing', 'contribute', 'pr', 'pull request', '贡献']):
        score += 4
    if any(w in lower for w in ['issues', 'bug report', 'feedback', '问题反馈']):
        score += 3
    if any(w in lower for w in ['discussions', 'discord', 'slack', 'community', '社区', 'gitter']):
        score += 3

    return min(score, 10)


def score_readiness(content, lines):
    """Pre-publish readiness heuristics (10 pts)"""
    score = 0
    lower = content.lower()

    # License mention
    if re.search(r'license|licence|mit|apache|gpl', lower):
        score += 2
    # Version mention
    if re.search(r'version|v\d+\.\d+|changelog', lower):
        score += 2
    # Table of contents
    if re.search(r'table of contents|目录|## contents', lower):
        score += 2
    # Roadmap
    if re.search(r'roadmap|todo|计划|路线图', lower):
        score += 2
    # Acknowledgments / Credits
    if re.search(r'acknowledgment|credit|thank|感谢|致谢', lower):
        score += 2

    return min(score, 10)


# ── Helpers ──

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


def detect_project_type(project_dir):
    """Detect project type from directory structure."""
    if not os.path.isdir(project_dir):
        return {"type": "unknown", "reason": "directory not found"}

    files = set(os.listdir(project_dir))

    # Agent Skill
    if 'SKILL.md' in files:
        return {"type": "agent-skill", "reason": "SKILL.md found"}

    # Data / Resource
    data_files = [f for f in files if f.endswith(('.csv', '.parquet'))]
    if data_files and not any(f in files for f in ['package.json', 'pyproject.toml', 'Cargo.toml', 'src', 'lib']):
        return {"type": "data-resource", "reason": f"data files found: {data_files[:3]}"}

    # Library / SDK
    pkg_json = os.path.join(project_dir, 'package.json')
    if os.path.exists(pkg_json):
        try:
            import json
            with open(pkg_json) as f:
                pkg = json.load(f)
            has_bin = bool(pkg.get('bin'))
            has_main = bool(pkg.get('main') or pkg.get('exports'))
            deps = pkg.get('dependencies', {})
            has_ui = any(k in deps for k in ['react', 'vue', 'svelte', 'solid-js'])

            if has_bin:
                return {"type": "cli-tool", "reason": "package.json has 'bin' field"}
            elif has_ui or any(k in deps for k in ['next', 'vite', 'astro']):
                if any(k in deps for k in ['next', 'react-router', 'astro']):
                    return {"type": "app-product", "reason": "UI framework + router detected"}
            elif has_main:
                return {"type": "library-sdk", "reason": "package.json has 'main'/'exports'"}
        except Exception:
            pass

    # Python CLI
    pyproject = os.path.join(project_dir, 'pyproject.toml')
    if os.path.exists(pyproject):
        try:
            with open(pyproject) as f:
                content = f.read()
            if '[tool.poetry.scripts]' in content or 'console_scripts' in content or 'click' in content:
                return {"type": "cli-tool", "reason": "Python CLI (scripts/click detected)"}
            return {"type": "library-sdk", "reason": "pyproject.toml found"}
        except Exception:
            pass

    # Detect by file patterns
    if any(f.endswith('.py') for f in files) and 'requirements.txt' in files:
        return {"type": "library-sdk", "reason": "Python project with requirements.txt"}

    if any(f.endswith('.html') or f.endswith('.jsx') or f.endswith('.tsx') for f in files):
        return {"type": "app-product", "reason": "UI files detected"}

    return {"type": "unknown", "reason": "no strong signals found"}


def audit_readme(filepath):
    """Full audit of a README file."""
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}", "score": 0}

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    sections = parse_sections(content)

    results = {}
    results['first_impression'] = score_first_impression(content, lines)
    results['problem_statement'] = score_problem_statement(content, sections)
    results['quick_start'] = score_quick_start(content, sections)
    results['visual_demo'] = score_visual_demo(content, lines)
    results['feature_clarity'] = score_feature_clarity(content, sections)
    results['usage_docs'] = score_usage_docs(content, sections)
    results['badges'] = score_badges(content)
    results['community'] = score_community(content, sections)
    results['readiness'] = score_readiness(content, lines)

    total = sum(results.values())

    return {
        "score": total,
        "grade": get_grade(total),
        "dimensions": results,
        "max_per_dimension": {
            "first_impression": 15,
            "problem_statement": 10,
            "quick_start": 20,
            "visual_demo": 10,
            "feature_clarity": 10,
            "usage_docs": 10,
            "badges": 5,
            "community": 10,
            "readiness": 10,
        }
    }


def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def get_improvements(results):
    """Generate improvement suggestions for low-scoring dimensions."""
    dims = results['dimensions']
    maxes = results['max_per_dimension']
    suggestions = []

    labels = {
        'first_impression': 'First Impression',
        'problem_statement': 'Problem Statement',
        'quick_start': 'Quick Start',
        'visual_demo': 'Visual Demo',
        'feature_clarity': 'Feature Clarity',
        'usage_docs': 'Usage / API Docs',
        'badges': 'Badges & Metadata',
        'community': 'Community & Links',
        'readiness': 'Pre-Publish Readiness',
    }

    tips = {
        'first_impression': 'Add an H1 title + one-line tagline + screenshot/GIF in the first 10 lines',
        'problem_statement': 'Add a "Why" section explaining what pain point this solves and for whom',
        'quick_start': 'Add install + first run instructions in ≤3 copy-paste commands',
        'visual_demo': 'Add a screenshot, GIF, or video demonstrating the tool in action',
        'feature_clarity': 'Add a feature list or table with short descriptions',
        'usage_docs': 'Add 2+ code examples covering the main use cases',
        'badges': 'Add license, version, and CI status badges from shields.io',
        'community': 'Add Contributing guide, Issues link, and Discussions/Chat',
        'readiness': 'Add License mention, version/changelog, Table of Contents, Roadmap',
    }

    for key in dims:
        ratio = dims[key] / maxes[key] if maxes[key] > 0 else 0
        if ratio < 0.6:
            status = '🔴'
        elif ratio < 1.0:
            status = '🟡'
        else:
            status = '✅'

        if ratio < 1.0:
            suggestions.append(f"  {status} {labels[key]}: {dims[key]}/{maxes[key]} — {tips[key]}")
        else:
            suggestions.append(f"  {status} {labels[key]}: {dims[key]}/{maxes[key]}")

    return suggestions


def main():
    parser = argparse.ArgumentParser(
        description='📝 Better README — Audit and score your README.md'
    )
    parser.add_argument('--path', help='Path to README.md file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--detect', help='Detect project type from directory')
    args = parser.parse_args()

    # Detect mode
    if args.detect:
        result = detect_project_type(args.detect)
        print(f"\n🔍 Project Type Detection")
        print(f"   Directory: {args.detect}")
        print(f"   Type: {result['type']}")
        print(f"   Reason: {result['reason']}")
        type_templates = {
            'library-sdk': '📦 Use Library/SDK template',
            'cli-tool': '🔧 Use CLI Tool template',
            'app-product': '🚀 Use App/Product template',
            'agent-skill': '🧩 Use Agent Skill template',
            'data-resource': '📊 Use Data/Resource template',
        }
        print(f"   {type_templates.get(result['type'], '❓ Unknown type — manual selection needed')}\n")
        return

    if not args.path:
        parser.print_help()
        return

    results = audit_readme(args.path)

    if 'error' in results:
        print(f"❌ {results['error']}")
        return

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Pretty print
    print(f"\n📝 BETTER README — AUDIT REPORT")
    print(f"   File: {args.path}")
    print(f"")
    print(f"   📊 Total Score: {results['score']}/100 ({results['grade']})")
    print(f"")
    print(f"   Dimension Breakdown:")
    for s in get_improvements(results):
        print(s)
    print(f"")

    grade = results['grade']
    if grade in ('A', 'B'):
        print(f"   ✅ README is in good shape!")
    elif grade == 'C':
        print(f"   🟡 Decent, but needs improvement before launch.")
    else:
        print(f"   🔴 Needs major work. Use a template from references/templates.md")
    print()


if __name__ == '__main__':
    main()
