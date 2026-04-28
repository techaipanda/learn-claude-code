# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。

## 概述

这是一个 **harness 工程**学习项目——教你如何为 AI 代理模型构建环境（工具、知识、上下文管理、权限）。模型提供智能；harness 提供代理运行的世界。

仓库包含 12 个渐进式会话（s01–s12）+ 一个 capstone（s_full.py），每个会话都在不修改核心循环的情况下，向基础代理循环叠加一层 harness 机制。

## 命令

### Python 代理
```sh
pip install -r requirements.txt
cp .env.example .env   # 添加你的 ANTHROPIC_API_KEY

python agents/s01_agent_loop.py       # 从这里开始 — 基础循环
python agents/s12_worktree_task_isolation.py
python agents/s_full.py                # 所有机制组合
```

### 测试
```sh
python -m pytest tests/test_agents_smoke.py -q    # 冒烟测试
python -m pytest tests/ -q                        # 所有测试
```

### Web 平台（交互式可视化）
```sh
cd web && npm install && npm run dev   # http://localhost:3000
```

### CI
- Python: `pytest tests/test_agents_smoke.py`
- Web: TypeScript 类型检查 (`tsc --noEmit`) + Next.js 构建 (`next build`)

## 架构

```
learn-claude-code/
├── agents/                    # Python 参考实现
│   ├── s01_agent_loop.py      # 基础 while 循环 + stop_reason
│   ├── s02_tool_use.py        # 工具分发映射
│   ├── s03_todo_write.py      # TodoManager + 计划优先执行
│   ├── s04_subagent.py        # 每个子代理独立 messages[]
│   ├── s05_skill_loading.py    # 通过 tool_result 注入 SKILL.md
│   ├── s06_context_compact.py  # 3层上下文压缩
│   ├── s07_task_system.py      # 基于文件的任务图及依赖
│   ├── s08_background_tasks.py # 守护线程 + 通知队列
│   ├── s09_agent_teams.py      # 持久化队友 + JSONL 邮箱
│   ├── s10_team_protocols.py    # 请求-响应协商有限状态机
│   ├── s11_autonomous_agents.py # 空闲扫描 + 自动认领
│   ├── s12_worktree_task_isolation.py  # 任务 + 工作树协调
│   └── s_full.py               # 集大成者：所有机制组合
├── docs/{en,zh,ja}/           # 文档（3种语言）
├── skills/                    # s05 使用的 SKILL.md 文件
├── web/                       # Next.js 交互式学习平台
└── .github/workflows/         # CI 流水线
```

## 会话进程

| 会话 | 主题 | 核心机制 |
|---------|-------|----------------|
| s01 | Agent 循环 | `while True` + `stop_reason` 决定工具使用还是返回 |
| s02 | 工具使用 | 分发映射：`name → handler`；循环不变 |
| s03 | TodoWrite | 先计划再执行；完成率翻倍 |
| s04 | 子代理 | 每个子代理独立 `messages[]`；主对话保持干净 |
| s05 | 技能加载 | 通过 `tool_result` 加载知识，非系统提示词 |
| s06 | 上下文压缩 | 3层压缩策略实现无限会话 |
| s07 | 任务系统 | 基于文件的 CRUD 任务图及依赖 |
| s08 | 后台任务 | 守护线程；代理继续思考 |
| s09 | 代理团队 | 持久化队友 + 异步 JSONL 邮箱 |
| s10 | 团队协议 | 共享协商规则；关闭/批准有限状态机 |
| s11 | 自主代理 | 空闲扫描 + 自动任务认领 |
| s12 | 工作树隔离 | 每个代理在独立目录工作 |

**核心模式**永不改变：
```python
while True:
    response = client.messages.create(model=MODEL, messages=messages, tools=TOOLS)
    messages.append({"role": "assistant", "content": response.content})
    if response.stop_reason != "tool_use":
        return
    for block in response.content:
        if block.type == "tool_use":
            output = TOOL_HANDLERS[block.name](**block.input)
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})
    messages.append({"role": "user", "content": results})
```

## 关键设计原则

1. **循环保持不变** — harness 机制叠加在代理核心之上，无需修改核心
2. **工具是分发映射中的处理器** — 添加工具只需在 `TOOL_HANDLERS` 中添加一条记录
3. **上下文需要管理，而非无限** — 压缩发生在三层（最近、重要、工作记忆）
4. **子代理获得干净上下文** — 每个子代理用全新的 `messages[]` 避免噪音泄漏
5. **任务持久化目标** — 基于文件的任務图跨越会话边界
6. **团队通过共享协议协调** — JSONL 邮箱配合显式请求/响应模式

## 范围限制

这是一个 0→1 教学项目。特此简化：
- 完整的事件/钩子总线（仅 s12 中有最小的追加式事件流）
- 基于规则的权限治理和信任工作流
- 会话生命周期控制（恢复/分叉）
- 完整 MCP 运行时细节（传输/OAuth/资源订阅/轮询）

## 相关项目

- **[Kode CLI](https://github.com/shareAI-lab/Kode-cli)** — 开源编码代理 CLI，支持技能/LSP
- **[Kode SDK](https://github.com/shareAI-lab/Kode-agent-sdk)** — 嵌入式代理 SDK（无每用户进程开销）
- **[claw0](https://github.com/shareAI-lab/claw0)** — 常驻代理 harness，包含心跳、cron、IM 频道、记忆和灵魂人格
