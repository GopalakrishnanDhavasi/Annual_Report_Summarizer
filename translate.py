# translate.py
"""
Translation helpers for the Annual Report Summarizer
(Uses Deep Translator for Google Translate backend)
"""

from typing import Dict
from deep_translator import GoogleTranslator, exceptions as dt_exceptions

# Predefined language map
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Portuguese": "pt",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Arabic": "ar",
    "Hindi": "hi",
    "Bengali": "bn",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Dutch": "nl",
}


def _get_language_map() -> Dict[str, str]:
    """Return supported languages."""
    return LANGUAGES


def translate_text(text: str, dest: str) -> str:
    """Translate a text block using Deep Translator."""
    if not text:
        return ""

    try:
        translated = GoogleTranslator(source="auto", target=dest).translate(text)
        return translated if isinstance(translated, str) else str(translated)
    except dt_exceptions.NotValidPayload as e:
        raise RuntimeError(f"Invalid payload: {e}")
    except dt_exceptions.NotValidLength as e:
        raise RuntimeError(f"Text too long: {e}")
    except Exception as e:
        raise RuntimeError(f"Translation error: {e}")
