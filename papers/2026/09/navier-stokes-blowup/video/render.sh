#!/usr/bin/env bash
# Render this video with the shared tools (see ../../../../../tools/video/render.sh for options):
#   ./render.sh                                   # silent 1080p
#   QUALITY=-l JOBS=4 ./render.sh                 # quick 480p preview
#   NARRATION_VOICES="us-male=a.onnx,us-female=b.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
export VIDEO_DIR="$HERE" SCENE_FILE=ns_video.py NAME=navier-stokes-blowup
export SCENES="C0Open C1Equations C2Question C3Force C4Claim C5Core C6Pulses C6Rest C7Check C8Meaning C9Close"
exec "$HERE/../../../../../tools/video/render.sh"
