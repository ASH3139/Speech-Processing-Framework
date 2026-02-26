context = {}

def update_context(intent, entities):
    context["last_intent"] = intent
    context["last_entities"] = entities
