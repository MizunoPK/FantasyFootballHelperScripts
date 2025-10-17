"""
Tests for DraftedDataWriter.

Author: Kai Mizuno
"""

import pytest
import csv
from pathlib import Path
from league_helper.util.DraftedDataWriter import DraftedDataWriter
from utils.FantasyPlayer import FantasyPlayer


class TestGetAllTeamNames:
    """Test suite for get_all_team_names() method."""

    def test_get_all_team_names_returns_sorted_list(self, tmp_path):
        """Test that get_all_team_names returns teams in alphabetical order."""
        # Create CSV with teams
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patrick Mahomes QB - KC", "Zebra Team"])
            writer.writerow(["Josh Allen QB - BUF", "Alpha Team"])
            writer.writerow(["Travis Kelce TE - KC", "Beta Team"])

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        teams = drafted_writer.get_all_team_names()

        # Verify - sorted alphabetically
        assert teams == ["Alpha Team", "Beta Team", "Zebra Team"]

    def test_get_all_team_names_handles_duplicates(self, tmp_path):
        """Test that get_all_team_names removes duplicate teams."""
        # Create CSV with duplicate teams
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patrick Mahomes QB - KC", "Team A"])
            writer.writerow(["Josh Allen QB - BUF", "Team B"])
            writer.writerow(["Travis Kelce TE - KC", "Team A"])
            writer.writerow(["Tyreek Hill WR - MIA", "Team B"])

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        teams = drafted_writer.get_all_team_names()

        # Verify - only unique teams
        assert teams == ["Team A", "Team B"]

    def test_get_all_team_names_handles_empty_file(self, tmp_path):
        """Test that get_all_team_names handles empty CSV."""
        # Create empty CSV
        csv_path = tmp_path / "drafted_data.csv"
        csv_path.touch()

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        teams = drafted_writer.get_all_team_names()

        # Verify
        assert teams == []

    def test_get_all_team_names_handles_missing_file(self, tmp_path):
        """Test that get_all_team_names handles missing file gracefully."""
        # Use non-existent path
        csv_path = tmp_path / "nonexistent.csv"

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        teams = drafted_writer.get_all_team_names()

        # Verify - returns empty list
        assert teams == []

    def test_get_all_team_names_ignores_whitespace(self, tmp_path):
        """Test that get_all_team_names strips whitespace from team names."""
        # Create CSV with whitespace
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patrick Mahomes QB - KC", "  Team A  "])
            writer.writerow(["Josh Allen QB - BUF", "Team B"])

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        teams = drafted_writer.get_all_team_names()

        # Verify - whitespace stripped
        assert teams == ["Team A", "Team B"]

    def test_get_all_team_names_ignores_malformed_rows(self, tmp_path):
        """Test that get_all_team_names ignores rows with less than 2 columns."""
        # Create CSV with malformed rows
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patrick Mahomes QB - KC", "Team A"])
            writer.writerow(["Invalid Row"])  # Only 1 column
            writer.writerow(["Josh Allen QB - BUF", "Team B"])

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        teams = drafted_writer.get_all_team_names()

        # Verify - malformed row ignored
        assert teams == ["Team A", "Team B"]


