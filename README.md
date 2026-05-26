# Production-Ready Agents

Build a deep agent, deploy it to LangSmith Deployments, then evaluate it.

This technical session covers the harness architecture, tools, subagents, memory, and human-in-the-loop patterns behind Deep Agents and gives you time to build your own. You'll close with deploying your agent to production, and leverage LangSmith tracing and evaluations to observe and improve what you've built.

## Agenda

| # | Module | Duration | Notebook |
|---|--------|----------|----------|
| **1** | Deep Agents — Build a research agent from scratch using `create_deep_agent`. Covers the harness architecture, custom tools, subagents, backends, middleware, human-in-the-loop, and skills. | ~60 min | `modules/01_deep_agents.ipynb` |
| | **Break — Build your own agent!** | | `my_agent/` |
| **2** | Deploy — Ship your agent to LangSmith Deployments with the `langgraph` CLI. Test locally in Studio, validate, and deploy. | ~30 min | `modules/02_deploy.ipynb` |
| | **Break — Test & ship your agent!** | | |
| **3** | LangSmith — Trace your agent, query runs, and build offline evals (LLM-as-judge + trajectory). Set up online evals and annotation queues to score and review production traffic automatically. | ~30 min | `modules/03_langsmith.ipynb` |

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
uv sync
```

### 3. Set environment variables

```bash
cp .env.example .env
```

Open `.env` and set **all three** keys:

| Key | Get one |
|-----|---------|
| `OPENAI_API_KEY` | <https://platform.openai.com> |
| `LANGSMITH_API_KEY` | <https://smith.langchain.com> |
| `TAVILY_API_KEY` | <https://tavily.com> |

> **Using a different model provider?** Edit `utils/models.py` — uncomment the provider you want (Anthropic, Azure OpenAI, AWS Bedrock) and set the matching API key in `.env`. No notebook changes required.

### 4. Verify

```bash
uv run jupyter notebook
```

Open `modules/01_deep_agents.ipynb` and run the first setup cell to confirm everything is working.

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

Your `LANGSMITH_API_KEY` must have deployment permissions (use a `lsv2_sk_...` service key).

## Build Your Own Agent

After completing the modules, build your own agent from scratch using the scaffold in `my_agent/`:

| File | Purpose |
|------|---------|
| `my_agent/agent.py` | Your agent — `create_deep_agent` with commented-out sections for tools, subagents, backends, middleware, and HITL |
| `my_agent/AGENTS.md` | Your agent's identity and instructions (editable at runtime) |

The scaffold is already wired up in `langgraph.json`, so you can test it immediately:

```bash
# Run locally with Studio UI
langgraph dev --port 2024
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
│   └── langsmith_rules.py          (run rule helpers for Module 3)
├── agents/
│   ├── research_agent.py           (shared agent factory — Module 3 imports for eval)
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
    ├── 02_deploy.ipynb             (Module 2)
    └── 03_langsmith.ipynb          (Module 3)
```

## Common Issues

**`langgraph deploy` fails with 403 / permission denied**
Your API key is a personal token. Generate a service key (`lsv2_sk_...`) in LangSmith settings.

**Notebook can't find `utils` / `agents`**
Each module's setup cell prepends `project_root` (the project root) to `sys.path`. If you moved a notebook, update the `Path().resolve().parent` line to point at the project root.

**`my_agent` doesn't appear in Studio**
Make sure `langgraph.json` has the `"my_agent"` entry and you're running `langgraph dev` from the project root.
