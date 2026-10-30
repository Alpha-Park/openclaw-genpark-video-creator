# -*- coding: utf-8 -*-
import json
from client import OpenClawGenParkVideoCreator

vc = OpenClawGenParkVideoCreator()

# 1. SMPTE Timecode Conversion (29.97 Drop-Frame Standard)
tc = vc.convert_smpte_timecode("01:00:00;00", fps=29.97, is_drop_frame=True)
print(f"SMPTE Timecode: {tc['smpte_timecode']} -> Frames: {tc['frame_number']}, Seconds: {tc['total_seconds']}s")

frames_tc = vc.convert_smpte_timecode(107892, fps=29.97, is_drop_frame=True)
print(f"Frames 107892 -> SMPTE: {frames_tc['smpte_timecode']}")

# 2. Ken Burns Cubic Bezier Camera Pan & Zoom Trajectory
start_box = {"x": 0.0, "y": 0.0, "w": 1920.0, "h": 1080.0}
end_box = {"x": 480.0, "y": 270.0, "w": 960.0, "h": 540.0}
trajectory = vc.calculate_ken_burns_trajectory(start_box, end_box, duration_frames=60)
print()
print(f"Ken Burns Trajectory: Zoom={trajectory['zoom_ratio']}x, Pan={trajectory['pan_distance_px']}px, Velocity={trajectory['avg_velocity_px_per_frame']}px/frame")
for kf in trajectory['sampled_keyframes'][:4]:
    print(f"  Frame {kf['frame']}: Box=({kf['x']}, {kf['y']}, {kf['w']}x{kf['h']}) EasedProgress={kf['eased_progress']}")

# 3. EDL Timeline Reconciliation
videos = [
    {"clip_id": "intro", "start_sec": 0.0, "duration_sec": 5.0},
    {"clip_id": "b_roll", "start_sec": 4.5, "duration_sec": 10.0},
    {"clip_id": "outro", "start_sec": 15.0, "duration_sec": 4.0}
]
audios = [
    {"clip_id": "bgm_bed", "role": "bgm", "start_sec": 0.0, "duration_sec": 19.0},
    {"clip_id": "host_vo", "role": "voiceover", "start_sec": 1.0, "duration_sec": 6.0}
]
edl = vc.reconcile_edl_timeline(videos, audios, target_duration_sec=19.0)
print()
print(f"EDL Timeline: Duration={edl['total_timeline_duration_sec']}s, Compliant={edl['is_target_compliant']}")
print(f"Crossfades: {json.dumps(edl['crossfade_overlaps'])}")
print(f"Ducking Triggers: {json.dumps(edl['audio_ducking_events'])}")
