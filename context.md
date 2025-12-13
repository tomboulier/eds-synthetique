# Contexte de projet — Génération d’un SIH synthétique (France)

## 1. Objectif général

L’objectif de ce projet est de construire **un Système d’Information Hospitalier (SIH) synthétique minimal**, crédible et maîtrisé, **puis dans un second temps un Entrepôt de Données de Santé (EDS)**
synthétique lui aussi.

Ce SIH est :
- **entièrement synthétique** (aucune donnée réelle),
- **français dans sa terminologie métier**,
- **simple, itératif et pédagogique**,
- **traçable et reproductible**,
- destiné à servir de **socle technique** pour des démonstrations, expérimentations et futurs exports.

Les projections vers des standards internationaux (FHIR, OMOP, etc.) **ne sont pas un objectif immédiat** et seront traitées ultérieurement comme des **couches de traduction**.

---

## 2. Philosophie générale

### 2.1 Principe fondamental

> **Un patient n’existe dans un SIH que par ses interactions avec l’hôpital.**

Conséquences :
- une simple liste de patients n’est pas suffisante,
- la **dimension temporelle** est centrale,
- la **trajectoire de soins** donne le sens métier.

L’identité est nécessaire, mais **insuffisante sans interaction**.

---

### 2.2 Ordre logique du projet

1. Générer un **SIH synthétique propre**
2. Vérifier la cohérence métier (patients, passages, séjours)
3. Ensuite seulement (hors périmètre initial) :
   - exports FHIR
   - projection OMOP
   - construction d’un EDS

---

## 3. Positionnement par rapport à Synthea

### 3.1 Décision

Synthea **n’est pas utilisé comme générateur direct**, car :
- très orienté **contexte américain**,
- trop riche pour un démarrage minimal,
- peu aligné avec le vocabulaire SIH français.

### 3.2 Ce qui est conservé de Synthea (conceptuellement)

Synthea sert uniquement **d’inspiration conceptuelle** pour :
- la séparation **identité / trajectoire**,
- la centralité du temps,
- la génération reproductible via des seeds,
- la traçabilité des runs via des métadonnées.

Synthea **n’est pas un modèle cible**.

---

## 4. Choix terminologiques (DDD / Ubiquitous Language)

### 4.1 Principe

Le **domaine métier est exprimé en français**, conformément au contexte hospitalier français et aux usages SIH / PMSI.

Les standards internationaux (FHIR, OMOP, etc.) seront abordés plus tard via des **mappings explicites**.

---

### 4.2 Vocabulaire métier retenu (v0.1)

| Concept | Définition |
|------|-----------|
| Patient | Personne suivie par l’hôpital |
| Passage | Interaction ponctuelle avec le SIH (urgences, consultation, venue) |
| Séjour | Hospitalisation avec date d’entrée et de sortie |
| Établissement | Hôpital ou clinique |
| Unité | Service ou unité fonctionnelle |
| Acte | Geste ou procédure réalisée |
| Observation | Mesure ou constat clinique |

Notes :
- **Passage** ≠ **Séjour**
- Le **Séjour** est un type particulier d’interaction prolongée
- Aucun calcul PMSI ou GHM n’est implémenté à ce stade

---

## 5. Périmètre fonctionnel initial (volontairement minimal)

### 5.1 Entités métier à implémenter

#### Patient
- identifiant unique interne
- nom
- prénom
- date de naissance
- sexe

#### Passage
- identifiant unique
- référence au patient
- date/heure de début
- date/heure de fin
- type de passage (ex. urgences, ambulatoire, hospitalisation)

> Le patient existe dans le SIH **par ses passages**.

---

### 5.2 Ce qui est explicitement hors périmètre initial

- diagnostics détaillés
- actes médicaux
- biologie
- PMSI / GHM
- facturation
- exports FHIR / OMOP
- EDS

---

## 6. Génération des données synthétiques

### 6.1 Approche générale

La génération est faite **entièrement en Python**, à la main, avec :
- des règles simples,
- des contraintes temporelles cohérentes,
- un contrôle total du modèle.

Objectif : **cohérence et lisibilité**, pas réalisme exhaustif.

---

### 6.2 Reproductibilité

Chaque génération doit être **reproductible** via :
- une seed aléatoire,
- un fichier de métadonnées décrivant le run.

---

## 7. Métadonnées de génération

Chaque exécution du générateur produit un fichier de métadonnées contenant a minima :

- identifiant du run
- date/heure d’exécution
- seed utilisée
- nombre de patients générés
- nombre de passages générés
- période couverte
- version du générateur

Ces métadonnées permettent :
- la traçabilité,
- la reproductibilité,
- la documentation scientifique ou pédagogique.

---

## 8. Architecture logicielle attendue

### 8.1 Principes

- code clair et lisible
- séparation domaine / génération / export
- pas de sur-architecture pour le moment
- extensibilité future possible (vers architecture Clean/hexagonale)

### 8.2 Orientation DDD

- **Domaine métier** : français
- **Infrastructure / export** : potentiellement bilingue plus tard
- mappings explicites (anti-corruption layer)

### 8.3 Pile technique

- python (dernière version)
- package manager: uv
- création du projet avec "uv init"
- utilisation des fichiers "pyproject.toml" et "uv.lock"
- tests avec pytest (+ CI/CD github actions)
- documentation avec les docstrings, en utilisant Materials for MkDocs
- utiliser les bonnes pratiques de développement en Python
   - linting et formatting avec Ruff
   - type checking avec Ty ou Pyrefly (suivant ce qui est le plus simple et rapide)
   - pas de "print", utiliser le module logging (avec un module de setup)

### 8.4 Style de Code

- Clean Code :
   - utiliser des noms de variables/méthodes/classes/fonctions/modules qui aient un sens,
     qui disent ce qu'ils font et font ce qu'ils disent
     - penser à l'aspect DDD, et notamment le langage ubiquitaire, et donc utiliser 
       le français et le langage médical/PMSI français
- des commentaires en français
- des docstrings au format numpydoc
- des type hints
- du TDD
- des commits réguliers et petits
- des messages de commit au format conventionnal commit (en français) : le titre
   ne dépasse pas 72 caractères, ensuite on explique dans le corps

---

## 9. Vision à moyen terme (hors périmètre immédiat)

- ajout d’Observations, Actes
- projection vers FHIR
- projection vers OMOP
- construction d’un EDS
- scénarios de démonstration

---

## 10. Phrase directrice du projet

> **On commence par un SIH synthétique simple, cohérent et traçable ; l’EDS n’est qu’une projection analytique secondaire.**
