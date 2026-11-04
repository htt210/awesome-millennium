#!/usr/bin/env bash
# Render the BSD video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=bsd_video.py NAME=exact-bsd-low-selmer-corank
export SCENES="C0Open C1Points C2Experiment C3Formula C4Known C5Claim C6How C7Follow C8Check C9Close"
exec "$HERE/../../../../../tools/video/render.sh"
