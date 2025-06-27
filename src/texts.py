"""Module for handling internationalization (i18n) texts.
This module provides functions to load and retrieve localized text strings
from YAML files based on the selected language.
It supports variable substitution in the text strings."""
# pylint: disable=W0718
import os
import yaml

I18N_PATH = os.path.join(os.path.dirname(__file__), 'i18n')
_LANG_CACHE = {}

def _load_lang(lang):
    if lang not in _LANG_CACHE:
        with open(os.path.join(I18N_PATH, f'{lang}.yaml'), encoding='utf-8') as f:
            _LANG_CACHE[lang] = yaml.safe_load(f)
    return _LANG_CACHE[lang]

def get_text(section, lang, **kwargs):
    """Получить текст для секции и языка, с подстановкой переменных"""
    try:
        txt = _load_lang(lang).get(section)
        if not txt:
            txt = _load_lang('ru').get(section, '')
        return txt.format(**kwargs) if txt else ''
    except Exception:
        return ''
