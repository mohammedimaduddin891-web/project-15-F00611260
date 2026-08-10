#!/usr/bin/env python3
"""MCP host/client demonstrating consent and Resource reading."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from pydantic import AnyUrl

from mcp import (
    ClientSession,
    StdioServerParameters,
)

from mcp.client.stdio import (
    stdio_client,
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

SERVER_PATH = (
    PROJECT_ROOT
    / "code"
    / "disk_mcp_server.py"
)


def print_tool_result(
    result: object,
) -> None:

    structured = getattr(
        result,
        "structuredContent",
        None,
    )

    if structured is not None:
        print(
            f"TOOL RESULT: {structured}"
        )
        return

    for item in getattr(
        result,
        "content",
        [],
    ):
        text = getattr(
            item,
            "text",
            None,
        )

        if text is not None:
            print(
                f"TOOL RESULT: {text}"
            )


def print_resource_result(
    result: object,
) -> None:

    for item in getattr(
        result,
        "contents",
        [],
    ):
        text = getattr(
            item,
            "text",
            None,
        )

        if text is not None:
            print(
                "RESOURCE CONTENT START"
            )

            print(
                text.rstrip()
            )

            print(
                "RESOURCE CONTENT END"
            )


async def run(
    args: argparse.Namespace,
) -> int:

    server = StdioServerParameters(
        command=sys.executable,
        args=[
            str(SERVER_PATH),
        ],
    )

    async with stdio_client(
        server
    ) as (
        read_stream,
        write_stream,
    ):

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            resources = (
                await session.list_resources()
            )

            print(
                "TOOLS: "
                f"{[tool.name for tool in tools.tools]}"
            )

            print(
                "RESOURCES: "
                f"{[
                    str(resource.uri)
                    for resource
                    in resources.resources
                ]}"
            )

            if args.tool:

                print(
                    "CONSENT REQUIRED "
                    "BEFORE TOOL INVOCATION"
                )

                response = input(
                    "Type YES to allow "
                    "get_disk_usage: "
                ).strip()

                if response != "YES":
                    print(
                        "CONSENT DENIED: "
                        "tool was not invoked"
                    )

                    return 2

                print(
                    "CONSENT GRANTED"
                )

                result = await session.call_tool(
                    "get_disk_usage",
                    arguments={
                        "path": args.path,
                    },
                )

                print_tool_result(
                    result
                )

            if args.resource:

                result = await session.read_resource(
                    AnyUrl(
                        "file://incident-log"
                    )
                )

                print_resource_result(
                    result
                )

    return 0


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--tool",
        action="store_true",
    )

    parser.add_argument(
        "--resource",
        action="store_true",
    )

    parser.add_argument(
        "--path",
        default="/",
    )

    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(
        asyncio.run(
            run(
                parse_args()
            )
        )
    )
