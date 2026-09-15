# systemd units

Copy to `/etc/systemd/system/`, then:

```sh
systemctl daemon-reload
systemctl enable --now abliterated-gateway
systemctl enable --now abliterated-reaper.timer
```

Both read `/opt/abliterated/autopilot.env` (mode 600), which holds the Vast API
key and the instance id. That file is never committed — see
[autopilot docs](../../docs/AUTOPILOT.md#setup) for its contents.

`abliterated-reaper.timer` fires every 5 minutes and stops the GPU once it has
been idle past `ABL_IDLE_MINUTES`. Remove `ABL_AUTOPILOT` from the gateway unit
to disable wake-on-request and run the gateway as a plain proxy.
