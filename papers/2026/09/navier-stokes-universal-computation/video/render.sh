#!/usr/bin/env bash
# Render the Navier–Stokes computation video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=nscomp_video.py NAME=navier-stokes-universal-computation
export SCENES="C0Open C1Fluids C2Machines C3Claim C4How C5Close"
exec "$HERE/../../../../../tools/video/render.sh"
