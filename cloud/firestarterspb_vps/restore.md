# Restore Notes

This is a conservative restore path for Phase 1 cloud control infrastructure.

1. Provision a fresh Ubuntu 24.04 VPS.
2. Clone `chrispropil/firestarterspb`.
3. Copy the selected backup folder into `cloud/firestarterspb_vps/backups/`.
4. Recreate `.env` manually from `.env.example`; do not restore secrets into git.
5. Run `./setup_ubuntu.sh`.
6. Start Postgres only:

```bash
docker compose --env-file .env up -d postgres
```

7. Restore n8n database:

```bash
docker compose --env-file .env exec -T postgres psql -U "$POSTGRES_USER" "$POSTGRES_DB" < backups/YYYYMMDDTHHMMSSZ/n8n_postgres.sql
```

8. Restore runtime logs/state only if needed:

```bash
tar -xzf backups/YYYYMMDDTHHMMSSZ/firestarterspb_cloud_runtime.tgz -C ../../
```

9. Run `./deploy.sh`.
10. Re-import n8n workflows only if the database restore did not include them.

Rollback is simple: stop the compose stack, redeploy the previous git revision, and restore the previous database dump.
