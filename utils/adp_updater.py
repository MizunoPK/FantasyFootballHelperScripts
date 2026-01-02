"""
ADP Player Data Updater Module

Purpose: Match CSV players to JSON players using fuzzy matching and update ADP values.
Adapts fuzzy matching logic from DraftedRosterManager.py and uses atomic write pattern
from PlayerManager.py.

Author: Claude Code (Epic: fix_2025_adp, Feature 2)
Created: 2025-12-31
"""

import json
import re
from pathlib import Path
from typing import Union, Dict, List, Tuple, Optional, Any
from difflib import SequenceMatcher

import pandas as pd

from utils.LoggingManager import get_logger

# Initialize logger
logger = get_logger()

# Constants
CONFIDENCE_THRESHOLD = 0.75  # Proven threshold from DraftedRosterManager
POSITION_FILES = {
    'QB': 'qb_data.json',
    'RB': 'rb_data.json',
    'WR': 'wr_data.json',
    'TE': 'te_data.json',
    'K': 'k_data.json',
    'DST': 'dst_data.json'
}


def normalize_name(name: str) -> str:
    """
    Normalize player name for fuzzy matching.

    Adapted from DraftedRosterManager._normalize_player_info().
    Removes punctuation, suffixes, and standardizes spacing.

    Args:
        name (str): Player name to normalize

    Returns:
        str: Normalized name (lowercase, no punctuation/suffixes)

    Example:
        >>> normalize_name("Amon-Ra St. Brown Jr.")
        'amonra st brown'
    """
    # Lowercase and collapse whitespace
    normalized = re.sub(r'\s+', ' ', name.strip().lower())

    # Remove suffixes (Jr., Sr., III, IV, II)
    normalized = re.sub(r'\b(jr\.?|sr\.?|iii?|iv|ii)\b', '', normalized)

    # Remove punctuation
    normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')

    # Final cleanup
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized


def calculate_similarity(name1: str, name2: str) -> float:
    """
    Calculate similarity score between two names.

    Uses difflib.SequenceMatcher.ratio() for similarity scoring.
    Adapted from DraftedRosterManager._similarity_score().

    Args:
        name1 (str): First name (normalized)
        name2 (str): Second name (normalized)

    Returns:
        float: Similarity score between 0.0 and 1.0

    Example:
        >>> calculate_similarity("patrick mahomes", "patrick mahomes ii")
        0.95  # High similarity despite suffix difference
    """
    return SequenceMatcher(None, name1, name2).ratio()


def extract_dst_team_name(name: str) -> str:
    """
    Extract team name from DST/Defense name for matching.

    Handles both formats:
    - JSON format: "Ravens D/ST" → "ravens"
    - CSV format: "Baltimore Ravens" → "ravens"

    Args:
        name (str): DST/Defense name in any format

    Returns:
        str: Normalized team name (last word, lowercase)

    Example:
        >>> extract_dst_team_name("Ravens D/ST")
        'ravens'
        >>> extract_dst_team_name("Baltimore Ravens")
        'ravens'
    """
    # Remove D/ST suffix if present
    name = re.sub(r'\s*d/st\s*$', '', name, flags=re.IGNORECASE)

    # Get last word (team name)
    words = name.strip().split()
    if words:
        return words[-1].lower()
    return name.lower()


def find_best_match(
    json_player_name: str,
    csv_df: pd.DataFrame,
    position: str
) -> Optional[Tuple[str, float, float]]:
    """
    Find best matching CSV player for a JSON player using fuzzy matching.

    Special handling for DST: Extracts team name from both JSON ("Ravens D/ST") and
    CSV ("Baltimore Ravens") formats to enable matching despite name differences.

    Args:
        json_player_name (str): Name of player from JSON file
        csv_df (pd.DataFrame): DataFrame with CSV player data
        position (str): Position to filter by (QB, RB, WR, TE, K, DST)

    Returns:
        Optional[Tuple[str, float, float]]: (csv_name, adp_value, confidence) or None
            - csv_name: Matched player name from CSV
            - adp_value: ADP value from CSV
            - confidence: Match confidence score (0.0-1.0)
            Returns None if no match found above threshold

    Example:
        >>> find_best_match("Patrick Mahomes II", csv_df, "QB")
        ("Patrick Mahomes", 15.5, 0.95)
        >>> find_best_match("Ravens D/ST", csv_df, "DST")
        ("Baltimore Ravens", 120.7, 1.0)
    """
    # Filter CSV by position
    position_players = csv_df[csv_df['position'] == position]

    if len(position_players) == 0:
        return None

    # Special handling for DST: Extract team names for matching
    # JSON: "Ravens D/ST" → "ravens", CSV: "Baltimore Ravens" → "ravens"
    if position == 'DST':
        json_team = extract_dst_team_name(json_player_name)

        # Find exact team name match
        for _, row in position_players.iterrows():
            csv_name = row['player_name']
            csv_team = extract_dst_team_name(csv_name)

            if json_team == csv_team:
                # Exact team name match for DST
                return (csv_name, row['adp'], 1.0)

        # No match found
        return None

    # Regular player matching (non-DST)
    normalized_json = normalize_name(json_player_name)

    # Find best match
    best_match = None
    best_score = 0.0
    best_adp = None

    for _, row in position_players.iterrows():
        csv_name = row['player_name']
        normalized_csv = normalize_name(csv_name)

        score = calculate_similarity(normalized_json, normalized_csv)

        if score > best_score:
            best_score = score
            best_match = csv_name
            best_adp = row['adp']

    # Return only if above confidence threshold
    if best_score >= CONFIDENCE_THRESHOLD:
        return (best_match, best_adp, best_score)

    return None


