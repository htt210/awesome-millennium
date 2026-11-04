#!/usr/bin/env bash
# Render the quasi-Riemann hypothesis video with the shared toolkit in tools/video (see its render.sh for options).
HERE="$(cd "$(dirname "$0")" && pwd)"
export VIDEO_DIR="$HERE" SCENE_FILE=qrh_video.py NAME=quasi-riemann-hypothesis
export SCENES="C0Open C1Primes C2Zeta C3Question C4Claim C5Cancel C6Crowd C7Follow C8Check C9Close"
exec "$HERE/../../../../../tools/video/render.sh"
