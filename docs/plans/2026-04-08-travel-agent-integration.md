# Travel Agent Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the local `travel-agents` project into DeerFlow 2.0 on Windows with a Docker-friendly layout that matches DeerFlow's current extension model.

**Architecture:** The integration uses DeerFlow's native extension points instead of the older template structure from `travel-agents`. A custom skill lives under `skills/custom/`, a custom agent lives under `backend/.deer-flow/agents/`, runtime config lives in `config.yaml`, and MCP wiring lives in `extensions_config.json`.

**Tech Stack:** DeerFlow 2.0, Docker Compose dev environment, LangChain `ChatOpenAI` compatible model config, custom skills, custom agents, MCP extensions.

---

### Task 1: Create the DeerFlow-native integration skeleton

**Files:**
- Create: `D:\workspace\deer-flow\skills\custom\travel-agent\SKILL.md`
- Create: `D:\workspace\deer-flow\backend\.deer-flow\agents\travel-agent\config.yaml`
- Create: `D:\workspace\deer-flow\backend\.deer-flow\agents\travel-agent\SOUL.md`

- [ ] **Step 1: Add a valid DeerFlow custom skill**

Write a `SKILL.md` with YAML frontmatter, a valid `travel-agent` name, and instructions tailored to DeerFlow 2.0.

- [ ] **Step 2: Add a custom agent entry**

Write `backend/.deer-flow/agents/travel-agent/config.yaml` so DeerFlow can surface the custom agent in the UI and route requests through `agent_name`.

- [ ] **Step 3: Add the agent identity**

Write `backend/.deer-flow/agents/travel-agent/SOUL.md` so the custom agent has stable behavior and fallback rules when MCP tools are unavailable.

### Task 2: Add local runtime configuration

**Files:**
- Create: `D:\workspace\deer-flow\config.yaml`
- Create: `D:\workspace\deer-flow\extensions_config.json`
- Create: `D:\workspace\deer-flow\.env`
- Create: `D:\workspace\deer-flow\frontend\.env`

- [ ] **Step 1: Add a Docker-oriented DeerFlow config**

Write `config.yaml` with:
- a `qwen-plus` model pointing at DashScope
- DeerFlow core tool groups and sandbox tools
- Docker sandbox provider settings
- a default mobile-channel session routing to `travel-agent`
- disabled Telegram and Feishu channel stubs

- [ ] **Step 2: Add extension config**

Write `extensions_config.json` with:
- the `travel-agent` skill enabled
- a prepared `baidu-maps` MCP server definition
- MCP disabled by default until the runtime package or external service is available

- [ ] **Step 3: Add env templates**

Write root `.env` and `frontend/.env` so Docker Compose can start without missing env-file errors, while still requiring the user to fill the real secrets.

### Task 3: Document how to run it on Windows

**Files:**
- Create: `D:\workspace\deer-flow\docs\travel-agent-windows-docker.md`

- [ ] **Step 1: Document Windows + Docker startup**

Explain:
- why this integration differs from the original `travel-agents` README
- how to fill `.env`
- how to decide whether to enable `baidu-maps`
- how to run `make docker-init` and `make docker-start`
- how to use the `travel-agent` in the Web UI

- [ ] **Step 2: Call out known gaps**

Document that:
- `/plan` and `/adjust` are not channel commands in DeerFlow yet
- the old `TOOLS_REGISTRY` Python helpers are not auto-loaded by DeerFlow 2.0
- natural language prompts are the supported first path

### Task 4: Verify the integration structure

**Files:**
- Verify: `D:\workspace\deer-flow\skills\custom\travel-agent\SKILL.md`
- Verify: `D:\workspace\deer-flow\backend\.deer-flow\agents\travel-agent\config.yaml`
- Verify: `D:\workspace\deer-flow\config.yaml`
- Verify: `D:\workspace\deer-flow\extensions_config.json`

- [ ] **Step 1: Validate JSON and YAML syntax**

Run lightweight local parsing commands only. Do not start Docker services in this task.

- [ ] **Step 2: Validate skill discoverability assumptions**

Confirm the skill has valid frontmatter and the custom agent points to the correct skill name.
