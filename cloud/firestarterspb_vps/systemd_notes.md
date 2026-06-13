# systemd Notes

Docker Compose services use `restart: unless-stopped`, which is enough for the Phase 1 VPS package.

If a dedicated systemd unit is preferred, create `/etc/systemd/system/firestarterspb-cloud.service`:

```ini
[Unit]
Description=FirestarterSPB Cloud Docker Compose Stack
Requires=docker.service
After=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/firestarterspb/cloud/firestarterspb_vps
ExecStart=/usr/bin/docker compose --env-file .env up -d
ExecStop=/usr/bin/docker compose --env-file .env down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now firestarterspb-cloud.service
```

Keep n8n scheduling inside n8n. Do not add a second overlapping systemd timer for the same workflow lane.
