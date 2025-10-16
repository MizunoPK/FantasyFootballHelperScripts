"""
Tests for PlayerSearch fuzzy search functionality.

Author: Kai Mizuno
"""

import pytest
from utils.FantasyPlayer import FantasyPlayer
from league_helper.util.player_search import PlayerSearch


class TestPlayerSearchBasic:
    """Test suite for basic PlayerSearch initialization and utility methods."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(
                id=1,
                name="Patrick Mahomes",
                team="KC",
                position="QB",
                bye_week=7,
                drafted=2,  # On roster
                locked=0,
                score=95.0,
                fantasy_points=350.0
            ),
            FantasyPlayer(
                id=2,
                name="Tyreek Hill",
                team="MIA",
                position="WR",
                bye_week=8,
                drafted=1,  # Drafted by others
                locked=0,
                score=85.0,
                fantasy_points=280.0
            ),
            FantasyPlayer(
                id=3,
                name="Christian McCaffrey",
                team="SF",
                position="RB",
                bye_week=9,
                drafted=0,  # Available
                locked=0,
                score=92.0,
                fantasy_points=320.0
            ),
            FantasyPlayer(
                id=4,
                name="Travis Kelce",
                team="KC",
                position="TE",
                bye_week=7,
                drafted=2,  # On roster
                locked=1,  # Locked
                score=80.0,
                fantasy_points=250.0
            ),
            FantasyPlayer(
                id=5,
                name="Josh Allen",
                team="BUF",
                position="QB",
                bye_week=10,
                drafted=0,  # Available
                locked=0,
                score=90.0,
                fantasy_points=330.0
            ),
        ]

    @pytest.fixture
    def player_search(self, sample_players):
        """Create PlayerSearch instance with sample players."""
        return PlayerSearch(sample_players)

    def test_init_stores_players(self, sample_players):
        """Test that __init__ stores the players list."""
        search = PlayerSearch(sample_players)
        assert search.players == sample_players
        assert len(search.players) == 5

    def test_find_players_by_drafted_status_available(self, player_search):
        """Test finding available players (drafted=0)."""
        available = player_search.find_players_by_drafted_status(0)
        assert len(available) == 2
        assert all(p.drafted == 0 for p in available)
        assert "Christian McCaffrey" in [p.name for p in available]
        assert "Josh Allen" in [p.name for p in available]

    def test_find_players_by_drafted_status_drafted(self, player_search):
        """Test finding drafted players (drafted=1)."""
        drafted = player_search.find_players_by_drafted_status(1)
        assert len(drafted) == 1
        assert all(p.drafted == 1 for p in drafted)
        assert drafted[0].name == "Tyreek Hill"

    def test_find_players_by_drafted_status_roster(self, player_search):
        """Test finding roster players (drafted=2)."""
        roster = player_search.find_players_by_drafted_status(2)
        assert len(roster) == 2
        assert all(p.drafted == 2 for p in roster)
        assert "Patrick Mahomes" in [p.name for p in roster]
        assert "Travis Kelce" in [p.name for p in roster]

    def test_get_roster_players(self, player_search):
        """Test get_roster_players() convenience method."""
        roster = player_search.get_roster_players()
        assert len(roster) == 2
        assert all(p.drafted == 2 for p in roster)

    def test_get_available_players(self, player_search):
        """Test get_available_players() convenience method."""
        available = player_search.get_available_players()
        assert len(available) == 2
        assert all(p.drafted == 0 for p in available)

    def test_get_drafted_players(self, player_search):
        """Test get_drafted_players() convenience method."""
        drafted = player_search.get_drafted_players()
        assert len(drafted) == 1
        assert all(p.drafted == 1 for p in drafted)


class TestSearchPlayersByName:
    """Test suite for search_players_by_name() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for search testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted=0, locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Patrick Peterson", team="PIT", position="CB", bye_week=8, drafted=1, locked=0, score=50.0, fantasy_points=100.0),
            FantasyPlayer(id=3, name="Josh Allen", team="BUF", position="QB", bye_week=10, drafted=2, locked=0, score=90.0, fantasy_points=330.0),
            FantasyPlayer(id=4, name="Keenan Allen", team="CHI", position="WR", bye_week=11, drafted=0, locked=0, score=75.0, fantasy_points=220.0),
            FantasyPlayer(id=5, name="Travis Kelce", team="KC", position="TE", bye_week=7, drafted=2, locked=1, score=80.0, fantasy_points=250.0),
        ]

    @pytest.fixture
    def player_search(self, sample_players):
        """Create PlayerSearch instance."""
        return PlayerSearch(sample_players)

    def test_search_by_full_name(self, player_search):
        """Test search with full player name."""
        matches = player_search.search_players_by_name("Patrick Mahomes")
        assert len(matches) == 1
        assert matches[0].name == "Patrick Mahomes"

    def test_search_by_first_name(self, player_search):
        """Test search with first name only."""
        matches = player_search.search_players_by_name("Patrick")
        assert len(matches) == 2
        names = [p.name for p in matches]
        assert "Patrick Mahomes" in names
        assert "Patrick Peterson" in names

    def test_search_by_last_name(self, player_search):
        """Test search with last name only."""
        matches = player_search.search_players_by_name("Allen")
        assert len(matches) == 2
        names = [p.name for p in matches]
        assert "Josh Allen" in names
        assert "Keenan Allen" in names

    def test_search_by_partial_name(self, player_search):
        """Test search with partial name match."""
        matches = player_search.search_players_by_name("Kel")
        assert len(matches) == 1
        assert matches[0].name == "Travis Kelce"

    def test_search_case_insensitive(self, player_search):
        """Test that search is case insensitive."""
        matches_lower = player_search.search_players_by_name("mahomes")
        matches_upper = player_search.search_players_by_name("MAHOMES")
        matches_mixed = player_search.search_players_by_name("MaHoMeS")

        assert len(matches_lower) == 1
        assert len(matches_upper) == 1
        assert len(matches_mixed) == 1
        assert matches_lower[0].name == "Patrick Mahomes"
        assert matches_upper[0].name == "Patrick Mahomes"
        assert matches_mixed[0].name == "Patrick Mahomes"

    def test_search_empty_string_returns_empty_list(self, player_search):
        """Test that empty search string returns empty list."""
        matches = player_search.search_players_by_name("")
        assert len(matches) == 0

    def test_search_no_matches_returns_empty_list(self, player_search):
        """Test that search with no matches returns empty list."""
        matches = player_search.search_players_by_name("Zzzzzz")
        assert len(matches) == 0

    def test_search_with_drafted_filter_available(self, player_search):
        """Test search with drafted_filter=0 (available only)."""
        matches = player_search.search_players_by_name("Allen", drafted_filter=0)
        assert len(matches) == 1
        assert matches[0].name == "Keenan Allen"
        assert matches[0].drafted == 0

    def test_search_with_drafted_filter_drafted(self, player_search):
        """Test search with drafted_filter=1 (drafted by others)."""
        matches = player_search.search_players_by_name("Patrick", drafted_filter=1)
        assert len(matches) == 1
        assert matches[0].name == "Patrick Peterson"
        assert matches[0].drafted == 1

    def test_search_with_drafted_filter_roster(self, player_search):
        """Test search with drafted_filter=2 (on roster)."""
        matches = player_search.search_players_by_name("Allen", drafted_filter=2)
        assert len(matches) == 1
        assert matches[0].name == "Josh Allen"
        assert matches[0].drafted == 2

    def test_search_with_drafted_filter_none_returns_all(self, player_search):
        """Test search with drafted_filter=None returns all matches."""
        matches = player_search.search_players_by_name("Allen", drafted_filter=None)
        assert len(matches) == 2
        names = [p.name for p in matches]
        assert "Josh Allen" in names
        assert "Keenan Allen" in names

    def test_search_exact_match_true(self, player_search):
        """Test exact_match=True requires exact name."""
        matches = player_search.search_players_by_name("patrick mahomes", exact_match=True)
        assert len(matches) == 1
        assert matches[0].name == "Patrick Mahomes"

    def test_search_exact_match_partial_fails(self, player_search):
        """Test exact_match=True rejects partial matches."""
        matches = player_search.search_players_by_name("Patrick", exact_match=True)
        assert len(matches) == 0

    def test_search_locked_players_shown(self, player_search):
        """Test that locked players appear in search results."""
        matches = player_search.search_players_by_name("Kelce")
        assert len(matches) == 1
        assert matches[0].locked == 1


