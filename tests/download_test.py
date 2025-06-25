# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
"""Unit tests for the download module.
This module contains unit tests for the download functionality,
including book path retrieval, format checking, and conversion.
It uses unittest framework and mocks external dependencies."""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import download

class TestDownload(unittest.TestCase):
    """Test cases for the download module."""
    @patch('download.logger')
    @patch('download.CALIBRE_DB', 'fake.db')
    @patch('download.BOOKS_DIR', '/tmp/books')
    def test_get_book_path(self, mock_logger):
        with patch('sqlite3.connect') as mock_connect, \
             patch('os.path.exists', return_value=True):
            mock_conn = MagicMock()
            mock_connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = ['folder', 'bookname', 'fb2']
            mock_conn.close.return_value = None
            path = download.get_book_path(1, 'epub')
            self.assertTrue(path)

    @patch('download.logger')
    @patch('download.CALIBRE_DB', 'fake.db')
    def test_get_book_formats(self, mock_logger):
        with patch('sqlite3.connect') as mock_connect:
            mock_conn = MagicMock()
            mock_connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [('epub',), ('fb2',)]
            mock_conn.close.return_value = None
            formats = download.get_book_formats(1)
            self.assertIn('epub', formats)
            self.assertIn('fb2', formats)

    @patch('download.logger')
    def test_convert_book_none(self, mock_logger):
        self.assertIsNone(download.convert_book(None, 'fb2'))

if __name__ == '__main__':
    unittest.main()
