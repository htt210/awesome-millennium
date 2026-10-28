#!/usr/bin/env python3
"""Build captions.srt and script.md from the caption timings that each scene
logs to build/captions/<Scene>.json (see Narrated in eth_video.py).

    python3 make_captions.py S1Hook S2Polynomial ...   # scenes in video order
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from captions_util import plain, to_markdown  # noqa: E402

TITLES = {
    "C0Open": "0. Cold open",
    "C1Puzzle": "1. The puzzle",
    "C2Doubling": "2. Why it gets hard so fast",
    "C3Shortcuts": "3. Fifty years of shortcuts",
    "C4Bet": "4. The bet called ETH",
    "C5Claim": "5. The new claim",
    "C6aArithmetic": "6a. Turning checking into arithmetic",
    "C6bTeams": "6b. The dream: independent teams",
    "C6cTotals": "6c. Teams that share only a total",
    "C6dDial": "6d. The dial",
    "C6eCurve": "6e. From the easy points back to zero",
    "C6fBalance": "6f. The balancing act, and the rest",
    "C7Catch": "7. The catch",
    "C8Meaning": "8. What it means, and what it doesn't",
    "C9Status": "9. Is it true?",
    "C10Close": "10. Closing",
}


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


def main(scenes: list[str]) -> int:
    offset = 0.0
    srt, md = [], ["# Narration script", "",
                   "Generated from the captions burned into the video (`make_captions.py`). "
                   "Timestamps refer to `eth-is-false.mp4`. The words come from "
                   "[`storyboard.md`](storyboard.md), the reviewed script, which also describes what is on "
                   "screen.", ""]
    index = 1
    for scene in scenes:
        data = json.loads((HERE / "build" / "captions" / f"{scene}.json").read_text())
        duration = video_duration(HERE / "build" / "scenes" / f"{scene}.mp4") or data["duration"]
        md += [f"## {TITLES.get(scene, scene)}", ""]
        for cap in data["captions"]:
            start, end = offset + cap["start"], offset + cap["end"]
            srt += [str(index), f"{stamp(start)} --> {stamp(end)}", plain(cap["text"]), ""]
            index += 1
            md.append(f"**[{stamp(start)[:8]}]** {to_markdown(cap['text'])}")
            md.append("")
        offset += duration
    (HERE / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    md.append(f"Total running time: {int(offset // 60)} min {offset % 60:.0f} s.")
    (HERE / "script.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote captions.srt ({index - 1} captions) and script.md; total {offset:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or list(TITLES)))
