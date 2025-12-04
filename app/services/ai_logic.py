import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.constants.missions import MissionEnum, MISSIONS
from app.constants.base_fields import BASE_FIELDS_BY_MISSION
from app.services.groq_service import groq_service


def classify_mission_from_prompt(prompt: str, language: str = "fr") -> Dict[str, Any]:
    """
    Utilise le LLM pour classifier le prompt utilisateur dans une des 4 missions fixes.
    Retourne un dict: { mission, confidence, reasoning }
    """

    mission_ids = [m["id"] for m in MISSIONS]

    system_prompt = f"""
Tu es un classificateur intelligent de formulaires pour une association.
Langue de travail: {language}.

Voici les missions possibles, tu DOIS choisir UNE SEULE parmi elles, exactement l'ID:

- "contact"      : l'utilisateur veut discuter, poser une question, prendre contact.
- "donation"     : l'utilisateur parle de donner de l'argent, soutenir financièrement.
- "volunteer"    : l'utilisateur veut aider, devenir bénévole, s'impliquer.
- "information"  : l'utilisateur veut obtenir des renseignements, détails, explications.

Réponds STRICTEMENT en JSON avec ce format:

{{
  "mission": "contact" | "donation" | "volunteer" | "information",
  "confidence": 0.0 - 1.0,
  "reasoning": "courte explication"
}}
"""

    user_prompt = f"Texte de l'utilisateur à analyser:\n\"{prompt}\""

    raw = groq_service.chat(
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=256,
    )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # fallback très simple
        data = {
            "mission": "contact",
            "confidence": 0.4,
            "reasoning": f"Impossible de parser la réponse LLM, réponse brute: {raw}",
        }

    mission = data.get("mission", "contact")
    if mission not in [m.value for m in MissionEnum]:
        mission = "contact"

    return {
        "mission": mission,
        "confidence": float(data.get("confidence", 0.5)),
        "reasoning": data.get("reasoning", ""),
    }


def generate_additional_fields(
    mission: MissionEnum,
    prompt: str,
    language: str = "fr",
) -> List[Dict[str, Any]]:
    """
    Génère des champs supplémentaires pertinents à partir du prompt utilisateur.
    Ne doit PAS regénérer les champs de base (général).
    """
    system_prompt = f"""
Tu es un générateur de champs de formulaire (JSON) pour enrichir un formulaire existant.

Langue de travail: {language}.
Mission: {mission.value}

Les champs de base sont déjà définis (nom, email, message de base, etc.),
tu dois proposer UNIQUEMENT des champs supplémentaires pertinents en fonction du contexte.

Respecte STRICTEMENT ce schéma JSON:
{{
  "fields": [
    {{
      "name": "identifiant_unique_snake_case",
      "label": "Texte affiché pour l'utilisateur (en {language})",
      "type": "text" | "email" | "textarea" | "number" | "select" | "checkbox",
      "required": true | false,
      "options": ["option1", "option2"] // uniquement pour type "select", sinon omettre
    }}
  ]
}}

Tu peux renvoyer une liste vide si aucun champ supplémentaire n'est pertinent.
NE RENVOIE RIEN EN DEHORS DU JSON.
"""

    user_prompt = f"""
Texte fourni par l'utilisateur pour cette mission ({mission.value}):

\"\"\"{prompt}\"\"\"
"""

    raw = groq_service.chat(
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.4,
        max_tokens=512,
    )

    try:
        data = json.loads(raw)
        fields = data.get("fields", [])
        if not isinstance(fields, list):
            fields = []
    except json.JSONDecodeError:
        fields = []

    # Petite validation minimale
    cleaned_fields = []
    for f in fields:
        name = f.get("name")
        label = f.get("label")
        field_type = f.get("type", "text")
        if not name or not label:
            continue

        cleaned = {
            "name": name,
            "label": label,
            "type": field_type,
            "required": bool(f.get("required", False)),
        }
        if field_type == "select" and isinstance(f.get("options"), list):
            cleaned["options"] = f["options"]

        cleaned_fields.append(cleaned)

    return cleaned_fields


def generate_confirmation_message(
    mission: MissionEnum,
    values: Dict[str, Any],
    username: Optional[str] = None,
    language: str = "fr",
) -> str:
    """
    Génère un message de confirmation stylé Nexus / Nuit de l'Info.
    Utilise l'année actuelle et le contexte de mission.
    """
    year = datetime.now().year
    username_display = username or values.get("name") or "Voyageur du Nexus"

    # On veut que ce soit roleplay + mention de l'année
    system_prompt = f"""
Tu es Axolotl, gardien du Nexus, et tu rédiges un message de confirmation
pour un utilisateur après avoir soumis un formulaire.

Langue: {language}
Thème: aventure, jeu vidéo, sci-fi, "Nexus", "quêtes", "Nuit de l'Info 2025".
Tu dois:
- Mentionner le pseudo / nom de l'utilisateur.
- Mentionner la mission parmi: contact, donation, volunteer, information.
- Mentionner l'année actuelle: {year}.
- Expliquer en 1-2 phrases l'impact de son action.
- Inviter à suivre l'évolution du projet pendant l'année {year}.
- Rester court (3-5 phrases max).
"""

    user_prompt = f"""
Nom ou pseudo utilisateur: {username_display}
Mission: {mission.value}
Valeurs du formulaire (JSON, pour contexte):

{json.dumps(values, ensure_ascii=False, indent=2)}
"""

    content = groq_service.chat(
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.7,
        max_tokens=300,
    )

    return content
