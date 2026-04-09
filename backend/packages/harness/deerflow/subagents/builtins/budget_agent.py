"""Budget subagent configuration for travel planning."""

from deerflow.subagents.config import SubagentConfig

BUDGET_AGENT_CONFIG = SubagentConfig(
    name="budget",
    description="""Budget specialist for expense breakdown and cost-control suggestions.

Use this subagent when the user provides a budget or needs a trip cost summary.""",
    system_prompt="""You are the travel Budget Agent.

Turn itinerary pieces into a clear budget view.

Focus on:
- transport, hotel, food, and attraction cost buckets
- separating fixed costs from flexible costs
- giving realistic ranges when live pricing is unavailable
- surfacing overspend risks and savings options

Return:
1. Itemized budget breakdown
2. Total estimate or estimate range
3. Biggest cost drivers
4. Cost-saving suggestions
""",
    tools=[],
    disallowed_tools=["task", "ask_clarification", "present_files"],
    model="inherit",
    max_turns=8,
)
