#!/usr/bin/env python3
"""Minimal read-only MCP server for Project 15.

It exposes one Tool named get_disk_usage and one Resource containing the
fictional incident log.

There is deliberately no write Tool. Least privilege is enforced by design.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("ops-readonly")

LOG_PATH = (
    Path(__file__)
    .resolve()
    .parent
    / "sample_incident.log"
)


@mcp.tool()
def get_disk_usage(
    path: str = "/",
) -> dict[str, int | float | str]:
    """Return disk totals for a path. This function is read only."""

    total, used, free = shutil.disk_usage(
        path
    )

    used_pct = round(
        used / total * 100,
        1,
    )

    return {
        "path": path,
        "total": total,
        "used": used,
        "free": free,
        "used_pct": used_pct,
    }


@mcp.resource(
    "file://incident-log"
)
def incident_log() -> str:
    """Return the fictional incident log as a read-only Resource."""

    if not LOG_PATH.exists():
        return ""

    return LOG_PATH.read_text(
        encoding="utf-8",
    )


if __name__ == "__main__":
    mcp.run()
