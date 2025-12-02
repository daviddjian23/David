# 📚 Générateur Automatique de Planning Scolaire

> Système intelligent de planification de devoirs et révisions avec calcul de priorités personnalisable

## 🎯 Description

Ce générateur automatique crée des plannings de travail optimisés pour les étudiants en fonction de :
- ✅ Deadlines des devoirs
- ✅ Difficultés estimées
- ✅ Disponibilités variables jour par jour
- ✅ Préférences de sessions de travail
- ✅ Poids configurables pour le calcul des priorités

## 🚀 Fonctionnalités

### 📊 Analyse Intelligente des Devoirs

- **Normalisation automatique** : Extraction du titre, sujet, description depuis du texte brut (OCR)
- **Estimation automatique** : Durée et difficulté si non fournies
- **Calcul de priorité** : Score 0-100 basé sur des poids configurables
- **Tags intelligents** : Détection de mots-clés (contrôle, examen, DM, etc.)

### 🎨 Planning Visual & Structuré

- **Cartouches par matière** : Couleur + emoji associés à chaque sujet
- **Résumé quotidien** : Vue d'ensemble de la charge de travail
- **Conseils personnalisés** : 3-6 recommandations par jour
- **Sessions optimisées** : Respect des durées préférées et contraintes

### ⚠️ Détection de Conflits

- **Analyse automatique** : Détecte les impossibilités de planning
- **Solutions concrètes** : 3 propositions pour chaque conflit
- **Transparence** : Minutes disponibles vs requises

## 📦 Installation

### Prérequis

- Python 3.7+
- Aucune dépendance externe (utilise uniquement la bibliothèque standard)

### Installation

```bash
# Cloner le repository
git clone <votre-repo>
cd David

# Rendre le script exécutable
chmod +x school_schedule_generator.py
```

## 🔧 Utilisation

### 1. Créer un fichier d'entrée JSON

Créez un fichier `mon_planning.json` avec la structure suivante :

```json
{
  "today": "2025-12-02",
  "user_id": "etudiant_1",
  "max_session_minutes": 90,
  "buffer_percent": 10,
  "prefer_spread": true,
  "availability": [
    {"date": "2025-12-02", "available_minutes": 60},
    {"date": "2025-12-03", "available_minutes": 120}
  ],
  "homeworks_raw": [
    {
      "id": "hw_1",
      "raw_text": "Contrôle de mathématiques chapitre 4...",
      "due_date": "2025-12-04",
      "tags": ["contrôle", "important"]
    }
  ],
  "weights": {
    "w_proximity": 0.5,
    "w_user_importance": 0.25,
    "w_difficulty_and_duration": 0.2,
    "keyword_bonus": 0.15
  },
  "session_preferences": {
    "preferred_session_min": 25,
    "preferred_session_max": 50
  },
  "time_preferences": {
    "earliest_hour": 17,
    "latest_hour": 21
  }
}
```

### 2. Exécuter le générateur

```bash
python3 school_schedule_generator.py mon_planning.json > planning_resultat.json
```

### 3. Utiliser le résultat

Le fichier `planning_resultat.json` contient :
- `meta` : Métadonnées (date génération, totaux, poids utilisés)
- `homeworks` : Liste des devoirs normalisés avec priorités
- `schedule` : Planning jour par jour avec sessions
- `conflicts` : Liste des conflits avec solutions

## 📖 Structure des Données

### Input JSON

#### Champs Obligatoires

| Champ | Type | Description |
|-------|------|-------------|
| `today` | string | Date du jour (YYYY-MM-DD) |
| `availability` | array | Liste des disponibilités par jour |
| `homeworks_raw` | array | Liste des devoirs bruts |

#### Champs Optionnels

| Champ | Type | Défaut | Description |
|-------|------|--------|-------------|
| `max_session_minutes` | number | 90 | Durée max d'une session |
| `buffer_percent` | number | 10 | % de buffer à garder |
| `prefer_spread` | boolean | true | Répartir uniformément vs concentrer |
| `weights` | object | voir ci-dessous | Poids pour calcul priorité |
| `session_preferences` | object | voir ci-dessous | Préférences de sessions |
| `time_preferences` | object | {} | Horaires préférés |

