# Vast.ai operations

The only current runtime path is **Vast.ai + llama.cpp over private SSH**.
Modal was retired from this project's operating path for its cost budget;
its gateway and `mn` commands are [archive only](../archive/modal/README.md).

## Before starting

The retained owner instance is `49433042`: A100 PCIe 40 GB, 120 GB container disk.
It was **STOPPED** in the [2026-09-05 20:12 UTC recheck](evidence/2026-09-05-vast-recheck.json).
No inference was tested. Do not start it to check billing or read docs.
Other users need their own contract ID, credentials and approved hourly budget;
review the [running and retained-disk costs](../README.md#cost).

Use an authenticated Vast CLI compatible with your Python version. Check
`vastai --help` and the [official CLI source](https://github.com/vast-ai/vast-python);
the earlier `/tmp/vastai-venv/bin/vastai` installation no longer exists.
Never commit the account API key or give it to inference clients.

## 1. Inspect, then start deliberately

```sh
vastai show instance 49433042 --raw
# Only when you want paid compute:
vastai start instance 49433042
vastai show instance 49433042 --raw
```

Inspect `actual_status`, `intended_status` and `cur_state`, not `status_msg` prose.
A successful start request is not proof of a running model. `scheduling` can mean
someone else rented the GPU; resume availability and boot time are not guaranteed.
For account inventory, use the current CLI's v1 listing; API/pagination details
are in [status evidence](STATUS.md#inventory-details).

## 2. Verify the remote server

Use fresh SSH connection details from Vast, including the actual SSH port mapping.
Do not assume the old host/port still works. Keep host-key verification enabled;
verify a changed host key before trusting it.

On the remote instance:

```sh
pgrep -af llama-server
curl --fail --show-error --max-time 10 http://127.0.0.1:8080/health
curl --fail --show-error --max-time 10 http://127.0.0.1:8080/v1/models
```

The last inspected `onstart` was null: **model autostart is not verified**.
If the server is absent, inspect the retained startup script, `/root/server.log`,
available VRAM and the installed binary's `--help` before launching it. Do not start
a second copy or indiscriminately kill matching processes.

The last artifact was `/root/models/Qwen3.8-27B-OBLITERATED-Q6_K.gguf`, with
`--jinja`, context `262144`, full GPU offload and explicit sampling. Model
revision/hash and llama.cpp build pins were not captured. At the next approved
restart, record them and verify a version-compatible launch command; there is no
reproducibly pinned launch recipe here. Use loopback binding, not the old
`--host 0.0.0.0` on an unprotected public port. Template generation and reasoning
parser/output controls vary by runtime: `--reasoning off` is not a universal
thinking-disable switch. Validate output rather than assuming a flag or quant
has fixed every failure.

## 3. Connect and test locally

Keep this SSH session open, replacing the destination and port with Vast's values:

```sh
ssh -i ~/.ssh/id_ed25519 -p <SSH_PORT> \
  -o IdentitiesOnly=yes -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=15 -o ServerAliveCountMax=3 \
  -N -L 127.0.0.1:8080:127.0.0.1:8080 root@<SSH_HOST>
```

`<SSH_PORT>` and `<SSH_HOST>` are placeholders. Alternatively, inspect the existing
Mac LaunchAgent `~/Library/LaunchAgents/com.emin.vast-tunnel.plist` and update only
its verified destination. It maintains a tunnel, not a GPU or model server. Do not
run both tunnels on the same local port.

```sh
curl --fail --show-error --max-time 10 http://127.0.0.1:8080/health
curl --fail --show-error --max-time 10 http://127.0.0.1:8080/v1/models
```

Use the ID returned by `/v1/models` for direct API tests; historically it was the
full GGUF path, while clients used alias `qwen3.8-27b-obl`. Several picker aliases
do not load several models or switch weights: Huihui/R1 are not simultaneous
alternatives on this single-model server.

Test non-streaming and streaming with a bounded prompt such as "List three
programming languages." Require non-empty `content` and normal completion;
inspect `finish_reason`, errors and timings. HTTP 200 or health alone is not enough.
Then test the intended client. **No inference smoke test was run in this audit:**
the GPU stayed stopped.

### Choose a client

**Plain chat:** open `http://127.0.0.1:8080/` when the server and tunnel are ready.
This is the built-in llama-server UI, not Open WebUI or the public website.

**Pi:** custom providers live in `~/.pi/agent/models.json`, not
`~/.config/pi/config.json`. Merge into the existing file; do not replace unrelated
providers. The inspected local definition is:

```json
{
  "providers": {
    "uncensored": {
      "baseUrl": "http://127.0.0.1:8080/v1",
      "api": "openai-completions",
      "apiKey": "none",
      "models": [{"id": "qwen3.8-27b-obl", "contextWindow": 262144}]
    }
  }
}
```

`none` is a client placeholder, not authentication; use a real key if required by
the server. Verify the alias. `contextWindow` sets Pi's budget, not the server's
capacity or proven long-context quality. [Pi's model documentation](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/models.md)
says `/model` reloads definitions; restarting the app is not generally required.

```sh
pi --provider uncensored --model qwen3.8-27b-obl
```

To isolate a tool-loop issue, the installed Pi CLI supports this no-tools mode
(flags checked with `pi --help`; generation not retested):

```sh
pi --provider uncensored --model qwen3.8-27b-obl \
  --no-tools --no-extensions --no-skills --no-context-files \
  --system-prompt "You are a helpful assistant."
```

**OpenCode:** the inspected `~/.config/opencode/opencode.json` uses provider
`uncensored`, adapter `@ai-sdk/openai-compatible`, `options.baseURL` =
`http://127.0.0.1:8080/v1`, model key `qwen3.8-27b-obl`, `limit.context` = `262144`
and `limit.output` = `8192`.

```sh
opencode --model uncensored/qwen3.8-27b-obl
```

Pi, OpenCode and `hermes chat` are agent paths by default, not inherently raw chat.
Config inspection does not establish tool/agent reliability; test the actual
harness. Model size alone does not establish tool capability. On another computer,
localhost means that computer: use an authorized tunnel or an explicitly secured
shared endpoint. Do not distribute root SSH keys or the Vast account key.
Public multi-user inference is not deployed.

## 4. Stop and verify

```sh
vastai stop instance 49433042
vastai show instance 49433042 --raw
```

Wait for actual `exited`/stopped and intended `stopped`; request acceptance is not
confirmation. Stop the local tunnel if no longer needed.

**GPU compute stops; storage billing continues.** The retained disk costs about
$0.80/day. It persists while the instance/contract exists, but is not an off-host
backup: host loss or contract expiry can threaten data. Keep unique work elsewhere.

There is **no verified automatic idle shutdown**. The prior local timer was
canceled. For unattended deadlines, configure and test a durable scheduler and
read back the final cloud state; do not rely on a sleeping laptop.

**Destruction is separate:** it permanently deletes the container disk and is not
part of normal start/stop. Back up unique files, verify the backup and obtain
explicit deletion approval first. A separate volume also costs money; none was
provisioned or needed merely to stop/resume this instance.

References: [Vast lifecycle](https://docs.vast.ai/documentation/instances/manage-instances.md) ·
[Vast storage](https://docs.vast.ai/documentation/instances/storage/types.md)
