from speech import speak
from context import update_context

def execute(intent, entities, text):

    if intent == "AC":
        if entities.get("temperature"):
            response = f"Temperature set to {entities['temperature']}"
        else:
            response = "Temperature adjusted"

    elif intent == "WINDOW":
        if entities.get("direction") == "down":
            response = "Window lowered"
        elif entities.get("direction") == "up":
            response = "Window raised"
        else:
            response = "Window adjusted"

    elif intent == "MEDIA":
        if "play" in text:
            response = "Playing music"
        else:
            response = "Media stopped"

    elif intent == "NAVIGATION":
        response = f"Navigating to {entities.get('location') or entities.get('destination') or 'destination'}"

    elif intent == "CALL":
        response = f"Calling {entities.get('contact') or 'contact'}"

    else:
        response = "Command not understood"

    speak(response)
    update_context(intent, entities)
