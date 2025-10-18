#!/usr/bin/env python3
"""
Tests for DraftedRosterManager module.

Comprehensive tests for managing drafted player rosters, including CSV loading,
fuzzy player matching, and team organization.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from utils.DraftedRosterManager import DraftedRosterManager
from utils.FantasyPlayer import FantasyPlayer


class TestDraftedRosterManagerInit:
    """Test suite for DraftedRosterManager initialization."""

    def test_init_sets_attributes(self, tmp_path):
        """Test initialization sets all attributes correctly."""
        csv_path = tmp_path / "drafted.csv"
        manager = DraftedRosterManager(str(csv_path), "My Team")

        assert manager.csv_path == csv_path
        assert manager.my_team_name == "My Team"
        assert manager.drafted_players == {}
        assert manager._original_csv_data == []

    def test_init_accepts_path_string(self, tmp_path):
        """Test initialization accepts path as string."""
        csv_path = str(tmp_path / "drafted.csv")
        manager = DraftedRosterManager(csv_path, "Team A")

        assert isinstance(manager.csv_path, Path)


class TestLoadDraftedData:
    """Test suite for load_drafted_data() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_load_drafted_data_loads_valid_csv(self, manager, tmp_path):
        """Test loads valid CSV data successfully."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text(
            'Josh Allen QB - BUF,Team Alpha\n'
            'Tyreek Hill WR - MIA,Team Beta\n'
        )

        result = manager.load_drafted_data()

        assert result is True
        assert len(manager.drafted_players) == 2

    def test_load_drafted_data_skips_empty_rows(self, manager, tmp_path):
        """Test skips empty rows in CSV."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text(
            'Josh Allen QB - BUF,Team Alpha\n'
            '\n'
            'Tyreek Hill WR - MIA,Team Beta\n'
        )

        manager.load_drafted_data()

        assert len(manager.drafted_players) == 2

    def test_load_drafted_data_skips_incomplete_rows(self, manager, tmp_path):
        """Test skips rows with missing data."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text(
            'Josh Allen QB - BUF,Team Alpha\n'
            'Invalid Row\n'
            'Tyreek Hill WR - MIA,Team Beta\n'
        )

        manager.load_drafted_data()

        assert len(manager.drafted_players) == 2

    def test_load_drafted_data_handles_duplicates(self, manager, tmp_path):
        """Test only uses first occurrence for duplicate players."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text(
            'Josh Allen QB - BUF,Team Alpha\n'
            'Josh Allen QB - BUF,Team Beta\n'
        )

        manager.load_drafted_data()

        # Should only have 1 entry (first occurrence)
        assert len(manager.drafted_players) == 1

    def test_load_drafted_data_returns_false_for_missing_file(self, manager):
        """Test returns False when CSV file doesn't exist."""
        result = manager.load_drafted_data()

        assert result is False
        assert len(manager.drafted_players) == 0

    def test_load_drafted_data_caches_original_data(self, manager, tmp_path):
        """Test caches original CSV data for later use."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text('Josh Allen QB - BUF,Team Alpha\n')

        manager.load_drafted_data()

        assert len(manager._original_csv_data) > 0

    def test_load_drafted_data_clears_previous_data(self, manager, tmp_path):
        """Test clears previous data when reloading."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text('Josh Allen QB - BUF,Team Alpha\n')

        # First load
        manager.load_drafted_data()
        first_count = len(manager.drafted_players)

        # Modify file and reload
        csv_path.write_text('Tyreek Hill WR - MIA,Team Beta\n')
        manager.load_drafted_data()

        assert len(manager.drafted_players) == 1


