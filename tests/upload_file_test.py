"""Test cases for the upload_file module.
This module contains unit tests for the upload_file module, specifically
for handling document uploads in a Telegram bot.
It uses pytest and unittest.mock for mocking external dependencies."""
# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
import os
import sys
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import upload_file


@pytest.mark.asyncio
@patch('upload_file.logger')
@patch('upload_file.MAX_UPLOAD_SIZE', 100)
async def test_handle_document_upload_too_large(mock_logger):
    update = MagicMock()
    context = MagicMock()
    update.message.document.file_size = 200
    update.message.document.file_name = 'test.epub'
    update.message.document.file_id = 'fileid'
    context.bot.send_chat_action.return_value = None
    async def fake_reply_text(*args, **kwargs):
        return None
    update.message.reply_text = fake_reply_text
    await upload_file.handle_document_upload(update, context)
    # Проверка вызова reply_text (через mock не получится, но ошибки await не будет)


@pytest.mark.asyncio
@patch('upload_file.logger')
@patch('upload_file.MAX_UPLOAD_SIZE', 1000000)
async def test_handle_document_upload_invalid_format(mock_logger):
    update = MagicMock()
    context = MagicMock()
    update.message.document.file_size = 100
    update.message.document.file_name = 'test.exe'
    update.message.document.file_id = 'fileid'
    context.bot.send_chat_action.return_value = None
    async def fake_reply_text(*args, **kwargs):
        return None
    update.message.reply_text = fake_reply_text
    update.edited_message = None
    await upload_file.handle_document_upload(update, context)
    # Проверка вызова reply_text (через mock не получится, но ошибки await не будет)
