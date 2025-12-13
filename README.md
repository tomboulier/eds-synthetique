# EDS Synthétique

[![CI](https://github.com/tomboulier/eds-synthetique/workflows/CI/badge.svg)](https://github.com/tomboulier/eds-synthetique/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Générateur de Système d'Information Hospitalier (SIH) synthétique français en vue d'être utilisé pour simuler un entrepôt de données de santé hospitalier(EDSH). Le but est de fournir un outil pour l'expérimentation et la formation.

## 📋 Contexte et objectifs

Ce projet vise à construire **un Système d'Information Hospitalier (SIH) synthétique minimal**, crédible et maîtrisé, destiné à servir de socle technique pour des démonstrations, expérimentations et futurs exports vers des formats standardisés (FHIR, OMOP, etc.).

### Principes directeurs

> **Un patient n'existe dans un SIH que par ses interactions avec l'hôpital.**

- **100% synthétique** : aucune donnée réelle
- **Terminologie française** : vocabulaire SIH/PMSI français
- **Simple et itératif** : approche minimale et progressive
- **Traçable et reproductible** : génération via seeds, métadonnées complètes
- **Domain-Driven Design (DDD)** : langage ubiquitaire en français

Pour plus de détails sur le contexte métier, consultez [context.md](context.md).

## 🎯 Périmètre actuel (v0.1)

### Entités métier implémentées

- **Patient** : identifiant, nom, prénom, date de naissance, sexe
- **Passage** : interaction ponctuelle avec le SIH (urgences, consultation, hospitalisation, ambulatoire)

### Hors périmètre initial

- Diagnostics détaillés, actes médicaux, biologie
- PMSI/GHM, facturation
- Exports FHIR/OMOP
- Construction d'un Entrepôt de Données de Santé (EDS)

Ces fonctionnalités seront ajoutées progressivement dans les versions futures.

## 🚀 Installation

### Prérequis

- Python 3.12 ou supérieur
- [uv](https://github.com/astral-sh/uv) (gestionnaire de paquets)

### Installation du projet

```bash
# Cloner le dépôt
git clone https://github.com/tomboulier/eds-synthetique.git
cd eds-synthetique

# Installer les dépendances (y compris dev)
uv sync --extra dev
```

## 📁 Structure du projet

```
eds_synthetique/
├── src/
│   └── eds_synthetique/
│       ├── domaine/          # Modèle de domaine (DDD)
│       │   ├── patient.py    # Entité Patient
│       │   └── passage.py    # Entité Passage
│       ├── generation/       # Logique de génération synthétique
│       ├── infrastructure/   # Exports, persistence
│       └── utils/            # Utilitaires (logging, etc.)
├── tests/                    # Tests unitaires et d'intégration
├── docs/                     # Documentation MkDocs
├── .github/workflows/        # CI/CD GitHub Actions
└── pyproject.toml            # Configuration du projet
```

## 🛠️ Développement

### Lancer les tests

```bash
uv run pytest
```

### Linting et formatage

```bash
# Vérifier le code
uv run ruff check src/ tests/

# Formater le code
uv run ruff format src/ tests/
```

### Type checking

```bash
uv run pyright src/
```

### Générer la documentation

```bash
uv run mkdocs serve
```

## 🧪 Tests et qualité du code

Le projet suit les bonnes pratiques de développement Python :

- **TDD** (Test-Driven Development)
- **Linting et formatage** : Ruff
- **Type checking** : Pyright (mode strict)
- **Tests** : pytest avec coverage
- **Documentation** : Material for MkDocs avec docstrings numpydoc
- **CI/CD** : GitHub Actions

## 🗺️ Roadmap

### Version actuelle (v0.1)
- [x] Structure du projet et configuration
- [x] Entités Patient et Passage
- [x] Configuration des outils de développement
- [ ] Implémentation TDD des entités
- [ ] Générateur de données synthétiques
- [ ] Métadonnées de génération

### Versions futures
- [ ] Ajout d'Observations et d'Actes
- [ ] Génération de séjours hospitaliers
- [ ] Export CSV/JSON
- [ ] Projection FHIR
- [ ] Projection OMOP
- [ ] Construction d'un EDS

## 📄 License

Ce projet est sous license MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Merci de :
- Suivre les conventions de code du projet (Ruff, Pyright)
- Écrire des tests pour toute nouvelle fonctionnalité
- Utiliser des commits conventionnels en français
- Documenter le code avec des docstrings numpydoc

## 📚 Références

- [Context métier](context.md) - Documentation détaillée du contexte et de la philosophie du projet
- [uv](https://github.com/astral-sh/uv) - Gestionnaire de paquets Python
- [Ruff](https://github.com/astral-sh/ruff) - Linter et formatter Python ultra-rapide
- [Pyright](https://github.com/microsoft/pyright) - Type checker Python

---

**Note** : Ce projet génère uniquement des données synthétiques. Aucune donnée réelle de patients n'est utilisée ou stockée.
