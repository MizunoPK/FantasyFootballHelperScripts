from typing import List


def show_list_selection(title : str, options : List[str], quit_str : str) -> int:
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