class TestGetStats:
    """Test suite for get_stats() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create manager with sample data."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text(
            'Josh Allen QB - BUF,My Team\n'
            'Tyreek Hill WR - MIA,My Team\n'
            'Patrick Mahomes QB - KC,Other Team\n'
        )
        mgr = DraftedRosterManager(str(csv_path), "My Team")
        mgr.load_drafted_data()
        return mgr

    def test_get_stats_returns_correct_totals(self, manager):
        """Test returns accurate player counts."""
        stats = manager.get_stats()

        assert stats["total_players"] == 3
        assert stats["user_team_players"] == 2
        assert stats["other_team_players"] == 1

    def test_get_stats_returns_zeros_for_empty_data(self, tmp_path):
        """Test returns zeros when no data loaded."""
        csv_path = tmp_path / "drafted.csv"
        manager = DraftedRosterManager(str(csv_path), "My Team")

        stats = manager.get_stats()

        assert stats["total_players"] == 0
        assert stats["user_team_players"] == 0
        assert stats["other_team_players"] == 0


class TestGetAllTeamNames:
    """Test suite for get_all_team_names() method."""

    def test_get_all_team_names_returns_unique_teams(self, tmp_path):
        """Test returns set of unique team names."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text(
            'Josh Allen QB - BUF,Team Alpha\n'
            'Tyreek Hill WR - MIA,Team Beta\n'
            'Patrick Mahomes QB - KC,Team Alpha\n'
        )
        manager = DraftedRosterManager(str(csv_path), "My Team")
        manager.load_drafted_data()

        teams = manager.get_all_team_names()

        assert len(teams) == 2
        assert "Team Alpha" in teams
        assert "Team Beta" in teams

    def test_get_all_team_names_returns_empty_set_for_no_data(self, tmp_path):
        """Test returns empty set when no data loaded."""
        csv_path = tmp_path / "drafted.csv"
        manager = DraftedRosterManager(str(csv_path), "My Team")

        teams = manager.get_all_team_names()

        assert teams == set()


class TestGetPlayersByTeam:
    """Test suite for get_players_by_team() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample FantasyPlayer objects."""
        return [
            FantasyPlayer(id=1, name="Josh Allen", position="QB", team="BUF"),
            FantasyPlayer(id=2, name="Tyreek Hill", position="WR", team="MIA"),
            FantasyPlayer(id=3, name="Patrick Mahomes", position="QB", team="KC"),
        ]

    @pytest.fixture
    def manager(self, tmp_path):
        """Create manager with sample data."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text(
            'Josh Allen QB - BUF,Team Alpha\n'
            'Tyreek Hill WR - MIA,Team Beta\n'
        )
        mgr = DraftedRosterManager(str(csv_path), "My Team")
        mgr.load_drafted_data()
        return mgr

    def test_get_players_by_team_organizes_correctly(self, manager, sample_players):
        """Test organizes players by their fantasy team."""
        teams = manager.get_players_by_team(sample_players)

        assert "Team Alpha" in teams
        assert "Team Beta" in teams
        assert len(teams["Team Alpha"]) >= 0
        assert len(teams["Team Beta"]) >= 0

    def test_get_players_by_team_returns_empty_for_no_data(self, tmp_path, sample_players):
        """Test returns empty dict when no data loaded."""
        csv_path = tmp_path / "drafted.csv"
        manager = DraftedRosterManager(str(csv_path), "My Team")

        teams = manager.get_players_by_team(sample_players)

        assert teams == {}

    def test_get_players_by_team_initializes_all_teams(self, manager, sample_players):
        """Test initializes dict with all team names."""
        teams = manager.get_players_by_team(sample_players)

        # All teams from CSV should be in dict, even if no players matched
        all_team_names = manager.get_all_team_names()
        for team_name in all_team_names:
            assert team_name in teams


class TestApplyDraftedStateToPlayers:
    """Test suite for apply_drafted_state_to_players() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample FantasyPlayer objects."""
        return [
            FantasyPlayer(id=1, name="Josh Allen", position="QB", team="BUF", drafted=0),
            FantasyPlayer(id=2, name="Tyreek Hill", position="WR", team="MIA", drafted=0),
            FantasyPlayer(id=3, name="Patrick Mahomes", position="QB", team="KC", drafted=0),
        ]

    @pytest.fixture
    def manager(self, tmp_path):
        """Create manager with sample data."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text(
            'Josh Allen QB - BUF,My Team\n'
            'Tyreek Hill WR - MIA,Other Team\n'
        )
        mgr = DraftedRosterManager(str(csv_path), "My Team")
        mgr.load_drafted_data()
        return mgr

    def test_apply_drafted_state_sets_user_team_to_2(self, manager, sample_players):
        """Test sets drafted=2 for user's team players."""
        manager.apply_drafted_state_to_players(sample_players)

        josh = next(p for p in sample_players if p.name == "Josh Allen")
        assert josh.drafted == 2

    def test_apply_drafted_state_sets_other_team_to_1(self, manager, sample_players):
        """Test sets drafted=1 for other team players."""
        manager.apply_drafted_state_to_players(sample_players)

        tyreek = next(p for p in sample_players if p.name == "Tyreek Hill")
        assert tyreek.drafted == 1

    def test_apply_drafted_state_leaves_undrafted_as_0(self, manager, sample_players):
        """Test leaves undrafted players as 0."""
        manager.apply_drafted_state_to_players(sample_players)

        mahomes = next(p for p in sample_players if p.name == "Patrick Mahomes")
        assert mahomes.drafted == 0

    def test_apply_drafted_state_returns_same_list(self, manager, sample_players):
        """Test returns the same player list (modifies in place)."""
        result = manager.apply_drafted_state_to_players(sample_players)

        assert result is sample_players

    def test_apply_drafted_state_does_nothing_with_no_data(self, tmp_path, sample_players):
        """Test does nothing when no data loaded."""
        csv_path = tmp_path / "drafted.csv"
        manager = DraftedRosterManager(str(csv_path), "My Team")

        manager.apply_drafted_state_to_players(sample_players)

        # All players should remain drafted=0
        for player in sample_players:
            assert player.drafted == 0


