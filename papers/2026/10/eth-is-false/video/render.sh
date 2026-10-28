#!/usr/bin/env bash
# Render the explainer video with 3b1b's manim (manimgl 1.7.2).
#
#   ./render.sh            # 1080p30, every scene, then concatenate + poster + captions
#   QUALITY=-l ./render.sh # quick 480p preview
#   JOBS=3 ./render.sh     # render scenes in parallel
#   RESUME=1 ./render.sh   # keep scenes already rendered (build/scenes/<Scene>.mp4 and its caption log)
#   NARRATION_VOICES="us-male=a.onnx,us-female=b.onnx" PYTHON=venv/bin/python ./render.sh
#                          # voiced: eth-is-false.mp4 with the first voice, eth-is-false-<key>.mp4
#                          # with the others; every scene waits for the slowest voice (voice.py)
#
# Needs manimgl, a LaTeX installation with dvisvgm, ffmpeg and the CMU Serif
# font. Without a display it runs under xvfb-run (Mesa's software renderer is
# enough).
set -euo pipefail
cd "$(dirname "$0")"

SCENES=(C0Open C1Puzzle C2Doubling C3Shortcuts C4Bet C5Claim C6aArithmetic C6bTeams C6cTotals C6dDial C6eCurve C6fBalance C7Catch C8Meaning C9Status C10Close)
QUALITY=${QUALITY:---hd}
JOBS=${JOBS:-1}
MANIMGL=${MANIMGL:-manimgl}
OUT=build/scenes
mkdir -p "$OUT" build/captions build/logs

run() {
  if [ -z "${DISPLAY:-}" ]; then
    xvfb-run -a -s "-screen 0 1920x1080x24" "$@"
  else
    "$@"
  fi
}
export -f run
export MANIMGL QUALITY OUT RESUME

printf '%s\n' "${SCENES[@]}" | xargs -P "$JOBS" -I{} bash -c \
  'if [ -n "${RESUME:-}" ] && [ -s "$OUT/{}.mp4" ] && [ -s build/captions/{}.json ]; then echo "kept {}"; exit 0; fi
   run "$MANIMGL" eth_video.py {} -w $QUALITY --config_file custom_config.yml --video_dir "$OUT" > build/logs/{}.log 2>&1 \
   && echo "rendered {}" || { echo "FAILED {} (see build/logs/{}.log)"; exit 255; }'

: > build/concat.txt
for s in "${SCENES[@]}"; do echo "file 'scenes/$s.mp4'" >> build/concat.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i build/concat.txt -c copy -movflags +faststart build/silent.mp4
if [ -n "${NARRATION_VOICES:-}" ]; then
  "${PYTHON:-python3}" make_voiceover.py build/silent.mp4 "${SCENES[@]}"
else
  cp build/silent.mp4 eth-is-false.mp4
  echo "wrote eth-is-false.mp4 (no narration)"
fi

run "$MANIMGL" eth_video.py Thumbnail -w -s $QUALITY --config_file custom_config.yml --video_dir "$OUT" > build/logs/Thumbnail.log 2>&1
cp "$OUT/Thumbnail.png" poster.png
echo "wrote poster.png"

python3 make_captions.py "${SCENES[@]}"
