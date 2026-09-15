#!/usr/bin/env bash
# Everyday GPU control: status, start, stop, serve, tunnel.
#
#   ./scripts/gpu.sh status <ID>    # what is it doing, what does it cost
#   ./scripts/gpu.sh start  <ID>    # start a stopped instance
#   ./scripts/gpu.sh stop   <ID>    # stop it, keep the disk and the model
#   ./scripts/gpu.sh serve  <ID>    # start llama-server on the GPU
#   ./scripts/gpu.sh tunnel <ID>    # open http://127.0.0.1:8080 on this machine
#
# stop keeps your disk (small daily fee) and never deletes anything.
set -euo pipefail

CMD="${1:?usage: gpu.sh <status|start|stop|serve|tunnel> <INSTANCE_ID>}"
ID="${2:?usage: gpu.sh $CMD <INSTANCE_ID>}"
MODEL_FILE="${MODEL_FILE:-Qwen3.8-27B-OBLITERATED-Q6_K.gguf}"
CTX="${CTX:-65536}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519}"

command -v vastai >/dev/null || { echo "pip install vastai"; exit 1; }

info() {
  vastai show instance "$ID" --raw 2>/dev/null | python3 -c '
import json,sys
d=json.load(sys.stdin)
print(d.get("ssh_host") or "-", d.get("ssh_port") or "-",
      d.get("actual_status") or "-", d.get("intended_status") or "-",
      round(float(d.get("dph_total") or 0),3),
      round(float(d.get("storage_total_cost") or 0)*24,2),
      d.get("gpu_name","?").replace(" ","_"))'
}

read -r HOST PORT ACTUAL INTENDED HOURLY DISKDAY GPU <<<"$(info)"
SSH=(ssh -o StrictHostKeyChecking=accept-new -o IdentitiesOnly=yes -i "$SSH_KEY" -p "$PORT" "root@$HOST")

case "$CMD" in
  status)
    echo "instance $ID (${GPU//_/ })"
    echo "  state:    $ACTUAL (intended: $INTENDED)"
    if [[ "$ACTUAL" == "running" ]]; then
      echo "  costing:  \$$HOURLY/hour right now"
      echo "  ssh:      ssh -p $PORT root@$HOST"
    else
      echo "  costing:  \$$DISKDAY/day (disk only, GPU not billed)"
    fi
    ;;

  start)
    vastai start instance "$ID"
    echo "Start requested. It can sit in 'scheduling' while it waits for a free card."
    echo "Watch with:  ./scripts/gpu.sh status $ID"
    ;;

  stop)
    vastai stop instance "$ID"
    echo "Stop requested. GPU billing ends; the disk stays at \$$DISKDAY/day."
    echo "Your model files are kept - starting again does not re-download them."
    ;;

  serve)
    [[ "$ACTUAL" == "running" ]] || { echo "Instance is $ACTUAL. Start it first: ./scripts/gpu.sh start $ID"; exit 1; }
    echo "Starting llama-server on the GPU..."
    "${SSH[@]}" "pkill -f llama-server || true; sleep 1; \
      nohup /root/llama.cpp/build/bin/llama-server \
        -m /root/models/$MODEL_FILE \
        --host 127.0.0.1 --port 8080 \
        -ngl 999 -c $CTX -fa on --jinja --reasoning off \
        > /root/server.log 2>&1 & sleep 8; \
      curl -sf http://127.0.0.1:8080/health >/dev/null && echo '  server is up' || (tail -5 /root/server.log; exit 1)"
    echo
    echo "Now open the tunnel:  ./scripts/gpu.sh tunnel $ID"
    ;;

  tunnel)
    [[ "$ACTUAL" == "running" ]] || { echo "Instance is $ACTUAL. Start it first."; exit 1; }
    echo "Tunnel open. Chat at http://127.0.0.1:8080/   (Ctrl-C to close)"
    exec ssh -o StrictHostKeyChecking=accept-new -o IdentitiesOnly=yes -i "$SSH_KEY" \
      -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 \
      -N -L 127.0.0.1:8080:127.0.0.1:8080 -p "$PORT" "root@$HOST"
    ;;

  *)
    echo "unknown command: $CMD"; exit 1;;
esac