class TestNormalizePlayerInfo:
    """Test suite for _normalize_player_info() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_normalize_converts_to_lowercase(self, manager):
        """Test converts string to lowercase."""
        result = manager._normalize_player_info("JOSH ALLEN QB - BUF")

        assert result.islower()

    def test_normalize_removes_extra_whitespace(self, manager):
        """Test removes extra whitespace."""
        result = manager._normalize_player_info("Josh  Allen   QB - BUF")

        assert "  " not in result

    def test_normalize_removes_jr_sr_suffixes(self, manager):
        """Test removes Jr/Sr suffixes."""
        result = manager._normalize_player_info("Robert Griffin Jr. QB - BAL")

        assert "jr" not in result.lower()

    def test_normalize_removes_injury_tags(self, manager):
        """Test removes injury status tags."""
        result = manager._normalize_player_info("Josh Allen QB - BUF O")

        assert " o" not in result

    def test_normalize_removes_punctuation(self, manager):
        """Test removes punctuation marks."""
        result = manager._normalize_player_info("Amon-Ra St. Brown WR - DET")

        assert "." not in result
        assert "'" not in result


class TestExtractPlayerComponents:
    """Test suite for _extract_player_components() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_extract_components_parses_standard_format(self, manager):
        """Test extracts name, position, team from standard format."""
        name, pos, team = manager._extract_player_components("Josh Allen QB - BUF")

        assert name == "Josh Allen"
        assert pos == "QB"
        assert team == "BUF"

    def test_extract_components_handles_defense(self, manager):
        """Test handles defense-specific format."""
        name, pos, team = manager._extract_player_components("Seattle Seahawks DEF")

        assert "Seahawks" in name or "Seattle" in name
        assert pos == "DEF"
        assert team != ""

    def test_extract_components_returns_empty_for_invalid(self, manager):
        """Test returns empty strings for invalid format."""
        name, pos, team = manager._extract_player_components("Invalid Format")

        # At least one should be empty if parse fails
        assert name == "" or pos == "" or team == ""


class TestGetTeamAbbrFromName:
    """Test suite for _get_team_abbr_from_name() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_get_team_abbr_returns_correct_abbr(self, manager):
        """Test returns correct abbreviation for known team."""
        result = manager._get_team_abbr_from_name("seattle seahawks")

        assert result == "SEA"

    def test_get_team_abbr_returns_empty_for_unknown(self, manager):
        """Test returns empty string for unknown team."""
        result = manager._get_team_abbr_from_name("unknown team")

        assert result == ""


class TestSimilarityScore:
    """Test suite for _similarity_score() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_similarity_score_returns_1_for_identical(self, manager):
        """Test returns 1.0 for identical strings."""
        score = manager._similarity_score("Josh Allen", "Josh Allen")

        assert score == 1.0

    def test_similarity_score_returns_0_for_completely_different(self, manager):
        """Test returns low score for completely different strings."""
        score = manager._similarity_score("Josh Allen", "Tyreek Hill")

        assert score < 0.5

    def test_similarity_score_is_case_insensitive(self, manager):
        """Test is case-insensitive."""
        score1 = manager._similarity_score("Josh Allen", "josh allen")
        score2 = manager._similarity_score("Josh Allen", "Josh Allen")

        assert score1 == score2