def update_player_adp_values(
    adp_dataframe: pd.DataFrame,
    sim_data_folder: Union[str, Path]
) -> Dict[str, Any]:
    """
    Match CSV players to JSON players and update ADP values across all simulation weeks.

    MULTI-WEEK PROCESSING:
    Dynamically discovers all week_* folders in sim_data_folder using glob pattern, then
    iterates through each week folder sequentially. Processes 6 position files per week
    (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json).
    For 18 weeks, this updates 108 total files.

    DATA STRUCTURE:
    Simulation JSON files use DIRECT ARRAYS (e.g., [{player1}, {player2}]), NOT wrapper
    dicts (e.g., {"qb_data": [...]}) like the main data folder. Function validates this
    structure and raises ValueError if wrapper dict detected.

    ATOMIC WRITES:
    All JSON updates use atomic write pattern (write to .tmp file, then replace original)
    to prevent corruption if process is interrupted during any of the 108 file writes.

    Args:
        adp_dataframe (pd.DataFrame): DataFrame from Feature 1 with columns:
            - player_name (str): Player name
            - adp (float): ADP value
            - position (str): Clean position (QB, RB, WR, TE, K, DST)
        sim_data_folder (Union[str, Path]): Path to simulation weeks folder
            (e.g., simulation/sim_data/2025/weeks/) containing week_01, week_02, ..., week_18

    Returns:
        Dict[str, Any]: Comprehensive match report AGGREGATED across all weeks:
            {
                'summary': {
                    'total_json_players': int,  # Aggregated count from all weeks
                    'matched': int,              # Total matches across all weeks
                    'unmatched_json': int,       # Unmatched players (aggregated)
                    'unmatched_csv': int         # CSV players not found in any week
                },
                'unmatched_json_players': List[Dict],  # From all weeks
                'unmatched_csv_players': List[Dict],   # CSV players not matched
                'confidence_distribution': Dict[str, int],  # Aggregated confidence stats
                'individual_matches': List[Dict]       # All matches from all weeks
            }

    Raises:
        ValueError: If DataFrame is empty, has wrong columns, or JSON has unexpected structure
        FileNotFoundError: If sim_data_folder doesn't exist or no week folders found
        PermissionError: If JSON files can't be written

    Example:
        >>> from utils.adp_csv_loader import load_adp_from_csv
        >>> csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')
        >>> adp_df = load_adp_from_csv(csv_path)
        >>> sim_folder = Path('simulation/sim_data/2025/weeks/')
        >>> report = update_player_adp_values(adp_df, sim_folder)
        >>> print(f"Matched: {report['summary']['matched']} players across 18 weeks")
        Matched: 11,700 players across 18 weeks  # 650 players × 18 weeks
    """
    # Validate input DataFrame
    if adp_dataframe.empty:
        raise ValueError("ADP DataFrame is empty")

    required_cols = ['player_name', 'adp', 'position']
    if not all(col in adp_dataframe.columns for col in required_cols):
        raise ValueError(f"DataFrame missing required columns: {required_cols}")

    # Convert to Path object
    sim_data_folder = Path(sim_data_folder)

    # Validate folder exists
    if not sim_data_folder.exists():
        raise FileNotFoundError(f"Simulation data folder not found: {sim_data_folder}")

    # MULTI-WEEK DISCOVERY: Dynamically find all week_* folders (week_01, week_02, ..., week_18)
    # Using glob pattern instead of hardcoding allows graceful handling of incomplete data
    week_folders = sorted(sim_data_folder.glob('week_*'))

    if len(week_folders) == 0:
        raise FileNotFoundError(f"No week folders found in: {sim_data_folder}")

    # Warn if missing weeks, but continue processing (graceful degradation)
    if len(week_folders) < 18:
        logger.warning(f"Expected 18 weeks, found {len(week_folders)} in {sim_data_folder}")

    logger.info(f"Found {len(week_folders)} week folders to process")

    # Initialize tracking variables - accumulate results across ALL weeks
    # For 18 weeks × ~650 players = ~11,700 total player entries processed
    total_json_players = 0
    matched_count = 0
    unmatched_json = []
    matched_csv_names = set()
    individual_matches = []
    confidence_dist = {'1.0': 0, '0.9-0.99': 0, '0.75-0.89': 0}

    logger.info("Starting player matching and ADP updates across all weeks...")

    # MULTI-WEEK ITERATION: Process each week folder sequentially
    # For 18 weeks × 6 positions = 108 total JSON files to update
    for week_folder in week_folders:
        week_name = week_folder.name
        logger.info(f"Processing {week_name}...")  # Per-week progress logging

        # Process each position within this week
        for position, filename in POSITION_FILES.items():
            json_path = week_folder / filename

            if not json_path.exists():
                logger.warning(f"JSON file not found: {json_path}")
                continue

            # DIRECT ARRAY LOADING: Simulation files use [{player1}, {player2}] structure
            # NOT {"qb_data": [...]} like main data folder - this is critical difference!
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    players = json.load(f)  # Returns list directly, not dict

                # STRUCTURE VALIDATION: Verify direct array, fail fast if wrapper dict detected
                # This catches incorrect file structure before attempting to process
                if not isinstance(players, list):
                    raise ValueError(
                        f"Unexpected JSON structure in {json_path}: "
                        f"Expected direct array [], got {type(players).__name__}. "
                        f"Simulation files should NOT have wrapper dict."
                    )
            except json.JSONDecodeError as e:
                # MALFORMED JSON: Fail entire operation if any file corrupted
                # All-or-nothing approach prevents partial updates across 108 files
                logger.error(f"Malformed JSON in {json_path}: {e}")
                raise ValueError(f"Failed to parse JSON file {json_path}: {e}") from e

            total_json_players += len(players)

            # Match each player
            for player in players:
                player_name = player.get('name', '')

                # Find best match in CSV
                match_result = find_best_match(player_name, adp_dataframe, position)

                if match_result:
                    csv_name, adp_value, confidence = match_result

                    # Update ADP value
                    old_adp = player.get('average_draft_position', 170.0)
                    player['average_draft_position'] = adp_value

                    # Track match
                    matched_count += 1
                    matched_csv_names.add(csv_name)

                    # Record individual match
                    individual_matches.append({
                        'json_name': player_name,
                        'csv_name': csv_name,
                        'position': position,
                        'old_adp': old_adp,
                        'new_adp': adp_value,
                        'confidence': confidence
                    })

                    # Track confidence distribution
                    if confidence == 1.0:
                        confidence_dist['1.0'] += 1
                    elif confidence >= 0.9:
                        confidence_dist['0.9-0.99'] += 1
                    else:
                        confidence_dist['0.75-0.89'] += 1
                else:
                    # No match found - keep existing 170.0 value
                    unmatched_json.append({
                        'name': player_name,
                        'position': position,
                        'adp': player.get('average_draft_position', 170.0)
                    })

            # ATOMIC WRITE PATTERN: Write to .tmp, then replace original
            # Critical for 108-file operation - prevents corruption if process interrupted
            tmp_path = json_path.with_suffix('.tmp')
            try:
                # DIRECT ARRAY WRITE: Write [{player1}, {player2}] NOT {"key": [...]}
                # This preserves simulation file structure (different from main data folder)
                with open(tmp_path, 'w', encoding='utf-8') as f:
                    json.dump(players, f, indent=2)  # players is list, not dict

                # Atomic replace - only replace if write succeeded (prevents partial writes)
                tmp_path.replace(json_path)
            except PermissionError as e:
                # PERMISSION ERROR: Clean up temp file and fail
                # Better to fail clean than leave .tmp files scattered across 108 locations
                logger.error(f"Permission denied writing to {json_path}: {e}")
                if tmp_path.exists():
                    tmp_path.unlink()  # Clean up temp file
                raise PermissionError(f"Cannot write to {json_path}: {e}") from e

            logger.info(f"Updated {week_name}/{filename}: {len(players)} players processed")

    # Find unmatched CSV players
    unmatched_csv = []
    for _, row in adp_dataframe.iterrows():
        if row['player_name'] not in matched_csv_names:
            unmatched_csv.append({
                'name': row['player_name'],
                'position': row['position'],
                'adp': row['adp']
            })

    # Log summary
    logger.info(f"Matching complete:")
    logger.info(f"  Total JSON players: {total_json_players}")
    logger.info(f"  Matched: {matched_count}")
    logger.info(f"  Unmatched JSON: {len(unmatched_json)}")
    logger.info(f"  Unmatched CSV: {len(unmatched_csv)}")
    logger.info(f"  Match rate: {matched_count / total_json_players * 100:.1f}%")

    # Build comprehensive report
    report = {
        'summary': {
            'total_json_players': total_json_players,
            'matched': matched_count,
            'unmatched_json': len(unmatched_json),
            'unmatched_csv': len(unmatched_csv)
        },
        'unmatched_json_players': unmatched_json,
        'unmatched_csv_players': unmatched_csv,
        'confidence_distribution': confidence_dist,
        'individual_matches': individual_matches
    }

    return report
