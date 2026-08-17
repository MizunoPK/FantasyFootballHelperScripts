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
import re
from pathlib import Path
from typing import Any, Dict, List

from player_data_fetcher.espn_client import ESPNClient
from player_data_fetcher.espn_credentials import load_espn_env
from player_data_fetcher.player_data_fetcher_main import Settings

SCHEMA_VERSION = 1
SANITIZER_VERSION = 1
SENTINEL_LEAGUE_ID = 999999999

# ESPN's SWID cookie (the live authenticated credential) and its `members[].id`
# counterpart are both `{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}`-shaped GUIDs.
# Any GUID-shaped string surviving sanitization is treated as unmodelled
# identity data (KDD2 fail-closed hardening, polish pass 3).
_GUID_PATTERN = re.compile(
    r"\{?[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\}?"
)


class SanitizationLeakError(RuntimeError):
    """Raised when sanitized output still contains identity-shaped data.

    Fail-closed guard: refusing to write a corpus is always preferred over
    emitting one that might carry a real ESPN member GUID or name.
    """


def _scrub_identity_shaped_strings(value: Any) -> Any:
    """Recursively replace any GUID-shaped string found anywhere in `value`.

    Used on fields (e.g. `members[].notificationSettings`) whose sub-shape
    is not fully modeled but which may embed a GUID-shaped identity value.
    """
    if isinstance(value, dict):
        return {k: _scrub_identity_shaped_strings(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_scrub_identity_shaped_strings(v) for v in value]
    if isinstance(value, str) and _GUID_PATTERN.search(value):
        return "[REDACTED-IDENTITY-VALUE]"
    return value


def assert_no_identity_leak(payload: Dict[str, Any]) -> None:
    """Fail-closed post-sanitization scan (KDD2 hardening, polish pass 3).

    Scans the full serialized payload for any GUID-shaped value anywhere.
    A clean `sanitize_league_payload()` output should never contain one --
    a hit means some ESPN field carrying identity data (a `members[].id`
    SWID-shaped credential, or any other unmodelled field) was not
    recognized and replaced by the sanitizer. This is deliberately a
    write-time gate rather than an input allowlist: an allowlist that
    dropped unknown top-level keys would risk silently discarding fields
    the replay corpus actually needs (this script's whole job is to
    preserve mDraftDetail/mTeam shape for replay), whereas refusing to
    write forces a human to explicitly teach the sanitizer about the new
    field before any corpus reaches disk.

    Raises:
        SanitizationLeakError: If a GUID-shaped value is found anywhere.
    """
    match = _GUID_PATTERN.search(json.dumps(payload))
    if match:
        raise SanitizationLeakError(
            f"Refusing to write corpus: sanitized payload still contains a "
            f"GUID-shaped value ({match.group(0)!r}) after sanitize_league_payload(). "
            f"This means some ESPN payload field carrying identity data (e.g. a "
            f"members[].id SWID-shaped credential) was not recognized and replaced. "
            f"Add handling for the offending field to sanitize_league_payload() "
            f"before re-running -- do not bypass this check."
        )


def sanitize_league_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministically sanitize a raw league payload (KDD2).

    Replaces the production league ID, ESPN owner identifiers, real
    team/league names, and the top-level `members` array (owner GUIDs
    a.k.a. the SWID-shaped credential, first/last/display names,
    notification settings) with deterministic positional synthetic
    values. Preserves every pick<->team<->player integer relationship:
    team `id`, `playerId`, `overallPickNumber`, `roundId`, and
    `lineupSlotId` are left untouched — only identity-bearing
    string/name fields and the league ID are replaced.

    Any `members[].id` referenced by `teams[].owners` or
    `teams[].primaryOwner` is replaced consistently (same real GUID ->
    same synthetic token everywhere it appears), so identity
    relationships the corpus depends on for replay are preserved.

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

    # Sanitize the top-level `members` array first so its real-GUID ->
    # synthetic-token mapping is available when sanitizing `teams` below.
    member_id_map: Dict[str, str] = {}
    members = sanitized.get("members")
    if isinstance(members, list):
        for idx, member in enumerate(members, start=1):
            if not isinstance(member, dict):
                continue
            synthetic_id = f"SYNTHETIC-MEMBER-{idx}"
            real_id = member.get("id")
            if isinstance(real_id, str):
                member_id_map[real_id] = synthetic_id
            if "id" in member:
                member["id"] = synthetic_id
            if "firstName" in member:
                member["firstName"] = "Synthetic"
            if "lastName" in member:
                member["lastName"] = f"Member{idx}"
            if "displayName" in member:
                member["displayName"] = f"syntheticmember{idx}"
            if "notificationSettings" in member:
                member["notificationSettings"] = _scrub_identity_shaped_strings(
                    member["notificationSettings"]
                )

    for idx, team in enumerate(sanitized.get("teams", []), start=1):
        for name_field in ("name", "location", "nickname", "abbrev"):
            if name_field in team:
                team[name_field] = f"Synthetic Team {idx}"
        owners = team.get("owners")
        if isinstance(owners, list):
            new_owners = []
            for j, owner in enumerate(owners, start=1):
                if isinstance(owner, str) and owner in member_id_map:
                    new_owners.append(member_id_map[owner])
                else:
                    new_owners.append(f"Synthetic Owner {j}")
            team["owners"] = new_owners
        if "primaryOwner" in team:
            real_primary = team["primaryOwner"]
            team["primaryOwner"] = member_id_map.get(real_primary, "SYNTHETIC-PRIMARY-OWNER")

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
        SanitizationLeakError: If `sanitized_source` or any step still
            contains a GUID-shaped value after sanitization (fail-closed
            guard, polish pass 3) -- checked before anything is written.
    """
    if output_dir.exists():
        raise FileExistsError(
            f"Corpus directory already exists: {output_dir}. Refusing to overwrite. "
            f"Review the existing corpus and explicitly replace it (rm -r) before rerunning, "
            f"or write to a fresh temp/output location and swap it in as a reviewed step."
        )

    # Fail-closed: refuse to write anything if identity-shaped data survived
    # sanitization, in the source or in any derived step.
    assert_no_identity_leak(sanitized_source)
    for step_payload in steps:
        assert_no_identity_leak(step_payload)

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
    """Call ESPNClient._get_raw_league_snapshot once (R5-a) and close the client.

    Must enter `client.session()` before issuing the request: `BaseAPIClient` only
    populates `self._client` inside `session()` (espn_client.py), and `_make_request`
    dereferences it unconditionally. `session()`'s own `finally` does not tear the
    client down (that is `close()`'s job), so the explicit `close()` below is still
    required and is not redundant with entering `session()`.
    """
    settings = Settings(season=season)
    client = ESPNClient(settings)
    try:
        async with client.session():
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

    # Entry-point startup: load .env before any credential read (D17.1 UD3 --
    # explicit, non-import-time loader; this is the designated caller).
    load_espn_env()

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
