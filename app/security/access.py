from __future__ import annotations

import base64
import ipaddress
from collections.abc import Iterable

from fastapi import HTTPException, Request, status

from app.core.config import Settings


def is_ip_allowed(client_ip: str, allowed_cidrs: Iterable[str]) -> bool:
    """check if client ip belongs to allowed cidr ranges."""
    try:
        ip = ipaddress.ip_address(client_ip)
    except ValueError:
        return False
    for cidr in allowed_cidrs:
        try:
            network = ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            continue
        if ip in network:
            return True
    return not list(allowed_cidrs)


def enforce_dashboard_access(request: Request, config: Settings) -> None:
    """enforce dashboard access control (vpn + optional basicauth).

    - first, check ip allowlist (e.g., tailscale subnets/ips)
    - if basicauth credentials are configured, validate authorization header
    """
    client_ip = request.headers.get(
        "x-forwarded-for", request.client.host if request.client else ""
    )
    if not is_ip_allowed(client_ip.split(",")[0].strip(), config.allowed_dashboard_cidrs):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    user = config.dashboard_basic_auth_user
    password = config.dashboard_basic_auth_password
    if user and password:
        auth_header: str | None = request.headers.get("authorization")
        if not auth_header or not auth_header.lower().startswith("basic "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        try:
            encoded = auth_header.split(" ", 1)[1]
            decoded = base64.b64decode(encoded).decode("utf-8")
            u, p = decoded.split(":", 1)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            ) from err
        if u != user or p != password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