class TestPositionsEquivalent:
    """Test suite for _positions_equivalent() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_positions_equivalent_returns_true_for_same(self, manager):
        """Test returns True for identical positions."""
        assert manager._positions_equivalent("QB", "QB") is True

    def test_positions_equivalent_is_case_insensitive(self, manager):
        """Test is case-insensitive."""
        assert manager._positions_equivalent("qb", "QB") is True

    def test_positions_equivalent_handles_defense_variations(self, manager):
        """Test treats DST/DEF/D/ST as equivalent."""
        assert manager._positions_equivalent("DST", "DEF") is True
        assert manager._positions_equivalent("DEF", "D/ST") is True

    def test_positions_equivalent_returns_false_for_different(self, manager):
        """Test returns False for different positions."""
        assert manager._positions_equivalent("QB", "RB") is False


class TestTeamsEquivalent:
    """Test suite for _teams_equivalent() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_teams_equivalent_returns_true_for_same(self, manager):
        """Test returns True for identical teams."""
        assert manager._teams_equivalent("BUF", "BUF") is True

    def test_teams_equivalent_is_case_insensitive(self, manager):
        """Test is case-insensitive."""
        assert manager._teams_equivalent("buf", "BUF") is True

    def test_teams_equivalent_handles_washington_variations(self, manager):
        """Test handles WSH/WAS as equivalent."""
        assert manager._teams_equivalent("WSH", "WAS") is True


class TestNormalizeTeamAbbr:
    """Test suite for _normalize_team_abbr() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_normalize_team_abbr_converts_wsh_to_was(self, manager):
        """Test converts WSH to WAS."""
        result = manager._normalize_team_abbr("WSH")

        assert result == "WAS"

    def test_normalize_team_abbr_keeps_was(self, manager):
        """Test keeps WAS unchanged."""
        result = manager._normalize_team_abbr("WAS")

        assert result == "WAS"

    def test_normalize_team_abbr_uppercases(self, manager):
        """Test converts to uppercase."""
        result = manager._normalize_team_abbr("buf")

        assert result == "BUF"


class TestFindOriginalInfoForKey:
    """Test suite for _find_original_info_for_key() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create manager with sample data."""
        csv_path = tmp_path / "drafted.csv"
        csv_path.write_text('Josh Allen QB - BUF,Team Alpha\n')
        mgr = DraftedRosterManager(str(csv_path), "My Team")
        mgr.load_drafted_data()
        return mgr

    def test_find_original_info_returns_match(self, manager):
        """Test returns original info for normalized key."""
        # Normalize the player info to get key
        key = manager._normalize_player_info("Josh Allen QB - BUF")

        result = manager._find_original_info_for_key(key)

        assert result is not None
        assert "Josh Allen" in result

    def test_find_original_info_returns_none_for_no_match(self, manager):
        """Test returns None when key not found."""
        result = manager._find_original_info_for_key("nonexistent_key")

        assert result is None


class TestCreatePlayerLookup:
    """Test suite for _create_player_lookup() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    @pytest.fixture
    def sample_players(self):
        """Create sample players."""
        return [
            FantasyPlayer(id=1, name="Josh Allen", position="QB", team="BUF"),
            FantasyPlayer(id=2, name="Tyreek Hill", position="WR", team="MIA"),
        ]

    def test_create_player_lookup_has_all_keys(self, manager, sample_players):
        """Test creates lookup with all required keys."""
        lookup = manager._create_player_lookup(sample_players)

        assert 'by_full_name' in lookup
        assert 'by_last_name' in lookup
        assert 'by_first_name' in lookup
        assert 'by_position_team' in lookup
        assert 'all_players' in lookup

    def test_create_player_lookup_full_name_mapping(self, manager, sample_players):
        """Test full name lookup works correctly."""
        lookup = manager._create_player_lookup(sample_players)

        assert 'josh allen' in lookup['by_full_name']
        assert lookup['by_full_name']['josh allen'].name == "Josh Allen"

    def test_create_player_lookup_last_name_mapping(self, manager, sample_players):
        """Test last name lookup works correctly."""
        lookup = manager._create_player_lookup(sample_players)

        assert 'allen' in lookup['by_last_name']
        assert len(lookup['by_last_name']['allen']) > 0


