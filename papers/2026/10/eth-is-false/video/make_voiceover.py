#!/usr/bin/env python3
"""Lay the narration clips under the rendered video, one soundtrack per voice.

Each scene logs when each caption's clip starts (voice_at, in
build/captions/<Scene>.json); the clips were made by voice.py and cached in
build/voice/<key>/ while the scenes rendered. The scenes waited for the slowest
voice, so clips never overlap, and every voice fits the same picture.

    NARRATION_VOICES="us-male=a.onnx,us-female=b.onnx" \\
        python make_voiceover.py build/silent.mp4 S1Hook S2Polynomial ...

writes eth-is-false.mp4 with the first voice and eth-is-false-<key>.mp4 with
each of the others.
"""

from __future__ import annotations

import json
import subprocess
import sys
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from make_captions import video_duration  # noqa: E402
from voice import voices_from_env  # noqa: E402


def soundtrack(voice, scenes: list[str], total: float, out: Path) -> int:
    rate = voice.sample_rate
    pcm = bytearray(2 * int(total * rate + 1))
    offset, placed = 0.0, 0
    for scene in scenes:
        data = json.loads((HERE / "build" / "captions" / f"{scene}.json").read_text())
        for cap in data["captions"]:
            with wave.open(str(voice.clip(cap["say"])), "rb") as w:
                assert w.getframerate() == rate and w.getsampwidth() == 2 and w.getnchannels() == 1
                clip = w.readframes(w.getnframes())
            start = 2 * int((offset + cap["voice_at"]) * rate)
            clip = clip[: len(pcm) - start]
            pcm[start:start + len(clip)] = clip
            placed += 1
        offset += video_duration(HERE / "build" / "scenes" / f"{scene}.mp4") or data["duration"]
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(pcm))
    return placed


def main(silent: str, scenes: list[str]) -> int:
    voices = voices_from_env(HERE / "build" / "voice")
    if not voices:
        sys.exit("set NARRATION_VOICES (see voice.py)")
    total = video_duration(Path(silent))
    for i, (key, voice) in enumerate(voices.items()):
        track = HERE / "build" / f"narration-{key}.wav"
        placed = soundtrack(voice, scenes, total, track)
        out = HERE / ("eth-is-false.mp4" if i == 0 else f"eth-is-false-{key}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", str(track),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "64k",
                        "-metadata:s:a:0", f"title=Narration ({key})", "-movflags", "+faststart", str(out)],
                       check=True)
        print(f"wrote {out.name} ({placed} narration clips, voice {key})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2:]))
