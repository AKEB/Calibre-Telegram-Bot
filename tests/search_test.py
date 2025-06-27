"""Unit tests for the search module."""
# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
import unittest
from unittest.mock import patch
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
# pylint: disable=C0413
# pylint: disable=E0401
import search

class TestSearch(unittest.TestCase):
    """Test cases for the search module."""
    @patch('search.logger')
    def test_get_file_size(self, mock_logger):
        self.assertEqual(search.get_file_size(500), '500B')
        self.assertEqual(search.get_file_size(2048), '2.00KB')
        self.assertEqual(search.get_file_size(2 * 1024 * 1024), '2.00MB')
        self.assertEqual(search.get_file_size(3 * 1024 * 1024 * 1024), '3.00GB')

    @patch('search.logger')
    def test_get_books_list_text(self, mock_logger):
        books = [
            {
                'title': 'Book1',
                'author': 'Author1',
                'languages': 'ru',
                'id': '1',
                'publisher': 'Pub',
                'size': 1024,
                'series': '',
                'series_index': '',
                'tags': ''
            },
            {
                'title': 'Book2',
                'author': 'Author2',
                'languages': '',
                'id': '',
                'publisher': '',
                'size': '',
                'series': 'Ser',
                'series_index': '1',
                'tags': 'tag'
            }
        ]
        text = search.get_books_list_text(books, 0, lang='ru')
        self.assertIn('Book1', text)
        self.assertIn('Book2', text)
        self.assertIn('Author1', text)
        self.assertIn('Author2', text)
        self.assertIn('ID: 1', text)
        self.assertIn('Pub', text)
        self.assertIn('Жанр: tag', text)

if __name__ == '__main__':
    unittest.main()
