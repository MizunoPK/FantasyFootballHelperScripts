"""
Unit Tests for Round-Robin Scheduler

Tests schedule generation for fantasy football leagues including single
and double round-robin algorithms, NFL season fitting, and validation.

Author: Kai Mizuno
"""

import pytest

from simulation.utils.scheduler import (
    generate_round_robin,
    generate_double_round_robin,
    generate_schedule_for_nfl_season,
    validate_schedule
)



class TestGenerateRoundRobin:
    """Test single round-robin schedule generation"""

    def test_basic_4_teams(self):
        """Test 4-team single round-robin schedule"""
        teams = [1, 2, 3, 4]
        schedule = generate_round_robin(teams)

        assert len(schedule) == 3

        for week in schedule:
            assert len(week) == 2

    def test_10_teams_produces_9_weeks(self):
        """Test 10-team league produces 9 weeks"""
        teams = list(range(1, 11))
        schedule = generate_round_robin(teams)

        assert len(schedule) == 9

        for week in schedule:
            assert len(week) == 5

    def test_each_team_plays_every_other_team_once(self):
        """Test that each team plays every other team exactly once"""
        teams = [1, 2, 3, 4]
        schedule = generate_round_robin(teams)

        matchups = set()
        for week in schedule:
            for team1, team2 in week:
                matchup = tuple(sorted([team1, team2]))
                assert matchup not in matchups, f"Duplicate matchup: {matchup}"
                matchups.add(matchup)

        assert len(matchups) == 6

    def test_no_team_plays_itself(self):
        """Test that no team plays against itself"""
        teams = [1, 2, 3, 4, 5, 6]
        schedule = generate_round_robin(teams)

        for week in schedule:
            for team1, team2 in week:
                assert team1 != team2, f"Team {team1} plays itself"

    def test_each_team_plays_once_per_week(self):
        """Test that each team plays exactly once per week"""
        teams = [1, 2, 3, 4]
        schedule = generate_round_robin(teams)

        for week_num, week in enumerate(schedule):
            teams_playing = []
            for team1, team2 in week:
                teams_playing.extend([team1, team2])

            assert len(teams_playing) == len(set(teams_playing)), \
                f"Week {week_num+1}: Some team plays multiple times"

    def test_odd_teams_raises_error(self):
        """Test that odd number of teams raises ValueError"""
        teams = [1, 2, 3]

        with pytest.raises(ValueError) as exc_info:
            generate_round_robin(teams)

        assert "even number" in str(exc_info.value).lower()

    def test_2_teams(self):
        """Test minimal case with 2 teams"""
        teams = ['A', 'B']
        schedule = generate_round_robin(teams)

        assert len(schedule) == 1
        assert len(schedule[0]) == 1
        assert schedule[0][0] == ('A', 'B') or schedule[0][0] == ('B', 'A')

    def test_works_with_string_teams(self):
        """Test schedule generation works with string team identifiers"""
        teams = ['Cowboys', 'Giants', 'Eagles', 'Washington']
        schedule = generate_round_robin(teams)

        assert len(schedule) == 3
        all_teams = set()
        for week in schedule:
            for team1, team2 in week:
                all_teams.add(team1)
                all_teams.add(team2)
        assert all_teams == set(teams)



class TestGenerateDoubleRoundRobin:
    """Test double round-robin schedule generation"""

    def test_basic_4_teams(self):
        """Test 4-team double round-robin schedule"""
        teams = [1, 2, 3, 4]
        schedule = generate_double_round_robin(teams)

        assert len(schedule) == 6

    def test_10_teams_produces_18_weeks(self):
        """Test 10-team league produces 18 weeks"""
        teams = list(range(1, 11))
        schedule = generate_double_round_robin(teams)

        assert len(schedule) == 18

    def test_each_team_plays_every_other_team_twice(self):
        """Test that each team plays every other team exactly twice"""
        teams = [1, 2, 3, 4]
        schedule = generate_double_round_robin(teams)

        matchups = []
        for week in schedule:
            for team1, team2 in week:
                matchups.append((team1, team2))

        from collections import Counter
        matchup_counts = Counter([tuple(sorted([t1, t2])) for t1, t2 in matchups])

        for count in matchup_counts.values():
            assert count == 2, "Each matchup should occur exactly twice"

    def test_second_half_reverses_matchups(self):
        """Test that second half has reversed matchups (home/away swap)"""
        teams = [1, 2, 3, 4]
        schedule = generate_double_round_robin(teams)

        first_half = schedule[:3]
        second_half = schedule[3:]

        first_matchups = []
        for week in first_half:
            first_matchups.extend(week)

        second_matchups = []
        for week in second_half:
            second_matchups.extend(week)

        for team1, team2 in first_matchups:
            assert (team2, team1) in second_matchups, \
                f"Matchup ({team1}, {team2}) not reversed in second half"

    def test_odd_teams_raises_error(self):
        """Test that odd number of teams raises ValueError"""
        teams = [1, 2, 3, 5]
        teams.append(5)
        teams = [1, 2, 3, 5, 7]

        with pytest.raises(ValueError):
            generate_double_round_robin(teams)



