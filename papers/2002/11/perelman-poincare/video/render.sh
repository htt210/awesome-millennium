#!/usr/bin/env bash
# Render the Poincaré video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=poincare_video.py NAME=perelman-poincare
export SCENES="C0Open C1Shapes C2Question C3Flow C4Necks C5Perelman C6Together C7Checked C8Meaning C9Close"
exec "$HERE/../../../../../tools/video/render.sh"
