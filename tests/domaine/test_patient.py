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


# Tests pour l'entité Patient


def test_creer_patient_valide() -> None:
    """Test de création d'un Patient avec tous les champs valides."""
    from datetime import date

    from eds_synthetique.domaine.patient import Patient, Sexe

    identifiant = IdentifiantPatient.generer()
    patient = Patient(
        identifiant=identifiant,
        nom="Dupont",
        prenom="Jean",
        date_naissance=date(1980, 5, 15),
        sexe=Sexe.MASCULIN,
    )

    assert patient.identifiant == identifiant
    assert patient.nom == "Dupont"
    assert patient.prenom == "Jean"
    assert patient.date_naissance == date(1980, 5, 15)
    assert patient.sexe == Sexe.MASCULIN


def test_patient_immutable() -> None:
    """Test de l'immutabilité de l'entité Patient."""
    from datetime import date

    from eds_synthetique.domaine.patient import Patient, Sexe

    patient = Patient(
        identifiant=IdentifiantPatient.generer(),
        nom="Dupont",
        prenom="Jean",
        date_naissance=date(1980, 5, 15),
        sexe=Sexe.MASCULIN,
    )

    with pytest.raises(FrozenInstanceError):
        patient.nom = "Martin"  # type: ignore[misc]


def test_patient_egalite() -> None:
    """Test que deux patients avec le même identifiant sont égaux."""
    from datetime import date

    from eds_synthetique.domaine.patient import Patient, Sexe

    identifiant = IdentifiantPatient.generer()
    patient1 = Patient(
        identifiant=identifiant,
        nom="Dupont",
        prenom="Jean",
        date_naissance=date(1980, 5, 15),
        sexe=Sexe.MASCULIN,
    )
    patient2 = Patient(
        identifiant=identifiant,
        nom="Dupont",
        prenom="Jean",
        date_naissance=date(1980, 5, 15),
        sexe=Sexe.MASCULIN,
    )

    assert patient1 == patient2


def test_patient_sexe_valeurs() -> None:
    """Test que tous les sexes possibles fonctionnent."""
    from datetime import date

    from eds_synthetique.domaine.patient import Patient, Sexe

    for sexe in [Sexe.MASCULIN, Sexe.FEMININ, Sexe.INCONNU]:
        patient = Patient(
            identifiant=IdentifiantPatient.generer(),
            nom="Dupont",
            prenom="Jean",
            date_naissance=date(1980, 5, 15),
            sexe=sexe,
        )
        assert patient.sexe == sexe
