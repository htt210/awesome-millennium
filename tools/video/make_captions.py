#!/usr/bin/env python3
"""Build captions.srt and script.md for a narrated video from the caption timings
each scene logs to <video dir>/build/captions/<Scene>.json (see narrated.py).

    python3 make_captions.py VIDEO_DIR VIDEO_FILE Scene1 Scene2 ...   # scenes in video order
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from captions_util import plain, to_markdown  # noqa: E402


def stamp(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def video_duration(path: Path) -> float | None:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                              str(path)], capture_output=True, text=True, check=True).stdout
        return float(out.strip())
    except (OSError, subprocess.CalledProcessError, ValueError):
        return None


def main(video_dir: Path, video_file: str, scenes: list[str]) -> int:
    offset = 0.0
    srt, md = [], ["# Narration script", "",
                   f"Generated from the captions burned into the video (`make_captions.py`). "
                   f"Timestamps refer to `{video_file}`. The words come from "
                   "[`storyboard.md`](storyboard.md), the script, which also describes what is on screen.", ""]
    index = 1
    for scene in scenes:
        data = json.loads((video_dir / "build" / "captions" / f"{scene}.json").read_text())
        duration = video_duration(video_dir / "build" / "scenes" / f"{scene}.mp4") or data["duration"]
        md += [f"## {data.get('title', scene)}", ""]
        for cap in data["captions"]:
            start, end = offset + cap["start"], offset + cap["end"]
            srt += [str(index), f"{stamp(start)} --> {stamp(end)}", plain(cap["text"]), ""]
            index += 1
            md.append(f"**[{stamp(start)[:8]}]** {to_markdown(cap['text'])}")
            md.append("")
        offset += duration
    (video_dir / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    md.append(f"Total running time: {int(offset // 60)} min {offset % 60:.0f} s.")
    (video_dir / "script.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote captions.srt ({index - 1} captions) and script.md; total {offset:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3:]))
