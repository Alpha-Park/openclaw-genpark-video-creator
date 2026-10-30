# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Video Creator FastMCP Server
"""

import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from client import OpenClawGenParkVideoCreator

mcp = FastMCP("openclaw-genpark-video-creator")
creator = OpenClawGenParkVideoCreator()

@mcp.tool()
def convert_smpte_timecode(
    time_or_frames: str,
    fps: float = 29.97,
    is_drop_frame: bool = True
) -> str:
    """
    Converts between SMPTE timecode string (HH:MM:SS;FF) and absolute frame count / seconds.
    """
    res = creator.convert_smpte_timecode(time_or_frames, fps, is_drop_frame)
    return json.dumps(res, indent=2)

@mcp.tool()
def calculate_ken_burns_trajectory(
    start_rect_json: str,
    end_rect_json: str,
    duration_frames: int = 60,
    easing_curve: str = "cubic_bezier"
) -> str:
    """
    Calculates cubic Bezier smooth camera pan and zoom trajectory between bounding boxes.
    """
    start_rect = json.loads(start_rect_json)
    end_rect = json.loads(end_rect_json)
    res = creator.calculate_ken_burns_trajectory(start_rect, end_rect, duration_frames, easing_curve)
    return json.dumps(res, indent=2)

@mcp.tool()
def reconcile_edl_timeline(
    video_tracks_json: str,
    audio_tracks_json: str,
    target_duration_sec: Optional[float] = None
) -> str:
    """
    Reconciles multi-track EDL timeline: detects overlaps/crossfades, timeline gaps, and audio ducking triggers.
    """
    video_tracks = json.loads(video_tracks_json)
    audio_tracks = json.loads(audio_tracks_json)
    res = creator.reconcile_edl_timeline(video_tracks, audio_tracks, target_duration_sec)
    return json.dumps(res, indent=2)

def main():
    print("Testing Video Creator:")
    print(convert_smpte_timecode("00:01:00;00", 29.97, True))

if __name__ == "__main__":
    main()
