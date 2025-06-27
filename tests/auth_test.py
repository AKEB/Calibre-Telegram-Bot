# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
"""Test cases for the auth module.
This module contains unit tests for the authentication functionalities.
It uses unittest framework and mocks external dependencies."""
import unittest
from unittest.mock import patch, mock_open
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import auth

class TestAuth(unittest.TestCase):
    """Unit tests for the auth module."""
    @patch('auth.AUTHORIZED_USERS_FILE', 'test_users.txt')
    @patch('auth.logger')
    def test_load_authorized_users_file_exists(self, mock_logger):
        """Test loading authorized users from a file that exists."""
        m = mock_open(read_data='123\n456\n')
        with patch('builtins.open', m), patch('os.path.exists', return_value=True):
            a = auth.Auth()
            self.assertEqual(a.authorized_users, {'123': 'ru', '456': 'ru'})

    @patch('auth.AUTHORIZED_USERS_FILE', 'test_users.txt')
    @patch('auth.logger')
    def test_load_authorized_users_file_not_exists(self, mock_logger):
        """Test loading authorized users from a file that does not exist."""
        with patch('os.path.exists', return_value=False):
            a = auth.Auth()
            self.assertEqual(a.authorized_users, {})

    @patch('auth.logger')
    def test_is_authorized(self, mock_logger):
        """Test checking if a user is authorized."""
        a = auth.Auth()
        a.authorized_users = {'1': 'ru', '2': 'ru'}
        self.assertTrue(a.is_authorized('1'))
        self.assertFalse(a.is_authorized('3'))

    @patch('auth.TELEGRAM_ADMIN_USERS', ['10', '20'])
    @patch('auth.logger')
    def test_is_admin(self, mock_logger):
        """Test checking if a user is an admin."""
        a = auth.Auth()
        self.assertTrue(a.is_admin('10'))
        self.assertFalse(a.is_admin('30'))

    @patch('auth.AUTHORIZED_USERS_FILE', 'test_users.txt')
    @patch('auth.logger')
    def test_add_authorized_user_success(self, mock_logger):
        """Test adding an authorized user successfully."""
        a = auth.Auth()
        with patch('builtins.open', mock_open()) as m, \
             patch.object(
                 a, 'load_authorized_users',
                 return_value={'1': 'ru', '2': 'ru', '3': 'ru'}
            ):
            result = a.add_authorized_user('3')
            self.assertTrue(result)
            m().write.assert_called_with('3,ru\n')
            self.assertEqual(a.authorized_users, {'1': 'ru', '2': 'ru', '3': 'ru'})

    @patch('auth.AUTHORIZED_USERS_FILE', 'test_users.txt')
    @patch('auth.logger')
    def test_add_authorized_user_fail(self, mock_logger):
        """Test adding an authorized user that already exists."""
        a = auth.Auth()
        with patch('builtins.open', side_effect=OSError('fail')):
            result = a.add_authorized_user('4')
            self.assertFalse(result)
            mock_logger.error.assert_called()

if __name__ == '__main__':
    unittest.main()
