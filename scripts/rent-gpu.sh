#!/usr/bin/env bash
# Rent a GPU and put an uncensored model on it. One command, your own account.
#
#   export VAST_API_KEY=...          # from https://cloud.vast.ai/account/
#   ./scripts/rent-gpu.sh            # cheapest 24GB card, 27B model
#   ./scripts/rent-gpu.sh --big      # 96GB card, 176B model
#
# Prints the instance id and the exact next command. Nothing is destroyed,
# nothing runs unattended, and you are told the price before it charges.
set -euo pipefail

MODEL_REPO="${MODEL_REPO:-OBLITERATUS/Qwen3.8-27B-OBLITERATED}"
MODEL_FILE="${MODEL_FILE:-Qwen3.8-27B-OBLITERATED-Q6_K.gguf}"
MIN_VRAM=24000
DISK=120
MAX_PRICE="${MAX_PRICE:-0.60}"

if [[ "${1:-}" == "--big" ]]; then
  MODEL_REPO="apetersson/Qwen3.8-Flash-Next-Abliterated-GGUF"
  MODEL_FILE="Qwen3.8-Flash-Next-Abliterated-Q5_K_M.gguf"
  MIN_VRAM=95000
  DISK=300
  MAX_PRICE="${MAX_PRICE:-2.00}"
fi

command -v vastai >/dev/null || { echo "Install the CLI first:  pip install vastai"; exit 1; }
[[ -n "${VAST_API_KEY:-}" ]] || { echo "Set VAST_API_KEY (https://cloud.vast.ai/account/)"; exit 1; }
vastai set api-key "$VAST_API_KEY" >/dev/null

echo "Looking for a GPU with at least $((MIN_VRAM/1000))GB VRAM under \$$MAX_PRICE/hour..."
OFFER=$(vastai search offers \
  "num_gpus=1 gpu_ram>=${MIN_VRAM} reliability>0.98 disk_space>=${DISK} rented=False dph<${MAX_PRICE}" \
  --order dph_total --limit 1 --raw 2>/dev/null \
  | python3 -c 'import json,sys
d=json.load(sys.stdin); d=d.get("offers",d) if isinstance(d,dict) else d
if not d: sys.exit("none")
o=d[0]; print(o["id"], o["gpu_name"], round(o["dph_total"],3), o.get("geolocation","?"), sep="|")' 2>/dev/null) || {
  echo "No offer matched. Raise MAX_PRICE or try again - the marketplace changes by the minute."
  exit 1
}

IFS='|' read -r OFFER_ID GPU PRICE LOCATION <<<"$OFFER"
MONTHLY=$(python3 -c "print(f'{float('$PRICE')*720:.0f}')")
echo
echo "  GPU:      $GPU ($LOCATION)"
echo "  Price:    \$$PRICE/hour  (\$$MONTHLY/month if you never stop it)"
echo "  Model:    $MODEL_REPO"
echo "  Disk:     ${DISK}GB"
echo
read -r -p "Rent it? [y/N] " ok
[[ "$ok" == "y" || "$ok" == "Y" ]] || { echo "Nothing rented."; exit 0; }

ID=$(vastai create instance "$OFFER_ID" \
  --image nvidia/cuda:12.8.0-devel-ubuntu24.04 \
  --disk "$DISK" --ssh --direct --label abliterated --raw 2>/dev/null \
  | python3 -c 'import json,sys
d=json.load(sys.stdin)
if not d.get("success", True): sys.exit(d.get("msg","create failed"))
print(d["new_contract"])')

echo
echo "Instance $ID is booting. Next:"
echo
echo "  ./scripts/setup-model.sh $ID        # build llama.cpp + download the model"
echo "  ./scripts/gpu.sh stop $ID           # stop it when you are done"
echo
echo "You are being charged \$$PRICE/hour from now until you stop it."