#### Poids par Défaut

```json
{
  "w_proximity": 0.5,           // Impact proximité deadline
  "w_user_importance": 0.25,     // Importance fournie par user
  "w_difficulty_and_duration": 0.2,  // Difficulté + durée
  "keyword_bonus": 0.15          // Bonus mots-clés (contrôle, examen)
}
```

**Note** : Si la somme des 3 premiers poids > 1.0, ils sont automatiquement normalisés.

#### Structure d'un Devoir Brut

```json
{
  "id": "hw_1",
  "raw_text": "Texte OCR ou description",  // Utilisé pour extraction auto
  "title": null,                          // Auto-extrait si null
  "subject": null,                        // Auto-détecté si null
  "description": null,                    // Auto-généré si null
  "due_date": "2025-12-04",              // null = non-urgent
  "estimated_minutes": null,              // Auto-estimé si null
  "difficulty": null,                     // Auto-estimé : facile/moyen/difficile
  "tags": ["contrôle"],                   // Optionnel
  "user_importance": 0.8                  // Optionnel (0..1)
}
```

### Output JSON

#### Structure Globale

```json
{
  "meta": { ... },
  "homeworks": [ ... ],
  "schedule": [ ... ],
  "conflicts": [ ... ]
}
```

#### Exemple de Session

```json
{
  "homework_id": "hw_1",
  "start_time": "17:00",  // null si pas de time_preferences
  "duration_minutes": 50,
  "short_task_desc": "Contrôle de maths...",
  "emoji": "🧮",
  "color": "#DCE7FF"
}
```

#### Exemple de Jour

```json
{
  "date": "2025-12-02",
  "day_total_allocated_minutes": 120,
  "available_minutes": 150,
  "cartouche": {
    "emoji": "🧮",
    "color": "#DCE7FF",
    "label": "Mathématiques"
  },
  "sessions": [ ... ],
  "daily_summary": "Aujourd'hui : 2 sessions (120 min) en maths, français.",
  "advice": [
    "Charge équilibrée : reste concentré.",
    "Prépare ton espace de travail.",
    ...
  ]
}
```

## 🎨 Mapping Matières → Couleurs/Emojis

| Matière | Couleur | Emoji |
|---------|---------|-------|
| Mathématiques | `#DCE7FF` | 🧮 |
| Français | `#FFE5E5` | 📝 |
| Histoire/Géo | `#FFF4E5` / `#E5F4FF` | 📚 / 🌍 |
| Anglais | `#F0E5FF` | 🇬🇧 |
| Espagnol | `#FFE5F0` | 🇪🇸 |
| Allemand | `#E5FFE5` | 🇩🇪 |
| Physique | `#E5FFFF` | ⚛️ |
| Chimie | `#FFE5FF` | 🧪 |
| SVT/Biologie | `#E5FFE5` | 🧬 |
| Sciences | `#E5FFE5` | 🔬 |
| EPS/Sport | `#FFFFE5` | ⚽ |
| Urgent | `#FF6B6B` | 🚨 |
| Défaut | `#F0F0F0` | 📌 |

## 🧮 Calcul des Priorités

### Formule d'Importance (0..1)

```
importance = w_proximity × proximity_metric
           + w_user_importance × user_importance_metric
           + w_difficulty_and_duration × difficulty_duration_metric
           + keyword_bonus (si applicable)
```

#### Métriques

1. **Proximity Metric** : `1 / (1 + jours_restants)`
   - Plus la deadline est proche, plus la valeur est élevée
   - Valeur = 1.0 si déjà en retard

2. **User Importance Metric** : Valeur fournie par l'utilisateur (0..1)
   - Si non fournie : 0

3. **Difficulty & Duration Metric** : `(difficulté + durée_normalisée) / 2`
   - Difficulté : facile=0.25, moyen=0.6, difficile=1.0
   - Durée normalisée : `min(durée / 180, 1.0)`

