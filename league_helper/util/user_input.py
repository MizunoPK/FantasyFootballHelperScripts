"""
User Input Utilities

Interactive CLI utilities for displaying menus and getting user selections.
Provides numbered menu displays with quit options for consistent user experience
throughout the league helper application.

Key responsibilities:
- Displaying formatted numbered menus with titles
- Handling user input with validation and retry logic
- Supporting custom quit option labels
- Input sanitization (stripping whitespace)
- Error handling for invalid inputs (non-integers)
- Returning user selection as integer (1-based indexing)

Author: Kai Mizuno
"""

from typing import List


def show_list_selection(title : str, options : List[str], quit_str : str) -> int:
    """
    Display a numbered menu and get user selection.

    Presents a formatted menu with numbered options and a quit option,
    then prompts the user for input with validation and retry logic.

    Args:
        title (str): Menu title to display at the top
        options (List[str]): List of menu options to display (numbered 1-N)
        quit_str (str): Label for the quit option (displayed as option N+1)

    Returns:
        int: User's choice as 1-based index (1 to len(options)+1)
            - Values 1 to len(options) represent menu options
            - Value len(options)+1 represents quit selection

    Example:
        >>> choice = show_list_selection("Main Menu", ["Option A", "Option B"], "Exit")
        =========================
        Main Menu
        =========================
        1. Option A
        2. Option B
        -----
        3. Exit
        =========================
        Enter your choice (1-3): 1
    """
    print("="*25)
    print(title)
    print("="*25)

    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    print("-----")

    max_choice = len(options) + 1
    print(f"{max_choice}. {quit_str}")
    print("="*25)

    while (True):
        try:
            choice = int(input(f"Enter your choice (1-{max_choice}): ").strip())
            return choice
        except ValueError:
            print("Invalid choice. Please try again.")