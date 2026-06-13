#!/usr/bin/env python3
"""Send FirestarterSPB notifications through ntfy without storing secrets in repo."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        raise FileNotFoundError(f"ntfy env file not found: {path}")
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def send_ntfy(
    *,
    env_path: Path,
    title: str,
    message: str,
    priority: str,
    tags: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    env = load_env(env_path)
    base_url = env.get("NTFY_BASE_URL", "https://ntfy.sh").rstrip("/")
    topic = env.get("NTFY_TOPIC", "")
    token = env.get("NTFY_TOKEN", "")

    if not topic:
        raise ValueError("NTFY_TOPIC is missing from ntfy env file.")
    if not token and not dry_run:
        raise ValueError("NTFY_TOKEN is missing from ntfy env file.")

    target = f"{base_url}/{topic}"
    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "target": target,
            "title": title,
            "priority": priority,
            "tags": tags,
            "message": message,
            "token_present": bool(token),
            "token_length": len(token),
        }

    request = urllib.request.Request(
        target,
        data=message.encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Title": title,
            "Priority": priority,
            "Tags": tags,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 300,
                "dry_run": False,
                "http_status": response.status,
                "target": target,
                "response_tail": body[-1000:],
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "dry_run": False,
            "http_status": exc.code,
            "target": target,
            "error": body[-1000:],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a FirestarterSPB ntfy notification.")
    parser.add_argument("--title", default="FirestarterSPB")
    parser.add_argument("--message", required=True)
    parser.add_argument("--priority", default="4")
    parser.add_argument("--tags", default="fire")
    parser.add_argument("--env", default="/root/.config/firestarter/ntfy.env")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = send_ntfy(
        env_path=Path(args.env),
        title=args.title,
        message=args.message,
        priority=args.priority,
        tags=args.tags,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
