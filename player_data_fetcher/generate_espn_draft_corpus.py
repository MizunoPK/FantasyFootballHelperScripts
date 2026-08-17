#!/usr/bin/env python3
"""
ESPN Draft Corpus Generator

Standalone, manually-run CLI tool that captures ONE real authenticated ESPN
private-league snapshot (mDraftDetail + mTeam), sanitizes it (KDD2), and
locally derives the immutable step_NNN.json / manifest.json replay corpus
under tests/fixtures/espn_api/league_draft/ (TD5, R5).

This script is NEVER imported by run_all_tests.py and is never marked
@pytest.mark.live_api — it is a one-time authoring action against a real
league, not a repeatable test (KDD1).

Usage:
    python -m player_data_fetcher.generate_espn_draft_corpus \\
        --league-id <ESPN_LEAGUE_ID> --season <season> \\
        --output-dir tests/fixtures/espn_api/league_draft

Author: Kai Mizuno
"""

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

from player_data_fetcher.espn_client import ESPNClient
from player_data_fetcher.player_data_fetcher_main import Settings

SCHEMA_VERSION = 1
SANITIZER_VERSION = 1
SENTINEL_LEAGUE_ID = 999999999


def sanitize_league_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministically sanitize a raw league payload (KDD2).

    Replaces the production league ID, ESPN owner identifiers, and real
    team/league names with deterministic positional synthetic values.
    Preserves every pick<->team<->player integer relationship: team `id`,
    `playerId`, `overallPickNumber`, `roundId`, and `lineupSlotId` are
    left untouched — only identity-bearing string/name fields and the
    league ID are replaced.

    Args:
        raw: Raw dict as returned by ESPNClient._get_raw_league_snapshot.

    Returns:
        A new dict (the input is not mutated) with sensitive identity
        fields replaced by deterministic synthetic values.
    """
    sanitized = json.loads(json.dumps(raw))  # deep copy, JSON-safe

    if "id" in sanitized:
        sanitized["id"] = SENTINEL_LEAGUE_ID

    settings_block = sanitized.get("settings")
    if isinstance(settings_block, dict) and "name" in settings_block:
        settings_block["name"] = "Synthetic League"

    for idx, team in enumerate(sanitized.get("teams", []), start=1):
        for name_field in ("name", "location", "nickname", "abbrev"):
            if name_field in team:
                team[name_field] = f"Synthetic Team {idx}"
        owners = team.get("owners")
        if isinstance(owners, list):
            team["owners"] = [f"Synthetic Owner {j}" for j, _ in enumerate(owners, start=1)]

    return sanitized


def derive_steps(sanitized_source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Locally derive every step_NNN payload as a picks[0:N] truncation.

    Args:
        sanitized_source: The sanitized source.json content.

    Returns:
        List of step payload dicts, one per completed-picks count from 0
        through len(picks) inclusive, index-ordered.
    """
    draft_detail = sanitized_source.get("draftDetail", {})
    picks = draft_detail.get("picks", [])

    steps = []
    for n in range(len(picks) + 1):
        step_payload = json.loads(json.dumps(sanitized_source))
        step_payload["draftDetail"]["picks"] = picks[:n]
        steps.append(step_payload)
    return steps


def write_corpus(output_dir: Path, sanitized_source: Dict[str, Any], steps: List[Dict[str, Any]]) -> None:
    """Write source.json, step_NNN.json files, and manifest.json (R5).

    Refuses to run if output_dir already exists (no-overwrite, R5-e).

    Args:
        output_dir: Target league_draft/ directory (must not yet exist).
        sanitized_source: Sanitized source.json content.
        steps: Ordered list of step payloads from derive_steps().

    Raises:
        FileExistsError: If output_dir already exists.
    """
    if output_dir.exists():
        raise FileExistsError(
            f"Corpus directory already exists: {output_dir}. Refusing to overwrite. "
            f"Review the existing corpus and explicitly replace it (rm -r) before rerunning, "
            f"or write to a fresh temp/output location and swap it in as a reviewed step."
        )

    output_dir.mkdir(parents=True)

    source_path = output_dir / "source.json"
    source_path.write_text(json.dumps(sanitized_source, indent=2))

    entries = []
    width = max(3, len(str(len(steps) - 1)))
    for step_idx, step_payload in enumerate(steps):
        filename = f"step_{step_idx:0{width}d}.json"
        file_path = output_dir / filename
        content = json.dumps(step_payload, indent=2)
        file_path.write_text(content)
        sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
        completed_picks = sum(
            1 for p in step_payload["draftDetail"]["picks"] if p.get("playerId") != -1
        )
        entries.append(
            {
                "step": step_idx,
                "completed_picks": completed_picks,
                "file": filename,
                "sha256": sha256,
            }
        )

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "provenance": {
            "capture_date": __import__("datetime").date.today().isoformat(),
            "endpoint_class": "league_draft",
            "views": ["mDraftDetail", "mTeam"],
            "sanitizer_version": SANITIZER_VERSION,
        },
        "entries": entries,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))


async def _capture_raw_payload(league_id: int, season: int) -> Dict[str, Any]:
    """Call ESPNClient._get_raw_league_snapshot once (R5-a) and close the client."""
    settings = Settings(season=season)
    client = ESPNClient(settings)
    try:
        return await client._get_raw_league_snapshot(league_id, season)
    finally:
        await client.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the sanitized ESPN league_draft replay corpus.")
    parser.add_argument("--league-id", type=int, required=True, help="Real ESPN league ID (never committed).")
    parser.add_argument("--season", type=int, required=True, help="Season year.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("tests/fixtures/espn_api/league_draft"),
        help="Target corpus directory (must not already exist).",
    )
    args = parser.parse_args()

    raw = asyncio.run(_capture_raw_payload(args.league_id, args.season))
    sanitized = sanitize_league_payload(raw)
    steps = derive_steps(sanitized)

    try:
        write_corpus(args.output_dir, sanitized, steps)
    except FileExistsError as e:
        print(f"ERROR: {e}")
        raise SystemExit(1)

    print(f"Wrote {len(steps)} steps + manifest.json to {args.output_dir}")


if __name__ == "__main__":
    main()
