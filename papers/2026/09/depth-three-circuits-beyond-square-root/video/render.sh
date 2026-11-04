#!/usr/bin/env bash
# Render the depth-three circuits video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=circuits_video.py NAME=depth-three-circuits-beyond-square-root
export SCENES="C0Open C1Circuits C2Layers C3Barrier C4Claim C5How C6Close"
exec "$HERE/../../../../../tools/video/render.sh"
