"""
Comprehensive Unit Tests for user_input.py

Tests the user input utility functions for displaying menus and getting selections:
- show_list_selection: Display numbered menu and get user choice

This module provides interactive CLI functionality for the league helper.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, patch, call
from io import StringIO

from league_helper.util.user_input import show_list_selection



class TestShowListSelection:
    """Test show_list_selection() function"""

    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_first_option(self, mock_stdout, mock_input):
        """Test selecting first option"""
        options = ['Option 1', 'Option 2', 'Option 3']
        result = show_list_selection('Test Menu', options, 'Quit')

        assert result == 1
        mock_input.assert_called_once()

    @patch('builtins.input', return_value='3')
    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_middle_option(self, mock_stdout, mock_input):
        """Test selecting middle option"""
        options = ['Option 1', 'Option 2', 'Option 3']
        result = show_list_selection('Test Menu', options, 'Quit')

        assert result == 3
        mock_input.assert_called_once()

    @patch('builtins.input', return_value='4')
    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_quit_option(self, mock_stdout, mock_input):
        """Test selecting quit option (max_choice)"""
        options = ['Option 1', 'Option 2', 'Option 3']
        result = show_list_selection('Test Menu', options, 'Quit')

        assert result == 4
        mock_input.assert_called_once()

    @patch('builtins.input', side_effect=['invalid', 'abc', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_then_valid_input(self, mock_stdout, mock_input):
        """Test that invalid input is retried until valid input given"""
        options = ['Option 1', 'Option 2']
        result = show_list_selection('Test Menu', options, 'Quit')

        assert result == 2
        assert mock_input.call_count == 3
        output = mock_stdout.getvalue()
        assert output.count('Invalid choice. Please try again.') == 2

    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_title(self, mock_stdout, mock_input):
        """Test that title is displayed correctly"""
        options = ['Option 1']
        show_list_selection('My Title', options, 'Exit')

        output = mock_stdout.getvalue()
        assert 'My Title' in output
        assert '=' * 25 in output

    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_all_options(self, mock_stdout, mock_input):
        """Test that all options are displayed with numbering"""
        options = ['First', 'Second', 'Third']
        show_list_selection('Menu', options, 'Quit')

        output = mock_stdout.getvalue()
        assert '1. First' in output
        assert '2. Second' in output
        assert '3. Third' in output

    @patch('builtins.input', return_value='2')
    @patch('sys.stdout', new_callable=StringIO)
    def test_displays_quit_option(self, mock_stdout, mock_input):
        """Test that quit option is displayed with correct number"""
        options = ['Option 1']
        show_list_selection('Menu', options, 'Exit Program')

        output = mock_stdout.getvalue()
        assert '2. Exit Program' in output

    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=StringIO)
    def test_single_option_list(self, mock_stdout, mock_input):
        """Test with single option"""
        options = ['Only Option']
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 1
        output = mock_stdout.getvalue()
        assert '1. Only Option' in output
        assert '2. Quit' in output

    @patch('builtins.input', return_value='10')
    @patch('sys.stdout', new_callable=StringIO)
    def test_large_number_valid(self, mock_stdout, mock_input):
        """Test that large but valid numbers are accepted"""
        options = [f'Option {i}' for i in range(1, 11)]
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 10

    @patch('builtins.input', side_effect=['0', '100', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_out_of_range_numbers_rejected_and_reprompted(self, mock_stdout, mock_input):
        """Test that out-of-range numbers are rejected and re-prompted until a valid choice"""
        options = ['Option 1']
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 2
        assert mock_input.call_count == 3
        output = mock_stdout.getvalue()
        assert output.count('Invalid choice. Please try again.') == 2

    @patch('builtins.input', side_effect=['  5  ', ])
    @patch('sys.stdout', new_callable=StringIO)
    def test_input_with_whitespace(self, mock_stdout, mock_input):
        """Test that input with whitespace is handled (stripped)"""
        options = ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5']
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 5

    @patch('builtins.input', side_effect=['', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_input_retries(self, mock_stdout, mock_input):
        """Test that empty input is rejected and retried"""
        options = ['Option 1', 'Option 2']
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 2
        assert mock_input.call_count == 2
        output = mock_stdout.getvalue()
        assert 'Invalid choice. Please try again.' in output


class TestShowListSelectionRangeValidation:
    """Test that show_list_selection enforces its advertised 1..max_choice range (T81)."""

    @patch('builtins.input', side_effect=['0', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_zero_is_rejected_and_reprompted(self, mock_stdout, mock_input):
        """Test that 0 re-prompts instead of returning and indexing options[-1]"""
        options = ['Option 1', 'Option 2', 'Option 3']
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 2
        assert mock_input.call_count == 2
        output = mock_stdout.getvalue()
        assert output.count('Invalid choice. Please try again.') == 1

    @patch('builtins.input', side_effect=['-1', '1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_negative_is_rejected_and_reprompted(self, mock_stdout, mock_input):
        """Test that a negative number re-prompts instead of returning"""
        options = ['Option 1', 'Option 2', 'Option 3']
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 1
        assert mock_input.call_count == 2
        output = mock_stdout.getvalue()
        assert output.count('Invalid choice. Please try again.') == 1

    @patch('builtins.input', side_effect=['99', '3'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_high_out_of_range_is_rejected_and_reprompted(self, mock_stdout, mock_input):
        """Test that a far-out-of-range number re-prompts instead of raising downstream"""
        options = ['Option 1', 'Option 2', 'Option 3']
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 3
        assert mock_input.call_count == 2
        output = mock_stdout.getvalue()
        assert output.count('Invalid choice. Please try again.') == 1

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_value_one_above_the_sentinel_is_rejected(self, mock_stdout, mock_input):
        """Test that the first value past the quit sentinel is rejected, not returned"""
        options = ['Option 1', 'Option 2', 'Option 3']
        sentinel = len(options) + 1
        mock_input.side_effect = [str(sentinel + 1), '1']

        result = show_list_selection('Menu', options, 'Quit')

        assert result == 1
        assert mock_input.call_count == 2
        output = mock_stdout.getvalue()
        assert output.count('Invalid choice. Please try again.') == 1

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_cancel_sentinel_is_accepted_on_a_one_option_menu(self, mock_stdout, mock_input):
        """Test that the quit/cancel sentinel len(options)+1 is still accepted (smallest menu)"""
        options = ['Only Option']
        sentinel = len(options) + 1
        mock_input.side_effect = [str(sentinel)]

        result = show_list_selection('Menu', options, 'Cancel')

        assert result == sentinel
        assert mock_input.call_count == 1
        output = mock_stdout.getvalue()
        assert 'Invalid choice. Please try again.' not in output

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_cancel_sentinel_is_accepted_on_a_ten_option_menu(self, mock_stdout, mock_input):
        """Test that the quit/cancel sentinel is still accepted on a realistic 10-team menu"""
        options = [f'Team {i}' for i in range(1, 11)]
        sentinel = len(options) + 1
        mock_input.side_effect = [str(sentinel)]

        result = show_list_selection('TEAM SELECTION', options, 'Cancel')

        assert result == sentinel
        assert mock_input.call_count == 1
        output = mock_stdout.getvalue()
        assert 'Invalid choice. Please try again.' not in output

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_last_real_option_is_accepted(self, mock_stdout, mock_input):
        """Test that the last real option len(options) is still accepted (upper in-range boundary)"""
        options = [f'Team {i}' for i in range(1, 11)]
        last_option = len(options)
        mock_input.side_effect = [str(last_option)]

        result = show_list_selection('TEAM SELECTION', options, 'Cancel')

        assert result == last_option
        assert mock_input.call_count == 1
        output = mock_stdout.getvalue()
        assert 'Invalid choice. Please try again.' not in output


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


