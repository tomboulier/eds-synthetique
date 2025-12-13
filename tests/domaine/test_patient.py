"""Tests pour l'entité Patient et le Value Object IdentifiantPatient."""

import uuid
from dataclasses import FrozenInstanceError

import pytest

from eds_synthetique.domaine.patient import IdentifiantPatient

# Tests pour IdentifiantPatient (Value Object)


def test_creer_identifiant_patient_valide() -> None:
    """Test de création d'un IdentifiantPatient avec un UUID valide."""
    uuid_valide = str(uuid.uuid4())
    identifiant = IdentifiantPatient(uuid_valide)

    assert identifiant.valeur == uuid_valide


def test_creer_identifiant_patient_genere_uuid() -> None:
    """Test de génération automatique d'un IdentifiantPatient."""
    identifiant = IdentifiantPatient.generer()

    # Vérifier que c'est un UUID valide
    assert uuid.UUID(identifiant.valeur)
    # Vérifier que deux générations donnent des UUIDs différents
    identifiant2 = IdentifiantPatient.generer()
    assert identifiant.valeur != identifiant2.valeur


def test_identifiant_patient_immutable() -> None:
    """Test de l'immutabilité du Value Object IdentifiantPatient."""
    identifiant = IdentifiantPatient.generer()

    with pytest.raises(FrozenInstanceError):
        identifiant.valeur = "nouveau-uuid"  # type: ignore[misc]


def test_identifiant_patient_egalite() -> None:
    """Test que deux IdentifiantPatient avec le même UUID sont égaux."""
    uuid_test = str(uuid.uuid4())
    identifiant1 = IdentifiantPatient(uuid_test)
    identifiant2 = IdentifiantPatient(uuid_test)

    assert identifiant1 == identifiant2


def test_identifiant_patient_format_invalide_leve_erreur() -> None:
    """Test qu'un format invalide lève une ValueError."""
    with pytest.raises(ValueError, match="Identifiant patient invalide"):
        IdentifiantPatient("pas-un-uuid")


def test_identifiant_patient_vers_str() -> None:
    """Test de conversion d'un IdentifiantPatient en string."""
    uuid_test = str(uuid.uuid4())
    identifiant = IdentifiantPatient(uuid_test)

    assert str(identifiant) == uuid_test


# Tests pour l'entité Patient (à implémenter après intégration des VOs)

# TODO: Ajouter les tests pour la création d'un patient avec IdentifiantPatient
# TODO: Ajouter les tests pour la validation des champs
# TODO: Ajouter les tests pour l'immutabilité (frozen dataclass)
