"""
Unit Tests for ScoredPlayer Class

Tests the ScoredPlayer class which wraps a FantasyPlayer with calculated
score and scoring reasons. Verifies the __str__ method that formats the
display output with bullet-pointed reasons.

Author: Claude Code
Date: 2025-10-10
"""

import pytest
from util.ScoredPlayer import ScoredPlayer
from utils.FantasyPlayer import FantasyPlayer


class TestScoredPlayerConstruction:
    """Test ScoredPlayer initialization and attributes"""

    def test_scored_player_initialization(self):
        """Test basic ScoredPlayer construction"""
        player = FantasyPlayer(
            id=1,
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            fantasy_points=250.0
        )
        reasons = ["Base Points: 100.0", "ADP: EXCELLENT"]

        scored_player = ScoredPlayer(player, 125.5, reasons)

        assert scored_player.player == player
        assert scored_player.score == 125.5
        assert scored_player.reason == reasons

    def test_scored_player_empty_reasons(self):
        """Test ScoredPlayer with empty reasons list"""
        player = FantasyPlayer(
            id=2,
            name="Test Player",
            team="BUF",
            position="RB"
        )

        scored_player = ScoredPlayer(player, 50.0, [])

        assert scored_player.reason == []
        assert len(scored_player.reason) == 0

    def test_scored_player_default_reasons(self):
        """Test ScoredPlayer with default reasons parameter"""
        player = FantasyPlayer(
            id=3,
            name="Default Player",
            team="PHI",
            position="WR"
        )

        # Default parameter is empty list
        scored_player = ScoredPlayer(player, 75.0)

        assert scored_player.reason == []


class TestScoredPlayerStringRepresentation:
    """Test the __str__ method that formats display output"""

    def test_str_basic_format(self):
        """Test basic __str__ output format"""
        player = FantasyPlayer(
            id=1,
            name="Patrick Mahomes",
            team="KC",
            position="QB"
        )
        scored_player = ScoredPlayer(player, 123.45, [])

        result = str(scored_player)

        # Header should include position, team, name, and score
        assert "[QB]" in result
        assert "[KC]" in result
        assert "Patrick Mahomes" in result
        assert "123.45 pts" in result

    def test_str_with_reasons(self):
        """Test __str__ output includes reasons as bullet points"""
        player = FantasyPlayer(
            id=2,
            name="Josh Allen",
            team="BUF",
            position="QB"
        )
        reasons = [
            "Projected: 20.00 pts, Weighted: 50.00 pts",
            "Consistency: EXCELLENT",
            "Matchup: GOOD"
        ]
        scored_player = ScoredPlayer(player, 100.0, reasons)

        result = str(scored_player)

        # Check header
        assert "[QB] [BUF] Josh Allen - 100.00 pts" in result

        # Check each reason appears as a bullet point
        for reason in reasons:
            assert f"- {reason}" in result

    def test_str_indentation(self):
        """Test that reasons have correct indentation (12 spaces)"""
        player = FantasyPlayer(
            id=3,
            name="Tyreek Hill",
            team="MIA",
            position="WR"
        )
        reasons = ["Reason 1", "Reason 2"]
        scored_player = ScoredPlayer(player, 95.0, reasons)

        result = str(scored_player)
        lines = result.split('\n')

        # First line should be header (no indentation)
        assert lines[0].startswith("[WR]")

        # Subsequent lines should have 12 spaces indentation
        if len(lines) > 1:
            for line in lines[1:]:
                if line.strip():  # Non-empty lines
                    assert line.startswith("            -")  # 12 spaces

    def test_str_score_formatting(self):
        """Test that score is formatted to 2 decimal places"""
        player = FantasyPlayer(
            id=4,
            name="Travis Kelce",
            team="KC",
            position="TE"
        )

        # Test various score values
        test_cases = [
            (123.456, "123.46 pts"),
            (100.0, "100.00 pts"),
            (99.999, "100.00 pts"),
            (0.123, "0.12 pts"),
        ]

        for score, expected in test_cases:
            scored_player = ScoredPlayer(player, score, [])
            result = str(scored_player)
            assert expected in result

    def test_str_multiline_output(self):
        """Test that __str__ produces correct multiline output"""
        player = FantasyPlayer(
            id=5,
            name="Christian McCaffrey",
            team="SF",
            position="RB"
        )
        reasons = [
            "Projected: 25.50 pts, Weighted: 60.00 pts",
            "Consistency: GOOD",
            "Matchup: EXCELLENT",
            "Team Quality: EXCELLENT"
        ]
        scored_player = ScoredPlayer(player, 150.75, reasons)

        result = str(scored_player)
        lines = result.split('\n')

        # Should have 1 header line + 4 reason lines = 5 total
        assert len(lines) == 5

        # First line is header (includes bye week info)
        assert lines[0] == "[RB] [SF] Christian McCaffrey - 150.75 pts (Bye=None)"

        # Each subsequent line is a reason
        for i, reason in enumerate(reasons, start=1):
            assert f"- {reason}" in lines[i]

    def test_str_with_long_player_name(self):
        """Test __str__ with long player names"""
        player = FantasyPlayer(
            id=6,
            name="JuJu Smith-Schuster",
            team="NE",
            position="WR"
        )
        scored_player = ScoredPlayer(player, 88.88, ["Reason 1"])

        result = str(scored_player)

        assert "JuJu Smith-Schuster" in result
        assert "[WR]" in result
        assert "[NE]" in result
        assert "88.88 pts" in result

    def test_print_scored_player(self, capsys):
        """Test that print() uses __str__ method correctly"""
        player = FantasyPlayer(
            id=7,
            name="Stefon Diggs",
            team="HOU",
            position="WR"
        )
        reasons = ["Test Reason 1", "Test Reason 2"]
        scored_player = ScoredPlayer(player, 111.11, reasons)

        # Print the scored player
        print(scored_player)

        # Capture printed output
        captured = capsys.readouterr()

        # Verify output matches __str__
        assert "[WR] [HOU] Stefon Diggs - 111.11 pts" in captured.out
        assert "- Test Reason 1" in captured.out
        assert "- Test Reason 2" in captured.out


class TestScoredPlayerEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_scored_player_with_many_reasons(self):
        """Test ScoredPlayer with many scoring reasons"""
        player = FantasyPlayer(
            id=8,
            name="Many Reasons Player",
            team="DAL",
            position="QB"
        )
        # Create 10 reasons
        reasons = [f"Reason {i}" for i in range(10)]
        scored_player = ScoredPlayer(player, 200.0, reasons)

        result = str(scored_player)
        lines = result.split('\n')

        # Should have header + 10 reasons = 11 lines
        assert len(lines) == 11

        # All reasons should be present
        for i in range(10):
            assert f"- Reason {i}" in result

    def test_scored_player_zero_score(self):
        """Test ScoredPlayer with zero score"""
        player = FantasyPlayer(
            id=9,
            name="Zero Score",
            team="JAX",
            position="K"
        )
        scored_player = ScoredPlayer(player, 0.0, [])

        result = str(scored_player)

        assert "0.00 pts" in result

    def test_scored_player_negative_score(self):
        """Test ScoredPlayer with negative score"""
        player = FantasyPlayer(
            id=10,
            name="Negative Score",
            team="NYJ",
            position="DST"
        )
        scored_player = ScoredPlayer(player, -50.5, ["Heavy Penalties"])

        result = str(scored_player)

        assert "-50.50 pts" in result
        assert "- Heavy Penalties" in result

    def test_scored_player_very_large_score(self):
        """Test ScoredPlayer with very large score"""
        player = FantasyPlayer(
            id=11,
            name="Big Score",
            team="KC",
            position="RB"
        )
        scored_player = ScoredPlayer(player, 9999.99, [])

        result = str(scored_player)

        assert "9999.99 pts" in result

    def test_scored_player_with_special_characters_in_reasons(self):
        """Test reasons containing special characters"""
        player = FantasyPlayer(
            id=12,
            name="Special Player",
            team="BUF",
            position="TE"
        )
        reasons = [
            "Score: 100.5 (adjusted)",
            "Team Quality: EXCELLENT - #1 rank",
            "Matchup: vs. #32 defense"
        ]
        scored_player = ScoredPlayer(player, 125.0, reasons)

        result = str(scored_player)

        # All special characters should be preserved
        for reason in reasons:
            assert f"- {reason}" in result


