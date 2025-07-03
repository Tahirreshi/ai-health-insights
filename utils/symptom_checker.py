from utils.symptom_knowledge import symptom_database

def match_symptoms(user_input):
    user_symptoms = set(sym.strip().lower() for sym in user_input.split(","))
    matches = []

    for entry in symptom_database:
        entry_symptoms = set(sym.lower() for sym in entry["symptoms"])
        if user_symptoms & entry_symptoms:
            matches.append({
                "symptoms": entry["symptoms"],
                "conditions": entry["conditions"]
            })

    return matches
