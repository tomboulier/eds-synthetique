# Guide de contribution

Ce document décrit les conventions et le workflow de développement pour le projet `eds_synthetique`.

## Workflow Git : GitHub Flow

Le projet utilise le **GitHub Flow**, un workflow simple et efficace basé sur des branches.

### Principes du GitHub Flow

1. **La branche `master` est toujours déployable**
   - Tous les commits sur `master` doivent passer les tests
   - Le code sur `master` est considéré comme stable

2. **Créer une branche par fonctionnalité**
   - Format du nom : `feature/nom-de-la-fonctionnalite`
   - Exemples : `feature/generateur-patients`, `feature/export-fhir`

3. **Commits réguliers et petits**
   - Commiter fréquemment sur votre branche
   - Messages au format Conventional Commits (voir ci-dessous)

4. **Ouvrir une Pull Request**
   - Dès que vous voulez des retours ou merger
   - La PR sert de discussion et de revue de code

5. **Merger après validation**
   - Tests passent (CI/CD)
   - Revue de code effectuée si nécessaire
   - Merge sur `master`

6. **Supprimer la branche feature après merge**
   - Garder le dépôt propre

---

## Workflow détaillé

### 1. Créer une branche feature

```bash
# S'assurer d'être à jour
git checkout master
git pull origin master

# Créer et basculer sur la nouvelle branche
git checkout -b feature/nom-de-la-fonctionnalite
```

### 2. Développer en TDD

**Cycle TDD (Test-Driven Development) :**

1. **Red** : Écrire un test qui échoue
   ```bash
   uv run pytest tests/  # Le test doit échouer
   ```

2. **Green** : Écrire le code minimal pour faire passer le test
   ```bash
   uv run pytest tests/  # Le test passe
   ```

3. **Refactor** : Améliorer le code si nécessaire
   ```bash
   uv run pytest tests/  # Les tests passent toujours
   ```

### 3. Vérifier la qualité du code

Avant chaque commit, vérifier :

```bash
# Linting et formatage
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Type checking
uv run pyright src/ tests/

# Tests et couverture
uv run pytest tests/ --cov=src/eds_synthetique
```

### 4. Commiter régulièrement

```bash
git add <fichiers-modifiés>
git commit -m "type: description courte

Explication détaillée si nécessaire.
```

### 5. Pousser la branche

```bash
git push -u origin feature/nom-de-la-fonctionnalite
```

### 6. Créer une Pull Request

```bash
# Via l'interface GitHub ou avec gh CLI
gh pr create --title "feat: description de la fonctionnalité" \
  --body "## Summary
- Bullet points décrivant les changements

## Test plan
- [ ] Tests unitaires ajoutés
- [ ] Tests passent en local
- [ ] Coverage maintenu ou amélioré

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

### 7. Merger la Pull Request

Une fois la PR validée (tests passent, revue OK) :

```bash
# Via l'interface GitHub ou avec gh CLI
gh pr merge --squash  # ou --merge selon les préférences
```

### 8. Nettoyer

```bash
# Revenir sur master
git checkout master
git pull origin master

# Supprimer la branche locale
git branch -d feature/nom-de-la-fonctionnalite
```

---

## Format des messages de commit

Le projet utilise **Conventional Commits** en français.

### Structure

```
<type>(<scope optionnel>): <description>

<corps optionnel>

<footer optionnel>
```

### Types de commits

| Type | Description | Exemple |
|------|-------------|---------|
| `feat` | Nouvelle fonctionnalité | `feat: ajout du générateur de patients` |
| `fix` | Correction de bug | `fix: corrige la validation des dates` |
| `test` | Ajout ou modification de tests | `test: ajout des tests pour Periode` |
| `refactor` | Refactoring sans changement de comportement | `refactor: extraction de la logique métier` |
| `docs` | Documentation uniquement | `docs: mise à jour du README` |
| `chore` | Tâches de maintenance | `chore: mise à jour des dépendances` |
| `ci` | Configuration CI/CD | `ci: ajout du workflow GitHub Actions` |
| `perf` | Amélioration de performance | `perf: optimisation de la génération` |
| `style` | Formatage, point-virgules, etc. | `style: formatage avec Ruff` |

### Règles

- Titre limité à 72 caractères
- Utiliser l'impératif ("ajoute" pas "ajouté" ou "ajouter")
- Pas de point final dans le titre
- Corps optionnel pour expliquer le "pourquoi"
- Footer pour les breaking changes ou issues

### Exemples

```bash
# Simple
git commit -m "feat: ajout du générateur de patients"