class TestGenerateScheduleForNFLSeason:
    """Test schedule generation for NFL season length"""

    def test_default_16_weeks(self):
        """Test default 16-week NFL season"""
        teams = list(range(1, 11))
        schedule = generate_schedule_for_nfl_season(teams)

        assert len(schedule) == 16

    def test_custom_week_count(self):
        """Test custom number of weeks"""
        teams = list(range(1, 11))
        schedule = generate_schedule_for_nfl_season(teams, num_weeks=14)

        assert len(schedule) == 14

    def test_no_trimming_needed_if_schedule_shorter(self):
        """Test no trimming if schedule is already short enough"""
        teams = [1, 2, 3, 4]
        schedule = generate_schedule_for_nfl_season(teams, num_weeks=10)

        assert len(schedule) == 6

    def test_trimming_preserves_structure(self):
        """Test that trimming preserves valid weekly structure"""
        teams = list(range(1, 11))
        schedule = generate_schedule_for_nfl_season(teams, num_weeks=16)

        for week in schedule:
            assert len(week) == 5
            teams_in_week = set()
            for team1, team2 in week:
                teams_in_week.add(team1)
                teams_in_week.add(team2)
            assert len(teams_in_week) == 10



class TestValidateSchedule:
    """Test schedule validation function"""

    def test_valid_round_robin_schedule(self):
        """Test validation of valid round-robin schedule"""
        teams = [1, 2, 3, 4]
        schedule = generate_round_robin(teams)

        assert validate_schedule(schedule, teams) == True

    def test_valid_double_round_robin_schedule(self):
        """Test validation of valid double round-robin schedule"""
        teams = [1, 2, 3, 4]
        schedule = generate_double_round_robin(teams)

        assert validate_schedule(schedule, teams) == True

    def test_invalid_team_plays_itself(self):
        """Test validation fails when team plays itself"""
        teams = [1, 2, 3, 4]
        invalid_schedule = [
            [(1, 1), (2, 3)]
        ]

        assert validate_schedule(invalid_schedule, teams) == False

    def test_invalid_duplicate_team_in_week(self):
        """Test validation fails when team plays multiple times in same week"""
        teams = [1, 2, 3, 4]
        invalid_schedule = [
            [(1, 2), (1, 3)]
        ]

        assert validate_schedule(invalid_schedule, teams) == False

    def test_empty_schedule(self):
        """Test validation of empty schedule"""
        teams = [1, 2, 3, 4]
        empty_schedule = []

        assert validate_schedule(empty_schedule, teams) == True

    def test_single_matchup_valid(self):
        """Test validation of single matchup"""
        teams = [1, 2]
        schedule = [[(1, 2)]]

        assert validate_schedule(schedule, teams) == True



class TestScheduleIntegration:
    """Test integration scenarios and complete workflows"""

    def test_10_team_league_full_workflow(self):
        """Test complete workflow for 10-team league"""
        teams = list(range(1, 11))

        full_schedule = generate_double_round_robin(teams)
        assert len(full_schedule) == 18

        nfl_schedule = generate_schedule_for_nfl_season(teams, num_weeks=16)
        assert len(nfl_schedule) == 16

        assert validate_schedule(nfl_schedule, teams) == True

    def test_schedule_fairness_properties(self):
        """Test that generated schedules have fairness properties"""
        teams = list(range(1, 11))
        schedule = generate_round_robin(teams)

        games_per_team = {team: 0 for team in teams}
        for week in schedule:
            for team1, team2 in week:
                games_per_team[team1] += 1
                games_per_team[team2] += 1

        expected_games = len(teams) - 1
        for team, games in games_per_team.items():
            assert games == expected_games, \
                f"Team {team} played {games} games, expected {expected_games}"

    def test_6_team_league(self):
        """Test schedule generation for 6-team league"""
        teams = ['A', 'B', 'C', 'D', 'E', 'F']
        schedule = generate_round_robin(teams)

        assert len(schedule) == 5

        for week in schedule:
            assert len(week) == 3

        assert validate_schedule(schedule, teams) == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