class TestSearchPlayersNotAvailable:
    """Test suite for search_players_by_name_not_available() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted=2, locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted=1, locked=0, score=85.0, fantasy_points=280.0),
            FantasyPlayer(id=3, name="Christian McCaffrey", team="SF", position="RB", bye_week=9, drafted=0, locked=0, score=92.0, fantasy_points=320.0),
            FantasyPlayer(id=4, name="Travis Kelce", team="KC", position="TE", bye_week=7, drafted=2, locked=1, score=80.0, fantasy_points=250.0),
            FantasyPlayer(id=5, name="Josh Allen", team="BUF", position="QB", bye_week=10, drafted=0, locked=0, score=90.0, fantasy_points=330.0),
        ]

    @pytest.fixture
    def player_search(self, sample_players):
        """Create PlayerSearch instance."""
        return PlayerSearch(sample_players)

    def test_search_not_available_excludes_drafted_zero(self, player_search):
        """Test that search_players_by_name_not_available excludes drafted=0."""
        matches = player_search.search_players_by_name_not_available("Allen")
        # Josh Allen is drafted=0, should not be included
        assert len(matches) == 0

    def test_search_not_available_includes_drafted_one(self, player_search):
        """Test that search includes drafted=1 players."""
        matches = player_search.search_players_by_name_not_available("Tyreek")
        assert len(matches) == 1
        assert matches[0].name == "Tyreek Hill"
        assert matches[0].drafted == 1

    def test_search_not_available_includes_drafted_two(self, player_search):
        """Test that search includes drafted=2 players."""
        matches = player_search.search_players_by_name_not_available("Mahomes")
        assert len(matches) == 1
        assert matches[0].name == "Patrick Mahomes"
        assert matches[0].drafted == 2

    def test_search_not_available_includes_both_drafted_statuses(self, player_search):
        """Test that search includes both drafted=1 and drafted=2."""
        # Add another player with same partial name
        player_search.players.append(
            FantasyPlayer(id=6, name="Patrick Peterson", team="PIT", position="CB", bye_week=8, drafted=1, locked=0, score=50.0, fantasy_points=100.0)
        )
        matches = player_search.search_players_by_name_not_available("Patrick")
        assert len(matches) == 2
        drafted_statuses = {p.drafted for p in matches}
        assert 1 in drafted_statuses  # Patrick Peterson (drafted=1)
        assert 2 in drafted_statuses  # Patrick Mahomes (drafted=2)
        assert 0 not in drafted_statuses  # No drafted=0 players

    def test_search_not_available_empty_string(self, player_search):
        """Test that empty string returns empty list."""
        matches = player_search.search_players_by_name_not_available("")
        assert len(matches) == 0

    def test_search_not_available_no_matches(self, player_search):
        """Test that no matches returns empty list."""
        matches = player_search.search_players_by_name_not_available("Zzzzzz")
        assert len(matches) == 0

    def test_search_not_available_case_insensitive(self, player_search):
        """Test that search is case insensitive."""
        matches = player_search.search_players_by_name_not_available("KELCE")
        assert len(matches) == 1
        assert matches[0].name == "Travis Kelce"

    def test_search_not_available_fuzzy_matching(self, player_search):
        """Test that fuzzy matching works."""
        matches = player_search.search_players_by_name_not_available("Kel")
        assert len(matches) == 1
        assert matches[0].name == "Travis Kelce"

    def test_search_not_available_exact_match_true(self, player_search):
        """Test exact_match=True requires exact name."""
        matches = player_search.search_players_by_name_not_available("travis kelce", exact_match=True)
        assert len(matches) == 1
        assert matches[0].name == "Travis Kelce"

    def test_search_not_available_exact_match_partial_fails(self, player_search):
        """Test exact_match=True rejects partial matches."""
        matches = player_search.search_players_by_name_not_available("Kelce", exact_match=True)
        assert len(matches) == 0


class TestInteractiveSearchEdgeCases:
    """Test suite for interactive_search() edge cases and validation.

    Note: Full interactive testing with user input is handled in integration tests.
    These tests validate the logic and edge cases.
    """

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted=0, locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted=1, locked=0, score=85.0, fantasy_points=280.0),
            FantasyPlayer(id=3, name="Travis Kelce", team="KC", position="TE", bye_week=7, drafted=2, locked=1, score=80.0, fantasy_points=250.0),
        ]

    @pytest.fixture
    def player_search(self, sample_players):
        """Create PlayerSearch instance."""
        return PlayerSearch(sample_players)

    def test_interactive_search_validates_drafted_filter_parameter(self, player_search):
        """Test that interactive_search accepts drafted_filter parameter."""
        # This test validates the method signature, actual interactive behavior
        # is tested in integration tests
        assert hasattr(player_search, 'interactive_search')
        import inspect
        sig = inspect.signature(player_search.interactive_search)
        assert 'drafted_filter' in sig.parameters
        assert 'prompt' in sig.parameters
        assert 'not_available' in sig.parameters

    def test_interactive_search_validates_not_available_parameter(self, player_search):
        """Test that interactive_search has not_available parameter."""
        import inspect
        sig = inspect.signature(player_search.interactive_search)
        param = sig.parameters['not_available']
        assert param.default == False  # Default should be False
