"""Test cases for the utils module.
This module contains unit tests for the utility functions used in the application.
It uses unittest framework and mocks external dependencies."""
# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import utils

class TestUtils(unittest.TestCase):
    """Test cases for the utils module."""

    @patch('utils.logger')
    def test_count_files_by_pattern(self, mock_logger):
        with patch('os.scandir') as mock_scandir:
            mock_entry = MagicMock()
            mock_entry.is_file.return_value = True
            mock_entry.name = 'test.fb2'
            mock_scandir.return_value.__enter__.return_value = [mock_entry]
            count = utils.count_files_by_pattern('/fake', '*.*')
            self.assertEqual(count, 1)
        with patch('os.scandir', side_effect=OSError('fail')):
            count = utils.count_files_by_pattern('/fake', '*.*')
            self.assertEqual(count, 0)

if __name__ == '__main__':
    unittest.main()