class TestAddPlayer:
    """Test suite for add_player() method."""

    def test_add_player_appends_to_csv(self, tmp_path):
        """Test that add_player appends player to CSV file."""
        # Setup
        csv_path = tmp_path / "drafted_data.csv"
        csv_path.touch()

        player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",
            bye_week=7, drafted=1, locked=0, score=95.0, fantasy_points=350.0
        )

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        result = drafted_writer.add_player(player, "Sea Sharp")

        # Verify
        assert result is True

        # Read CSV and verify content
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0][0] == "Patrick Mahomes QB - KC"
        assert rows[0][1] == "Sea Sharp"

    def test_add_player_maintains_existing_data(self, tmp_path):
        """Test that add_player preserves existing CSV data."""
        # Create CSV with existing data
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Josh Allen QB - BUF", "Team A"])

        player = FantasyPlayer(
            id=2, name="Travis Kelce", team="KC", position="TE",
            bye_week=7, drafted=1, locked=0, score=80.0, fantasy_points=250.0
        )

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        result = drafted_writer.add_player(player, "Team B")

        # Verify
        assert result is True

        # Read CSV and verify both entries exist
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert rows[0][0] == "Josh Allen QB - BUF"
        assert rows[0][1] == "Team A"
        assert rows[1][0] == "Travis Kelce TE - KC"
        assert rows[1][1] == "Team B"

    def test_add_player_formats_correctly(self, tmp_path):
        """Test that add_player formats player info correctly."""
        csv_path = tmp_path / "drafted_data.csv"
        csv_path.touch()

        player = FantasyPlayer(
            id=3, name="Tyreek Hill", team="MIA", position="WR",
            bye_week=8, drafted=1, locked=0, score=85.0, fantasy_points=280.0
        )

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        drafted_writer.add_player(player, "The Eskimo Brothers")

        # Verify format: "Name POS - TEAM"
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert rows[0][0] == "Tyreek Hill WR - MIA"


class TestRemovePlayer:
    """Test suite for remove_player() method."""

    def test_remove_player_deletes_matching_entry(self, tmp_path):
        """Test that remove_player deletes the matching player entry."""
        # Create CSV with multiple players
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patrick Mahomes QB - KC", "Sea Sharp"])
            writer.writerow(["Travis Kelce TE - KC", "Team B"])
            writer.writerow(["Josh Allen QB - BUF", "Team C"])

        player = FantasyPlayer(
            id=2, name="Travis Kelce", team="KC", position="TE",
            bye_week=7, drafted=1, locked=0, score=80.0, fantasy_points=250.0
        )

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        result = drafted_writer.remove_player(player)

        # Verify
        assert result is True

        # Read CSV and verify Travis Kelce is removed
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert "Travis Kelce" not in rows[0][0]
        assert "Travis Kelce" not in rows[1][0]

    def test_remove_player_handles_missing_player(self, tmp_path):
        """Test that remove_player handles non-existent player gracefully."""
        # Create CSV without the target player
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patrick Mahomes QB - KC", "Sea Sharp"])

        player = FantasyPlayer(
            id=2, name="Travis Kelce", team="KC", position="TE",
            bye_week=7, drafted=1, locked=0, score=80.0, fantasy_points=250.0
        )

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        result = drafted_writer.remove_player(player)

        # Verify - returns False but doesn't crash
        assert result is False

    def test_remove_player_handles_missing_file(self, tmp_path):
        """Test that remove_player handles missing file gracefully."""
        csv_path = tmp_path / "nonexistent.csv"

        player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",
            bye_week=7, drafted=1, locked=0, score=95.0, fantasy_points=350.0
        )

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        result = drafted_writer.remove_player(player)

        # Verify - returns False
        assert result is False

    def test_remove_player_uses_fuzzy_matching(self, tmp_path):
        """Test that remove_player uses fuzzy name matching."""
        # Create CSV with player name variations
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patrick Mahomes II QB - KC", "Sea Sharp"])  # Has suffix

        player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",  # No suffix
            bye_week=7, drafted=1, locked=0, score=95.0, fantasy_points=350.0
        )

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        result = drafted_writer.remove_player(player)

        # Verify - should find match despite suffix difference
        assert result is True

        # Read CSV and verify it's empty
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 0

    def test_remove_player_preserves_other_entries(self, tmp_path):
        """Test that remove_player preserves all other entries."""
        # Create CSV with multiple players
        csv_path = tmp_path / "drafted_data.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patrick Mahomes QB - KC", "Sea Sharp"])
            writer.writerow(["Travis Kelce TE - KC", "Team B"])
            writer.writerow(["Josh Allen QB - BUF", "Team C"])
            writer.writerow(["Tyreek Hill WR - MIA", "Team D"])

        player = FantasyPlayer(
            id=2, name="Travis Kelce", team="KC", position="TE",
            bye_week=7, drafted=1, locked=0, score=80.0, fantasy_points=250.0
        )

        # Execute
        drafted_writer = DraftedDataWriter(csv_path)
        drafted_writer.remove_player(player)

        # Verify - all other entries preserved
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 3
        assert any("Patrick Mahomes" in row[0] for row in rows)
        assert any("Josh Allen" in row[0] for row in rows)
        assert any("Tyreek Hill" in row[0] for row in rows)
        assert not any("Travis Kelce" in row[0] for row in rows)


