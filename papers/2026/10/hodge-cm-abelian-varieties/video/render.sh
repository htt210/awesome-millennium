#!/usr/bin/env bash
# Render the Hodge video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=hodge_video.py NAME=hodge-cm-abelian-varieties
export SCENES="C0Open C1Shapes C2Conjecture C3CM C4Claim C5How C6Follow C7Check C8Close"
exec "$HERE/../../../../../tools/video/render.sh"
