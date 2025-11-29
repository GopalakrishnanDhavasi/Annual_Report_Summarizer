"""
Audio generation module using Google Text-to-Speech (gTTS)
Generates MP3 audio files from given text and language code.
"""

import os
from gtts import gTTS
import tempfile


def generate_audio_from_text(text: str, lang: str = "en") -> str:
    """
    Generate an audio file from text using gTTS and return file path.

    Args:
        text (str): The text to convert to speech.
        lang (str): Language code for voice (default "en").

    Returns:
        str: Path to the generated audio file (MP3).
    """
    if not text.strip():
        raise ValueError("Text is empty. Cannot generate audio.")

    try:
        # Create a temporary file
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"summary_audio_{lang}.mp3")

        # Generate TTS audio
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)

        return output_path
    except Exception as e:
        raise RuntimeError(f"Audio generation failed: {e}")
