#!/usr/bin/env bash
# Render the Unique Games video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=ugc_video.py NAME=unique-games-theorem
export SCENES="C0Open C1Hard C2Game C3Conjecture C4Claim C5How C6Close"
exec "$HERE/../../../../../tools/video/render.sh"
