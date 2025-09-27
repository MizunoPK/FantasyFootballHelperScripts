"""
Core simulation engine for draft simulation.

Handles draft mechanics, team management, and turn-by-turn draft logic.
"""

import random
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared_files.FantasyPlayer import FantasyPlayer
from draft_helper.FantasyTeam import FantasyTeam
from draft_helper import draft_helper_config as base_config

@dataclass
class DraftPick:
    """Represents a single draft pick"""
    round_num: int
    pick_num: int
    team_index: int
    player: FantasyPlayer
    strategy_used: str

@dataclass
class SimulationTeam:
    """Represents a team in the simulation"""
    team_index: int
    strategy: str
    roster: FantasyTeam
    draft_picks: List[DraftPick]

    def __post_init__(self):
        if self.draft_picks is None:
            self.draft_picks = []

class DraftSimulationEngine:
    """Core engine for running draft simulations"""

    def __init__(self, players_df: pd.DataFrame, config_params: Dict[str, Any]):
        self.players_df = players_df.copy()
        self.config_params = config_params
        self.teams: List[SimulationTeam] = []
        self.available_players: List[FantasyPlayer] = []
        self.draft_history: List[DraftPick] = []
        self.current_round = 1
        self.current_pick = 1

        # Get draft teams CSV path (week 0) for positional rankings
        from .data_manager import SimulationDataManager
        self.data_manager = SimulationDataManager()
        self.draft_teams_csv_path = self.data_manager.teams_weekly_csvs[0]  # Week 0

        # Initialize teams
        self._initialize_teams()

        # Initialize available players
        self._initialize_available_players()

    def _initialize_teams(self) -> None:
        """Initialize all teams for the draft"""
        from .config import TEAM_STRATEGIES

        team_index = 0
        for strategy, count in TEAM_STRATEGIES.items():
            for _ in range(count):
                fantasy_team = FantasyTeam()
                sim_team = SimulationTeam(
                    team_index=team_index,
                    strategy=strategy,
                    roster=fantasy_team,
                    draft_picks=[]
                )
                self.teams.append(sim_team)
                team_index += 1

        # Randomize team order for snake draft
        random.shuffle(self.teams)

    def _initialize_available_players(self) -> None:
        """Initialize list of available players from dataframe"""
        self.available_players = []

        for idx, row in self.players_df.iterrows():
            # Only include players who aren't already drafted
            if row.get('drafted', 0) == 0:
                player = FantasyPlayer(
                    id=str(idx),  # Use dataframe index as ID
                    name=row.get('name', ''),
                    position=row.get('position', ''),
                    team=row.get('team', ''),
                    injury_status=row.get('injury_status', 'LOW'),
                    bye_week=row.get('bye_week', 0)
                )

                # Add weekly projections - set individual week fields
                for week in range(1, 18):  # Weeks 1-17
                    week_col = f'week_{week}_points'
                    if week_col in row:
                        points = row[week_col] if pd.notna(row[week_col]) else 0.0
                        setattr(player, week_col, float(points))

                self.available_players.append(player)

    def get_draft_order(self, round_num: int) -> List[int]:
        """Get the draft order for a given round (snake draft)"""
        if round_num % 2 == 1:  # Odd rounds: 1, 2, 3, ..., 10
            return list(range(len(self.teams)))
        else:  # Even rounds: 10, 9, 8, ..., 1
            return list(range(len(self.teams) - 1, -1, -1))

    def run_complete_draft(self, user_team_index: Optional[int] = None) -> Dict[str, Any]:
        """Run a complete draft simulation"""
        if user_team_index is None:
            user_team_index = random.randint(0, len(self.teams) - 1)

        # Mark which team is the user's team
        self.user_team_index = user_team_index

        total_rounds = base_config.MAX_PLAYERS

        for round_num in range(1, total_rounds + 1):
            self.current_round = round_num
            draft_order = self.get_draft_order(round_num)

            for position_in_round, team_index in enumerate(draft_order):
                self.current_pick = (round_num - 1) * len(self.teams) + position_in_round + 1
                team = self.teams[team_index]

                # Make the pick
                picked_player = self._make_team_pick(team, round_num)

                if picked_player:
                    # Record the pick
                    draft_pick = DraftPick(
                        round_num=round_num,
                        pick_num=self.current_pick,
                        team_index=team_index,
                        player=picked_player,
                        strategy_used=team.strategy
                    )

                    team.draft_picks.append(draft_pick)
                    self.draft_history.append(draft_pick)

                    # Remove player from available list
                    self.available_players.remove(picked_player)

                    # Add to team roster
                    team.roster.draft_player(picked_player)

        return self._generate_draft_results()

    def _make_team_pick(self, team: SimulationTeam, round_num: int) -> Optional[FantasyPlayer]:
        """Make a draft pick for a specific team"""
        from .team_strategies import TeamStrategyManager

        strategy_manager = TeamStrategyManager(self.config_params, self.draft_teams_csv_path)

        # Get top picks based on team strategy
        top_picks = strategy_manager.get_team_picks(
            team.strategy,
            self.available_players,
            team.roster,
            round_num
        )

        if not top_picks:
            return None

        # Apply human error (15% chance to pick from top 10 instead of #1)
        from .config import HUMAN_ERROR_RATE, SUBOPTIMAL_CHOICE_POOL

        if random.random() < HUMAN_ERROR_RATE:
            # Pick from top N choices instead of the best
            choice_pool_size = min(SUBOPTIMAL_CHOICE_POOL, len(top_picks))
            return random.choice(top_picks[:choice_pool_size])
        else:
            # Pick the best available
            return top_picks[0]

    def _generate_draft_results(self) -> Dict[str, Any]:
        """Generate summary of draft results"""
        results = {
            'teams': [],
            'user_team_index': self.user_team_index,
            'draft_history': self.draft_history,
            'total_picks': len(self.draft_history)
        }

        for i, team in enumerate(self.teams):
            team_result = {
                'team_index': i,
                'strategy': team.strategy,
                'roster_size': len(team.roster.roster),
                'draft_picks': team.draft_picks,
                'is_user_team': i == self.user_team_index
            }
            results['teams'].append(team_result)

        return results

    def get_player_week_points(self, player: FantasyPlayer, week: int) -> float:
        """Get points for a player for a specific week"""
        week_attr = f'week_{week}_points'
        return getattr(player, week_attr, 0.0) or 0.0

    def get_player_total_points(self, player: FantasyPlayer) -> float:
        """Get total points for a player across all weeks"""
        total = 0.0
        for week in range(1, 18):
            total += self.get_player_week_points(player, week)
        return total

    def get_team_by_index(self, team_index: int) -> Optional[SimulationTeam]:
        """Get a team by its index"""
        if 0 <= team_index < len(self.teams):
            return self.teams[team_index]
        return None