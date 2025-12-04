from enum import Enum


class MissionEnum(str, Enum):
    CONTACT = "contact"
    DONATION = "donation"
    VOLUNTEER = "volunteer"
    INFORMATION = "information"


MISSIONS = [
    {
        "id": MissionEnum.CONTACT,
        "label": "Établir le contact",
        "description": "Envoyer un message ou poser une question générale.",
    },
    {
        "id": MissionEnum.DONATION,
        "label": "Offrir un don",
        "description": "Soutenir l'association par un don financier.",
    },
    {
        "id": MissionEnum.VOLUNTEER,
        "label": "Rejoindre la guilde des bénévoles",
        "description": "Proposer son aide, ses compétences, son temps.",
    },
    {
        "id": MissionEnum.INFORMATION,
        "label": "Demander des informations",
        "description": "Obtenir des détails sur l'association, ses projets, etc.",
    },
]
