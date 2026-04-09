# DeerFlow Travel Agent 配置指南：MiniMax、飞书与百度地图 MCP

本文档基于你本地的 DeerFlow 2.0 代码结构整理，目标是解决 3 件事：

1. 用 MiniMax API 作为 DeerFlow 的主对话模型
2. 正确配置飞书渠道
3. 正确配置百度地图 MCP Server

同时本文档也说明这些配置分别应该改 **哪个文件**，以及在 Win11 上应该怎么启动服务。

## 先说结论

在当前这份 DeerFlow 2.0 里：

- **模型配置** 改 [config.yaml](/D:/workspace/deer-flow/config.yaml)
- **飞书渠道配置** 改 [config.yaml](/D:/workspace/deer-flow/config.yaml)
- **MCP Server 配置** 改 [extensions_config.json](/D:/workspace/deer-flow/extensions_config.json)
- **密钥和令牌** 改 [\.env](/D:/workspace/deer-flow/.env)
- **前端 env 文件** 一般不用动，只要保留 [frontend/.env](/D:/workspace/deer-flow/frontend/.env) 存在即可

## 1. MiniMax 应该怎么接到 DeerFlow

### 1.1 为什么这里不用 `M2-her` 作为默认模型

MiniMax 官方“文本对话”文档说明，`M2-her` 是一个“专为对话场景优化”的模型，更偏角色扮演和多轮聊天。  
来源：MiniMax 官方文本对话文档 [文本对话](https://platform.minimaxi.com/docs/guides/text-chat)

但 DeerFlow 不是普通聊天壳，它是一个 **agent harness**，会调用工具、skill、subagent、MCP。  
MiniMax 官方“工具使用 & 交错思维链”文档说明，`MiniMax-M2.7` 是一款 Agentic Model，适合工具使用场景。  
来源：MiniMax 官方文档 [工具使用 & 交错思维链](https://platform.minimaxi.com/docs/guides/text-m2-function-call)

因此这里的推荐配置是：

- 如果你是要让 DeerFlow 真正跑 agent、MCP、旅游规划：**推荐 `MiniMax-M2.7`**
- 如果你只是想把它当普通聊天机器人：可以改成 `M2-her`

这是一条基于 MiniMax 官方文档和 DeerFlow 当前架构做出的推荐性判断。

### 1.2 DeerFlow 推荐怎么接 MiniMax

MiniMax 官方“OpenAI API 兼容”文档给出的国内版配置是：

- `OPENAI_BASE_URL=https://api.minimaxi.com/v1`
- `OPENAI_API_KEY=<YOUR_API_KEY>`
- 示例模型为 `MiniMax-M2.7`

来源：MiniMax 官方文档 [OpenAI API 兼容](https://platform.minimaxi.com/docs/api-reference/text-openai-api)

DeerFlow 当前 `config.example.yaml` 里也已经预留了 MiniMax 的 OpenAI-compatible 配置示例。  
因此在 DeerFlow 里，最直接的接法就是：

- `use: langchain_openai:ChatOpenAI`
- `base_url: https://api.minimaxi.com/v1`
- `api_key: $MINIMAX_API_KEY`
- `model: MiniMax-M2.7`

### 1.3 现在应该改哪个文件

改 [config.yaml](/D:/workspace/deer-flow/config.yaml)。

当前已经改成了：

```yaml
models:
  - name: minimax-m2.7
    display_name: MiniMax M2.7 (CN)
    use: langchain_openai:ChatOpenAI
    model: MiniMax-M2.7
    api_key: $MINIMAX_API_KEY
    base_url: https://api.minimaxi.com/v1
    request_timeout: 600.0
    max_retries: 2
    max_tokens: 8192
    temperature: 1.0
    supports_vision: true
    supports_thinking: true
```

### 1.4 如果你想改成 `M2-her`

把 [config.yaml](/D:/workspace/deer-flow/config.yaml) 里的 `models` 改成下面这样即可：

```yaml
models:
  - name: minimax-m2-her
    display_name: MiniMax M2-her (CN)
    use: langchain_openai:ChatOpenAI
    model: M2-her
    api_key: $MINIMAX_API_KEY
    base_url: https://api.minimaxi.com/v1
    request_timeout: 600.0
    max_retries: 2
    max_tokens: 2048
    temperature: 1.0
```

然后还要把 [travel-agent agent config](/D:/workspace/deer-flow/backend/.deer-flow/agents/travel-agent/config.yaml) 里的模型名一起改掉：

```yaml
model: minimax-m2-her
```

但如果你后面要依赖工具调用、MCP、复杂旅游规划，我仍然建议你保留 `MiniMax-M2.7`。

### 1.5 MiniMax 的密钥改哪里

改 [\.env](/D:/workspace/deer-flow/.env)：

```bash
MINIMAX_API_KEY=your_real_minimax_api_key
```

## 2. 飞书配置应该改哪里

飞书相关配置在 DeerFlow 里属于 **channel 配置**，不放在 MCP 文件里。  
应改 [config.yaml](/D:/workspace/deer-flow/config.yaml) 和 [\.env](/D:/workspace/deer-flow/.env)。

### 2.1 `config.yaml` 里的飞书配置

当前已经预留：

```yaml
channels:
  session:
    assistant_id: travel-agent
    config:
      recursion_limit: 100
    context:
      thinking_enabled: true
      is_plan_mode: false
      subagent_enabled: true

  feishu:
    enabled: false
    app_id: $FEISHU_APP_ID
    app_secret: $FEISHU_APP_SECRET
    verification_token: $FEISHU_VERIFICATION_TOKEN
    encrypt_key: $FEISHU_ENCRYPT_KEY
    domain: https://open.feishu.cn
    mode: webhook
    webhook_port: 8080
    webhook_path: /feishu/webhook
```

你真正需要改的是这几项：

1. 把 `enabled: false` 改成 `enabled: true`
2. 保持 `assistant_id: travel-agent`，这样飞书发来的消息会路由到旅游 agent
3. 如果你使用国际版 Lark，把 `domain` 改成：

```yaml
domain: https://open.larksuite.com
```

### 2.2 `.env` 里的飞书密钥

改 [\.env](/D:/workspace/deer-flow/.env)：

```bash
FEISHU_APP_ID=your_real_app_id
FEISHU_APP_SECRET=your_real_app_secret
FEISHU_VERIFICATION_TOKEN=your_real_verification_token
FEISHU_ENCRYPT_KEY=your_real_encrypt_key
```

### 2.3 这些飞书字段从哪里来

你需要在飞书开放平台创建应用并启用 Bot 能力。  
DeerFlow 自己的 README 也说明了 Feishu / Lark 需要 `app_id`、`app_secret`，并支持国内版 `open.feishu.cn` 与国际版 `open.larksuite.com`。  
来源：DeerFlow 仓库文档 [README_zh.md](/D:/workspace/deer-flow/README_zh.md#L252)

### 2.4 当前这份配置下，飞书消息会进哪个 agent

是 `travel-agent`。  
因为 `channels.session.assistant_id` 已经指向了 `travel-agent`。DeerFlow 会把它转成 `lead_agent + agent_name` 的运行方式。

## 3. 百度地图 MCP Server 配置应该改哪里

这部分不要再改 `config.yaml`。  
在 DeerFlow 2.0 当前结构里，MCP Server 应该改 [extensions_config.json](/D:/workspace/deer-flow/extensions_config.json)。

这也是 DeerFlow 官方 MCP 文档要求的方式。  
来源：DeerFlow 文档 [MCP_SERVER.md](/D:/workspace/deer-flow/backend/docs/MCP_SERVER.md#L3)

### 3.1 当前配置文件位置

当前 MCP 配置在：

[extensions_config.json](/D:/workspace/deer-flow/extensions_config.json)

内容是：

```json
{
  "mcpServers": {
    "baidu-maps": {
      "enabled": false,
      "type": "stdio",
      "command": "python",
      "args": [
        "-m",
        "mcp_server_baidu_maps"
      ],
      "env": {
        "BAIDU_MAPS_API_KEY": "$BAIDU_MAPS_API_KEY"
      },
      "description": "Baidu Maps MCP server for POI lookup and route planning"
    }
  },
  "skills": {
    "travel-agent": {
      "enabled": true
    }
  }
}
```

### 3.2 为什么这里不用 `BAIDU_MAP_AK`

你原来的 `travel-agents` 模板里写的是 `BAIDU_MAP_AK`，但如果你现在使用的是 Python 版 `mcp_server_baidu_maps`，官方 PyPI 示例和 GitHub README 用的是：

- `BAIDU_MAPS_API_KEY`

来源：

- PyPI: [mcp-server-baidu-maps](https://pypi.org/project/mcp-server-baidu-maps/)
- GitHub: [baidu-maps/mcp](https://github.com/baidu-maps/mcp)

因为我们当前配置走的是：

```json
"command": "python",
"args": ["-m", "mcp_server_baidu_maps"]
```

所以这里我已经改成官方 Python MCP server 对应的环境变量名 `BAIDU_MAPS_API_KEY`。

### 3.3 `.env` 里的百度地图密钥

改 [\.env](/D:/workspace/deer-flow/.env)：

```bash
BAIDU_MAPS_API_KEY=your_real_baidu_maps_key
```

### 3.4 什么时候把 MCP 改成启用

只有在你已经满足下面条件后，再把：

```json
"enabled": false
```

改成：

```json
"enabled": true
```

前提条件：

1. 你的运行环境里真的能执行 `python -m mcp_server_baidu_maps`
2. 对应 Python 运行环境里已经安装了 `mcp_server_baidu_maps`
3. 还需要一个可用的 Python 解释器

### 3.5 你当前环境的一个现实问题

你这个 Win11 当前会话里，`python` 命令本身不可用。  
这意味着即使把 `extensions_config.json` 里的 `baidu-maps` 打开，容器或者宿主环境如果没有对应 Python 运行时和依赖，也会起不来。

所以更稳妥的顺序是：

1. 先把 DeerFlow + MiniMax 跑起来
2. 确认 `travel-agent` 能工作
3. 再补百度 MCP 运行环境
4. 最后再开启 `baidu-maps.enabled`

## 4. 服务启动前，你最少要改哪些文件

### 必改

1. [\.env](/D:/workspace/deer-flow/.env)
   - `MINIMAX_API_KEY`

### 按需改

2. [config.yaml](/D:/workspace/deer-flow/config.yaml)
   - `channels.feishu.enabled`
   - `channels.telegram.enabled`
   - 如果你要切换模型，也改这里

3. [extensions_config.json](/D:/workspace/deer-flow/extensions_config.json)
   - `baidu-maps.enabled`

## 5. 推荐修改顺序

### 方案 A：先跑通 DeerFlow + MiniMax

推荐顺序：

1. 填 [\.env](/D:/workspace/deer-flow/.env) 里的 `MINIMAX_API_KEY`
2. 保持飞书关闭
3. 保持百度 MCP 关闭
4. 启动 DeerFlow
5. 先在 Web UI 里测试旅游 agent

这是最稳的路径。

### 方案 B：加上飞书

在方案 A 的基础上，再做：

1. 填飞书的 4 个密钥
2. 把 [config.yaml](/D:/workspace/deer-flow/config.yaml) 里 `channels.feishu.enabled` 改为 `true`
3. 重启 DeerFlow

### 方案 C：再加上百度地图 MCP

在方案 B 或 A 的基础上，再做：

1. 确认 `mcp_server_baidu_maps` 可运行
2. 填 [\.env](/D:/workspace/deer-flow/.env) 里的 `BAIDU_MAPS_API_KEY`
3. 把 [extensions_config.json](/D:/workspace/deer-flow/extensions_config.json) 里 `baidu-maps.enabled` 改为 `true`
4. 重启 DeerFlow

## 6. Win11 上怎么启动

你前面已经确认过，`make docker-init` / `make docker-start` 最终调用的是 bash 脚本。  
所以在 Win11 上，推荐用 **Git Bash**。

### 6.1 推荐启动方式

打开 Git Bash，执行：

```bash
cd /d/workspace/deer-flow
make docker-init
make docker-start
```

如果 Git Bash 里没有 `make`，就直接执行脚本：

```bash
cd /d/workspace/deer-flow
./scripts/docker.sh init
./scripts/docker.sh start
```

### 6.2 如果你想从 PowerShell 触发

可以这样调用 Git Bash：

```powershell
& "C:\Program Files\Git\bin\bash.exe" -lc "cd /d/workspace/deer-flow && ./scripts/docker.sh init && ./scripts/docker.sh start"
```

## 7. 启动后怎么验证

启动完成后，打开：

```text
http://localhost:2026
```

然后：

1. 进入 Agents 页面
2. 选择 `travel-agent`
3. 发送：

```text
请为我规划北京 3 天旅行，预算 3000 元，偏好美食、地铁、亲子。
```

### 预期结果

- 如果 MiniMax 配置正确：会正常返回旅游规划
- 如果飞书启用了但配置不对：渠道服务会报鉴权或连接错误
- 如果百度 MCP 启用了但依赖没装好：MCP 工具加载会失败，但 DeerFlow 主体仍可能启动

## 8. 当前配置的实际建议

如果你现在的目标是“先用起来”，建议按下面顺序：

1. 先只启用 MiniMax
2. 然后启用飞书
3. 最后再启用百度地图 MCP

这是因为 MiniMax 是 DeerFlow 主模型，飞书只是入口渠道，百度 MCP 则是额外能力，依赖链最长，最容易卡住。

## 参考资料

- MiniMax 官方文本对话文档：<https://platform.minimaxi.com/docs/guides/text-chat>
- MiniMax 官方 OpenAI API 兼容文档：<https://platform.minimaxi.com/docs/api-reference/text-openai-api>
- MiniMax 官方工具使用文档：<https://platform.minimaxi.com/docs/guides/text-m2-function-call>
- DeerFlow 中文 README： [README_zh.md](/D:/workspace/deer-flow/README_zh.md)
- DeerFlow MCP 文档： [MCP_SERVER.md](/D:/workspace/deer-flow/backend/docs/MCP_SERVER.md)
- 百度地图 MCP GitHub：<https://github.com/baidu-maps/mcp>
- 百度地图 MCP PyPI：<https://pypi.org/project/mcp-server-baidu-maps/>
