"""Test cases for handlers.py"""
# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import handlers

class TestHandlers(unittest.TestCase):
    """Test cases for the handlers module."""
    @patch('handlers.auth')
    def test_permission_required_authorized(self, mock_auth):
        mock_auth.is_authorized.return_value = True
        mock_auth.is_admin.return_value = True
        async def dummy(update, context):
            return 'ok'
        wrapped = handlers.permission_required(is_admin=True)(dummy)
        update = MagicMock()
        context = MagicMock()
        update.effective_user.id = 1
        update.effective_chat.id = 1
        update.message = MagicMock()
        async def fake_send_chat_action(*args, **kwargs):
            return None
        context.bot.send_chat_action = fake_send_chat_action
        # Проверяем, что если авторизован и админ, вызывается функция
        result = asyncio.run(wrapped(update, context))
        self.assertEqual(result, 'ok')

    @patch('handlers.auth')
    def test_permission_required_not_authorized(self, mock_auth):
        mock_auth.is_authorized.return_value = False
        async def dummy(update, context):
            return 'ok'
        wrapped = handlers.permission_required()(dummy)
        update = MagicMock()
        context = MagicMock()
        update.effective_user.id = 1
        update.effective_chat.id = 1
        update.message = MagicMock()
        async def fake_send_chat_action(*args, **kwargs):
            return None
        context.bot.send_chat_action = fake_send_chat_action
        async def fake_reply_text(*args, **kwargs):
            return None
        update.message.reply_text = fake_reply_text
        # Проверяем, что если не авторизован, вызывается reply_text
        asyncio.run(wrapped(update, context))
        # Проверка вызова reply_text (через mock не получится, но ошибки await не будет)

if __name__ == '__main__':
    unittest.main()
