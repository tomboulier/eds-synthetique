"""Tests pour l'entité Passage et les Value Objects associés."""

import uuid
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from eds_synthetique.domaine.passage import IdentifiantPassage, Periode

# Tests pour IdentifiantPassage (Value Object)


def test_creer_identifiant_passage_valide() -> None:
    """Test de création d'un IdentifiantPassage avec un UUID valide."""
    uuid_valide = str(uuid.uuid4())
    identifiant = IdentifiantPassage(uuid_valide)

    assert identifiant.valeur == uuid_valide


def test_creer_identifiant_passage_genere_uuid() -> None:
    """Test de génération automatique d'un IdentifiantPassage."""
    identifiant = IdentifiantPassage.generer()

    # Vérifier que c'est un UUID valide
    assert uuid.UUID(identifiant.valeur)
    # Vérifier que deux générations donnent des UUIDs différents
    identifiant2 = IdentifiantPassage.generer()
    assert identifiant.valeur != identifiant2.valeur


def test_identifiant_passage_immutable() -> None:
    """Test de l'immutabilité du Value Object IdentifiantPassage."""
    identifiant = IdentifiantPassage.generer()

    with pytest.raises(FrozenInstanceError):
        identifiant.valeur = "nouveau-uuid"  # type: ignore[misc]


def test_identifiant_passage_egalite() -> None:
    """Test que deux IdentifiantPassage avec le même UUID sont égaux."""
    uuid_test = str(uuid.uuid4())
    identifiant1 = IdentifiantPassage(uuid_test)
    identifiant2 = IdentifiantPassage(uuid_test)

    assert identifiant1 == identifiant2


def test_identifiant_passage_format_invalide_leve_erreur() -> None:
    """Test qu'un format invalide lève une ValueError."""
    with pytest.raises(ValueError, match="Identifiant passage invalide"):
        IdentifiantPassage("pas-un-uuid")


def test_identifiant_passage_vers_str() -> None:
    """Test de conversion d'un IdentifiantPassage en string."""
    uuid_test = str(uuid.uuid4())
    identifiant = IdentifiantPassage(uuid_test)

    assert str(identifiant) == uuid_test


# Tests pour Periode (Value Object)


def test_creer_periode_valide() -> None:
    """Test de création d'une Periode avec début < fin."""
    debut = datetime(2025, 1, 1, 10, 0, 0)
    fin = datetime(2025, 1, 1, 12, 0, 0)
    periode = Periode(debut=debut, fin=fin)

    assert periode.debut == debut
    assert periode.fin == fin


def test_creer_periode_debut_egal_fin() -> None:
    """Test qu'on autorise début == fin (passages éclair)."""
    moment = datetime(2025, 1, 1, 10, 0, 0)
    periode = Periode(debut=moment, fin=moment)

    assert periode.debut == moment
    assert periode.fin == moment
    assert periode.duree() == timedelta(0)


def test_creer_periode_en_cours() -> None:
    """Test de création d'une Periode en cours (fin = None)."""
    debut = datetime(2025, 1, 1, 10, 0, 0)
    periode = Periode(debut=debut, fin=None)

    assert periode.debut == debut
    assert periode.fin is None


def test_periode_debut_apres_fin_leve_erreur() -> None:
    """Test qu'une période avec début > fin lève une ValueError."""
    debut = datetime(2025, 1, 1, 12, 0, 0)
    fin = datetime(2025, 1, 1, 10, 0, 0)

    with pytest.raises(ValueError, match="ne peut pas être postérieure"):
        Periode(debut=debut, fin=fin)


def test_periode_immutable() -> None:
    """Test de l'immutabilité du Value Object Periode."""
    periode = Periode(debut=datetime.now(), fin=None)

    with pytest.raises(FrozenInstanceError):
        periode.debut = datetime.now()  # type: ignore[misc]


def test_periode_duree() -> None:
    """Test du calcul de la durée d'une période."""
    debut = datetime(2025, 1, 1, 10, 0, 0)
    fin = datetime(2025, 1, 1, 12, 30, 0)
    periode = Periode(debut=debut, fin=fin)

    assert periode.duree() == timedelta(hours=2, minutes=30)


def test_periode_duree_en_cours_retourne_none() -> None:
    """Test que la durée d'une période en cours retourne None."""
    periode = Periode(debut=datetime.now(), fin=None)

    assert periode.duree() is None


def test_periode_est_en_cours_vrai() -> None:
    """Test qu'une période sans date de fin est en cours."""
    periode = Periode(debut=datetime.now(), fin=None)

    assert periode.est_en_cours() is True


