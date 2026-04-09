"""Smoke-test the Baidu Maps API flow used by the official Python MCP server.

This script does not require `mcp_server_baidu_maps` to be installed locally.
It validates the same HTTP endpoints and argument patterns that the official
server uses for:
- map_geocode
- map_search_places
- map_directions
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen


DEFAULT_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


def load_dotenv(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def call_json(endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    url = f"{endpoint}?{urlencode(params)}"
    with urlopen(url, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def ensure_ok(label: str, payload: dict[str, Any]) -> None:
    status = payload.get("status")
    if status != 0:
        raise RuntimeError(f"{label} failed: {json.dumps(payload, ensure_ascii=False)}")


def geocode(api_key: str, address: str) -> tuple[float, float]:
    payload = call_json(
        "https://api.map.baidu.com/geocoding/v3/",
        {
            "ak": api_key,
            "output": "json",
            "address": address,
            "from": "py_mcp",
        },
    )
    ensure_ok("map_geocode", payload)
    location = payload["result"]["location"]
    return float(location["lat"]), float(location["lng"])


def search_places(
    api_key: str,
    query: str,
    region: str,
    tag: str | None = None,
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {
        "ak": api_key,
        "output": "json",
        "query": query,
        "region": region,
        "region_limit": "true",
        "scope": 2,
        "from": "py_mcp",
    }
    if tag:
        params["type"] = tag

    payload = call_json("https://api.map.baidu.com/place/v3/region", params)
    ensure_ok("map_search_places", payload)
    return payload.get("results", [])


def directions(api_key: str, origin: str, destination: str, model: str) -> dict[str, Any]:
    origin_lat, origin_lng = geocode(api_key, origin)
    destination_lat, destination_lng = geocode(api_key, destination)

    payload = call_json(
        f"https://api.map.baidu.com/directionlite/v1/{model}",
        {
            "ak": api_key,
            "output": "json",
            "origin": f"{origin_lat},{origin_lng}",
            "destination": f"{destination_lat},{destination_lng}",
            "from": "py_mcp",
        },
    )
    ensure_ok("map_directions", payload)
    routes = payload.get("result", {}).get("routes", [])
    if not routes:
        raise RuntimeError(f"map_directions returned no routes: {json.dumps(payload, ensure_ascii=False)}")
    return routes[0]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_PATH), help="Path to the .env file")
    parser.add_argument("--region", default="北京市", help="Region used for map_search_places")
    parser.add_argument("--query", default="故宫博物院", help="POI query used for map_search_places")
    parser.add_argument("--tag", default="旅游景点", help="Optional place tag used for map_search_places")
    parser.add_argument("--origin", default="北京市故宫博物院", help="Origin for map_directions")
    parser.add_argument("--destination", default="北京市天坛公园", help="Destination for map_directions")
    parser.add_argument(
        "--model",
        default="walking",
        choices=["driving", "riding", "walking", "transit"],
        help="Routing mode for map_directions",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    load_dotenv(Path(args.env_file))

    api_key = os.getenv("BAIDU_MAPS_API_KEY", "").strip()
    if not api_key:
        print("FAIL: BAIDU_MAPS_API_KEY is missing", file=sys.stderr)
        return 1

    try:
        lat, lng = geocode(api_key, args.origin)
        print(f"PASS map_geocode: {args.origin} -> lat={lat:.6f}, lng={lng:.6f}")

        results = search_places(api_key, args.query, args.region, args.tag or None)
        if not results:
            raise RuntimeError(
                "map_search_places returned zero results. "
                "Try a shorter query phrase, for example '故宫博物院' instead of a full question."
            )
        top = results[0]
        print(
            "PASS map_search_places: "
            f"top_result={top.get('name')} | address={top.get('address', '')}"
        )

        route = directions(api_key, args.origin, args.destination, args.model)
        print(
            "PASS map_directions: "
            f"distance={route.get('distance')}m | duration={route.get('duration')}s"
        )
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
