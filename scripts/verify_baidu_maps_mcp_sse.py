"""Verify that DeerFlow can call Baidu Maps through remote SSE MCP.

Run inside the DeerFlow backend container, for example:

    docker exec -i deer-flow-langgraph sh -lc \
      "cd /app/backend && uv run python /app/scripts/verify_baidu_maps_mcp_sse.py"
"""

from __future__ import annotations

import asyncio
import json
import sys

from deerflow.config.extensions_config import ExtensionsConfig
from deerflow.mcp.client import build_servers_config


async def main() -> int:
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
    except ImportError:
        print("FAIL: langchain-mcp-adapters is not installed", file=sys.stderr)
        return 1

    cfg = ExtensionsConfig.from_file()
    server = cfg.mcp_servers.get("baidu-maps")
    if server is None or not server.enabled:
        print("FAIL: baidu-maps MCP server is not enabled", file=sys.stderr)
        return 1

    print(f"CONFIG type={server.type!r} url={server.url!r}")

    if server.type != "sse":
        print(f"FAIL: expected MCP transport 'sse', got {server.type!r}", file=sys.stderr)
        return 1

    if not server.url:
        print("FAIL: baidu-maps SSE URL is empty; env var likely not loaded into the running process", file=sys.stderr)
        return 1

    if "mcp.map.baidu.com/sse" not in server.url:
        print(f"FAIL: unexpected SSE URL {server.url!r}", file=sys.stderr)
        return 1

    servers_config = build_servers_config(cfg)
    client = MultiServerMCPClient(servers_config, tool_name_prefix=True)
    tools = await client.get_tools()

    tool_names = sorted(t.name for t in tools if t.name.startswith("baidu-maps_"))
    print("TOOLS", json.dumps(tool_names, ensure_ascii=False))

    if "baidu-maps_map_search_places" not in tool_names:
        print("FAIL: baidu-maps_map_search_places not found in loaded MCP tools", file=sys.stderr)
        return 1

    search_tool = next(t for t in tools if t.name == "baidu-maps_map_search_places")
    payload = {
        "query": "王府井酒店",
        "region": "北京市",
        "type": "酒店",
    }
    result = await search_tool.ainvoke(payload)
    text = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
    print("RESULT", text[:1200])

    if "results" in text and "[]" in text:
        print("FAIL: hotel-related place search returned empty results", file=sys.stderr)
        return 1

    print("PASS: Baidu Maps SSE MCP tool discovery and hotel search succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