class TestPlayerMatches:
    """Test suite for _player_matches() method."""

    def test_player_matches_exact_match(self):
        """Test _player_matches with exact name match."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",
            bye_week=7, drafted=1, locked=0, score=95.0, fantasy_points=350.0
        )

        csv_info = "Patrick Mahomes QB - KC"

        # Verify
        assert drafted_writer._player_matches(player, csv_info) is True

    def test_player_matches_case_insensitive(self):
        """Test _player_matches is case insensitive."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        player = FantasyPlayer(
            id=1, name="patrick mahomes", team="KC", position="QB",
            bye_week=7, drafted=1, locked=0, score=95.0, fantasy_points=350.0
        )

        csv_info = "PATRICK MAHOMES QB - KC"

        # Verify
        assert drafted_writer._player_matches(player, csv_info) is True

    def test_player_matches_handles_suffixes(self):
        """Test _player_matches handles name suffixes (Jr, Sr, III, etc)."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",
            bye_week=7, drafted=1, locked=0, score=95.0, fantasy_points=350.0
        )

        csv_info = "Patrick Mahomes II QB - KC"

        # Verify - should match despite suffix
        assert drafted_writer._player_matches(player, csv_info) is True

    def test_player_matches_checks_position(self):
        """Test _player_matches verifies position matches."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        player = FantasyPlayer(
            id=1, name="Josh Allen", team="BUF", position="QB",
            bye_week=10, drafted=1, locked=0, score=90.0, fantasy_points=330.0
        )

        # Same name, different position (there's also a Josh Allen LB)
        csv_info = "Josh Allen LB - JAX"

        # Verify - should NOT match (wrong position)
        assert drafted_writer._player_matches(player, csv_info) is False

    def test_player_matches_requires_both_name_and_position(self):
        """Test _player_matches requires both name and position to match."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",
            bye_week=7, drafted=1, locked=0, score=95.0, fantasy_points=350.0
        )

        # Has position but wrong name
        csv_info = "Tom Brady QB - TB"

        # Verify
        assert drafted_writer._player_matches(player, csv_info) is False


class TestNormalizeName:
    """Test suite for _normalize_name() method."""

    def test_normalize_name_lowercases(self):
        """Test _normalize_name converts to lowercase."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        result = drafted_writer._normalize_name("PATRICK MAHOMES")

        assert result == "patrick mahomes"

    def test_normalize_name_removes_suffixes(self):
        """Test _normalize_name removes common suffixes."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        test_cases = [
            ("Patrick Mahomes Jr", "patrick mahomes"),
            ("Ken Griffey Sr", "ken griffey"),
            ("Walter Payton III", "walter payton"),
            ("Joe Montana II", "joe montana"),
            ("Barry Sanders IV", "barry sanders"),
        ]

        for input_name, expected in test_cases:
            result = drafted_writer._normalize_name(input_name)
            assert result == expected

    def test_normalize_name_removes_punctuation(self):
        """Test _normalize_name removes punctuation."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        test_cases = [
            ("D'Angelo Russell", "dangelo russell"),
            ("Dont'a Hightower", "donta hightower"),
            ("T.J. Hockenson", "tj hockenson"),
        ]

        for input_name, expected in test_cases:
            result = drafted_writer._normalize_name(input_name)
            assert result == expected

    def test_normalize_name_handles_extra_whitespace(self):
        """Test _normalize_name removes extra whitespace."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        result = drafted_writer._normalize_name("Patrick   Mahomes  ")

        assert result == "patrick mahomes"

    def test_normalize_name_handles_hyphens(self):
        """Test _normalize_name converts hyphens to spaces."""
        drafted_writer = DraftedDataWriter(Path("dummy.csv"))

        result = drafted_writer._normalize_name("Stefon Diggs-Johnson")

        assert result == "stefon diggs johnson"