def test_periode_est_en_cours_faux() -> None:
    """Test qu'une période avec date de fin n'est pas en cours."""
    debut = datetime(2025, 1, 1, 10, 0, 0)
    fin = datetime(2025, 1, 1, 12, 0, 0)
    periode = Periode(debut=debut, fin=fin)

    assert periode.est_en_cours() is False


def test_periode_egalite() -> None:
    """Test que deux Periode avec les mêmes dates sont égales."""
    debut = datetime(2025, 1, 1, 10, 0, 0)
    fin = datetime(2025, 1, 1, 12, 0, 0)
    periode1 = Periode(debut=debut, fin=fin)
    periode2 = Periode(debut=debut, fin=fin)

    assert periode1 == periode2


# Tests pour l'entité Passage


def test_creer_passage_valide() -> None:
    """Test de création d'un Passage avec tous les champs valides."""
    from eds_synthetique.domaine.passage import Passage, TypePassage
    from eds_synthetique.domaine.patient import IdentifiantPatient

    identifiant_passage = IdentifiantPassage.generer()
    identifiant_patient = IdentifiantPatient.generer()
    debut = datetime(2025, 1, 15, 10, 0, 0)
    fin = datetime(2025, 1, 15, 12, 0, 0)
    periode = Periode(debut=debut, fin=fin)

    passage = Passage(
        identifiant=identifiant_passage,
        patient_id=identifiant_patient,
        periode=periode,
        type_passage=TypePassage.URGENCES,
    )

    assert passage.identifiant == identifiant_passage
    assert passage.patient_id == identifiant_patient
    assert passage.periode == periode
    assert passage.type_passage == TypePassage.URGENCES


def test_creer_passage_en_cours() -> None:
    """Test de création d'un Passage en cours (période sans fin)."""
    from eds_synthetique.domaine.passage import Passage, TypePassage
    from eds_synthetique.domaine.patient import IdentifiantPatient

    identifiant_passage = IdentifiantPassage.generer()
    identifiant_patient = IdentifiantPatient.generer()
    debut = datetime(2025, 1, 15, 10, 0, 0)
    periode = Periode(debut=debut, fin=None)

    passage = Passage(
        identifiant=identifiant_passage,
        patient_id=identifiant_patient,
        periode=periode,
        type_passage=TypePassage.HOSPITALISATION,
    )

    assert passage.periode.est_en_cours() is True
    assert passage.periode.duree() is None


def test_passage_immutable() -> None:
    """Test de l'immutabilité de l'entité Passage."""
    from eds_synthetique.domaine.passage import Passage, TypePassage
    from eds_synthetique.domaine.patient import IdentifiantPatient

    passage = Passage(
        identifiant=IdentifiantPassage.generer(),
        patient_id=IdentifiantPatient.generer(),
        periode=Periode(debut=datetime.now(), fin=None),
        type_passage=TypePassage.URGENCES,
    )

    with pytest.raises(FrozenInstanceError):
        passage.type_passage = TypePassage.CONSULTATION  # type: ignore[misc]


def test_passage_egalite() -> None:
    """Test que deux passages avec le même identifiant sont égaux."""
    from eds_synthetique.domaine.passage import Passage, TypePassage
    from eds_synthetique.domaine.patient import IdentifiantPatient

    identifiant_passage = IdentifiantPassage.generer()
    identifiant_patient = IdentifiantPatient.generer()
    debut = datetime(2025, 1, 15, 10, 0, 0)
    fin = datetime(2025, 1, 15, 12, 0, 0)
    periode = Periode(debut=debut, fin=fin)

    passage1 = Passage(
        identifiant=identifiant_passage,
        patient_id=identifiant_patient,
        periode=periode,
        type_passage=TypePassage.URGENCES,
    )
    passage2 = Passage(
        identifiant=identifiant_passage,
        patient_id=identifiant_patient,
        periode=periode,
        type_passage=TypePassage.URGENCES,
    )

    assert passage1 == passage2


def test_passage_types_valeurs() -> None:
    """Test que tous les types de passage possibles fonctionnent."""
    from eds_synthetique.domaine.passage import Passage, TypePassage
    from eds_synthetique.domaine.patient import IdentifiantPatient

    identifiant_patient = IdentifiantPatient.generer()
    debut = datetime(2025, 1, 15, 10, 0, 0)
    fin = datetime(2025, 1, 15, 12, 0, 0)
    periode = Periode(debut=debut, fin=fin)

    for type_passage in [
        TypePassage.URGENCES,
        TypePassage.CONSULTATION,
        TypePassage.HOSPITALISATION,
        TypePassage.AMBULATOIRE,
    ]:
        passage = Passage(
            identifiant=IdentifiantPassage.generer(),
            patient_id=identifiant_patient,
            periode=periode,
            type_passage=type_passage,
        )
        assert passage.type_passage == type_passage
