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
from unittest.mock import patch

import pytest

from player_data_fetcher.generate_espn_draft_corpus import (
    sanitize_league_payload,
    derive_steps,
    write_corpus,
    main,
    _capture_raw_payload,
    assert_no_identity_leak,
    SENTINEL_LEAGUE_ID,
    SanitizationLeakError,
)
from player_data_fetcher.espn_client import ESPNClient


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


class TestSanitizeMembersArray:
    """Regression tests (polish pass 3, D17.3): the top-level `members`
    array -- carrying `firstName`/`lastName`/`displayName`,
    `notificationSettings`, and an `id` that is the SWID-shaped account
    GUID -- must be fully scrubbed, and any `teams[].owners` /
    `teams[].primaryOwner` reference to a `members[].id` must resolve to
    the *same* synthetic token consistently.
    """

    @pytest.fixture
    def raw_payload_with_members(self):
        return {
            "id": 555,
            "settings": {"name": "Real League Name"},
            "members": [
                {
                    "id": "{AAAAAAAA-1111-2222-3333-444444444444}",
                    "firstName": "Real",
                    "lastName": "Operator",
                    "displayName": "realoperator",
                    "notificationSettings": [
                        {"id": "{AAAAAAAA-1111-2222-3333-444444444444}", "enabled": True}
                    ],
                },
                {
                    "id": "{BBBBBBBB-1111-2222-3333-444444444444}",
                    "firstName": "Other",
                    "lastName": "Owner",
                    "displayName": "otherowner",
                    "notificationSettings": [],
                },
            ],
            "teams": [
                {
                    "id": 1,
                    "name": "Real Team One",
                    "location": "Real",
                    "nickname": "One",
                    "abbrev": "RT1",
                    "owners": ["{AAAAAAAA-1111-2222-3333-444444444444}"],
                    "primaryOwner": "{AAAAAAAA-1111-2222-3333-444444444444}",
                },
                {
                    "id": 2,
                    "name": "Real Team Two",
                    "location": "Real",
                    "nickname": "Two",
                    "abbrev": "RT2",
                    "owners": ["{BBBBBBBB-1111-2222-3333-444444444444}"],
                    "primaryOwner": "{BBBBBBBB-1111-2222-3333-444444444444}",
                },
            ],
            "draftDetail": {
                "drafted": True,
                "inProgress": False,
                "picks": [
                    {"overallPickNumber": 1, "playerId": 4242, "teamId": 1, "roundId": 1, "lineupSlotId": 2},
                ],
            },
        }

    def test_members_bearing_payload_is_fully_scrubbed(self, raw_payload_with_members):
        result = sanitize_league_payload(raw_payload_with_members)
        dumped = json.dumps(result)

        # No real name, real GUID, or the raw notificationSettings id leaks anywhere.
        for real_value in (
            "Real", "Operator", "realoperator", "Other", "otherowner",
            "{AAAAAAAA-1111-2222-3333-444444444444}",
            "{BBBBBBBB-1111-2222-3333-444444444444}",
        ):
            assert real_value not in dumped

        assert result["members"][0]["id"] == "SYNTHETIC-MEMBER-1"
        assert result["members"][1]["id"] == "SYNTHETIC-MEMBER-2"
        assert result["members"][0]["firstName"] == "Synthetic"
        assert result["members"][0]["lastName"] == "Member1"
        assert result["members"][0]["displayName"] == "syntheticmember1"
        # notificationSettings' embedded GUID was scrubbed too.
        assert result["members"][0]["notificationSettings"][0]["id"] == "[REDACTED-IDENTITY-VALUE]"

        # Passes the fail-closed scan cleanly.
        assert_no_identity_leak(result)

    def test_member_id_substitution_is_consistent_across_references(self, raw_payload_with_members):
        result = sanitize_league_payload(raw_payload_with_members)

        # teams[0].owners[0] and teams[0].primaryOwner both referenced the same
        # real member GUID -- they must resolve to the same synthetic token,
        # and that token must equal the member's own sanitized id.
        assert result["teams"][0]["owners"][0] == result["members"][0]["id"]
        assert result["teams"][0]["primaryOwner"] == result["members"][0]["id"]
        assert result["teams"][1]["owners"][0] == result["members"][1]["id"]
        assert result["teams"][1]["primaryOwner"] == result["members"][1]["id"]
        # Distinct real owners still map to distinct synthetic tokens.
        assert result["teams"][0]["primaryOwner"] != result["teams"][1]["primaryOwner"]


