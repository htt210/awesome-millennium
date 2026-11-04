#!/usr/bin/env bash
# Render the Ricci-flow video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=ricci_video.py NAME=ricci-flow-scalar-curvature-extension
export SCENES="C0Open C1Flow C2Curvature C3Question C4Claims C5Close"
exec "$HERE/../../../../../tools/video/render.sh"
