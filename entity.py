import re

# ═══════════════════════════════════════════════════════════
#  Multilingual Entity Extractor
#  Handles English, Hindi (romanised), Telugu (romanised), Spanish
# ═══════════════════════════════════════════════════════════

# Direction keywords per language
OPEN_WORDS  = [
    # English
    "open", "lower", "roll down", "down",
    # Hindi
    "kholo", "neeche", "neeche karo", "girayo",
    # Telugu
    "teruvu", "kindiki", "kindiki cheyyi",
    # Spanish
    "abre", "baja", "abajo",
]

CLOSE_WORDS = [
    # English
    "close", "raise", "roll up", "up",
    # Hindi
    "band karo", "upar", "upar karo", "uthao",
    # Telugu
    "muyyi", "paikki", "paikki cheyyi", "band cheyyi",
    # Spanish
    "cierra", "sube", "arriba",
]

# Location strip phrases per language
LOCATION_STRIP = [
    # English
    "navigate to", "take me to", "go to", "drive to", "directions to", "find",
    # Hindi
    "chalo", "le chalo", "le jao", "jao", "navigate karo",
    # Telugu
    "ki vellu", "ki teesuko", "vellu", "navigate cheyyi", "daari chupinchu",
    # Spanish
    "navega a", "llevame a", "llévame a", "ir a", "ir al", "ir a la",
    "como llego a", "navegara", "direcciones a",
]

# Contact strip phrases per language
CONTACT_STRIP = [
    # English
    "call my", "call", "dial", "phone",
    # Hindi
    "ko call karo", "ko phone karo", "call karo", "phone karo",
    "call lagao", "phone milao",
    # Telugu
    "ki call cheyyi", "ki phone cheyyi", "call cheyyi", "phone cheyyi", "dial cheyyi",
    # Spanish
    "llama a mi", "llama a", "llamar a", "telefona a", "marcar", "hacer una llamada",
]


def extract_entities(text):
    t = text.lower()

    # ── Temperature (digits work in all languages) ──────────
    temps = re.findall(r'\d+', t)

    # ── Direction ───────────────────────────────────────────
    direction = None
    for w in OPEN_WORDS:
        if w in t:
            direction = "down"
            break
    if direction is None:
        for w in CLOSE_WORDS:
            if w in t:
                direction = "up"
                break

    # ── Location ────────────────────────────────────────────
    location = t
    for phrase in sorted(LOCATION_STRIP, key=len, reverse=True):
        location = location.replace(phrase, "")
    location = location.strip()

    # ── Contact ─────────────────────────────────────────────
    contact = t
    for phrase in sorted(CONTACT_STRIP, key=len, reverse=True):
        contact = contact.replace(phrase, "")
    contact = contact.strip()

    return {
        "temperature": temps[0] if temps else None,
        "direction":   direction,
        "location":    location,
        "contact":     contact,
    }
