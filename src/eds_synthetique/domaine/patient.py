"""Module définissant l'entité Patient du domaine."""

from dataclasses import dataclass
from datetime import date
from enum import Enum


class Sexe(Enum):
    """Sexe biologique du patient."""

    MASCULIN = "M"
    FEMININ = "F"
    INCONNU = "I"


@dataclass(frozen=True)
class Patient:
    """
    Entité Patient dans le SIH.

    Représente l'identité d'une personne suivie par l'hôpital.
    Un patient n'existe réellement dans le SIH que par ses passages.

    Parameters
    ----------
    identifiant : str
        Identifiant unique interne du patient
    nom : str
        Nom de famille du patient
    prenom : str
        Prénom du patient
    date_naissance : date
        Date de naissance du patient
    sexe : Sexe
        Sexe biologique du patient
    """

    identifiant: str
    nom: str
    prenom: str
    date_naissance: date
    sexe: Sexe
