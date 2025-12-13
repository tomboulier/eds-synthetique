"""Module définissant l'entité Passage du domaine."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TypePassage(Enum):
    """Type de passage dans le SIH."""

    URGENCES = "urgences"
    CONSULTATION = "consultation"
    HOSPITALISATION = "hospitalisation"
    AMBULATOIRE = "ambulatoire"


@dataclass(frozen=True)
class Passage:
    """
    Entité Passage dans le SIH.

    Représente une interaction ponctuelle d'un patient avec l'hôpital.
    C'est par les passages qu'un patient existe dans le SIH.

    Parameters
    ----------
    identifiant : str
        Identifiant unique du passage
    patient_id : str
        Référence à l'identifiant du patient
    date_heure_debut : datetime
        Date et heure de début du passage
    date_heure_fin : datetime | None
        Date et heure de fin du passage (None si passage en cours)
    type_passage : TypePassage
        Type de passage (urgences, consultation, etc.)
    """

    identifiant: str
    patient_id: str
    date_heure_debut: datetime
    date_heure_fin: datetime | None
    type_passage: TypePassage
