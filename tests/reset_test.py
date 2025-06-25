"""Unit tests for the reset module."""
# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import reset

class TestReset(unittest.TestCase):
    """Test cases for the reset module."""
    @patch('reset.logger')
    def test_reset_last_command(self, mock_logger):
        context = MagicMock()
        context.user_data = {
            'search_results': 1,
            'current_page': 2,
            'search_message_id': 3,
            'selected_book': 4
        }
        result = reset.reset_last_command(context)
        self.assertNotIn('search_results', context.user_data)
        self.assertNotIn('current_page', context.user_data)
        self.assertNotIn('search_message_id', context.user_data)
        self.assertNotIn('selected_book', context.user_data)
        self.assertIsNotNone(result)

    @patch('reset.logger')
    def test_reset_search(self, mock_logger):
        context = MagicMock()
        context.user_data = {
            'search_type': 1,
            'search_query': 2,
            'other': 3
        }
        with patch('reset.reset_last_command', return_value=42) as _:
            result = reset.reset_search(context)
            self.assertNotIn('search_type', context.user_data)
            self.assertNotIn('search_query', context.user_data)
            self.assertEqual(result, 42)

if __name__ == '__main__':
    unittest.main()
