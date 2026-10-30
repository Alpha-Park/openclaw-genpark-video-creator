# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Video Creator Client
Zero-dependency SMPTE timecode converter, Ken Burns cubic Bezier camera trajectory solver, and EDL timeline reconciler.
"""

import math
from typing import Dict, List, Any, Optional

class OpenClawGenParkVideoCreator:
    """
    Solves SMPTE 12M drop-frame/non-drop-frame timecodes, cubic Bezier camera trajectories,
    and reconciles multi-track EDL (Edit Decision List) timelines.
    """

    def convert_smpte_timecode(
        self,
        time_or_frames: Any,
        fps: float = 29.97,
        is_drop_frame: bool = True
    ) -> Dict[str, Any]:
        """
        Converts between SMPTE timecode string (HH:MM:SS;FF or HH:MM:SS:FF) and absolute frame count / seconds.
        Implements SMPTE 12M drop-frame compensation for NTSC (29.97 fps drops 2 frames/min except decaminutes).
        """
        if isinstance(time_or_frames, str):
            # Parse timecode string
            clean_tc = time_or_frames.strip().replace(";", ":")
            parts = clean_tc.split(":")
            if len(parts) != 4:
                raise ValueError("Timecode must be in format HH:MM:SS:FF or HH:MM:SS;FF")
            
            h, m, s, f = [int(p) for p in parts]
            total_minutes = 60 * h + m
            
            if is_drop_frame and abs(fps - 29.97) < 0.1:
                # 29.97 fps drop frame: drop 2 frames every minute except minutes % 10 == 0
                drop_frames = 2 * (total_minutes - (total_minutes // 10))
                nominal_fps = 30
                frame_number = (total_minutes * 60 + s) * nominal_fps + f - drop_frames
            else:
                frame_number = int(round((total_minutes * 60 + s) * fps + f))
            
            total_sec = frame_number / fps
        else:
            frame_number = int(time_or_frames)
            if frame_number < 0:
                raise ValueError("Frame count must be non-negative.")
            
            total_sec = frame_number / fps

            if is_drop_frame and abs(fps - 29.97) < 0.1:
                # Reverse drop-frame calculation
                nominal_fps = 30
                drop_per_min = 2
                frames_per_10min = 17982  # (10 * 60 * 30) - 18
                frames_per_min = 1798     # (60 * 30) - 2

                d = frame_number // frames_per_10min
                m_rem = frame_number % frames_per_10min

                if m_rem >= frames_per_min:
                    m_idx = (m_rem - drop_per_min) // frames_per_min
                    adjusted_frames = frame_number + drop_per_min * (9 * d + m_idx)
                else:
                    adjusted_frames = frame_number + drop_per_min * 9 * d

                f = adjusted_frames % nominal_fps
                s = (adjusted_frames // nominal_fps) % 60
                m = ((adjusted_frames // nominal_fps) // 60) % 60
                h = ((adjusted_frames // nominal_fps) // 60) // 60
            else:
                total_s_int = int(frame_number // fps)
                f = int(frame_number % fps)
                s = total_s_int % 60
                m = (total_s_int // 60) % 60
                h = (total_s_int // 3600)

        delimiter = ";" if is_drop_frame else ":"
        tc_str = f"{h:02d}:{m:02d}:{s:02d}{delimiter}{f:02d}"

        return {
            "frame_number": frame_number,
            "smpte_timecode": tc_str,
            "total_seconds": round(total_sec, 4),
            "total_milliseconds": round(total_sec * 1000.0, 2),
            "fps": fps,
            "is_drop_frame": is_drop_frame
        }

    def calculate_ken_burns_trajectory(
        self,
        start_rect: Dict[str, float],
        end_rect: Dict[str, float],
        duration_frames: int = 60,
        easing_curve: str = "cubic_bezier"
    ) -> Dict[str, Any]:
        """
        Calculates cubic Bezier smooth camera pan and zoom trajectory between bounding boxes.
        Standard smooth cubic bezier: (0.42, 0.0, 0.58, 1.0)
        """
        if duration_frames <= 0:
            raise ValueError("Duration frames must be greater than zero.")

        # Ease-in-out cubic bezier approximation: 3*(1-t)*t^2 * P2 + t^3
        def bezier_ease(t: float) -> float:
            # P0 = 0, P1 = 0.25, P2 = 0.25, P3 = 1 (smooth S-curve)
            return t * t * (3.0 - 2.0 * t)

        w0, h0 = start_rect.get("w", 1920.0), start_rect.get("h", 1080.0)
        x0, y0 = start_rect.get("x", 0.0), start_rect.get("y", 0.0)

        w1, h1 = end_rect.get("w", 1280.0), end_rect.get("h", 720.0)
        x1, y1 = end_rect.get("x", 320.0), end_rect.get("y", 180.0)

        zoom_ratio = round(w1 / (w0 + 1e-9), 3)

        keyframes = []
        step_stride = max(1, duration_frames // 10)

        for f in range(0, duration_frames + 1, step_stride):
            t = f / float(duration_frames)
            e = bezier_ease(t)
            cur_x = round(x0 + (x1 - x0) * e, 2)
            cur_y = round(y0 + (y1 - y0) * e, 2)
            cur_w = round(w0 + (w1 - w0) * e, 2)
            cur_h = round(h0 + (h1 - h0) * e, 2)
            
            keyframes.append({
                "frame": f,
                "progress_t": round(t, 3),
                "eased_progress": round(e, 3),
                "x": cur_x,
                "y": cur_y,
                "w": cur_w,
                "h": cur_h
            })

        # Calculate average pan velocity in pixels/frame
        total_pan_dist = math.hypot(x1 - x0, y1 - y0)
        avg_velocity_px_per_frame = round(total_pan_dist / duration_frames, 2)

        return {
            "start_rect": start_rect,
            "end_rect": end_rect,
            "duration_frames": duration_frames,
            "easing_curve": easing_curve,
            "zoom_ratio": zoom_ratio,
            "pan_distance_px": round(total_pan_dist, 2),
            "avg_velocity_px_per_frame": avg_velocity_px_per_frame,
            "sampled_keyframes": keyframes
        }

    def reconcile_edl_timeline(
        self,
        video_tracks: List[Dict[str, Any]],
        audio_tracks: List[Dict[str, Any]],
        target_duration_sec: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Reconciles multi-track EDL timeline: detects overlaps/crossfades, timeline gaps, and audio ducking triggers.
        """
        # Sort video clips by in_point
        v_sorted = sorted(video_tracks, key=lambda c: c.get("start_sec", 0.0))
        gaps = []
        crossfades = []
        curr_v_end = 0.0

        for idx, clip in enumerate(v_sorted):
            c_start = clip.get("start_sec", 0.0)
            c_end = clip.get("end_sec", c_start + clip.get("duration_sec", 0.0))
            
            if idx > 0 and c_start > curr_v_end + 0.01:
                gaps.append({
                    "track": "video",
                    "start_sec": round(curr_v_end, 2),
                    "end_sec": round(c_start, 2),
                    "gap_duration_sec": round(c_start - curr_v_end, 2)
                })
            elif idx > 0 and c_start < curr_v_end:
                crossfades.append({
                    "track": "video",
                    "from_clip": v_sorted[idx - 1].get("clip_id", f"v_{idx-1}"),
                    "to_clip": clip.get("clip_id", f"v_{idx}"),
                    "overlap_duration_sec": round(curr_v_end - c_start, 2)
                })
            curr_v_end = max(curr_v_end, c_end)

        # Check audio ducking when dialogue clips overlap with background music
        ducking_events = []
        dialogue_tracks = [a for a in audio_tracks if a.get("role", "") in ["dialogue", "voiceover", "speech"]]
        bgm_tracks = [a for a in audio_tracks if a.get("role", "") in ["bgm", "music", "ambient"]]

        for d in dialogue_tracks:
            d_start = d.get("start_sec", 0.0)
            d_end = d.get("end_sec", d_start + d.get("duration_sec", 0.0))
            for b in bgm_tracks:
                b_start = b.get("start_sec", 0.0)
                b_end = b.get("end_sec", b_start + b.get("duration_sec", 0.0))
                # Check overlap
                overlap_start = max(d_start, b_start)
                overlap_end = min(d_end, b_end)
                if overlap_end > overlap_start:
                    ducking_events.append({
                        "bgm_clip_id": b.get("clip_id", "bgm"),
                        "dialogue_clip_id": d.get("clip_id", "dialogue"),
                        "duck_start_sec": round(overlap_start, 2),
                        "duck_end_sec": round(overlap_end, 2),
                        "recommended_attenuation_db": -12.0
                    })

        total_audio_end = max([a.get("end_sec", a.get("start_sec", 0.0) + a.get("duration_sec", 0.0)) for a in audio_tracks], default=0.0)
        final_duration_sec = max(curr_v_end, total_audio_end)
        compliance_target = True if (target_duration_sec is None or abs(final_duration_sec - target_duration_sec) < 1.0) else False

        return {
            "total_timeline_duration_sec": round(final_duration_sec, 2),
            "video_clip_count": len(video_tracks),
            "audio_clip_count": len(audio_tracks),
            "timeline_gaps_detected": gaps,
            "crossfade_overlaps": crossfades,
            "audio_ducking_events": ducking_events,
            "target_duration_sec": target_duration_sec,
            "is_target_compliant": compliance_target
        }
