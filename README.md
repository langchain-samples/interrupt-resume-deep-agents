# Deep Agents Lifecycle Workshop: Interrupt Resume

Build a deep agent, deploy it to LangSmith Deployments, then continuously improve it with Engine.

This technical session covers the harness architecture, tools, subagents, memory, and human-in-the-loop patterns behind Deep Agents and gives you time to build your own. You'll close with deploying your agent to production and using LangSmith Engine to automatically detect failures, diagnose root causes, propose fixes, and generate evaluators — creating a continuous improvement flywheel for your agent.

## Agenda

| # | Module | Duration | Notebook |
|---|--------|----------|----------|
| **1** | Deep Agents: Build a research agent from scratch using `create_deep_agent`. Covers the harness architecture, custom tools, subagents, backends, middleware, human-in-the-loop, and skills. | ~60 min | `modules/01_deep_agents.ipynb` |
| | **Break: Build your own agent!** | | `my_agent/` |
| **2** | Deploy: Ship your agent to LangSmith Deployments with the `langgraph` CLI. Test locally in Studio, validate, and deploy. | ~30 min | `modules/02_deploy.ipynb` |
| | **Break: Test & ship your agent!** | | |
| **3** | Engine: Continuously improve your deployed agent with LangSmith Engine. Engine automatically detects failures from production traces, diagnoses root causes against your codebase, proposes fixes, and generates evaluators to prevent regressions — closing the agent engineering flywheel. | ~30 min | Live demo |

## Prework Setup

Complete these steps **before the session starts**.

### 1. Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or pip
- A [LangSmith](https://smith.langchain.com) account

### 2. Clone and install

```bash
git clone <repo-url>
cd deep-agents-interrupt-resume

# Option A: uv (recommended)
uv sync

# Option B: pip
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Set environment variables

```bash
cp .env.example .env
```

Open `.env` and set **all three** keys:

| Key | Get one |
|-----|---------|
| `OPENAI_API_KEY` | <https://platform.openai.com> |
| `LANGSMITH_API_KEY` | <https://smith.langchain.com> — see [API key guide](#langsmith-api-key-guide) below |
| `TAVILY_API_KEY` | <https://tavily.com> |

> **Using a different model provider?** Edit `utils/models.py` — uncomment the provider you want (Anthropic, Azure OpenAI, AWS Bedrock) and set the matching API key in `.env`. No notebook changes required.

### 4. Verify

```bash
uv run jupyter notebook
```

Open `modules/01_deep_agents.ipynb` and run the first setup cell to confirm everything is working.

### LangSmith API Key Guide

Go to <https://smith.langchain.com> → Settings → API Keys to create a key.

| Key type | Prefix | Tracing | Deployments | Notes |
|----------|--------|---------|-------------|-------|
| **Personal Access Token** | `lsv2_pt_...` | Yes | No | Any user can create one. Easiest option for tracing during the workshop. |
| **Service Key (workspace-scoped)** | `lsv2_sk_...` | Yes | Yes | Must be scoped to a **specific workspace**, not the org. Required for `langgraph deploy`. |

> **Important:** If you create an org-scoped service key (the default), all API calls will return **403 Forbidden**. When creating a service key, select your workspace (e.g. "Workspace 1") instead of "Organization" to scope it correctly.

## Switching Models

All modules import `model` from `utils/models.py`. Change one line there to swap providers:

```python
# utils/models.py

# OpenAI (default)
model = init_chat_model("openai:gpt-4.1-mini")

# Anthropic
# model = init_chat_model("anthropic:claude-sonnet-4-5")

# Azure OpenAI
# from langchain_openai import AzureChatOpenAI
# model = AzureChatOpenAI(azure_deployment="gpt-4.1-mini", streaming=True)

# AWS Bedrock
# from langchain_aws import ChatBedrockConverse
# model = ChatBedrockConverse(provider="anthropic", model_id="...")
```

## Deploy (Module 2)

Module 2 deploys the agent at `agents/deep_agent/` to LangSmith via the `langgraph` CLI (installed by `uv sync`). The deploy config is `langgraph.json` at the project root.

Your `LANGSMITH_API_KEY` must have deployment permissions — use a workspace-scoped service key (`lsv2_sk_...`). See [API key guide](#langsmith-api-key-guide).

## Build Your Own Agent

After completing the modules, build your own agent from scratch using the scaffold in `my_agent/`:

| File | Purpose |
|------|---------|
| `my_agent/agent.py` | Your agent — `create_deep_agent` with commented-out sections for tools, subagents, backends, middleware, and HITL |
| `my_agent/AGENTS.md` | Your agent's identity and instructions (editable at runtime) |

The scaffold is already wired up in `langgraph.json`, so you can test it immediately:

```bash
# Run locally with Studio UI
uv run langgraph dev --port 2024
```

Studio will show both `deep_agent` (the one from the modules) and `my_agent` (yours). Select `my_agent` in the Studio dropdown to interact with it.

**Ideas to try:**
- Add a custom tool (database lookup, API call, code execution)
- Add a second subagent with a different specialty
- Wire up `CompositeBackend` so `/memories/` persists across threads
- Add middleware for compliance rules or audit logging
- Add `interrupt_on` for human-in-the-loop approval on sensitive tools
- Create a `my_agent/skills/` directory with a custom skill

## Project Structure

```
deep-agents-interrupt-resume/
├── README.md                       (this file)
├── pyproject.toml                  (dependencies)
├── .env.example
├── langgraph.json                  (registers deep_agent + my_agent for langgraph dev/deploy)
├── utils/
│   ├── models.py                   (model provider config — edit to swap LLMs)
│   ├── search.py                   (Tavily search with retry + fallback)
│   └── langsmith_rules.py          (run rule helpers)
├── agents/
│   ├── research_agent.py           (shared agent factory)
│   └── deep_agent/                 (deployable agent for Module 2)
│       ├── agent.py
│       ├── AGENTS.md
│       ├── deepagents.toml
│       └── skills/
│           ├── linkedin-post/SKILL.md
│           └── twitter-post/SKILL.md
├── my_agent/                       (your agent — build it yourself)
│   ├── agent.py                    (create_deep_agent scaffold)
│   └── AGENTS.md                   (your agent's identity)
├── images/                         (diagrams used by the notebooks)
└── modules/
    ├── 01_deep_agents.ipynb        (Module 1)
    └── 02_deploy.ipynb             (Module 2)
```

## Common Issues

**`langgraph deploy` or tracing fails with 403 Forbidden**
Your API key is likely org-scoped. Create a workspace-scoped service key (`lsv2_sk_...`) or use a personal access token (`lsv2_pt_...`) — see [API key guide](#langsmith-api-key-guide).

**Notebook can't find `utils` / `agents`**
Each module's setup cell prepends `project_root` (the project root) to `sys.path`. If you moved a notebook, update the `Path().resolve().parent` line to point at the project root.

**`my_agent` doesn't appear in Studio**
Make sure `langgraph.json` has the `"my_agent"` entry and you're running `langgraph dev` from the project root.
