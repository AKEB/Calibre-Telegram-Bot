"""Unit tests for the handlers module."""
# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import main

class TestMain(unittest.TestCase):
    """Test cases for the main module."""
    @patch('main.logger')
    @patch('main.print_config')
    @patch('main.check_db_permissions', return_value=True)
    @patch('main.setup_handlers')
    @patch('main.Application')
    @patch('main.check_config', return_value=True)
    def test_main_success(self,
                          mock_check_config,
                          mock_app,
                          mock_setup,
                          mock_check_db_permissions,
                          mock_print_config,
                          mock_logger):
        mock_builder = MagicMock()
        mock_app.builder.return_value = mock_builder
        mock_builder.token.return_value = mock_builder
        mock_builder.build.return_value = mock_app
        mock_app.run_polling.return_value = None
        main.main()
        mock_print_config.assert_called()
        mock_setup.assert_called()
        mock_app.run_polling.assert_called()

    @patch('main.logger')
    @patch('main.print_config')
    @patch('main.check_db_permissions', return_value=False)
    @patch('main.check_config', return_value=True)
    def test_main_fail(self, mock_check_config, mock_check_db_permissions, mock_print_config, mock_logger):
        with self.assertRaises(SystemExit):
            main.main()
        mock_logger.critical.assert_called()

if __name__ == '__main__':
    unittest.main()