4. **Keyword Bonus** : +0.15 (configurable)
   - Appliqué si tags contiennent "contrôle" ou "examen"

### Score de Priorité (0..100)

```
priority_score = round(importance × 100) + ajustement_proximité
```

Ajustement proximité :
- +5 si deadline ≤ 1 jour
- +3 si deadline ≤ 3 jours

## 📋 Exemples d'Utilisation

### Exemple 1 : Planning de Révisions

```json
{
  "today": "2025-12-02",
  "prefer_spread": false,
  "availability": [
    {"date": "2025-12-02", "available_minutes": 180},
    {"date": "2025-12-03", "available_minutes": 240}
  ],
  "homeworks_raw": [
    {
      "id": "rev_1",
      "raw_text": "Révision complète pour examen final de maths",
      "due_date": "2025-12-04",
      "tags": ["examen", "urgent"]
    }
  ]
}
```

**Résultat** : Sessions concentrées près de la deadline

### Exemple 2 : Charge Équilibrée

```json
{
  "today": "2025-12-02",
  "prefer_spread": true,
  "buffer_percent": 15,
  "availability": [
    {"date": "2025-12-02", "available_minutes": 90},
    {"date": "2025-12-03", "available_minutes": 90},
    {"date": "2025-12-04", "available_minutes": 90}
  ],
  "homeworks_raw": [
    {
      "id": "dm_1",
      "raw_text": "DM de physique : 10 exercices",
      "due_date": "2025-12-05",
      "estimated_minutes": 120
    }
  ]
}
```

**Résultat** : Sessions réparties uniformément avec buffer de 15%

### Exemple 3 : Poids Personnalisés

Pour privilégier la difficulté plutôt que la proximité :

```json
{
  "weights": {
    "w_proximity": 0.2,
    "w_user_importance": 0.2,
    "w_difficulty_and_duration": 0.6,
    "keyword_bonus": 0.1
  }
}
```

## 🔍 Gestion des Conflits

### Types de Conflits Détectés

1. **Disponibilités insuffisantes** : Pas assez de temps avant deadline
2. **Aucune date disponible** : Aucun créneau entre aujourd'hui et due_date

### Solutions Proposées

Pour chaque conflit, 3 solutions sont générées :

```json
{
  "homework_id": "hw_2",
  "reason": "Disponibilités insuffisantes avant la deadline",
  "required_minutes": 120,
  "available_before_due": 90,
  "solutions": [
    "Solution 1 : Augmenter la disponibilité de 10 min sur 3 jours...",
    "Solution 2 : Réduire le périmètre en ciblant l'essentiel...",
    "Solution 3 : Réorganiser d'autres sessions moins prioritaires..."
  ]
}
```

## ⚙️ Configuration Avancée

### Ajuster les Estimations Automatiques

Le code utilise des heuristiques pour estimer durée et difficulté. Vous pouvez les ajuster dans `school_schedule_generator.py` :

```python
def _estimate_duration(self, raw_text: str, tags: List[str]) -> int:
    base_duration = 60

    if any(tag.lower() in ["contrôle", "examen"] for tag in tags):
        base_duration = 120
    # ... personnaliser ici

    return base_duration
```

### Ajouter des Matières

Dans `SUBJECT_MAPPING` :

```python
SUBJECT_MAPPING = {
    "italien": ("#FFE5E5", "🇮🇹"),
    "philosophie": ("#E5E5FF", "💭"),
    # ... ajouter vos matières
}
```

## 📊 Cas d'Usage

### 1. Lycéen avec Disponibilités Variables

**Profil** : Travaille lundi/mercredi/vendredi après-midi

```json
{
  "availability": [
    {"date": "2025-12-02", "available_minutes": 0},     // Mardi : cours toute la journée
    {"date": "2025-12-03", "available_minutes": 180},   // Mercredi : après-midi libre
    {"date": "2025-12-04", "available_minutes": 0},     // Jeudi : cours
    {"date": "2025-12-05", "available_minutes": 120}    // Vendredi : 2h
  ]
}
```

