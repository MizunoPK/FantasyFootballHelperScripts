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

# Imports work via conftest.py which adds league_helper/util to path
from util.user_input import show_list_selection


# ============================================================================
# SHOW_LIST_SELECTION TESTS
# ============================================================================

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

        assert result == 4  # len(options) + 1
        mock_input.assert_called_once()

    @patch('builtins.input', side_effect=['invalid', 'abc', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_then_valid_input(self, mock_stdout, mock_input):
        """Test that invalid input is retried until valid input given"""
        options = ['Option 1', 'Option 2']
        result = show_list_selection('Test Menu', options, 'Quit')

        assert result == 2
        assert mock_input.call_count == 3
        # Check error message was printed
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
        options = [f'Option {i}' for i in range(1, 11)]  # 10 options
        result = show_list_selection('Menu', options, 'Quit')

        assert result == 10

    @patch('builtins.input', side_effect=['0', '100', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_out_of_range_numbers_accepted(self, mock_stdout, mock_input):
        """Test that out-of-range numbers are still returned (no validation)"""
        # Note: The function doesn't validate range, just that it's an integer
        options = ['Option 1']
        result = show_list_selection('Menu', options, 'Quit')

        # Function returns first valid integer, even if out of range
        assert result == 0

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


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
