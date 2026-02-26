"""
SPF Language Module — Manual Selection + Translation
=====================================================
• The user picks the language manually from the UI dropdown.
• Input text (non-English) is translated TO English before NLP.
• The English response is translated BACK to the user's language.

Translation powered by `deep-translator` (Google Translate).
Install:  pip install deep-translator
"""

from deep_translator import GoogleTranslator

# ── Supported languages ───────────────────────────────────────
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "ar": "Arabic",
    "zh-CN": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
}

# BCP-47 codes for Web Speech API — used by dashboard
SPEECH_RECOGNITION_LANGS = [
    {"code": "en-US", "label": "English",    "lang": "en"},
    {"code": "hi-IN", "label": "Hindi",      "lang": "hi"},
    {"code": "te-IN", "label": "Telugu",     "lang": "te"},
    {"code": "ta-IN", "label": "Tamil",      "lang": "ta"},
    {"code": "es-ES", "label": "Spanish",    "lang": "es"},
    {"code": "fr-FR", "label": "French",     "lang": "fr"},
    {"code": "de-DE", "label": "German",     "lang": "de"},
    {"code": "ko-KR", "label": "Korean",     "lang": "ko"},
    {"code": "ja-JP", "label": "Japanese",   "lang": "ja"},
    {"code": "pt-BR", "label": "Portuguese", "lang": "pt"},
    {"code": "kn-IN", "label": "Kannada",    "lang": "kn"},
    {"code": "ml-IN", "label": "Malayalam",  "lang": "ml"},
    {"code": "bn-IN", "label": "Bengali",    "lang": "bn"},
]

# ── Translation helpers ───────────────────────────────────────

def translate_to_english(text: str, source_lang: str) -> str:
    """Translate user input → English for NLP processing."""
    if not text or source_lang == "en":
        return text
    try:
        translated = GoogleTranslator(source=source_lang, target="en").translate(text)
        print(f"[SPF] → EN: '{text}' ⟶ '{translated}'")
        return translated or text
    except Exception as e:
        print(f"[SPF] translate_to_english failed ({e}) — using original")
        return text


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate English response → user's selected language."""
    if not text or target_lang == "en":
        return text
    try:
        translated = GoogleTranslator(source="en", target=target_lang).translate(text)
        print(f"[SPF] → {target_lang}: '{text}' ⟶ '{translated}'")
        return translated or text
    except Exception as e:
        print(f"[SPF] translate_from_english failed ({e}) — returning English")
        return text


# ── English response builder ─────────────────────────────────

def build_response(intent: str, entities: dict, lang: str, raw: str) -> str:
    """Build English response then translate to the user's selected language."""
    english = _build_english_response(intent, entities)
    return translate_from_english(english, lang)


def _build_english_response(intent: str, entities: dict) -> str:
    if intent == "AC":
        t = entities.get("temperature")
        return f"Temperature set to {t} degrees Celsius. Climate control is adjusting." if t else \
               "Temperature adjusted. Climate control is adjusting."

    if intent == "WINDOW":
        d   = entities.get("direction")
        pos = entities.get("position", "")
        label = pos + " " if pos else ""
        if d == "down": return f"Opening the {label}window smoothly."
        if d == "up":   return f"Closing the {label}window."
        return f"Adjusting the {label}window."

    if intent == "MEDIA":
        track  = entities.get("track",  "your music")
        artist = entities.get("artist", "the artist")
        return f'Now playing {track} by {artist}. Enjoy the ride.' \
               if entities.get("action") == "play" else "Music stopped."

    if intent == "NAVIGATION":
        dest = entities.get("destination") or entities.get("location") or "your destination"
        return f"Starting navigation to {dest}."

    if intent == "CALL":
        contact = entities.get("contact") or "your contact"
        return f"Calling {contact} now. Connecting."

    return "Command received and executed."


# ── TTS language hint ────────────────────────────────────────
TTS_LANG_HINTS = {
    "en": "en-US", "hi": "hi-IN", "te": "te-IN", "ta": "ta-IN",
    "es": "es-ES", "fr": "fr-FR", "de": "de-DE", "pt": "pt-BR",
    "ar": "ar-SA", "zh-CN": "zh-CN", "ja": "ja-JP", "ko": "ko-KR",
    "ru": "ru-RU", "kn": "kn-IN", "ml": "ml-IN", "bn": "bn-IN",
}
