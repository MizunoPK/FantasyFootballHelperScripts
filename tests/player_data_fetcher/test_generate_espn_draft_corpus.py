#!/usr/bin/env python3
"""
Tests for the ESPN Draft Corpus Generator

Offline, credential-free tests exercising sanitization, step derivation,
and manifest/no-overwrite writing against a small synthetic raw payload
(never a real captured one) — this module's whole job is offline-testable,
since generate_espn_draft_corpus.py itself is a manually-run CLI (KDD1).

Author: Kai Mizuno
"""

import hashlib
import json

import pytest

from player_data_fetcher.generate_espn_draft_corpus import (
    sanitize_league_payload,
    derive_steps,
    write_corpus,
    SENTINEL_LEAGUE_ID,
)


# FIXTURES

@pytest.fixture
def raw_payload():
    return {
        "id": 555,
        "settings": {"name": "Real League Name"},
        "teams": [
            {
                "id": 1,
                "name": "Real Team One",
                "location": "Real",
                "nickname": "One",
                "abbrev": "RT1",
                "owners": ["{real-owner-guid-1}"],
            },
            {
                "id": 2,
                "name": "Real Team Two",
                "location": "Real",
                "nickname": "Two",
                "abbrev": "RT2",
                "owners": ["{real-owner-guid-2}"],
            },
        ],
        "draftDetail": {
            "drafted": True,
            "inProgress": False,
            "picks": [
                {"overallPickNumber": 1, "playerId": 4242, "teamId": 1, "roundId": 1, "lineupSlotId": 2},
                {"overallPickNumber": 2, "playerId": -1, "teamId": 2, "roundId": 1, "lineupSlotId": 3},
            ],
        },
    }


class TestSanitizeLeaguePayload:
    """Test sanitize_league_payload (KDD2)."""

    def test_replaces_league_id_with_sentinel(self, raw_payload):
        result = sanitize_league_payload(raw_payload)
        assert result["id"] == SENTINEL_LEAGUE_ID

    def test_replaces_team_names_deterministically(self, raw_payload):
        result = sanitize_league_payload(raw_payload)
        assert result["teams"][0]["name"] == "Synthetic Team 1"
        assert result["teams"][1]["name"] == "Synthetic Team 2"
        assert "Real Team One" not in json.dumps(result)
        assert "Real Team Two" not in json.dumps(result)

    def test_replaces_owner_identifiers(self, raw_payload):
        result = sanitize_league_payload(raw_payload)
        assert result["teams"][0]["owners"] == ["Synthetic Owner 1"]
        assert "{real-owner-guid-1}" not in json.dumps(result)
        assert "{real-owner-guid-2}" not in json.dumps(result)

    def test_preserves_integer_relationships(self, raw_payload):
        result = sanitize_league_payload(raw_payload)
        assert result["teams"][0]["id"] == 1
        assert result["teams"][1]["id"] == 2
        picks = result["draftDetail"]["picks"]
        assert picks[0]["playerId"] == 4242
        assert picks[0]["teamId"] == 1
        assert picks[0]["overallPickNumber"] == 1
        assert picks[1]["playerId"] == -1

    def test_does_not_mutate_input(self, raw_payload):
        original = json.loads(json.dumps(raw_payload))
        sanitize_league_payload(raw_payload)
        assert raw_payload == original


class TestDeriveSteps:
    """Test derive_steps (R5-c)."""

    def test_produces_one_step_per_pick_count_inclusive_of_zero(self, raw_payload):
        sanitized = sanitize_league_payload(raw_payload)
        steps = derive_steps(sanitized)
        assert len(steps) == 3  # 0, 1, 2 completed picks

    def test_step_zero_has_no_picks(self, raw_payload):
        sanitized = sanitize_league_payload(raw_payload)
        steps = derive_steps(sanitized)
        assert steps[0]["draftDetail"]["picks"] == []

    def test_final_step_has_all_picks(self, raw_payload):
        sanitized = sanitize_league_payload(raw_payload)
        steps = derive_steps(sanitized)
        assert len(steps[-1]["draftDetail"]["picks"]) == 2

    def test_steps_are_independent_copies(self, raw_payload):
        sanitized = sanitize_league_payload(raw_payload)
        steps = derive_steps(sanitized)
        steps[0]["draftDetail"]["picks"].append({"playerId": 999})
        assert steps[1]["draftDetail"]["picks"] != steps[0]["draftDetail"]["picks"]


class TestWriteCorpus:
    """Test write_corpus (R5-d, R5-e)."""

    def test_writes_source_and_manifest(self, tmp_path, raw_payload):
        sanitized = sanitize_league_payload(raw_payload)
        steps = derive_steps(sanitized)
        target = tmp_path / "league_draft"
        write_corpus(target, sanitized, steps)
        assert (target / "source.json").exists()
        assert (target / "manifest.json").exists()

    def test_manifest_entries_are_contiguous_and_hash_verified(self, tmp_path, raw_payload):
        sanitized = sanitize_league_payload(raw_payload)
        steps = derive_steps(sanitized)
        target = tmp_path / "league_draft"
        write_corpus(target, sanitized, steps)
        manifest = json.loads((target / "manifest.json").read_text())
        entries = manifest["entries"]
        assert [e["step"] for e in entries] == list(range(len(steps)))
        for entry in entries:
            file_path = target / entry["file"]
            content = file_path.read_bytes()
            assert hashlib.sha256(content).hexdigest() == entry["sha256"]

    def test_refuses_to_overwrite_existing_directory(self, tmp_path, raw_payload):
        sanitized = sanitize_league_payload(raw_payload)
        steps = derive_steps(sanitized)
        target = tmp_path / "league_draft"
        target.mkdir()
        with pytest.raises(FileExistsError):
            write_corpus(target, sanitized, steps)
        assert list(target.iterdir()) == []

    def test_writes_nothing_on_refusal(self, tmp_path, raw_payload):
        sanitized = sanitize_league_payload(raw_payload)
        steps = derive_steps(sanitized)
        target = tmp_path / "league_draft"
        target.mkdir()
        (target / "sentinel.txt").write_text("pre-existing")
        with pytest.raises(FileExistsError):
            write_corpus(target, sanitized, steps)
        assert [p.name for p in target.iterdir()] == ["sentinel.txt"]
