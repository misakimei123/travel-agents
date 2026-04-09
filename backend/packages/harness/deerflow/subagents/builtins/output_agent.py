"""Output subagent configuration for travel planning."""

from deerflow.subagents.config import SubagentConfig

OUTPUT_AGENT_CONFIG = SubagentConfig(
    name="output",
    description="""Formatting specialist for turning travel findings into a clean final itinerary.

Use this subagent when the work is complete and needs polished presentation.""",
    system_prompt="""You are the travel Output Agent.

Format the final travel answer clearly and compactly in Simplified Chinese.

Focus on:
- one coherent final itinerary
- readable daily schedule blocks
- concise notes instead of raw research dumps
- keeping assumptions and fallback sections explicit

Return:
1. Final itinerary draft
2. Budget summary
3. Stay and dining recommendations
4. A short assumptions or fallback section
""",
    tools=[],
    disallowed_tools=["task", "ask_clarification", "present_files"],
    model="inherit",
    max_turns=8,
)
