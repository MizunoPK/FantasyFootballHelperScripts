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
    # Display menu header with title
    print("="*25)
    print(title)
    print("="*25)

    # Display all numbered menu options (1-indexed for user-friendly display)
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    # Visual separator before quit option
    print("-----")

    # Calculate and display quit option number (always last option)
    # If there are 3 options, quit option will be #4
    max_choice = len(options) + 1
    print(f"{max_choice}. {quit_str}")
    print("="*25)

    # Input loop with validation
    # Continues until user enters a valid integer
    while (True):
        try:
            # Get user input, strip whitespace, and convert to integer
            # Note: This function does NOT validate range - it only validates integer input
            # Range validation is handled by the caller
            choice = int(input(f"Enter your choice (1-{max_choice}): ").strip())
            return choice
        except ValueError:
            # Non-integer input (e.g., "abc", "", "1.5") triggers retry
            print("Invalid choice. Please try again.")