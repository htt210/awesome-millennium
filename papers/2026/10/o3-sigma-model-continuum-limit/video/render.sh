#!/usr/bin/env bash
# Render the O(3) video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=o3_video.py NAME=o3-sigma-model-continuum-limit
export SCENES="C0Open C1Gap C2Model C3Continuum C4Claim C5How C6Close"
exec "$HERE/../../../../../tools/video/render.sh"
