#!/usr/bin/env bash
# Render a narrated explainer video made with tools/video/narrated.py.
#
#   VIDEO_DIR=papers/.../video SCENE_FILE=ns_video.py NAME=navier-stokes-blowup \
#     SCENES="C0Open C1Equations ..." tools/video/render.sh
#
# Options (environment): QUALITY (default --hd = 1080p30; -l for a 480p preview),
# JOBS (scenes rendered in parallel), MANIMGL, PYTHON (an environment with manimgl,
# piper-tts and onnxruntime), NARRATION_VOICES (see voice.py; unset = silent),
# RESUME=1 (keep scenes already rendered), POSTER_SCENE (default Thumbnail).
# Writes VIDEO_DIR/NAME.mp4 (and NAME-<voice>.mp4 for further voices), poster.png,
# captions.srt and script.md. Intermediate files go to VIDEO_DIR/build.
set -euo pipefail
TOOLS=$(cd "$(dirname "$0")" && pwd)
cd "${VIDEO_DIR:?set VIDEO_DIR}"
: "${SCENE_FILE:?set SCENE_FILE}" "${NAME:?set NAME}" "${SCENES:?set SCENES}"
read -r -a SCENE_LIST <<< "$SCENES"
QUALITY=${QUALITY:---hd}
JOBS=${JOBS:-1}
MANIMGL=${MANIMGL:-manimgl}
PYTHON=${PYTHON:-python3}
POSTER_SCENE=${POSTER_SCENE:-Thumbnail}
CONFIG="$TOOLS/custom_config.yml"
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
export MANIMGL QUALITY OUT RESUME SCENE_FILE CONFIG

printf '%s\n' "${SCENE_LIST[@]}" | xargs -P "$JOBS" -I{} bash -c \
  'if [ -n "${RESUME:-}" ] && [ -s "$OUT/{}.mp4" ] && [ -s build/captions/{}.json ]; then echo "kept {}"; exit 0; fi
   export TMPDIR=$(mktemp -d)   # private temp files: parallel scenes otherwise race on the same text SVGs
   run "$MANIMGL" "$SCENE_FILE" {} -w $QUALITY --config_file "$CONFIG" --video_dir "$OUT" > build/logs/{}.log 2>&1 \
   && echo "rendered {}" || { echo "FAILED {} (see build/logs/{}.log)"; exit 255; }'

: > build/concat.txt
for s in "${SCENE_LIST[@]}"; do echo "file 'scenes/$s.mp4'" >> build/concat.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i build/concat.txt -c copy -movflags +faststart build/silent.mp4
if [ -n "${NARRATION_VOICES:-}" ]; then
  "$PYTHON" "$TOOLS/make_voiceover.py" . "$NAME" build/silent.mp4 "${SCENE_LIST[@]}"
else
  cp build/silent.mp4 "$NAME.mp4"
  echo "wrote $NAME.mp4 (no narration)"
fi

run "$MANIMGL" "$SCENE_FILE" "$POSTER_SCENE" -w -s $QUALITY --config_file "$CONFIG" --video_dir "$OUT" \
  > build/logs/$POSTER_SCENE.log 2>&1
cp "$OUT/$POSTER_SCENE.png" poster.png
echo "wrote poster.png"

python3 "$TOOLS/make_captions.py" . "$NAME.mp4" "${SCENE_LIST[@]}"
