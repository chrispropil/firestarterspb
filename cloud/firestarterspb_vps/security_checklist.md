# Security Checklist

- Replace every placeholder in `.env` before deployment.
- Never commit `.env`, API keys, exchange credentials, private keys, or production URLs with secrets.
- Keep n8n bound to `127.0.0.1` unless a reverse proxy with TLS is configured.
- Keep the worker bound to `127.0.0.1` from the host and reachable only inside Docker.
- Use long random values for `POSTGRES_PASSWORD`, `N8N_BASIC_AUTH_PASSWORD`, and `N8N_ENCRYPTION_KEY`.
- Enable host firewall rules for SSH and the intended dashboard or reverse proxy ports only.
- Do not import workflows that call themselves.
- Do not add webhook-triggered arbitrary command execution.
- Keep raw data out of commits and backups unless separately approved.
- Review `FIRESTARTER_CLOUD_WORKER_EXECUTE` before enabling runtime viewer writes.
- Rotate n8n credentials after restoring from backup.
- Keep Docker and Ubuntu security updates current.
