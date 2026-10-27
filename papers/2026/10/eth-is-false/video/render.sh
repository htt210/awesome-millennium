#!/usr/bin/env bash
# Render the explainer video with 3b1b's manim (manimgl 1.7.2).
#
#   ./render.sh            # 1080p30, every scene, then concatenate + poster + captions
#   QUALITY=-l ./render.sh # quick 480p preview
#   JOBS=3 ./render.sh     # render scenes in parallel
#
# Needs manimgl, a LaTeX installation with dvisvgm, ffmpeg and the CMU Serif
# font. Without a display it runs under xvfb-run (Mesa's software renderer is
# enough).
set -euo pipefail
cd "$(dirname "$0")"

SCENES=(S1Hook S2Polynomial S3Groups S4Separation S5Hermite S6Matrix S7Costs S8Meaning)
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
export MANIMGL QUALITY OUT

printf '%s\n' "${SCENES[@]}" | xargs -P "$JOBS" -I{} bash -c \
  'run "$MANIMGL" eth_video.py {} -w $QUALITY --config_file custom_config.yml --video_dir "$OUT" > build/logs/{}.log 2>&1 \
   && echo "rendered {}" || { echo "FAILED {} (see build/logs/{}.log)"; exit 255; }'

: > build/concat.txt
for s in "${SCENES[@]}"; do echo "file 'scenes/$s.mp4'" >> build/concat.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i build/concat.txt -c copy -movflags +faststart eth-is-false.mp4
echo "wrote eth-is-false.mp4"

run "$MANIMGL" eth_video.py Thumbnail -w -s $QUALITY --config_file custom_config.yml --video_dir "$OUT" > build/logs/Thumbnail.log 2>&1
cp "$OUT/Thumbnail.png" poster.png
echo "wrote poster.png"

python3 make_captions.py "${SCENES[@]}"