# Avec corps
git commit -m "feat(generateur): ajout de la génération de noms réalistes

Utilise la bibliothèque Faker pour générer des noms français
cohérents. La seed permet la reproductibilité."

# Avec breaking change
git commit -m "feat!: refonte de l'API du générateur

BREAKING CHANGE: Le paramètre 'nb_patients' devient 'nombre_patients'
pour plus de clarté."
```

---

## Standards de code

### Python

- **Version** : Python 3.12+
- **Style** : PEP 8 (appliqué par Ruff)
- **Type hints** : Obligatoires pour toutes les fonctions publiques
- **Docstrings** : Format numpydoc

### Exemple de fonction bien documentée

```python
def generer_patient(seed: int | None = None) -> Patient:
    """
    Génère un patient synthétique aléatoire.

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
    >>> patient.nom
    'Dupont'
    """
    # Implémentation...
```

### Bonnes pratiques

1. **Clean Code**
   - Noms explicites (français pour le domaine métier)
   - Fonctions courtes et focalisées
   - Pas de code commenté (utiliser git)

2. **DDD (Domain-Driven Design)**
   - Utiliser le langage ubiquitaire (français médical/PMSI)
   - Séparer domaine, application, infrastructure
   - Value Objects immuables

3. **Logging**
   - Utiliser le module `logging`, PAS de `print()`
   - Niveaux appropriés : DEBUG, INFO, WARNING, ERROR

4. **Tests**
   - Couverture minimale : 80% (viser 100% sur le domaine)
   - Tests unitaires rapides (< 1s au total)
   - Fixtures réutilisables

---

## Outils de développement

### Installation

```bash
# Cloner le projet
git clone git@github.com:tomboulier/eds-synthetique.git
cd eds-synthetique

# Installer les dépendances
uv sync
```

### Commandes utiles

```bash
# Lancer les tests
uv run pytest

# Tests avec couverture
uv run pytest --cov=src/eds_synthetique --cov-report=html

# Linting
uv run ruff check src/ tests/

# Auto-formatage
uv run ruff format src/ tests/

# Type checking
uv run pyright src/ tests/

# Documentation locale
uv run mkdocs serve
```

### Pre-commit hooks (optionnel)

```bash
# Installer pre-commit
uv add --dev pre-commit

# Installer les hooks
uv run pre-commit install
```

---

## Structure du projet

```
eds_synthetique/
├── src/
│   └── eds_synthetique/
│       ├── domaine/           # Entités et Value Objects
│       ├── generation/        # Générateurs de données
│       ├── infrastructure/    # Persistence, export
│       └── utils/             # Utilitaires (logging, etc.)
├── tests/
│   ├── domaine/
│   ├── generation/
│   └── infrastructure/
├── docs/                      # Documentation MkDocs
├── .github/
│   └── workflows/             # CI/CD
├── pyproject.toml             # Configuration du projet
├── uv.lock                    # Lock file
├── README.md
├── CONTRIBUTING.md            # Ce fichier
└── context.md                 # Contexte métier du projet
```

---

## Questions fréquentes

### Quand créer une branche ?

Dès que vous commencez à travailler sur une nouvelle fonctionnalité ou un fix.

### Quand ouvrir une Pull Request ?

- Dès que vous voulez des retours
- Quand la fonctionnalité est prête à merger
- Même pour des WIP (Work In Progress) - marquer `[WIP]` dans le titre

### Comment synchroniser ma branche avec master ?

```bash
# Option 1 : Rebase (historique linéaire)
git checkout feature/ma-branche
git fetch origin
git rebase origin/master

# Option 2 : Merge (si vous préférez)
git merge origin/master
```

### Les tests échouent en CI mais passent en local ?

Vérifier :
1. Version de Python identique
2. Dépendances à jour (`uv sync`)
3. Pas de fichiers non commitées

---

## Ressources

- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Numpydoc Style Guide](https://numpydoc.readthedocs.io/)

---

**Merci de contribuer au projet ! 🚀**
