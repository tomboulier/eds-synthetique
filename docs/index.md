# EDS Synthétique

Bienvenue dans la documentation du projet **EDS Synthétique** !

## Qu'est-ce que c'est ?

EDS Synthétique est un générateur de **Système d'Information Hospitalier (SIH) synthétique** français, conçu pour :

- L'**expérimentation** avec des données de santé réalistes mais totalement synthétiques
- La **formation** aux systèmes d'information hospitaliers
- Le **développement** de prototypes et démonstrateurs
- La **recherche** en informatique médicale

## Caractéristiques principales

- ✅ **100% synthétique** - Aucune donnée réelle de patients
- ✅ **Terminologie française** - Vocabulaire SIH/PMSI français
- ✅ **Reproductible** - Génération via seeds pour des résultats constants
- ✅ **Traçable** - Métadonnées complètes pour chaque génération
- ✅ **Open Source** - License MIT

## Démarrage rapide

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/USERNAME/eds-synthetique.git
cd eds-synthetique

# Installer les dépendances
uv sync --extra dev
```

### Premier test

```bash
# Lancer les tests
uv run pytest

# Vérifier le code
uv run ruff check src/
```

## Documentation

- [Contexte métier](context.md) - Comprendre la philosophie et les objectifs du projet
- [Guide de développement](#) - Comment contribuer au projet (à venir)
- [API Reference](#) - Documentation des entités et modules (à venir)

## Principe fondamental

!!! quote "Principe directeur"
    **Un patient n'existe dans un SIH que par ses interactions avec l'hôpital.**

Ce principe guide toute la conception du projet : un patient seul n'a pas de sens dans un SIH. C'est la **trajectoire de soins** (les passages, séjours, actes, etc.) qui donne sens aux données.

## Entités de domaine

### Patient

Représente l'identité d'une personne suivie par l'hôpital.

- Identifiant unique
- Nom, prénom
- Date de naissance
- Sexe

### Passage

Représente une interaction ponctuelle avec le SIH.

- Identifiant unique
- Référence au patient
- Dates de début et fin
- Type (urgences, consultation, hospitalisation, ambulatoire)

## Roadmap

### Version 0.1 (actuelle)
- [x] Structure du projet
- [x] Entités Patient et Passage
- [x] Configuration des outils de développement
- [ ] Implémentation TDD complète
- [ ] Générateur de données

### Versions futures
- Ajout d'Observations et Actes
- Exports FHIR et OMOP
- Construction d'un EDS
- Interface web de démonstration

## Contribuer

Les contributions sont les bienvenues ! Consultez le [README](https://github.com/USERNAME/eds-synthetique) pour plus d'informations.

## License

Ce projet est sous license [MIT](https://opensource.org/licenses/MIT).
