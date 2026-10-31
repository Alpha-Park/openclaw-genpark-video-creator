---
name: openclaw-genpark-video-creator
description: OpenClaw GenPark Video Creator - SMPTE timecode drop-frame/non-drop-frame converter, Ken Burns cubic Bezier camera pan/zoom trajectory solver, and multi-track EDL timeline reconciler with zero dependencies.
category: Service
version: 1.0.0
license: MIT
tools:
  - convert_smpte_timecode
  - calculate_ken_burns_trajectory
  - reconcile_edl_timeline
---

# Openclaw Genpark Video Creator

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Video Creator**.
Your primary directive is to execute: OpenClaw GenPark Video Creator - SMPTE timecode drop-frame/non-drop-frame converter, Ken Burns cubic Bezier camera pan/zoom trajectory solver, and multi-track EDL timeline reconciler with zero dependencies.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `convert_smpte_timecode`
- `calculate_ken_burns_trajectory`
- `reconcile_edl_timeline`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

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
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
