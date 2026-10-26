#!/usr/bin/env bash
# Runs Blender headless with mise's Python dropped from PATH: Blender takes its
# Python home from the first python3 it finds, and mise's lacks the stdlib layout
# Blender expects, so `import math` fails.
PATH=$(tr ':' '\n' <<<"$PATH" | grep -v 'mise/installs/python' | paste -sd:)
# On hybrid-graphics laptops, render on the discrete NVIDIA GPU: EEVEE on the
# integrated one is ~20x slower.
if command -v nvidia-smi >/dev/null; then
  export __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia
  export __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json
fi
exec blender -b "$@"
