"""
SPF — Smart Car AI  |  Multilingual Flask API  v2
==================================================
Manual language selection — user picks from UI dropdown.
Backend pipeline:
  1. Receive text + user-selected lang code
  2. Translate input → English
  3. NLP (intent + entities) — always English
  4. Build English response → translate back to selected lang

Run:   python api.py
Open:  http://localhost:5000
"""

import os
import re
import threading
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from preprocess import preprocess
from intent_model import predict_intent
from entity import extract_entities
from language import (
    translate_to_english,
    translate_from_english,
    build_response,
    SUPPORTED_LANGUAGES,
    SPEECH_RECOGNITION_LANGS,
    TTS_LANG_HINTS,
)
from action import execute
from context import context

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)

_lock  = threading.Lock()
_state = {
    "processing": False,
    "intent":     "",
    "entities":   {},
    "raw_voice":  "",
    "clean_text": "",
    "lang":       "en",
}


def _map_entities_for_dashboard(intent, entities, raw_english):
    """Map NLP entities to dashboard-ready format (English labels)."""
    out = {}

    if intent == "AC":
        out["temperature"] = int(entities["temperature"]) if entities.get("temperature") else 22

    elif intent == "WINDOW":
        d = entities.get("direction")
        out["direction"] = "Open" if d == "down" else "Close" if d == "up" else "Adjust"
        raw = raw_english.lower()
        if any(w in raw for w in ["driver", "left"]):
            out["position"] = "Driver"
        elif any(w in raw for w in ["passenger", "right"]):
            out["position"] = "Passenger"
        else:
            out["position"] = "All Windows"

    elif intent == "MEDIA":
        raw = raw_english.lower()
        out["action"] = "play" if "play" in raw else "stop"
        m = re.search(r'play (.+?) by (.+)', raw)
        if m:
            out["track"]  = m.group(1).strip().title()
            out["artist"] = m.group(2).strip().title()
        else:
            m2 = re.search(r'play (.+)', raw)
            out["track"]  = m2.group(1).strip().title() if m2 else "Your Music"
            out["artist"] = "SPF Radio"

    elif intent == "NAVIGATION":
        loc = entities.get("location", raw_english).strip()
        for v in ["navigate to", "take me to", "go to", "drive to", "directions to", "find"]:
            loc = loc.replace(v, "").strip()
        out["destination"] = loc.title() if loc else "Destination"
        out["eta"]         = "—"
        out["distance"]    = "—"

    elif intent == "CALL":
        contact = entities.get("contact", raw_english).strip()
        for v in ["call my", "call", "dial", "phone"]:
            contact = contact.replace(v, "").strip()
        out["contact"] = contact.title() if contact else "Contact"

    return out


# ══════════════════════════════════════════════════════════
@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/languages", methods=["GET"])
def languages():
    return jsonify({
        "languages":    SUPPORTED_LANGUAGES,
        "speech_langs": SPEECH_RECOGNITION_LANGS,
        "tts_hints":    TTS_LANG_HINTS,
    }), 200


@app.route("/process", methods=["POST"])
def process():
    """
    Body: { "text": "...", "lang": "<code>" }
    lang is the user-selected language code (e.g. "hi", "te", "es").
    Defaults to "en" if missing or unsupported.
    """
    body = request.get_json(silent=True) or {}
    raw  = (body.get("text") or "").strip()
    lang = (body.get("lang") or "en").strip()

    # Fallback for unsupported codes
    if lang not in SUPPORTED_LANGUAGES:
        print(f"[SPF] Unknown lang '{lang}', defaulting to 'en'")
        lang = "en"

    if not raw:
        return jsonify({"status": "error", "error": "No text received"}), 400

    with _lock:
        if _state["processing"]:
            return jsonify({"status": "busy"}), 409
        _state["processing"] = True

    try:
        # 1. Translate user input → English
        raw_lower    = raw.lower()
        english_text = translate_to_english(raw_lower, lang)

        # 2. NLP pipeline (always English)
        clean    = preprocess(english_text)
        intent   = predict_intent(clean)
        entities = extract_entities(clean)

        # 3. Map entities for dashboard
        dash_entities = _map_entities_for_dashboard(intent, entities, english_text)

        # 4. Build response + translate back to selected lang
        response_text = build_response(intent, dash_entities, lang, english_text)

        with _lock:
            _state.update({
                "raw_voice":  raw_lower,
                "clean_text": clean,
                "intent":     intent,
                "entities":   entities,
                "lang":       lang,
            })

        print(f"[SPF] lang={lang} intent={intent} en='{english_text}'")
        print(f"[SPF] response='{response_text}'")

        return jsonify({
            "status":   "ok",
            "intent":   intent,
            "heard":    raw,
            "entities": dash_entities,
            "lang":     lang,
            "response": response_text,
        }), 200

    except Exception as e:
        print(f"[SPF] Error: {e}")
        import traceback; traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500

    finally:
        with _lock:
            _state["processing"] = False


@app.route("/execute", methods=["POST"])
def execute_cmd():
    body = request.get_json(silent=True) or {}
    with _lock:
        intent   = body.get("intent")   or _state["intent"]
        entities = body.get("entities") or _state["entities"]
        text     = _state["clean_text"] or _state["raw_voice"]
        lang     = _state["lang"]

    if not intent:
        return jsonify({"success": False, "error": "No intent"}), 400

    try:
        execute(intent, _state["entities"], text)
    except Exception as e:
        print(f"[SPF] Execute warning (non-fatal): {e}")

    return jsonify({"success": True, "lang": lang}), 200


@app.route("/status", methods=["GET"])
def status():
    with _lock:
        return jsonify({
            "ok":         True,
            "processing": _state["processing"],
            "lang":       _state["lang"],
        }), 200


if __name__ == "__main__":
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    dash = os.path.join(TEMPLATE_DIR, "dashboard.html")
    if not os.path.exists(dash):
        print(f"\n  Missing: {dash}\n")
    print("=" * 60)
    print("  SPF Smart Car AI v2  →  http://localhost:5000")
    print(f"  Languages: {len(SUPPORTED_LANGUAGES)} supported (manual selection)")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
