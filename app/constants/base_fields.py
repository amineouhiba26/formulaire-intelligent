from app.constants.missions import MissionEnum


# Schéma simple pour les champs
# type: "text" | "email" | "textarea" | "number" | "select" | "checkbox"
BASE_FIELDS_BY_MISSION = {
    MissionEnum.CONTACT: [
        {
            "name": "name",
            "label": "Nom complet",
            "type": "text",
            "required": True,
        },
        {
            "name": "email",
            "label": "Adresse e-mail",
            "type": "email",
            "required": True,
        },
        {
            "name": "message",
            "label": "Votre message",
            "type": "textarea",
            "required": True,
        },
    ],
    MissionEnum.DONATION: [
        {
            "name": "name",
            "label": "Nom complet",
            "type": "text",
            "required": True,
        },
        {
            "name": "email",
            "label": "Adresse e-mail",
            "type": "email",
            "required": True,
        },
        {
            "name": "amount",
            "label": "Montant du don (€)",
            "type": "number",
            "required": True,
        },
        {
            "name": "recurrence",
            "label": "Récurrence du don",
            "type": "select",
            "required": True,
            "options": ["Unique", "Mensuel", "Annuel"],
        },
    ],
    MissionEnum.VOLUNTEER: [
        {
            "name": "name",
            "label": "Nom complet",
            "type": "text",
            "required": True,
        },
        {
            "name": "email",
            "label": "Adresse e-mail",
            "type": "email",
            "required": True,
        },
        {
            "name": "skills",
            "label": "Compétences / Domaines dans lesquels vous pouvez aider",
            "type": "textarea",
            "required": True,
        },
        {
            "name": "availability",
            "label": "Disponibilités",
            "type": "text",
            "required": False,
        },
    ],
    MissionEnum.INFORMATION: [
        {
            "name": "name",
            "label": "Nom complet",
            "type": "text",
            "required": False,
        },
        {
            "name": "email",
            "label": "Adresse e-mail",
            "type": "email",
            "required": True,
        },
        {
            "name": "topic",
            "label": "Sujet de la demande",
            "type": "text",
            "required": True,
        },
        {
            "name": "message",
            "label": "Détail de votre demande",
            "type": "textarea",
            "required": False,
        },
    ],
}
