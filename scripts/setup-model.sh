#!/usr/bin/env bash
# Build llama.cpp on a rented GPU and download an abliterated model.
#
#   ./scripts/setup-model.sh <INSTANCE_ID>
#
# Takes about 10 minutes: 5 for the build, 5 for the download. Safe to re-run -
# it skips work that is already done.
set -euo pipefail

ID="${1:?usage: setup-model.sh <INSTANCE_ID>}"
MODEL_REPO="${MODEL_REPO:-OBLITERATUS/Qwen3.8-27B-OBLITERATED}"
MODEL_FILE="${MODEL_FILE:-Qwen3.8-27B-OBLITERATED-Q6_K.gguf}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519}"

command -v vastai >/dev/null || { echo "pip install vastai"; exit 1; }

echo "Waiting for instance $ID to be reachable..."
for i in $(seq 1 60); do
  read -r HOST PORT STATUS <<<"$(vastai show instance "$ID" --raw 2>/dev/null \
    | python3 -c 'import json,sys
d=json.load(sys.stdin)
print(d.get("ssh_host") or "-", d.get("ssh_port") or "-", d.get("actual_status") or "-")')"
  [[ "$STATUS" == "running" && "$HOST" != "-" ]] && break
  printf '\r  %s (%ds)' "$STATUS" $((i*5)); sleep 5
done
echo
[[ "$STATUS" == "running" ]] || { echo "Instance never came up. Check: vastai show instance $ID"; exit 1; }

SSH=(ssh -o StrictHostKeyChecking=accept-new -o IdentitiesOnly=yes -i "$SSH_KEY" -p "$PORT" "root@$HOST")

echo "Building llama.cpp and downloading the model (about 10 minutes)..."
"${SSH[@]}" bash -s <<EOF
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

if [ ! -x /root/llama.cpp/build/bin/llama-server ]; then
  apt-get update -qq && apt-get install -y -qq cmake build-essential git python3-pip >/dev/null
  pip install -q huggingface_hub[cli] 2>/dev/null || pip install -q --break-system-packages huggingface_hub[cli]
  [ -d /root/llama.cpp ] || git clone -q https://github.com/ggml-org/llama.cpp /root/llama.cpp
  cd /root/llama.cpp
  cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=native >/dev/null
  cmake --build build --config Release -j >/dev/null
  echo "  llama.cpp built"
else
  echo "  llama.cpp already built"
fi

mkdir -p /root/models
if [ ! -f "/root/models/$MODEL_FILE" ]; then
  echo "  downloading $MODEL_FILE ..."
  hf download "$MODEL_REPO" "$MODEL_FILE" --local-dir /root/models >/dev/null
else
  echo "  model already downloaded"
fi
ls -la "/root/models/$MODEL_FILE"
EOF

echo
echo "Done. Start the server:"
echo
echo "  ./scripts/gpu.sh serve $ID"
echo
