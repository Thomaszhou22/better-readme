# 📝 Better README

**[English](README.md)** | **中文**

审计、生成并优化项目 README 文件，提供质量评分、模板匹配和多语言支持。适用于任何项目类型——库、命令行工具、Web 应用、Agent Skill 和数据集。

**问题所在：** 大多数 README 都是最后随便写的。没有"为什么"段落，没有可视化演示，10 步安装指南没人能跑完。Better README 解决这个问题——给现有 README 打分，按项目类型推荐模板，一次性生成中英双语文档。

## 安装

```bash
# ClawHub
clawhub install better-readme

# 或从源码安装
git clone https://github.com/Thomaszhou22/better-readme.git
cp -r better-readme ~/.openclaw/skills/
```

要求 Python 3.8+，无其他依赖。

## 快速开始

```bash
# 给现有 README 打分
python3 scripts/readme_audit.py --path ./README.md

# 检测项目类型（推荐对应模板）
python3 scripts/readme_audit.py --detect /path/to/project

# JSON 输出（供 CI/CD 使用）
python3 scripts/readme_audit.py --path ./README.md --json
```

或者直接跟你的 AI Agent 说：**"检查一下我的 README"**——它会搞定一切。

## 工作原理

```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
  │  1. 分类     │────▶│  2. 评分     │────▶│  3. 生成         │
  │  什么类型？  │     │  多好？       │     │  修复 + 双语     │
  └──────────────┘     └──────────────┘     └──────────────────┘
         ▲                                         │
         │          Agent 填充模板                  │
         └─────────────────────────────────────────┘
                     重新评分验证
```

### 第 1 步：分类

自动检测你的项目类型：

| 信号 | 类型 | 模板 |
|------|------|------|
| package.json 中有 `main`/`exports` | 库/SDK | API 优先 |
| 有 `bin` 字段或 CLI 框架 | 命令行工具 | 演示优先 |
| React/Vue + 部署目标 | 应用/产品 | 截图优先 |
| 存在 `SKILL.md` | Agent Skill | 触发条件优先 |
| `.csv`/`.json` 数据集 | 数据/资源 | Schema 优先 |

### 第 2 步：评分

9 维度打分（满分 100）：

| 维度 | 满分 | 检查内容 |
|------|------|---------|
| 第一印象 | 15 | 前 10 行有 H1 标题 + 一句话描述 + 图片 |
| 问题陈述 | 10 | 有"为什么"段落说明解决什么痛点 |
| 快速开始 | 20 | 安装 + 运行 ≤3 条命令 |
| 可视化演示 | 10 | 有截图、GIF 或视频 |
| 功能清晰度 | 10 | 可扫描的功能列表/表格 |
| 用法/API 文档 | 10 | 2 个以上代码示例 |
| 徽章和元数据 | 5 | 许可证、版本、CI 徽章 |
| 社区和链接 | 10 | 贡献指南、Issues 链接、社区 |
| 发布前就绪度 | 10 | 目录、路线图、更新日志 |

### 第 3 步：生成

- 从 `references/templates.md` 选取对应模板
- 扫描项目获取真实数据（名称、安装命令、许可证、功能）
- 填充模板——不留占位符
- 同时生成 `README.md`（英文）和 `README.zh-CN.md`（中文）
- 顶部添加语言切换链接

### 第 4 步：发布前检查清单

对照 `references/pre-publish-checklist.md` 检查：

- 🔴 **关键**：README、安装说明、许可证、GitHub About、Topics 标签
- 🟡 **重要**：截图、"为什么"段落、贡献指南、Issue 模板
- 🟢 **加分**：徽章、更新日志、Discussion、赞助

## 模板类型

| 类型 | 核心元素 | 重点 | 安装示例 |
|------|---------|------|---------|
| 📦 库/SDK | 代码片段 | API + 示例 | `npm install` |
| 🔧 命令行工具 | 演示 GIF | 命令表格 | `brew install` |
| 🚀 应用/产品 | 截图 | 功能 + 在线 Demo | 部署按钮 |
| 🧩 Agent Skill | 触发条件 | 工作流 + 兼容性 | `clawhub install` |
| 📊 数据/资源 | 统计卡片 | Schema + 样例 | 直接下载 |

## Agent 集成

跟你的 Agent 说以下任意一句：
- *"给这个项目写个 README"*
- *"给我的 README 打个分"*
- *"我的 README 太烂了，帮我修"*

Agent 会：
1. 检测项目类型
2. 运行审计脚本
3. 加载对应模板
4. 扫描代码库获取真实数据
5. 生成双语 README
6. 运行发布前检查清单

## 文件结构

```
better-readme/
├── SKILL.md                          # 触发条件 + 工作流
├── scripts/
│   └── readme_audit.py               # README 评分器 + 项目检测器
├── references/
│   ├── templates.md                  # 5 种项目类型模板
│   ├── scoring-rubric.md             # 完整评分标准
│   └── pre-publish-checklist.md      # GitHub 发布检查清单
└── README.md
```

## 兼容性

- ✅ OpenClaw
- ✅ Claude Code
- ✅ Cursor / Codex CLI / Gemini CLI
- ✅ 任何使用 SKILL.md 格式的平台

## 许可证

MIT © 2026 Thomas Zhou
