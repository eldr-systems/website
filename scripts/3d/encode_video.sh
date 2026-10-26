#!/usr/bin/env bash
# scripts/3d/encode_video.sh FRAMES_DIR OUT_BASENAME [POSTER_FRAME]
#
# PNG frames from render_video.py or render_assembly.py into OUT_BASENAME.webm (VP9, served
# first) and OUT_BASENAME.mp4 (H.264, for Safari), plus OUT_BASENAME.jpg, frame
# POSTER_FRAME (default 70, the burst fully open) as the poster and the no-motion
# fallback.
set -euo pipefail
frames=$1 out=$2 poster=$(printf %04d "${3:-70}")
common=(-loglevel error -y -framerate 30 -i "$frames/f%04d.png" -vf "scale=1200:-2:flags=lanczos" -an)

ffmpeg "${common[@]}" -c:v libvpx-vp9 -b:v 0 -crf 38 -row-mt 1 -pix_fmt yuv420p "$out.webm"
ffmpeg "${common[@]}" -c:v libx264 -crf 26 -preset slow -pix_fmt yuv420p -movflags +faststart "$out.mp4"
ffmpeg -loglevel error -y -i "$frames/f$poster.png" -vf "scale=1200:-2:flags=lanczos" -q:v 4 "$out.jpg"
ls -la "$out".*
