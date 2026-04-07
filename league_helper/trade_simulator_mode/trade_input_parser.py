"""
Trade Input Parser

Helper class for parsing user input in Trade Simulator Mode.
Handles parsing player selections, validating input, and splitting combined selections.

Author: Kai Mizuno
"""

from typing import List, Optional, Tuple

from utils.FantasyPlayer import FantasyPlayer


class TradeInputParser:
    """
    Helper class for parsing user input in trade selection.

    Provides methods for:
    - Parsing comma-separated player numbers
    - Getting players by indices from rosters
    - Splitting unified selections into my/their players
    - Parsing and validating unified player selections
    - Providing detailed error messages for invalid inputs
    """

    @staticmethod
    def parse_player_selection(input_str: str, max_index: int) -> Optional[List[int]]:
        """
        Parse comma-separated player numbers from user input.

        Args:
            input_str (str): User input string with comma-separated numbers
            max_index (int): Maximum valid index (1-based)

        Returns:
            Optional[List[int]]: List of valid 1-based indices, or None if:
                - Input is 'exit' (case-insensitive)
                - Input contains invalid characters
                - Any number is out of range [1, max_index]
                - Duplicate numbers detected
                - Empty input

        Examples:
            >>> parse_player_selection("1,2,3", 5)
            [1, 2, 3]
            >>> parse_player_selection("1, 2, 3", 5)  # Spaces accepted
            [1, 2, 3]
            >>> parse_player_selection("exit", 5)
            None
            >>> parse_player_selection("1,99", 5)
            None
        """
        input_str = input_str.strip()

        if input_str.lower() == 'exit':
            return None

        if not input_str:
            return None

        parts = [part.strip() for part in input_str.split(',')]

        indices = []
        try:
            for part in parts:
                index = int(part)
                indices.append(index)
        except ValueError:
            return None

        for index in indices:
            if index < 1 or index > max_index:
                return None

        if len(indices) != len(set(indices)):
            return None

        return indices

    @staticmethod
    def get_players_by_indices(roster: List[FantasyPlayer], indices: List[int]) -> List[FantasyPlayer]:
        """
        Extract players from roster by 1-based indices.

        Args:
            roster (List[FantasyPlayer]): The roster to extract from
            indices (List[int]): 1-based indices of players to extract

        Returns:
            List[FantasyPlayer]: Players at the specified indices
        """
        players = []
        for index in indices:
            players.append(roster[index - 1])
        return players

    @staticmethod
    def split_players_by_team(unified_indices: List[int], roster_boundary: int) -> Tuple[List[int], List[int]]:
        """
        Split unified player selection into my players and their players.

        Args:
            unified_indices (List[int]): List of all selected player indices (1-based)
            roster_boundary (int): Index where opponent roster starts (1-based)

        Returns:
            Tuple[List[int], List[int]]: (my_indices, their_indices)
                my_indices: Indices from my roster (1-based, relative to my roster)
                their_indices: Indices from their roster (1-based, relative to their roster)

        Example:
            If my roster is numbered 1-13 and their roster starts at 14:
            Input: [2, 6, 14, 21], roster_boundary=14
            Output: ([2, 6], [1, 8])  # Their indices adjusted to be 1-based relative to their roster
        """
        my_indices = []
        their_indices = []

        for index in unified_indices:
            if index < roster_boundary:
                my_indices.append(index)
            else:
                their_indices.append(index - roster_boundary + 1)

        return my_indices, their_indices

    @staticmethod
    def parse_unified_player_selection(input_str: str, max_index: int, roster_boundary: int) -> Optional[Tuple[List[int], List[int]]]:
        """
        Parse unified player selection and split into my players and their players.

        Validates that:
        - Input is valid (numbers, in range, no duplicates)
        - At least 1 player from each team
        - Supports both equal and unequal trades (1-for-2, 2-for-1, 2-for-3, etc.)

        Args:
            input_str (str): User input string with comma-separated numbers
            max_index (int): Maximum valid index (1-based)
            roster_boundary (int): Index where opponent roster starts (1-based)

        Returns:
            Optional[Tuple[List[int], List[int]]]: (my_indices, their_indices) or None if:
                - Input is 'exit' (case-insensitive)
                - Input contains invalid characters
                - Any number is out of range [1, max_index]
                - Duplicate numbers detected
                - Empty input
                - Less than 1 player from either team

        Examples:
            >>> parse_unified_player_selection("2,6,18,21", 30, 14)
            ([2, 6], [5, 8])  # Valid: 2-for-2 trade
            >>> parse_unified_player_selection("4,17,18", 30, 14)
            ([4], [4, 5])  # Valid: 1-for-2 trade
            >>> parse_unified_player_selection("1,2,3", 30, 14)
            None  # Invalid: all from my team
        """
        unified_indices = TradeInputParser.parse_player_selection(input_str, max_index)

        if unified_indices is None:
            return None

        my_indices, their_indices = TradeInputParser.split_players_by_team(unified_indices, roster_boundary)

        if len(my_indices) < 1 or len(their_indices) < 1:
            return None

        return my_indices, their_indices

    @staticmethod
    def parse_with_error_message(input_str: str, max_index: int, roster_boundary: int) -> Tuple[Optional[Tuple[List[int], List[int]]], str]:
        """
        Parse player selection and return detailed error message if invalid.

        Args:
            input_str (str): User input string
            max_index (int): Maximum valid index
            roster_boundary (int): Index where opponent roster starts

        Returns:
            Tuple of (parsed_result, error_message):
                - If valid: ((my_indices, their_indices), "")
                - If invalid: (None, "descriptive error message")
        """
        if input_str.strip().lower() == 'exit':
            return (None, "")

        if not input_str.strip():
            return (None, "Error: No players selected. Please enter player numbers separated by commas.")

        unified_indices = TradeInputParser.parse_player_selection(input_str, max_index)

        if unified_indices is None:
            parts = [part.strip() for part in input_str.split(',')]

            try:
                indices = [int(part) for part in parts]
            except ValueError:
                return (None, "Error: Invalid input. Please enter only numbers separated by commas (e.g., '4,17,18').")

            for idx in indices:
                if idx < 1 or idx > max_index:
                    return (None, f"Error: Player number {idx} is out of range. Valid range is 1-{max_index}.")

            if len(indices) != len(set(indices)):
                return (None, "Error: Duplicate player numbers detected. Each player can only be selected once.")

            return (None, "Error: Invalid input format.")

        my_indices, their_indices = TradeInputParser.split_players_by_team(unified_indices, roster_boundary)

        if len(my_indices) < 1:
            return (None, f"Error: You must select at least one player from your team (numbers 1-{roster_boundary-1}).")
        if len(their_indices) < 1:
            return (None, f"Error: You must select at least one player from the opponent's team (numbers {roster_boundary}+).")

        return ((my_indices, their_indices), "")


