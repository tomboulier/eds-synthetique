"""Tests pour le générateur de données synthétiques."""

from datetime import date

import pytest

from eds_synthetique.domaine.patient import IdentifiantPatient, Patient, Sexe

# Tests pour la génération de patients


def test_generer_un_patient_retourne_un_patient_valide() -> None:
    """Test que generer_patient() retourne un Patient valide."""
    from eds_synthetique.generation.generateur import generer_patient

    patient = generer_patient()

    assert isinstance(patient, Patient)
    assert isinstance(patient.identifiant, IdentifiantPatient)
    assert isinstance(patient.nom, str)
    assert len(patient.nom) > 0
    assert isinstance(patient.prenom, str)
    assert len(patient.prenom) > 0
    assert isinstance(patient.date_naissance, date)
    assert isinstance(patient.sexe, Sexe)


def test_generer_patient_avec_seed_est_reproductible() -> None:
    """Test que la génération avec seed produit le même patient."""
    from eds_synthetique.generation.generateur import generer_patient

    patient1 = generer_patient(seed=42)
    patient2 = generer_patient(seed=42)

    assert patient1.nom == patient2.nom
    assert patient1.prenom == patient2.prenom
    assert patient1.date_naissance == patient2.date_naissance
    assert patient1.sexe == patient2.sexe
    # Note: les identifiants seront différents car générés à chaque fois


def test_generer_patient_sans_seed_produit_patients_differents() -> None:
    """Test que sans seed, les patients générés sont différents."""
    from eds_synthetique.generation.generateur import generer_patient

    patients = [generer_patient() for _ in range(10)]

    # Au moins un patient doit être différent des autres
    noms = [p.nom for p in patients]
    assert len(set(noms)) > 1, "Tous les patients ont le même nom"


def test_generer_patient_date_naissance_coherente() -> None:
    """Test que la date de naissance est dans le passé et réaliste."""
    from eds_synthetique.generation.generateur import generer_patient

    patient = generer_patient()
    aujourd_hui = date.today()

    assert patient.date_naissance < aujourd_hui
    # Vérifier que l'âge est raisonnable (entre 0 et 120 ans)
    age_approx = aujourd_hui.year - patient.date_naissance.year
    assert 0 <= age_approx <= 120


def test_generer_patients_retourne_liste_de_patients() -> None:
    """Test que generer_patients() retourne le bon nombre de patients."""
    from eds_synthetique.generation.generateur import generer_patients

    nombre = 5
    patients = generer_patients(nombre=nombre)

    assert isinstance(patients, list)
    assert len(patients) == nombre
    assert all(isinstance(p, Patient) for p in patients)


def test_generer_patients_avec_seed_est_reproductible() -> None:
    """Test que la génération de plusieurs patients avec seed est reproductible."""
    from eds_synthetique.generation.generateur import generer_patients

    patients1 = generer_patients(nombre=3, seed=42)
    patients2 = generer_patients(nombre=3, seed=42)

    for p1, p2 in zip(patients1, patients2, strict=True):
        assert p1.nom == p2.nom
        assert p1.prenom == p2.prenom
        assert p1.date_naissance == p2.date_naissance
        assert p1.sexe == p2.sexe


def test_generer_patients_nombre_zero_retourne_liste_vide() -> None:
    """Test que generer_patients(0) retourne une liste vide."""
    from eds_synthetique.generation.generateur import generer_patients

    patients = generer_patients(nombre=0)

    assert patients == []


def test_generer_patients_nombre_negatif_leve_erreur() -> None:
    """Test qu'un nombre négatif lève une ValueError."""
    from eds_synthetique.generation.generateur import generer_patients

    with pytest.raises(ValueError, match="doit être positif"):
        generer_patients(nombre=-1)


# TODO: Ajouter les tests pour la génération de passages (après implémentation patients)
# TODO: Ajouter les tests pour les métadonnées de génération
# TODO: Ajouter les tests pour la cohérence temporelle