class TestAssertNoIdentityLeak:
    """Regression tests (polish pass 3, D17.3): the fail-closed guard must
    actually trigger on an unmodelled identity-bearing field, and write_corpus
    must refuse to write anything when it does.
    """

    def test_raises_on_guid_shaped_value_anywhere(self):
        with pytest.raises(SanitizationLeakError, match="GUID-shaped value"):
            assert_no_identity_leak(
                {"someUnmodelledField": "{DEADBEEF-0000-0000-0000-000000000000}"}
            )

    def test_passes_on_payload_with_no_guid_shaped_values(self):
        assert_no_identity_leak(
            {"id": 999999999, "teams": [{"owners": ["Synthetic Owner 1"]}]}
        )

    def test_write_corpus_refuses_to_write_when_leak_detected(self, tmp_path, raw_payload):
        # Simulate an unmodelled field slipping past sanitize_league_payload by
        # injecting a raw GUID directly into an already-"sanitized" payload.
        sanitized = sanitize_league_payload(raw_payload)
        sanitized["someUnmodelledField"] = "{DEADBEEF-0000-0000-0000-000000000000}"
        steps = derive_steps(sanitized)
        target = tmp_path / "league_draft"

        with pytest.raises(SanitizationLeakError):
            write_corpus(target, sanitized, steps)

        assert not target.exists()


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


class TestMainLoadsEnvBeforeCredentialRead:
    """Regression test (polish pass, D17.3): main() must call load_espn_env()
    at entry-point startup, before any credential read, per D17.1 UD3's
    "called from fetcher startup" design. Without this call the offline test
    suite is green (tests inject credentials directly) while the real CLI
    path fails with ConfigurationError before any network call -- this test
    exercises the actual entry point rather than injecting credentials, so
    it fails if the load_espn_env() call is ever removed or reordered.
    """

    def test_main_calls_load_espn_env_before_capturing_payload(self, tmp_path, monkeypatch):
        call_order = []

        def record_load_espn_env(*args, **kwargs):
            call_order.append("load_espn_env")

        def record_capture(coro):
            call_order.append("capture_raw_payload")
            coro.close()  # avoid "coroutine was never awaited" warning
            return {
                "id": 1,
                "settings": {},
                "teams": [],
                "draftDetail": {"picks": []},
            }

        output_dir = tmp_path / "league_draft"
        monkeypatch.setattr(
            "sys.argv",
            [
                "generate_espn_draft_corpus.py",
                "--league-id",
                "123",
                "--season",
                "2026",
                "--output-dir",
                str(output_dir),
            ],
        )

        with patch(
            "player_data_fetcher.generate_espn_draft_corpus.load_espn_env",
            side_effect=record_load_espn_env,
        ) as mock_load_env, patch(
            "player_data_fetcher.generate_espn_draft_corpus.asyncio.run",
            side_effect=record_capture,
        ):
            main()

        mock_load_env.assert_called_once()
        assert call_order == ["load_espn_env", "capture_raw_payload"], (
            "load_espn_env() must be called before the credential-requiring "
            "payload capture, so a missing .env fails clearly rather than "
            "the loader silently never running."
        )


class TestCapturePayloadEntersSession:
    """Regression test (2nd polish pass, D17.3): _capture_raw_payload() must enter
    ESPNClient.session() before calling _get_raw_league_snapshot(). BaseAPIClient
    only populates self._client inside session() (espn_client.py); _make_request
    dereferences self._client unconditionally. The prior implementation called
    client._get_raw_league_snapshot(...) directly, never entering session(), so
    self._client stayed None and every real invocation died with an AttributeError
    on the very first request -- retried 3x by tenacity and surfacing as a
    tenacity.RetryError, before any socket was opened. No offline test caught this
    because none exercised the real client lifecycle end to end. This test drives
    the actual production coroutine (not a mock standing in for the whole call) and
    asserts the client's session is populated at the moment the raw-snapshot request
    fires, and that it is torn down afterward.
    """

    @pytest.mark.asyncio
    async def test_client_has_active_session_when_snapshot_is_requested(self, monkeypatch):
        monkeypatch.setenv("espn_s2", "fake-s2")
        monkeypatch.setenv("SWID", "{fake-swid}")

        observed = {}

        async def fake_make_request(self, method, url, **kwargs):
            # If _capture_raw_payload had not entered session() first, self._client
            # would be None here and a real BaseAPIClient._make_request would raise
            # AttributeError on self._client.request(...).
            observed["client_was_active"] = self._client is not None
            return {"id": 1, "settings": {}, "teams": [], "draftDetail": {"picks": []}}

        with patch.object(ESPNClient, "_make_request", new=fake_make_request):
            result = await _capture_raw_payload(league_id=123, season=2026)

        assert observed.get("client_was_active") is True, (
            "_get_raw_league_snapshot() must run with an active session "
            "(client._client populated), not None."
        )
        assert result == {"id": 1, "settings": {}, "teams": [], "draftDetail": {"picks": []}}

    @pytest.mark.asyncio
    async def test_get_raw_league_snapshot_fails_clearly_without_session(self, monkeypatch):
        """The private seam itself: calling it with no active session must raise a
        clear RuntimeError rather than an AttributeError on a None client."""
        monkeypatch.setenv("espn_s2", "fake-s2")
        monkeypatch.setenv("SWID", "{fake-swid}")

        from player_data_fetcher.player_data_fetcher_main import Settings

        client = ESPNClient(Settings(season=2026))
        assert client._client is None

        with pytest.raises(RuntimeError, match="session"):
            await client._get_raw_league_snapshot(123, 2026)
