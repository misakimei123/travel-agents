# Travel Agent on Windows with Docker

This guide adapts the local `travel-agents` project to DeerFlow 2.0's current structure.

## What changed

The original `travel-agents` repository uses an older template shape:

- `mcpServers` inside `config.yaml`
- `assistants` inside `config.yaml`
- a `SKILL.md` without DeerFlow 2.0 frontmatter
- `/plan` and `/adjust` described as channel commands

DeerFlow 2.0 expects a different layout:

- custom skills under `skills/custom/`
- custom agents under `backend/.deer-flow/agents/`
- runtime config in `config.yaml`
- MCP servers in `extensions_config.json`

This repo has been prepared to match DeerFlow 2.0.

## Files added for the integration

- `skills/custom/travel-agent/SKILL.md`
- `backend/.deer-flow/agents/travel-agent/config.yaml`
- `backend/.deer-flow/agents/travel-agent/SOUL.md`
- `config.yaml`
- `extensions_config.json`
- `.env`
- `frontend/.env`

## Before first run

1. Edit `.env` and fill at least:
   - `DASHSCOPE_API_KEY`
2. If you want Telegram or Feishu, fill the related tokens and set the channel `enabled` field to `true` in `config.yaml`.
3. If you want Baidu Maps MCP:
   - make sure `mcp_server_baidu_maps` is actually available in the backend runtime, or provide an equivalent external MCP service
   - then set `"enabled": true` for `baidu-maps` in `extensions_config.json`

## Start on Windows

Use Git Bash, not raw PowerShell, for the standard DeerFlow startup flow.

```bash
cd /d/workspace/deer-flow
make docker-init
make docker-start
```

Open:

```text
http://localhost:2026
```

## How to use the travel agent

In the DeerFlow UI:

1. Open the agents page.
2. Select `travel-agent`.
3. Ask in natural language, for example:

```text
请为我规划北京 3 天旅行，预算 3000 元，偏好美食、地铁、亲子。
```

## Important current limits

- `/plan` and `/adjust` are not native DeerFlow channel commands yet.
- The original `travel-agents/mnt/skills/custom/travel-agent/tools/__init__.py` helper registry is not auto-loaded by DeerFlow 2.0.
- The current integration path is:
  - custom skill
  - custom agent
  - optional MCP
  - natural language prompts

If you want `/plan` and `/adjust` to work in Telegram or Feishu, the next step is to extend DeerFlow channel command handling.