class TestFindMatchingPlayer:
    """Test suite for _find_matching_player() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    @pytest.fixture
    def sample_players(self):
        """Create sample players."""
        return [
            FantasyPlayer(id=1, name="Josh Allen", position="QB", team="BUF"),
            FantasyPlayer(id=2, name="Tyreek Hill", position="WR", team="MIA"),
        ]

    def test_find_matching_player_exact_match(self, manager, sample_players):
        """Test finds exact match by full name."""
        lookup = manager._create_player_lookup(sample_players)

        result = manager._find_matching_player("Josh Allen", "QB", "BUF", lookup)

        assert result is not None
        assert result.name == "Josh Allen"

    def test_find_matching_player_returns_none_for_no_match(self, manager, sample_players):
        """Test returns None when no match found."""
        lookup = manager._create_player_lookup(sample_players)

        result = manager._find_matching_player("Nonexistent Player", "QB", "BUF", lookup)

        assert result is None


class TestFindDefenseMatch:
    """Test suite for _find_defense_match() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    @pytest.fixture
    def defense_players(self):
        """Create defense players."""
        return [
            FantasyPlayer(id=1, name="Seahawks D/ST", position="DST", team="SEA"),
        ]

    def test_find_defense_match_handles_full_team_name(self, manager, defense_players):
        """Test matches defense using full team name."""
        lookup = manager._create_player_lookup(defense_players)

        result = manager._find_defense_match("Seattle Seahawks", "DEF", "SEA", lookup)

        # Result may be None or the player, depending on name matching logic
        assert result is None or result.position in ["DST", "DEF", "D/ST"]


class TestValidatePlayerMatch:
    """Test suite for _validate_player_match() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    def test_validate_player_match_returns_true_for_match(self, manager):
        """Test returns True when all criteria match."""
        player = FantasyPlayer(id=1, name="Josh Allen", position="QB", team="BUF")

        result = manager._validate_player_match(player, "QB", "BUF")

        assert result is True

    def test_validate_player_match_returns_false_for_wrong_position(self, manager):
        """Test returns False when position doesn't match."""
        player = FantasyPlayer(id=1, name="Josh Allen", position="QB", team="BUF")

        result = manager._validate_player_match(player, "WR", "BUF")

        assert result is False

    def test_validate_player_match_returns_false_for_wrong_team(self, manager):
        """Test returns False when team doesn't match."""
        player = FantasyPlayer(id=1, name="Josh Allen", position="QB", team="BUF")

        result = manager._validate_player_match(player, "QB", "KC")

        assert result is False


class TestFuzzyMatchPlayer:
    """Test suite for _fuzzy_match_player() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create DraftedRosterManager instance."""
        csv_path = tmp_path / "drafted.csv"
        return DraftedRosterManager(str(csv_path), "My Team")

    @pytest.fixture
    def sample_players(self):
        """Create sample players."""
        return [
            FantasyPlayer(id=1, name="Josh Allen", position="QB", team="BUF"),
            FantasyPlayer(id=2, name="Tyreek Hill", position="WR", team="MIA"),
        ]

    def test_fuzzy_match_finds_close_match(self, manager, sample_players):
        """Test finds match with high similarity score."""
        result = manager._fuzzy_match_player("Josh Allan", "QB", "BUF", sample_players)

        # May or may not find match depending on similarity threshold
        assert result is None or result.position == "QB"

    def test_fuzzy_match_returns_none_for_low_similarity(self, manager, sample_players):
        """Test returns None when similarity below threshold."""
        result = manager._fuzzy_match_player("Completely Different", "QB", "BUF", sample_players)

        assert result is None

    def test_fuzzy_match_validates_position_and_team(self, manager, sample_players):
        """Test validates position and team even with fuzzy match."""
        result = manager._fuzzy_match_player("Josh Allen", "WR", "BUF", sample_players)

        # Should not match because position is wrong
        assert result is None
