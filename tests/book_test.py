# pylint: disable=C0116
# pylint: disable=W0613
# pylint: disable=C0413
# pylint: disable=E0401
"""Test cases for the book module.
This module contains unit tests for the book-related functionalities.
It uses unittest framework and mocks external dependencies."""
import os
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import book

class TestBookModule(unittest.TestCase):
    """Unit tests for the book module."""
    def setUp(self):
        self.book_data = {
            'id': '123',
            'title': 'Test Book',
            'author': 'Author Name',
            'series': 'Series Name',
            'series_index': '1',
            'publisher': 'Publisher Name',
            'text': 'Описание книги. ' * 50,
            'tags': 'fiction, adventure'
        }

    @patch('book.logger')
    def test_get_book_text_full(self, _mock_logger):
        """Test the get_book_text function with full book data."""
        text = book.get_book_text(self.book_data.copy(), user_id='123')
        self.assertIn('Test Book', text)
        self.assertIn('Author Name', text)
        self.assertIn('Series Name', text)
        self.assertIn('Publisher Name', text)
        self.assertIn('123', text)
        self.assertIn('fiction, adventure', text)
        self.assertIn('Описание', text)
        self.assertIn('✅ - доступен сразу', text)
        self.assertIn('🔄 - будет сконвертирован', text)

    @patch('book.logger')
    def test_get_book_text_missing_fields(self, _mock_logger):
        """Test the get_book_text function with missing fields."""
        book_data = {k: '' for k in self.book_data}
        book_data['title'] = 'No Fields'
        text = book.get_book_text(book_data, user_id='123')
        self.assertIn('No Fields', text)
        self.assertIn('✍️ Автор: ', text)
        self.assertIn('📖 Серия:  []', text)
        self.assertIn('Идентификатор: ', text)
        self.assertIn('Жанр: ', text)
        self.assertIn('Описание:', text)

    @patch('book.get_book_formats')
    @patch('book.logger')
    def test_book_selected_keyboard_and_text(self, _mock_logger, mock_get_formats):
        """Test the book_selected function with available formats."""
        mock_get_formats.return_value = ['epub', 'fb2']
        user_id = '123'
        reply_markup, text = book.book_selected(self.book_data.copy(), user_id)
        # Исправлено: выводим кнопки для отладки
        buttons = [btn for row in reply_markup.inline_keyboard for btn in row]
        button_texts = [btn.text for btn in buttons]
        from texts import get_text
        lang = 'ru'  # тестируем на русском
        self.assertTrue(any('EPUB' in t and '✅' in t for t in button_texts))
        self.assertTrue(any('FB2' in t and '✅' in t for t in button_texts))
        self.assertTrue(any('MOBI' in t and '🔄' in t for t in button_texts))
        self.assertTrue(any(get_text('btn_back', lang) in t for t in button_texts))
        self.assertTrue(any(get_text('btn_cancel', lang) in t for t in button_texts))
        self.assertIn('Test Book', text)

if __name__ == '__main__':
    unittest.main()
