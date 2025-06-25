# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
"""Test cases for the config module.
This module contains unit tests for the configuration settings and constants.
It uses unittest framework and mocks external dependencies."""
import sys
import os
import unittest
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import config

class TestConfigModule(unittest.TestCase):
    """Unit tests for the config module."""
    def test_constants_types_and_defaults(self):
        """Test the types and default values of configuration constants."""
        self.assertIsInstance(config.TELEGRAM_BOT_TOKEN, str)
        self.assertIsInstance(config.TELEGRAM_ADMIN_USERS, list)

        self.assertIsInstance(config.CALIBRE_DB, str)
        self.assertIsInstance(config.BOOKS_DIR, str)
        self.assertTrue(isinstance(config.BOOKS_IMPORT_DIR, str) or config.BOOKS_IMPORT_DIR is None)
        self.assertIsInstance(config.AUTHORIZED_USERS_FILE, str)

        self.assertIsInstance(config.CALIBRE_LIBRARY_URL, str)
        self.assertIsInstance(config.CALIBRE_LIBRARY_USER, str)
        self.assertIsInstance(config.CALIBRE_LIBRARY_PASS, str)
        self.assertTrue(isinstance(config.CALIBRE_WEB_URL, str) or config.CALIBRE_WEB_URL is None)

        self.assertIsInstance(config.RESULTS_PER_PAGE, int)
        self.assertIsInstance(config.RANDOM_BOOKS_COUNT, int)
        self.assertIsInstance(config.BOOKS_LIMIT_COUNT, int)
        self.assertIsInstance(config.MAX_UPLOAD_SIZE, int)

    @patch('config.logger')
    def test_print_config_logs(self, mock_logger):
        """Test that print_config logs the configuration settings."""
        config.print_config()
        # Проверяем, что logger.warning был вызван хотя бы один раз
        print('mock_logger.warning.call_args_list:', mock_logger.info.call_args_list)
        self.assertTrue(mock_logger.info.called)
        # Проверяем, что в логах есть ключевые переменные
        log_args = ' '.join(str(call) for call in mock_logger.info.call_args_list)
        self.assertIn('TELEGRAM_BOT_TOKEN', log_args)
        self.assertIn('CALIBRE_DB', log_args)
        self.assertIn('BOOKS_DIR', log_args)
        self.assertIn('TELEGRAM_ADMIN_USERS', log_args)

if __name__ == '__main__':
    unittest.main()
