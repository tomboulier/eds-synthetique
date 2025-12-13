"""Module définissant l'entité Patient du domaine."""

import uuid
from dataclasses import dataclass
from datetime import date
from enum import Enum


@dataclass(frozen=True)
class IdentifiantPatient:
    """
    Value Object représentant l'identifiant unique d'un patient.

    L'identifiant est un UUID v4 garantissant l'unicité globale.

    Parameters
    ----------
    valeur : str
        Chaîne UUID au format standard (ex: '550e8400-e29b-41d4-a716-446655440000')

    Raises
    ------
    ValueError
        Si la valeur fournie n'est pas un UUID valide

    Examples
    --------
    >>> identifiant = IdentifiantPatient.generer()
    >>> isinstance(identifiant, IdentifiantPatient)
    True
    """

    valeur: str

    def __post_init__(self) -> None:
        """Valide que la valeur est un UUID valide."""
        try:
            uuid.UUID(self.valeur)
        except ValueError as e:
            raise ValueError(f"Identifiant patient invalide: {self.valeur}") from e

    @classmethod
    def generer(cls) -> "IdentifiantPatient":
        """
        Génère un nouvel identifiant patient unique.

        Returns
        -------
        IdentifiantPatient
            Un nouvel identifiant patient avec un UUID v4 unique
        """
        return cls(str(uuid.uuid4()))

    def __str__(self) -> str:
        """Retourne la représentation string de l'identifiant."""
        return self.valeur


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
