"""Build your own deep agent.

This is your starting scaffold. Customize the system prompt, add tools,
configure subagents, backends, middleware, and skills to make it your own.

Once you're ready, test it locally with:

    langgraph dev --port 2024

This file is already registered in langgraph.json as "my_agent",
so Studio will pick it up automatically.
"""

from datetime import datetime

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StoreBackend, StateBackend
from langchain_core.tools import tool

from utils.models import model
from utils.search import resilient_tavily_search

# ------------------------------------------------------------------ #
# 1. Define your tools
# ------------------------------------------------------------------ #

@tool(parse_docstring=True)
def tavily_search(query: str) -> str:
    """Search the web for information on a given query.

    Args:
        query: Search query to execute.
    """
    return resilient_tavily_search(query, max_retries=2)


# Add more tools here:
#
# @tool(parse_docstring=True)
# def my_custom_tool(arg: str) -> str:
#     """Description of what this tool does.
#
#     Args:
#         arg: What this argument is for.
#     """
#     return "result"


# ------------------------------------------------------------------ #
# 2. Define subagents (optional)
# ------------------------------------------------------------------ #

research_subagent = {
    "name": "research-agent",
    "description": "Delegate research tasks. Give one topic at a time.",
    "system_prompt": (
        f"You are a research assistant. Today is {datetime.now().strftime('%Y-%m-%d')}.\n"
        "Use tools to gather information. Limit to 3 search calls."
    ),
    "tools": [tavily_search],
}

# Add more subagents here:
#
# writer_subagent = {
#     "name": "writer-agent",
#     "description": "Delegate writing tasks.",
#     "system_prompt": "You are a skilled writer...",
#     "tools": [],
# }


# ------------------------------------------------------------------ #
# 3. Configure backends (optional)
# ------------------------------------------------------------------ #
# Uncomment to add persistent memory across threads:
#
# from langgraph.store.memory import InMemoryStore
# store = InMemoryStore()
#
# backend = CompositeBackend(
#     default=StateBackend(),
#     routes={
#         "/memories/": StoreBackend(
#             store=store,
#             namespace=lambda rt: ("memories", "shared"),
#         ),
#     },
# )


# ------------------------------------------------------------------ #
# 4. Configure middleware (optional)
# ------------------------------------------------------------------ #
# from langchain.agents.middleware import wrap_model_call, wrap_tool_call
#
# @wrap_tool_call
# def audit_trail(request, handler):
#     """Log every tool call."""
#     print(f"Tool called: {request.tool_call['name']}")
#     return handler(request)


# ------------------------------------------------------------------ #
# 5. Create the agent
# ------------------------------------------------------------------ #

agent = create_deep_agent(
    model=model,
    tools=[tavily_search],
    system_prompt="You are a helpful assistant.",
    subagents=[research_subagent],
    memory=["./AGENTS.md"],
    # skills=["./skills/"],          # uncomment after adding a skills/ directory
    # backend=backend,               # uncomment after configuring backends above
    # store=store,                   # uncomment after configuring backends above
    # middleware=[audit_trail],      # uncomment after configuring middleware above
    # interrupt_on={"write_file": True},  # uncomment for human-in-the-loop
)
