"""Built-in subagent configurations."""

from .bash_agent import BASH_AGENT_CONFIG
from .budget_agent import BUDGET_AGENT_CONFIG
from .food_agent import FOOD_AGENT_CONFIG
from .general_purpose import GENERAL_PURPOSE_CONFIG
from .hotel_agent import HOTEL_AGENT_CONFIG
from .researcher_agent import RESEARCHER_AGENT_CONFIG
from .route_agent import ROUTE_AGENT_CONFIG

__all__ = [
    "GENERAL_PURPOSE_CONFIG",
    "BASH_AGENT_CONFIG",
    "RESEARCHER_AGENT_CONFIG",
    "ROUTE_AGENT_CONFIG",
    "HOTEL_AGENT_CONFIG",
    "FOOD_AGENT_CONFIG",
    "BUDGET_AGENT_CONFIG",
]

# Registry of built-in subagents
BUILTIN_SUBAGENTS = {
    "general-purpose": GENERAL_PURPOSE_CONFIG,
    "bash": BASH_AGENT_CONFIG,
    "researcher": RESEARCHER_AGENT_CONFIG,
    "route": ROUTE_AGENT_CONFIG,
    "hotel": HOTEL_AGENT_CONFIG,
    "food": FOOD_AGENT_CONFIG,
    "budget": BUDGET_AGENT_CONFIG,
}
