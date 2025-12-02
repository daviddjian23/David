#!/usr/bin/env python3
"""
Générateur automatique de planning scolaire
Système de planification intelligent pour devoirs et révisions
"""

import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class Homework:
    """Représente un devoir avec toutes ses métadonnées"""
    id: str
    title: str
    subject: str
    description: str
    due_date: Optional[str]
    estimated_minutes: int
    difficulty: str
    importance: float
    priority_score: int
    tags: List[str] = field(default_factory=list)
    raw_text: str = ""


@dataclass
class Session:
    """Représente une session de travail"""
    homework_id: str
    start_time: Optional[str]
    duration_minutes: int
    short_task_desc: str
    emoji: str
    color: str


@dataclass
class DaySchedule:
    """Planning d'une journée"""
    date: str
    day_total_allocated_minutes: int
    available_minutes: int
    cartouche: Dict[str, str]
    sessions: List[Session]
    daily_summary: str
    advice: List[str]


@dataclass
class Conflict:
    """Conflit de planification"""
    homework_id: str
    reason: str
    required_minutes: int
    available_before_due: int
    solutions: List[str]


class SchoolScheduleGenerator:
    """
    Générateur de planning scolaire intelligent
    Utilise des poids configurables pour calculer les priorités
    """

    # Mapping sujet -> (color, emoji)
    SUBJECT_MAPPING = {
        "mathématiques": ("#DCE7FF", "🧮"),
        "maths": ("#DCE7FF", "🧮"),
        "français": ("#FFE5E5", "📝"),
        "histoire": ("#FFF4E5", "📚"),
        "géographie": ("#E5F4FF", "🌍"),
        "anglais": ("#F0E5FF", "🇬🇧"),
        "espagnol": ("#FFE5F0", "🇪🇸"),
        "allemand": ("#E5FFE5", "🇩🇪"),
        "physique": ("#E5FFFF", "⚛️"),
        "chimie": ("#FFE5FF", "🧪"),
        "svt": ("#E5FFE5", "🧬"),
        "biologie": ("#E5FFE5", "🧬"),
        "sciences": ("#E5FFE5", "🔬"),
        "eps": ("#FFFFE5", "⚽"),
        "sport": ("#FFFFE5", "⚽"),
        "urgent": ("#FF6B6B", "🚨"),
        "default": ("#F0F0F0", "📌")
    }

    DIFFICULTY_VALUES = {
        "facile": 0.25,
        "moyen": 0.6,
        "difficile": 1.0
    }

    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le générateur avec la configuration fournie

        Args:
            config: Configuration incluant today, homeworks_raw, availability, weights, etc.
        """
        self.today = datetime.strptime(config["today"], "%Y-%m-%d")
        self.user_id = config.get("user_id", "user_1")
        self.max_session_minutes = config.get("max_session_minutes", 90)
        self.buffer_percent = config.get("buffer_percent", 10)
        self.prefer_spread = config.get("prefer_spread", True)
        self.availability = {
            item["date"]: item["available_minutes"]
            for item in config.get("availability", [])
        }
        self.homeworks_raw = config.get("homeworks_raw", [])

        # Poids pour le calcul d'importance
        weights = config.get("weights", {})
        self.w_proximity = weights.get("w_proximity", 0.5)
        self.w_user_importance = weights.get("w_user_importance", 0.25)
        self.w_difficulty_and_duration = weights.get("w_difficulty_and_duration", 0.2)
        self.keyword_bonus = weights.get("keyword_bonus", 0.15)

        # Normaliser les poids si leur somme > 1.0
        weight_sum = self.w_proximity + self.w_user_importance + self.w_difficulty_and_duration
        if weight_sum > 1.0:
            self.w_proximity /= weight_sum
            self.w_user_importance /= weight_sum
            self.w_difficulty_and_duration /= weight_sum

        # Préférences de session
        session_prefs = config.get("session_preferences", {})
        self.preferred_session_min = session_prefs.get("preferred_session_min", 25)
        self.preferred_session_max = session_prefs.get("preferred_session_max", 50)

        # Préférences horaires
        self.time_preferences = config.get("time_preferences", {})

        self.homeworks: List[Homework] = []
        self.schedule: List[DaySchedule] = []
        self.conflicts: List[Conflict] = []

    def normalize_homework(self, hw_raw: Dict[str, Any]) -> Homework:
        """
        Normalise un devoir brut en objet Homework structuré
        Estime les champs manquants (title, estimated_minutes, difficulty)
        """
        hw_id = hw_raw.get("id", f"hw_{len(self.homeworks) + 1}")
        raw_text = hw_raw.get("raw_text", "")
        tags = hw_raw.get("tags", [])

        # Extraire ou générer le titre
        title = hw_raw.get("title")
        if not title:
            # Extraire des mots clés du raw_text
            if raw_text:
                words = raw_text.split()[:5]
                title = " ".join(words)
            else:
                title = f"Devoir {hw_id}"

        # Extraire ou déduire le sujet
        subject = hw_raw.get("subject") or ""
        subject = subject.lower() if subject else ""
        if not subject and raw_text:
            # Chercher des mots-clés de matière dans le texte
            raw_lower = raw_text.lower()
            for subj in self.SUBJECT_MAPPING.keys():
                if subj in raw_lower:
                    subject = subj
                    break
            if not subject:
                subject = "général"

        # Description
        description = hw_raw.get("description")
        if not description and raw_text:
            # Première phrase ou premiers 100 caractères
            description = raw_text[:100] + ("..." if len(raw_text) > 100 else "")

        # Due date
        due_date = hw_raw.get("due_date")

        # Estimer la durée si manquante
        estimated_minutes = hw_raw.get("estimated_minutes")
        if not estimated_minutes:
            estimated_minutes = self._estimate_duration(raw_text, tags)

        # Estimer la difficulté si manquante
        difficulty = hw_raw.get("difficulty") or ""
        difficulty = difficulty.lower() if difficulty else ""
        if difficulty not in self.DIFFICULTY_VALUES:
            difficulty = self._estimate_difficulty(raw_text, tags, estimated_minutes)

        # Calculer importance et priority_score
        importance = self._calculate_importance(
            due_date, estimated_minutes, difficulty, tags, hw_raw.get("user_importance")
        )
        priority_score = self._calculate_priority_score(importance, due_date)

        return Homework(
            id=hw_id,
            title=title,
            subject=subject,
            description=description or title,
            due_date=due_date,
            estimated_minutes=estimated_minutes,
            difficulty=difficulty,
            importance=importance,
            priority_score=priority_score,
            tags=tags,
            raw_text=raw_text
        )

    def _estimate_duration(self, raw_text: str, tags: List[str]) -> int:
        """Estime la durée nécessaire en minutes"""
        # Logique d'estimation basique
        base_duration = 60

        # Ajuster selon les tags
        if any(tag.lower() in ["contrôle", "examen", "ds"] for tag in tags):
            base_duration = 120
        elif any(tag.lower() in ["dm", "devoir maison"] for tag in tags):
            base_duration = 90
        elif any(tag.lower() in ["exercice", "exos"] for tag in tags):
            base_duration = 45
        elif any(tag.lower() in ["lecture", "lire"] for tag in tags):
            base_duration = 30

        # Ajuster selon la longueur du texte
        if len(raw_text) > 200:
            base_duration += 30

        return base_duration

    def _estimate_difficulty(self, raw_text: str, tags: List[str], duration: int) -> str:
        """Estime la difficulté du devoir"""
        # Mots-clés difficiles
        difficult_keywords = ["complexe", "difficile", "approfondi", "analyse", "synthèse"]
        easy_keywords = ["simple", "facile", "rapide", "lecture"]

        raw_lower = raw_text.lower()

        if any(kw in raw_lower for kw in difficult_keywords):
            return "difficile"
        elif any(kw in raw_lower for kw in easy_keywords):
            return "facile"
        elif duration > 90:
            return "difficile"
        elif duration < 45:
            return "facile"
        else:
            return "moyen"

    def _calculate_importance(
        self,
        due_date: Optional[str],
        duration: int,
        difficulty: str,
        tags: List[str],
        user_importance: Optional[float]
    ) -> float:
        """
        Calcule l'importance (0..1) en utilisant les poids configurés
        """
        # Proximité de la deadline
        proximity_metric = 0.5
        if due_date:
            due = datetime.strptime(due_date, "%Y-%m-%d")
            days_until_due = (due - self.today).days
            if days_until_due < 0:
                proximity_metric = 1.0  # Déjà en retard !
            else:
                proximity_metric = 1.0 / (1 + days_until_due)

        # Importance utilisateur
        user_importance_metric = user_importance if user_importance is not None else 0.0

        # Difficulté et durée
        difficulty_val = self.DIFFICULTY_VALUES.get(difficulty, 0.6)
        # Normaliser la durée par rapport à 180 min
        duration_normalized = min(duration / 180.0, 1.0)
        difficulty_duration_metric = (difficulty_val + duration_normalized) / 2.0

        # Calculer l'importance de base
        importance_base = (
            self.w_proximity * proximity_metric +
            self.w_user_importance * user_importance_metric +
            self.w_difficulty_and_duration * difficulty_duration_metric
        )

        # Bonus mots-clés
        bonus = 0.0
        if any(tag.lower() in ["contrôle", "examen", "ds"] for tag in tags):
            bonus = self.keyword_bonus

        # Clamper entre 0 et 1
        importance = max(0.0, min(1.0, importance_base + bonus))

        return round(importance, 2)

    def _calculate_priority_score(self, importance: float, due_date: Optional[str]) -> int:
        """
        Calcule le score de priorité (0..100) avec léger ajustement pour proximité
        """
        base_score = round(importance * 100)

        # Ajustement de ±5 selon la proximité
        if due_date:
            due = datetime.strptime(due_date, "%Y-%m-%d")
            days_until_due = (due - self.today).days
            if days_until_due <= 1:
                base_score = min(100, base_score + 5)
            elif days_until_due <= 3:
                base_score = min(100, base_score + 3)

        return base_score

    def generate_schedule(self) -> Dict[str, Any]:
        """
        Point d'entrée principal : génère le planning complet
        Retourne le JSON structuré conforme au schéma
        """
        # 1. Normaliser tous les devoirs
        for hw_raw in self.homeworks_raw:
            hw = self.normalize_homework(hw_raw)
            self.homeworks.append(hw)

        # 2. Trier par priority_score décroissant
        self.homeworks.sort(key=lambda h: h.priority_score, reverse=True)

        # 3. Allouer les sessions sur les jours disponibles
        self._allocate_sessions()

        # 4. Construire le résultat final
        result = self._build_output()

        return result

    def _allocate_sessions(self):
        """
        Répartit les devoirs sur les jours disponibles en respectant les contraintes
        """
        # Dictionnaire date -> minutes restantes
        availability_remaining = self.availability.copy()

        # Appliquer le buffer
        for date in availability_remaining:
            buffer_minutes = int(availability_remaining[date] * self.buffer_percent / 100)
            availability_remaining[date] -= buffer_minutes

        # Dictionnaire date -> liste de sessions
        sessions_by_date: Dict[str, List[Session]] = {}
        for date in self.availability:
            sessions_by_date[date] = []

        # Pour chaque devoir (trié par priorité)
        for hw in self.homeworks:
            remaining_minutes = hw.estimated_minutes

            # Déterminer les jours valides pour ce devoir
            valid_dates = self._get_valid_dates_for_homework(hw)

            if not valid_dates:
                # Conflit : pas de dates disponibles
                self._add_conflict(hw, "Aucune date disponible avant la deadline")
                continue

            # Répartir les minutes sur les jours valides
            allocated = False
            if self.prefer_spread:
                # Répartir uniformément
                minutes_per_day = remaining_minutes / len(valid_dates)
                for date in valid_dates:
                    if remaining_minutes <= 0:
                        break

                    available = availability_remaining.get(date, 0)
                    if available <= 0:
                        continue

                    # Allouer au maximum minutes_per_day ou ce qui reste
                    to_allocate = min(remaining_minutes, int(minutes_per_day), available)
                    to_allocate = min(to_allocate, self.max_session_minutes)

                    if to_allocate >= self.preferred_session_min:
                        session = self._create_session(hw, to_allocate, date)
                        sessions_by_date[date].append(session)
                        availability_remaining[date] -= to_allocate
                        remaining_minutes -= to_allocate
                        allocated = True
            else:
                # Privilégier les jours proches de la deadline
                for date in valid_dates:
                    if remaining_minutes <= 0:
                        break

                    available = availability_remaining.get(date, 0)
                    if available <= 0:
                        continue

                    to_allocate = min(remaining_minutes, available, self.max_session_minutes)

                    if to_allocate >= self.preferred_session_min:
                        session = self._create_session(hw, to_allocate, date)
                        sessions_by_date[date].append(session)
                        availability_remaining[date] -= to_allocate
                        remaining_minutes -= to_allocate
                        allocated = True

            # Seulement ajouter un conflit si vraiment pas alloué
            if not allocated or remaining_minutes > 10:  # Marge de tolérance de 10 min
                # Conflit : pas assez de temps alloué
                if remaining_minutes > 10:
                    total_available = sum(availability_remaining.get(d, 0) for d in valid_dates)
                    allocated_minutes = hw.estimated_minutes - remaining_minutes
                    self._add_conflict(hw, "Disponibilités insuffisantes avant la deadline",
                                     allocated_minutes, remaining_minutes)

        # Construire le planning jour par jour
        for date in sorted(sessions_by_date.keys()):
            sessions = sessions_by_date[date]
            if not sessions:
                continue

            total_allocated = sum(s.duration_minutes for s in sessions)
            available = self.availability.get(date, 0)

            # Cartouche basé sur le sujet dominant
            dominant_subject = self._get_dominant_subject(sessions)
            cartouche = self._get_cartouche(dominant_subject)

            # Résumé et conseils
            daily_summary = self._generate_daily_summary(sessions, total_allocated)
            advice = self._generate_advice(sessions, total_allocated, available)

            day_schedule = DaySchedule(
                date=date,
                day_total_allocated_minutes=total_allocated,
                available_minutes=available,
                cartouche=cartouche,
                sessions=sessions,
                daily_summary=daily_summary,
                advice=advice
            )
            self.schedule.append(day_schedule)

    def _get_valid_dates_for_homework(self, hw: Homework) -> List[str]:
        """Retourne la liste des dates valides pour un devoir"""
        if not hw.due_date:
            # Pas de deadline : utiliser toutes les dates futures disponibles
            return sorted([
                d for d in self.availability.keys()
                if datetime.strptime(d, "%Y-%m-%d") >= self.today
            ])

        due = datetime.strptime(hw.due_date, "%Y-%m-%d")

        # Dates entre aujourd'hui et due_date (inclus)
        valid = []
        for date_str in self.availability.keys():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if self.today <= date_obj <= due:
                valid.append(date_str)

        return sorted(valid)

    def _create_session(self, hw: Homework, duration: int, date: str) -> Session:
        """Crée une session de travail"""
        color, emoji = self.SUBJECT_MAPPING.get(
            hw.subject.lower(),
            self.SUBJECT_MAPPING["default"]
        )

        # Générer start_time si time_preferences disponible
        start_time = None
        if self.time_preferences:
            start_time = self._estimate_start_time(date, duration)

        short_desc = hw.title[:30] + ("..." if len(hw.title) > 30 else "")

        return Session(
            homework_id=hw.id,
            start_time=start_time,
            duration_minutes=duration,
            short_task_desc=short_desc,
            emoji=emoji,
            color=color
        )

    def _estimate_start_time(self, date: str, duration: int) -> Optional[str]:
        """Estime une heure de début plausible dans les fenêtres préférées"""
        windows = self.time_preferences.get("preferred_start_windows", [])
        if not windows:
            earliest = self.time_preferences.get("earliest_hour", 17)
            return f"{earliest:02d}:00"

        # Prendre la première fenêtre
        window = windows[0]
        return window[0]

    def _get_dominant_subject(self, sessions: List[Session]) -> str:
        """Retourne le sujet dominant d'une journée"""
        # Compter les minutes par sujet
        subject_minutes = {}
        for session in sessions:
            hw = next((h for h in self.homeworks if h.id == session.homework_id), None)
            if hw:
                subject = hw.subject.lower()
                subject_minutes[subject] = subject_minutes.get(subject, 0) + session.duration_minutes

        if not subject_minutes:
            return "default"

        return max(subject_minutes, key=subject_minutes.get)

    def _get_cartouche(self, subject: str) -> Dict[str, str]:
        """Retourne le cartouche (emoji + couleur) pour un sujet"""
        color, emoji = self.SUBJECT_MAPPING.get(subject.lower(), self.SUBJECT_MAPPING["default"])

        # Capitaliser le sujet pour le label
        label = subject.capitalize()

        return {
            "emoji": emoji,
            "color": color,
            "label": label
        }

    def _generate_daily_summary(self, sessions: List[Session], total_minutes: int) -> str:
        """Génère un résumé quotidien"""
        nb_sessions = len(sessions)
        subjects = set()
        for session in sessions:
            hw = next((h for h in self.homeworks if h.id == session.homework_id), None)
            if hw:
                subjects.add(hw.subject)

        subjects_str = ", ".join(sorted(subjects))

        return f"Aujourd'hui : {nb_sessions} session(s) de travail ({total_minutes} min) en {subjects_str}."

    def _generate_advice(self, sessions: List[Session], total_minutes: int, available: int) -> List[str]:
        """Génère 3-6 conseils pratiques pour la journée"""
        advice = []

        # Conseil sur la charge de travail
        load_percent = (total_minutes / available * 100) if available > 0 else 0
        if load_percent > 80:
            advice.append("Journée chargée : prévois des pauses toutes les 50 minutes.")
        elif load_percent < 40:
            advice.append("Journée légère : profite du temps libre pour réviser en avance.")
        else:
            advice.append("Charge équilibrée : reste concentré et tu termineras à temps.")

        # Conseil selon le nombre de sessions
        if len(sessions) > 3:
            advice.append("Plusieurs matières aujourd'hui : alterne pour rester motivé.")

        # Conseil selon les difficultés
        difficult_sessions = [
            s for s in sessions
            if (hw := next((h for h in self.homeworks if h.id == s.homework_id), None))
            and hw.difficulty == "difficile"
        ]
        if difficult_sessions:
            advice.append("Tâches difficiles prévues : commence par celles-ci quand tu es le plus frais.")

        # Conseil général
        advice.append("Prépare ton espace de travail avant de commencer.")
        advice.append("Éteins les distractions (téléphone, réseaux sociaux).")

        # Limiter à 6 conseils max
        return advice[:6]

    def _add_conflict(self, hw: Homework, reason: str, allocated: int = 0, missing: int = 0):
        """Ajoute un conflit à la liste"""
        solutions = self._generate_solutions(hw, reason, allocated, missing)

        conflict = Conflict(
            homework_id=hw.id,
            reason=reason,
            required_minutes=hw.estimated_minutes,
            available_before_due=allocated,
            solutions=solutions
        )
        self.conflicts.append(conflict)

    def _generate_solutions(self, hw: Homework, reason: str, allocated: int, missing: int) -> List[str]:
        """Génère 3 solutions concrètes pour résoudre un conflit"""
        solutions = []

        if missing <= 0:
            missing = max(10, hw.estimated_minutes - allocated)

        solutions.append(
            f"Solution 1 : Augmenter la disponibilité journalière de {int(missing / 3)} min "
            f"sur 3 jours pour combler le manque de {missing} minutes."
        )

        if allocated > 0:
            solutions.append(
                f"Solution 2 : Réduire le périmètre du devoir en ciblant les exercices à forte valeur "
                f"({allocated} min déjà allouées pourraient suffire pour l'essentiel)."
            )
        else:
            solutions.append(
                f"Solution 2 : Réorganiser les priorités pour libérer du temps avant la deadline."
            )

        solutions.append(
            f"Solution 3 : Réorganiser d'autres sessions moins prioritaires pour libérer "
            f"{missing} minutes supplémentaires, ou décaler la deadline si possible."
        )

        return solutions

    def _build_output(self) -> Dict[str, Any]:
        """Construit le JSON de sortie conforme au schéma"""
        total_estimated = sum(hw.estimated_minutes for hw in self.homeworks)
        total_available = sum(self.availability.values())

        meta = {
            "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+01:00"),
            "today": self.today.strftime("%Y-%m-%d"),
            "total_homeworks": len(self.homeworks),
            "total_estimated_minutes": total_estimated,
            "total_available_minutes": total_available,
            "weights_used": {
                "w_proximity": self.w_proximity,
                "w_user_importance": self.w_user_importance,
                "w_difficulty_and_duration": self.w_difficulty_and_duration,
                "keyword_bonus": self.keyword_bonus
            }
        }

        # Convertir les dataclasses en dicts
        homeworks_list = [asdict(hw) for hw in self.homeworks]
        for hw_dict in homeworks_list:
            hw_dict.pop("raw_text", None)  # Enlever raw_text du résultat final

        schedule_list = []
        for day in self.schedule:
            day_dict = asdict(day)
            # Convertir les sessions
            day_dict["sessions"] = [asdict(s) for s in day.sessions]
            schedule_list.append(day_dict)

        conflicts_list = [asdict(c) for c in self.conflicts]

        return {
            "meta": meta,
            "homeworks": homeworks_list,
            "schedule": schedule_list,
            "conflicts": conflicts_list
        }


def main():
    """Point d'entrée CLI"""
    if len(sys.argv) < 2:
        print("Usage: python school_schedule_generator.py <input.json>")
        print("Le JSON d'entrée doit contenir : today, availability, homeworks_raw, weights, etc.")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    generator = SchoolScheduleGenerator(config)
    result = generator.generate_schedule()

    # Afficher le JSON résultat (et seulement le JSON)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
