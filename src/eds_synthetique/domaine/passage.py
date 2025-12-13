"""Module définissant l'entité Passage du domaine."""

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


@dataclass(frozen=True)
class IdentifiantPassage:
    """
    Value Object représentant l'identifiant unique d'un passage.

    L'identifiant est un UUID v4 garantissant l'unicité globale.

    Parameters
    ----------
    valeur : str
        Chaîne UUID au format standard

    Raises
    ------
    ValueError
        Si la valeur fournie n'est pas un UUID valide
    """

    valeur: str

    def __post_init__(self) -> None:
        """Valide que la valeur est un UUID valide."""
        try:
            uuid.UUID(self.valeur)
        except ValueError as e:
            raise ValueError(f"Identifiant passage invalide: {self.valeur}") from e

    @classmethod
    def generer(cls) -> "IdentifiantPassage":
        """
        Génère un nouvel identifiant passage unique.

        Returns
        -------
        IdentifiantPassage
            Un nouvel identifiant passage avec un UUID v4 unique
        """
        return cls(str(uuid.uuid4()))

    def __str__(self) -> str:
        """Retourne la représentation string de l'identifiant."""
        return self.valeur


@dataclass(frozen=True)
class Periode:
    """
    Value Object représentant une période temporelle avec début et fin.

    Une période peut être en cours (fin = None) ou terminée (fin définie).
    La validation garantit que la date de début ne peut pas être postérieure
    à la date de fin. Les périodes instantanées (début == fin) sont autorisées
    pour gérer les passages éclair.

    Parameters
    ----------
    debut : datetime
        Date et heure de début de la période
    fin : datetime | None
        Date et heure de fin de la période (None si période en cours)

    Raises
    ------
    ValueError
        Si la date de début est postérieure à la date de fin

    Examples
    --------
    >>> from datetime import datetime
    >>> debut = datetime(2025, 1, 1, 10, 0, 0)
    >>> fin = datetime(2025, 1, 1, 12, 0, 0)
    >>> periode = Periode(debut=debut, fin=fin)
    >>> periode.duree()
    datetime.timedelta(seconds=7200)
    """

    debut: datetime
    fin: datetime | None

    def __post_init__(self) -> None:
        """Valide que début <= fin (si fin est définie)."""
        # Note : on autorise début == fin pour les passages éclair
        if self.fin is not None and self.debut > self.fin:
            raise ValueError(
                f"La date de début ({self.debut}) ne peut pas être postérieure "
                f"à la date de fin ({self.fin})"
            )

    def duree(self) -> timedelta | None:
        """
        Calcule la durée de la période.

        Returns
        -------
        timedelta | None
            La durée de la période, ou None si la période est en cours
        """
        if self.fin is None:
            return None
        return self.fin - self.debut

    def est_en_cours(self) -> bool:
        """
        Indique si la période est encore en cours.

        Returns
        -------
        bool
            True si la période n'a pas de date de fin, False sinon
        """
        return self.fin is None


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
