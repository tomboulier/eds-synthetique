"""Module de génération de données synthétiques pour le SIH."""

import random
from datetime import date, timedelta

from faker import Faker

from eds_synthetique.domaine.patient import IdentifiantPatient, Patient, Sexe


def generer_patient(seed: int | None = None) -> Patient:
    """
    Génère un patient synthétique aléatoire.

    Utilise Faker pour générer des noms et prénoms français cohérents.
    La date de naissance est générée pour un âge entre 0 et 100 ans.

    Parameters
    ----------
    seed : int | None, optional
        Seed pour la génération aléatoire (reproductibilité), by default None

    Returns
    -------
    Patient
        Un patient synthétique avec des données cohérentes

    Examples
    --------
    >>> patient = generer_patient(seed=42)
    >>> isinstance(patient, Patient)
    True
    >>> patient.nom
    'Delahaye'
    """
    fake = Faker("fr_FR")
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    # Générer le sexe aléatoirement
    sexe = random.choice([Sexe.MASCULIN, Sexe.FEMININ])

    # Générer nom et prénom cohérents avec le sexe
    prenom = (
        fake.first_name_male() if sexe == Sexe.MASCULIN else fake.first_name_female()
    )

    nom = fake.last_name()

    # Générer une date de naissance (âge entre 0 et 100 ans)
    aujourd_hui = date.today()
    age_jours = random.randint(0, 100 * 365)  # 0 à 100 ans en jours
    date_naissance = aujourd_hui - timedelta(days=age_jours)

    # Créer le patient
    return Patient(
        identifiant=IdentifiantPatient.generer(),
        nom=nom,
        prenom=prenom,
        date_naissance=date_naissance,
        sexe=sexe,
    )


def generer_patients(nombre: int, seed: int | None = None) -> list[Patient]:
    """
    Génère une liste de patients synthétiques.

    Parameters
    ----------
    nombre : int
        Nombre de patients à générer (doit être >= 0)
    seed : int | None, optional
        Seed pour la génération aléatoire (reproductibilité), by default None

    Returns
    -------
    list[Patient]
        Liste de patients synthétiques

    Raises
    ------
    ValueError
        Si le nombre est négatif

    Examples
    --------
    >>> patients = generer_patients(5, seed=42)
    >>> len(patients)
    5
    >>> all(isinstance(p, Patient) for p in patients)
    True
    """
    if nombre < 0:
        raise ValueError(f"Le nombre de patients doit être positif, reçu: {nombre}")

    if nombre == 0:
        return []

    # Initialiser la seed si fournie
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    # Générer les patients
    # Note: on ne passe pas la seed à generer_patient() car elle est déjà initialisée
    return [generer_patient() for _ in range(nombre)]