### 2. Étudiant Universitaire avec Gros Projets

**Profil** : Gros projet à découper sur plusieurs jours

```json
{
  "max_session_minutes": 120,
  "preferred_session_min": 45,
  "preferred_session_max": 90,
  "homeworks_raw": [
    {
      "id": "projet_info",
      "raw_text": "Projet de programmation : application web complète",
      "estimated_minutes": 600,
      "due_date": "2025-12-15",
      "difficulty": "difficile"
    }
  ]
}
```

### 3. Préparation Examen avec Contraintes Horaires

**Profil** : Étudiant travaillant en soirée uniquement

```json
{
  "time_preferences": {
    "earliest_hour": 19,
    "latest_hour": 23,
    "preferred_start_windows": [
      ["19:00", "20:00"],
      ["20:30", "21:30"]
    ]
  }
}
```

## 🛠️ Développement

### Structure du Code

```
school_schedule_generator.py
├── SchoolScheduleGenerator    # Classe principale
│   ├── normalize_homework()   # Normalisation devoirs
│   ├── _calculate_importance() # Calcul priorités
│   ├── _allocate_sessions()   # Répartition temporelle
│   ├── _generate_advice()     # Génération conseils
│   └── generate_schedule()    # Point d'entrée
└── main()                      # CLI
```

### Étendre le Système

#### Ajouter une Métrique de Priorité

```python
def _calculate_importance(self, ...):
    # ... code existant

    # Nouvelle métrique : bonus pour matière préférée
    favorite_subject_bonus = 0.1 if subject == "mathématiques" else 0.0

    importance_base += favorite_subject_bonus
    # ...
```

#### Personnaliser les Conseils

```python
def _generate_advice(self, sessions, total_minutes, available):
    advice = []

    # Vos conseils personnalisés
    if self._is_weekend(date):
        advice.append("C'est le weekend : profite pour réviser en avance !")

    # ... code existant
    return advice
```

## 📝 Bonnes Pratiques

### 1. Fournir des Données de Qualité

- ✅ Estimer les durées réalistes
- ✅ Indiquer les vraies disponibilités
- ✅ Utiliser des tags pertinents ("contrôle", "urgent", etc.)

### 2. Ajuster les Poids

- 🎯 Tester différentes configurations de poids
- 📊 Comparer les plannings générés
- ⚖️ Trouver l'équilibre adapté à votre profil

### 3. Buffer de Temps

- 💡 Garder 10-20% de buffer pour les imprévus
- 🚫 Ne pas remplir 100% des disponibilités

### 4. Sessions de Travail

- ⏱️ Préférer 25-50 min pour rester concentré
- 🔄 Alterner matières difficiles et faciles
- 💪 Commencer par les tâches difficiles

## ❓ FAQ

**Q : Pourquoi mon devoir n'apparaît pas dans le planning ?**

R : Vérifiez que :
- La deadline (`due_date`) est après `today`
- Il y a des disponibilités entre aujourd'hui et la deadline
- La durée estimée peut rentrer dans les sessions disponibles

**Q : Comment forcer une priorité élevée ?**

R : Ajoutez `"user_importance": 1.0` au devoir et utilisez des tags comme `["urgent", "contrôle"]`.

**Q : Les sessions sont trop longues, comment les réduire ?**

R : Ajustez dans `session_preferences` :
```json
{
  "preferred_session_min": 20,
  "preferred_session_max": 35,
  "max_session_minutes": 45
}
```

**Q : Puis-je utiliser ce système sans dates ?**

R : Oui ! Mettez `due_date: null` pour les devoirs sans deadline. Ils seront traités comme non-urgents.

## 🤝 Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

MIT License - Voir le fichier LICENSE

## 🙏 Remerciements

Développé pour aider les étudiants à mieux organiser leur travail scolaire et réduire le stress lié aux deadlines.

---

**Fait avec ❤️ pour optimiser la réussite scolaire**
