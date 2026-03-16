# FloraVoice Voice Assistant — Backend

## Project Overview

This is the FastAPI backend for **FloraVoice**, a voice/chat assistant that handles real-time WebSocket communication between a frontend app and an OpenAI LLM. The AI agent can use tools to interact with the FloraVoice API — for example, creating flower orders on behalf of the user.

## Tech Stack

- **Python 3.14.3** — managed via `uv`
- **FastAPI** — API framework, including WebSocket support
- **openai-agents** — OpenAI Agents SDK for orchestrating the AI agent, tools, and streaming responses
- **uv** — package manager and virtual environment (lockfile: `uv.lock`)

## Architecture

```
app/
├── main.py          # FastAPI app, mounts all routers
└── routers/
    ├── __init__.py
    └── hello.py     # Placeholder health-check route (GET /hello/)
```

### Planned Structure

```
app/
├── main.py
├── agents/
│   ├── flora_agent.py   # Agent definition: model, instructions, tools
│   └── tools/
│       ├── create_order.py   # Tool: create a flower order via FloraVoice API
│       └── ...               # Additional tools (browse catalogue, check status, etc.)
├── routers/
│   ├── ws.py            # WebSocket endpoint — bridges frontend <-> agent
│   └── hello.py
└── config.py            # Settings loaded from environment
```

## WebSocket Flow

1. Frontend connects to `ws://.../ws`
2. Backend creates an OpenAI Agents `Runner` session
3. User messages are forwarded to the agent; streaming deltas are sent back over the socket
4. The agent may invoke tools (e.g. `create_order`) mid-conversation
5. Tool results are returned to the agent; final response is streamed to the frontend

## Agent Tools

### `create_order`
Calls the FloraVoice REST API to create a flower order. Required parameters collected from the conversation:
- recipient name / address
- flower selection (product ID or description)
- delivery date
- any special notes

Additional tools to consider:
- `list_products` — browse available flower arrangements
- `get_order_status` — look up an existing order
- `cancel_order` — cancel a pending order

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key used by the Agents SDK |
| `FLORA_API_BASE_URL` | Base URL for the FloraVoice orders API |
| `FLORA_API_KEY` | Auth key for the FloraVoice API (if required) |

Copy `.env.example` to `.env` (never commit `.env`).

## Running Locally

```bash
uv sync                        # install dependencies
uv run fastapi dev app/main.py # start dev server with hot-reload
```

The dev server runs at `http://localhost:8000`.

## Key Conventions

- Use `async def` for all route handlers and tool functions — the Agents SDK is fully async
- One router per domain area; mount routers in `main.py`
- Tool functions should be plain async Python functions decorated with `@function_tool` from the Agents SDK
- Keep agent instructions in `agents/flora_agent.py`; do not scatter them across tool files
- Validate all user-supplied data with Pydantic models before passing to the FloraVoice API