class TestScoredPlayerComparison:
    """Test comparison and sorting of ScoredPlayer objects"""

    def test_scored_players_have_different_scores(self):
        """Test that different scored players can be distinguished by score"""
        player1 = FantasyPlayer(id=1, name="Player 1", team="KC", position="QB")
        player2 = FantasyPlayer(id=2, name="Player 2", team="BUF", position="QB")

        sp1 = ScoredPlayer(player1, 100.0, [])
        sp2 = ScoredPlayer(player2, 200.0, [])

        assert sp1.score != sp2.score
        assert sp1.score < sp2.score

    def test_sorted_scored_players(self):
        """Test sorting scored players by score"""
        players_data = [
            ("Player A", 150.0),
            ("Player B", 200.0),
            ("Player C", 100.0),
            ("Player D", 175.0),
        ]

        scored_players = []
        for i, (name, score) in enumerate(players_data):
            player = FantasyPlayer(id=i, name=name, team="KC", position="RB")
            scored_players.append(ScoredPlayer(player, score, []))

        # Sort by score descending
        sorted_players = sorted(scored_players, key=lambda sp: sp.score, reverse=True)

        assert sorted_players[0].player.name == "Player B"  # 200.0
        assert sorted_players[1].player.name == "Player D"  # 175.0
        assert sorted_players[2].player.name == "Player A"  # 150.0
        assert sorted_players[3].player.name == "Player C"  # 100.0


class TestAdditionalEdgeCases:
    """Additional edge case tests for comprehensive coverage"""

    def test_scored_player_with_empty_string_reason(self):
        """Test ScoredPlayer with empty string in reasons list"""
        player = FantasyPlayer(
            id=13,
            name="Empty Reason Player",
            team="DEN",
            position="WR"
        )
        reasons = ["Valid Reason", "", "Another Valid Reason"]
        scored_player = ScoredPlayer(player, 100.0, reasons)

        result = str(scored_player)

        # Empty reason should still appear as a bullet point
        assert "- Valid Reason" in result
        assert "-  \n" in result or "-" in result  # Empty reason appears as "- "
        assert "- Another Valid Reason" in result

    def test_scored_player_with_very_long_reason(self):
        """Test ScoredPlayer with very long reason text"""
        player = FantasyPlayer(
            id=14,
            name="Long Reason Player",
            team="LAC",
            position="TE"
        )
        # Create a very long reason (200+ characters)
        long_reason = "A" * 200
        reasons = ["Short reason", long_reason, "Another short reason"]
        scored_player = ScoredPlayer(player, 88.0, reasons)

        result = str(scored_player)

        # Long reason should be included without truncation
        assert long_reason in result
        assert "- Short reason" in result
        assert "- Another short reason" in result

    def test_scored_player_with_unicode_name(self):
        """Test ScoredPlayer with unicode characters in player name"""
        player = FantasyPlayer(
            id=15,
            name="José Ramírez",
            team="SF",
            position="RB"
        )
        scored_player = ScoredPlayer(player, 95.5, ["Unicode Test"])

        result = str(scored_player)

        # Unicode characters should be preserved
        assert "José Ramírez" in result
        assert "95.50 pts" in result
        assert "- Unicode Test" in result

    def test_scored_player_with_whitespace_only_reason(self):
        """Test ScoredPlayer with whitespace-only reason"""
        player = FantasyPlayer(
            id=16,
            name="Whitespace Player",
            team="GB",
            position="QB"
        )
        reasons = ["Valid Reason", "   ", "Another Valid Reason"]
        scored_player = ScoredPlayer(player, 110.0, reasons)

        result = str(scored_player)

        # Whitespace reason should appear as bullet with spaces
        assert "- Valid Reason" in result
        assert "-    " in result  # Three spaces after dash
        assert "- Another Valid Reason" in result

    def test_scored_player_with_none_bye_week(self):
        """Test __str__ formatting when bye_week is None"""
        player = FantasyPlayer(
            id=17,
            name="No Bye Player",
            team="MIN",
            position="DST",
            bye_week=None
        )
        scored_player = ScoredPlayer(player, 75.0, ["Defense reason"])

        result = str(scored_player)

        # Should display "Bye=None" when bye_week is None
        assert "[DST] [MIN] No Bye Player - 75.00 pts (Bye=None)" in result
        assert "- Defense reason" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
