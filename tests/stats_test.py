"""Unit tests for the search module."""
# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import stats

class TestStats(unittest.TestCase):
    """Test cases for the stats module."""
    @patch('stats.logger')
    @patch('stats.sqlite3.connect')
    def test_get_stats_success(self, mock_connect, mock_logger):
        # Мокаем курсор и возвращаемые значения
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [
            (10,),  # books
            (5,),   # authors
            (2,),   # series
            (3,),   # categories
        ]
        mock_cursor.fetchall.side_effect = [
            [('ru', 7), ('en', 3)],  # languages
            [('EPUB', 8), ('FB2', 2)]  # formats
        ]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = stats.get_stats()
        self.assertEqual(result['books'], 10)
        self.assertEqual(result['authors'], 5)
        self.assertEqual(result['series'], 2)
        self.assertEqual(result['categories'], 3)
        self.assertEqual(result['languages'], {'ru': 7, 'en': 3})
        self.assertEqual(result['formats'], {'EPUB': 8, 'FB2': 2})

    @patch('stats.logger')
    @patch('stats.sqlite3.connect', side_effect=sqlite3.Error('db error'))
    def test_get_stats_db_error(self, mock_connect, mock_logger):
        result = stats.get_stats()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['books'], 0)
        mock_logger.error.assert_called()

    @patch('stats.logger')
    @patch('stats.sqlite3.connect', side_effect=OSError('fs error'))
    def test_get_stats_os_error(self, mock_connect, mock_logger):
        result = stats.get_stats()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['books'], 0)
        mock_logger.error.assert_called()

    @patch('stats.logger')
    @patch('stats.get_stats')
    @patch('stats.count_files_by_pattern', return_value=5)
    @patch('stats.BOOKS_IMPORT_DIR', '/tmp/books_import')
    def test_get_stats_message_success(self,
                                       mock_count,
                                       mock_get_stats,
                                       mock_logger):
        mock_get_stats.return_value = {
            'books': 10,
            'authors': 2,
            'series': 1,
            'categories': 3,
            'languages': {'ru': 7},
            'formats': {'EPUB': 8}
        }
        result = stats.get_stats_message()
        self.assertIn('Книг: 10', result)
        self.assertIn('Авторов: 2', result)
        self.assertIn('Категорий: 3', result)
        self.assertIn('Серий: 1', result)
        self.assertIn('Языков: 1', result)
        self.assertIn('- ru: 7', result)
        self.assertIn('Форматов: 1', result)
        self.assertIn('- EPUB: 8', result)
        self.assertIn('в очереди: 5', result)
        self.assertIn('ошибок: 5', result)

    @patch('stats.logger')
    @patch('stats.get_stats', return_value=None)
    def test_get_stats_message_none(self, mock_get_stats, mock_logger):
        result = stats.get_stats_message()
        self.assertIsNone(result)
        mock_logger.error.assert_called()

    @patch('stats.logger')
    @patch('stats.get_stats', side_effect=sqlite3.Error('db error'))
    def test_get_stats_message_exception(self, mock_get_stats, mock_logger):
        result = stats.get_stats_message()
        self.assertIsNone(result)
        mock_logger.error.assert_called()

if __name__ == '__main__':
    unittest.main()
