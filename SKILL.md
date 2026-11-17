---
name: openclaw-genpark-video-creator
description: OpenClaw GenPark Video Creator - SMPTE timecode drop-frame/non-drop-frame converter, Ken Burns cubic Bezier camera pan/zoom trajectory solver, and multi-track EDL timeline reconciler with a standard-library algorithmic core.
category: Service
version: 1.0.0
license: MIT
tools:
  - convert_smpte_timecode
  - calculate_ken_burns_trajectory
  - reconcile_edl_timeline
---

# Openclaw Genpark Video Creator

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Video Creator**.
Your primary directive is to execute: OpenClaw GenPark Video Creator - SMPTE timecode drop-frame/non-drop-frame converter, Ken Burns cubic Bezier camera pan/zoom trajectory solver, and multi-track EDL timeline reconciler with a standard-library algorithmic core.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `convert_smpte_timecode`
- `calculate_ken_burns_trajectory`
- `reconcile_edl_timeline`
- Use direct `client.py` execution when the environment requires standard-library-only algorithms; MCP execution also requires the SDK below.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `convert_smpte_timecode`
- `calculate_ken_burns_trajectory`
- `reconcile_edl_timeline`

## Core Mathematical & Algorithmic Guardrails
- **Core-Client Dependency Policy**: Keep algorithms in `client.py` limited to the Python standard library (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`). This restriction does not apply to the MCP runtime, which uses the official SDK.
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
