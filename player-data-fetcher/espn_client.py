#!/usr/bin/env python3
"""
ESPN Fantasy API Client

This module handles all ESPN API interactions for fantasy football data collection.
Separated from the main script for better organization and maintainability.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, List, Any, Optional
import math

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from models import ESPNPlayerData, ScoringFormat
from player_data_constants import (
    ESPN_TEAM_MAPPINGS, ESPN_POSITION_MAPPINGS, ESPN_USER_AGENT, ESPN_PLAYER_LIMIT,
    MIN_PLAYERS_FOR_EMPIRICAL_MAPPING, MIN_PLAYERS_PER_POSITION_MAPPING,
    POSITION_FALLBACK_CONFIG, DEFAULT_FALLBACK_CONFIG, MIN_ADP_RANGE_THRESHOLD,
    MIN_FANTASY_POINTS_BOUND_FACTOR, MAX_FANTASY_POINTS_BOUND_FACTOR,
    UNCERTAINTY_ADJUSTMENT_FACTOR, PositionDataDict, PositionMappingDict
)


class ESPNAPIError(Exception):
    """Custom exception for ESPN API errors"""
    pass


class ESPNRateLimitError(ESPNAPIError):
    """Rate limit exceeded exception"""
    pass


class ESPNServerError(ESPNAPIError):
    """ESPN server error exception"""  
    pass


class BaseAPIClient:
    """Base API client with common functionality"""
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self._client = None
    
    @asynccontextmanager
    async def session(self):
        """Async context manager for HTTP client session"""
        if self._client is None:
            timeout = httpx.Timeout(self.settings.request_timeout)
            self._client = httpx.AsyncClient(timeout=timeout)
        
        try:
            yield self._client
        finally:
            if self._client:
                await self._client.aclose()
                self._client = None
    
    @retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=10))
    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        self.logger.info(f"Making request to: {url}")
        
        # Add rate limiting delay
        await asyncio.sleep(self.settings.rate_limit_delay)
        
        try:
            response = await self._client.request(method, url, **kwargs)
            
            # Handle specific HTTP errors
            if response.status_code == 429:
                raise ESPNRateLimitError(f"Rate limit exceeded: {response.status_code}")
            elif response.status_code >= 500:
                raise ESPNServerError(f"ESPN server error: {response.status_code}")
            elif response.status_code >= 400:
                raise ESPNAPIError(f"ESPN API error: {response.status_code}")
                
            response.raise_for_status()
            self.logger.info("Request successful")
            return response.json()
            
        except httpx.RequestError as e:
            self.logger.error(f"Request failed: {e}")
            raise ESPNAPIError(f"Network error: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise


class ESPNClient(BaseAPIClient):
    """ESPN Fantasy API client for player projections"""
    
    def __init__(self, settings):
        super().__init__(settings)
        self.bye_weeks: Dict[str, int] = {}
    
    def _get_ppr_id(self) -> int:
        """Get ESPN scoring format ID"""
        scoring_map = {
            ScoringFormat.STANDARD: 1,
            ScoringFormat.PPR: 3, 
            ScoringFormat.HALF_PPR: 2
        }
        return scoring_map.get(self.settings.scoring_format, 3)
    
    async def get_season_projections(self) -> List[ESPNPlayerData]:
        """Get season projections from ESPN"""
        ppr_id = self._get_ppr_id()
        
        # ESPN's main fantasy API endpoint for player projections
        url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{self.settings.season}/segments/0/leaguedefaults/{ppr_id}"
        
        params = {
            "view": "kona_player_info",
            "scoringPeriodId": 0  # 0 = season projections
        }
        
        headers = {
            'User-Agent': ESPN_USER_AGENT,
            'X-Fantasy-Filter': f'{{"players":{{"limit":{ESPN_PLAYER_LIMIT},"sortPercOwned":{{"sortPriority":4,"sortAsc":false}}}}}}'
        }
        
        data = await self._make_request("GET", url, params=params, headers=headers)
        return self._parse_espn_data(data)
    
    async def _make_request(self, method: str, url: str, **kwargs):
        """Override to add ESPN-specific headers"""
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        
        # Ensure User-Agent is always set for ESPN
        if 'User-Agent' not in kwargs['headers']:
            kwargs['headers']['User-Agent'] = ESPN_USER_AGENT
        
        return await super()._make_request(method, url, **kwargs)
    
    def _parse_espn_data(self, data: Dict[str, Any]) -> List[ESPNPlayerData]:
        """Parse ESPN API response into ESPNPlayerData objects"""
        projections = []
        
        players = data.get('players', [])
        self.logger.info(f"Processing {len(players)} players from ESPN API")
        
        parsed_count = 0
        for player in players:
            try:
                # Extract basic info
                player_info = player.get('player', {})
                id = str(player_info.get('id', ''))
                
                if not id:
                    continue
                
                # Extract name parts
                name_parts = []
                if player_info.get('firstName'):
                    name_parts.append(player_info['firstName'])
                if player_info.get('lastName'):  
                    name_parts.append(player_info['lastName'])
                name = ' '.join(name_parts) if name_parts else 'Unknown Player'
                
                # Extract team
                pro_team_id = player_info.get('proTeamId')
                team = ESPN_TEAM_MAPPINGS.get(pro_team_id, 'UNK')
                
                # Skip players not on active NFL rosters (free agents, practice squad, etc.)
                if team == 'UNK':
                    continue
                
                # Extract position
                position_id = player_info.get('defaultPositionId')
                position = ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')
                
                # Get bye week
                bye_week = self.bye_weeks.get(team)
                
                # Extract fantasy points from stats with 2024 fallback
                fantasy_points = 0.0
                stats = player.get('player', {}).get('stats', [])
                
                # Debug DST data availability
                if position == 'DST':
                    self.logger.info(f"DST DEBUG: {name} has {len(stats)} stat entries")
                    season_entries = [stat for stat in stats if stat.get('scoringPeriodId') == 0]
                    self.logger.info(f"  Season projection entries (scoringPeriodId=0): {len(season_entries)}")
                    for i, stat in enumerate(season_entries):
                        self.logger.info(f"    Season entry {i}: seasonId={stat.get('seasonId')}, appliedTotal={stat.get('appliedTotal')}, projectedTotal={stat.get('projectedTotal')}")
                    for i, stat in enumerate(stats[:3]):  # Log first 3 entries
                        self.logger.info(f"  Entry {i}: seasonId={stat.get('seasonId')}, scoringPeriodId={stat.get('scoringPeriodId')}, appliedTotal={stat.get('appliedTotal')}, projectedTotal={stat.get('projectedTotal')}")
                
                # First try to get current season (2025) projections - pick highest positive value
                season_projections = []
                for stat_entry in stats:
                    if stat_entry.get('scoringPeriodId') == 0 and stat_entry.get('seasonId') == self.settings.season:
                        points = 0.0
                        if 'appliedTotal' in stat_entry:
                            points = float(stat_entry['appliedTotal'])
                        elif 'projectedTotal' in stat_entry:
                            points = float(stat_entry['projectedTotal'])
                        if points > 0:  # Only consider positive projections
                            season_projections.append(points)
                
                if season_projections:
                    fantasy_points = max(season_projections)  # Use the highest positive projection
                
                # If no current season projections found, fall back to 2024 season projections
                fallback_used = False
                if fantasy_points == 0.0:
                    season_2024_projections = []
                    for stat_entry in stats:
                        if stat_entry.get('scoringPeriodId') == 0 and stat_entry.get('seasonId') == 2024:
                            if position == 'DST':
                                self.logger.info(f"DST 2024 SEASON DEBUG: {name} found 2024 season entry: appliedTotal={stat_entry.get('appliedTotal')}, projectedTotal={stat_entry.get('projectedTotal')}")
                            
                            points = 0.0
                            if 'appliedTotal' in stat_entry:
                                points = float(stat_entry['appliedTotal'])
                            elif 'projectedTotal' in stat_entry:
                                points = float(stat_entry['projectedTotal'])
                            if points > 0:  # Only consider positive projections
                                season_2024_projections.append(points)
                    
                    if season_2024_projections:
                        fantasy_points = max(season_2024_projections)  # Use highest positive 2024 projection
                        fallback_used = True
                    
                    # Third fallback: Calculate season projection from 2024 weekly data
                    if fantasy_points == 0.0:
                        weekly_points = []
                        if position == 'DST':
                            self.logger.info(f"DST WEEKLY DEBUG: {name} checking weekly data from {len(stats)} entries")
                        
                        for stat_entry in stats:
                            # Get 2024 weekly data (periods 1-18)
                            if (stat_entry.get('seasonId') == 2024 and 
                                stat_entry.get('scoringPeriodId', 0) > 0 and 
                                stat_entry.get('scoringPeriodId', 0) <= 18):
                                
                                week_points = 0.0
                                if 'appliedTotal' in stat_entry:
                                    week_points = float(stat_entry['appliedTotal'])
                                elif 'projectedTotal' in stat_entry:
                                    week_points = float(stat_entry['projectedTotal'])
                                
                                if position == 'DST' and week_points != 0:
                                    self.logger.info(f"  Week {stat_entry.get('scoringPeriodId')}: {week_points} pts")
                                
                                # Include all scores for defenses (they can have negative weeks)
                                # For other positions, only include positive scores
                                if week_points != 0 and (position == 'DST' or week_points > 0):
                                    weekly_points.append(week_points)
                        
                        # Calculate projected season total from weekly averages
                        if weekly_points:
                            avg_per_week = sum(weekly_points) / len(weekly_points)
                            projected_season = avg_per_week * 17  # 17-game season
                            fantasy_points = projected_season
                            fallback_used = True
                            self.logger.info(f"Using weekly average fallback for {name}: {len(weekly_points)} weeks, {avg_per_week:.1f} avg, {projected_season:.1f} season total")
                        else:
                            # Final fallback - debug output for defenses
                            if position == 'DST':
                                self.logger.warning(f"DEFENSE DEBUG: {name} has no weekly data either. Stats count: {len(stats)}")
                                # Log all stat entries for this defense to see what data is available
                                for i, stat in enumerate(stats):
                                    self.logger.warning(f"  Stat {i}: seasonId={stat.get('seasonId')}, scoringPeriodId={stat.get('scoringPeriodId')}, appliedTotal={stat.get('appliedTotal')}, projectedTotal={stat.get('projectedTotal')}")
                            self.logger.warning(f"No usable data for {name} ({position}). Using 0.0 points.")
                
                # Log when fallback is used for transparency
                if fallback_used:
                    self.logger.info(f"Using 2024 fallback data for {name} ({position}): {fantasy_points:.1f} points")
                
                # Fantasy points are already positive from our selection logic above
                
                # Extract injury status
                injury_status = "ACTIVE"  # Default
                injury_info = player_info.get('injuryStatus')
                if injury_info:
                    injury_status = injury_info.upper()
                
                # Extract ADP data
                average_draft_position = None
                ownership_data = player_info.get('ownership', {})
                if ownership_data and 'averageDraftPosition' in ownership_data:
                    average_draft_position = float(ownership_data['averageDraftPosition'])
                
                # Create player projection
                projection = ESPNPlayerData(
                    id=id,
                    name=name,
                    team=team,
                    position=position,
                    bye_week=bye_week,
                    drafted=0,  # Initialize all players as not drafted
                    fantasy_points=fantasy_points,
                    average_draft_position=average_draft_position,
                    injury_status=injury_status,
                    api_source="ESPN"
                )
                
                projections.append(projection)
                parsed_count += 1
                
            except (KeyError, TypeError, ValueError) as e:
                player_id = player.get('player', {}).get('id', 'unknown')
                self.logger.warning(f"Failed to parse player {player_id}: {e}")
                continue
            except Exception as e:
                player_id = player.get('player', {}).get('id', 'unknown')
                self.logger.error(f"Unexpected error parsing player {player_id}: {e}")
                continue
        
        self.logger.info(f"Successfully parsed {parsed_count} players with projections")
        
        # Apply empirical ADP mapping for 0-point players
        projections = self._apply_empirical_adp_mapping(projections)
        
        return projections
    
    def _apply_empirical_adp_mapping(self, players: List[ESPNPlayerData]) -> List[ESPNPlayerData]:
        """Apply empirical ADP-to-fantasy-points mapping for players with 0 points"""
        
        # Step 1: Analyze existing players with both ADP and fantasy points
        players_with_both = []
        zero_point_players = []
        
        for player in players:
            if player.fantasy_points > 0 and player.average_draft_position:
                players_with_both.append(player)
            elif player.fantasy_points == 0 and player.average_draft_position:
                zero_point_players.append(player)
        
        self.logger.info(f"Found {len(players_with_both)} players with both fantasy points and ADP")
        self.logger.info(f"Found {len(zero_point_players)} zero-point players with ADP to update")
        
        if len(players_with_both) < MIN_PLAYERS_FOR_EMPIRICAL_MAPPING:
            self.logger.warning("Insufficient data for empirical ADP mapping - skipping")
            return players
        
        # Step 2: Build position-specific ADP->fantasy points mappings
        position_mappings = self._build_position_adp_mappings(players_with_both)
        
        # Step 3: Apply mappings to zero-point players
        updated_count = 0
        for player in zero_point_players:
            if player.position in position_mappings:
                estimated_points = self._estimate_fantasy_points_from_adp(
                    player.average_draft_position, 
                    player.position, 
                    position_mappings
                )
                player.fantasy_points = estimated_points
                updated_count += 1
                self.logger.debug(f"Updated {player.name} ({player.position}) ADP {player.average_draft_position:.1f} -> {estimated_points:.1f} points")
        
        self.logger.info(f"Updated fantasy points for {updated_count} players using empirical ADP mapping")
        return players
    
    def _build_position_adp_mappings(self, players_with_both: List[ESPNPlayerData]) -> Dict[str, PositionMappingDict]:
        """Build position-specific mappings from ADP to fantasy points using position-adjusted scaling"""
        # Group players by position
        position_data = self._group_players_by_position(players_with_both)
        
        # Create position-adjusted scaling models
        position_mappings = {}
        for position, data in position_data.items():
            if len(data['adp_values']) >= MIN_PLAYERS_PER_POSITION_MAPPING:
                mapping = self._create_position_mapping(position, data['adp_values'], data['fantasy_values'])
                if mapping:
                    position_mappings[position] = mapping
        
        return position_mappings
    
    def _group_players_by_position(self, players: List[ESPNPlayerData]) -> Dict[str, PositionDataDict]:
        """Group players by position for ADP analysis"""
        position_data = {}
        
        for player in players:
            position = player.position
            adp = player.average_draft_position
            fantasy_points = player.fantasy_points
            
            if position not in position_data:
                position_data[position] = {'adp_values': [], 'fantasy_values': []}
            
            position_data[position]['adp_values'].append(adp)
            position_data[position]['fantasy_values'].append(fantasy_points)
        
        return position_data
    
    def _create_position_mapping(self, position: str, adp_values: List[float], fantasy_values: List[float]) -> Optional[PositionMappingDict]:
        """Create position-specific ADP-to-fantasy-points mapping"""
        try:
            # Calculate position-specific ADP and fantasy point ranges
            min_adp = min(adp_values)
            max_adp = max(adp_values)
            min_points = min(fantasy_values)
            max_points = max(fantasy_values)
            
            # Avoid division by zero if all ADPs are the same
            if max_adp - min_adp < MIN_ADP_RANGE_THRESHOLD:
                self.logger.warning(f"Insufficient ADP range for {position}: {min_adp:.1f} to {max_adp:.1f}")
                return None
            
            # Calculate correlation to validate relationship strength
            correlation = self._calculate_correlation(adp_values, fantasy_values)
            if correlation is None:
                return None
            
            mapping = {
                'min_adp': min_adp,
                'max_adp': max_adp,
                'min_points': min_points,
                'max_points': max_points,
                'adp_range': max_adp - min_adp,
                'points_range': max_points - min_points,
                'sample_size': len(adp_values),
                'correlation': correlation
            }
            
            self.logger.debug(f"{position}: ADP {min_adp:.1f}-{max_adp:.1f}, "
                            f"Points {min_points:.1f}-{max_points:.1f}, "
                            f"correlation={correlation:.3f}, n={len(adp_values)}")
            
            return mapping
            
        except (ZeroDivisionError, ValueError) as e:
            self.logger.warning(f"Failed to create mapping for {position}: {e}")
            return None
    
    def _calculate_correlation(self, x_values: List[float], y_values: List[float]) -> Optional[float]:
        """Calculate Pearson correlation coefficient between two lists"""
        n = len(x_values)
        if n == 0:
            return None
            
        mean_x = sum(x_values) / n
        mean_y = sum(y_values) / n
        
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
        denominator_x = sum((x - mean_x) ** 2 for x in x_values)
        denominator_y = sum((y - mean_y) ** 2 for y in y_values)
        
        if denominator_x == 0 or denominator_y == 0:
            return None
            
        correlation = numerator / (math.sqrt(denominator_x) * math.sqrt(denominator_y))
        return correlation
    
    def _estimate_fantasy_points_from_adp(self, adp: float, position: str, position_mappings: Dict[str, PositionMappingDict]) -> float:
        """Estimate fantasy points from ADP using position-adjusted scaling"""
        
        if position not in position_mappings:
            # Position-aware fallback based on configurable constants
            config = POSITION_FALLBACK_CONFIG.get(position, DEFAULT_FALLBACK_CONFIG)
            return max(1.0, config.base_points - (adp * config.multiplier))
        
        mapping = position_mappings[position]
        
        # Position-adjusted scaling: normalize ADP within position range, then scale to fantasy points
        normalized_adp = (adp - mapping['min_adp']) / mapping['adp_range']
        
        # Clamp normalized ADP to [0, 1] range to handle players outside observed range
        normalized_adp = max(0.0, min(1.0, normalized_adp))
        
        # Convert to fantasy points: lower ADP (normalized closer to 0) = higher fantasy points
        estimated_points = mapping['max_points'] - (normalized_adp * mapping['points_range'])
        
        # Apply reasonable bounds with some flexibility
        min_bound = max(1.0, mapping['min_points'] * MIN_FANTASY_POINTS_BOUND_FACTOR)
        max_bound = mapping['max_points'] * MAX_FANTASY_POINTS_BOUND_FACTOR
        
        estimated_points = max(min_bound, min(max_bound, estimated_points))
        
        # Add small random component based on correlation strength to account for uncertainty
        # Lower correlation = more uncertainty = more conservative estimate
        uncertainty_factor = 1.0 - abs(mapping.get('correlation', 0.0))
        adjustment = estimated_points * uncertainty_factor * UNCERTAINTY_ADJUSTMENT_FACTOR
        estimated_points = max(min_bound, estimated_points - adjustment)
        
        return float(estimated_points)