import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Scoring weights shared by both implementations
MOOD_WEIGHT = 3
GENRE_WEIGHT = 2
ENERGY_WEIGHT = 2
ACOUSTIC_WEIGHT = 1
TOTAL_WEIGHT = MOOD_WEIGHT + GENRE_WEIGHT + ENERGY_WEIGHT + ACOUSTIC_WEIGHT

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        mood = 1.0 if song.mood == user.favorite_mood else 0.0
        genre = 1.0 if song.genre == user.favorite_genre else 0.0
        energy = 1.0 - abs(song.energy - user.target_energy)
        is_acoustic = song.acousticness >= 0.5
        acoustic = 1.0 if is_acoustic == user.likes_acoustic else 0.0

        weighted = (
            MOOD_WEIGHT * mood
            + GENRE_WEIGHT * genre
            + ENERGY_WEIGHT * energy
            + ACOUSTIC_WEIGHT * acoustic
        )
        return weighted / TOTAL_WEIGHT

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.mood == user.favorite_mood:
            reasons.append(f"matches your favorite mood ({user.favorite_mood})")
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({user.favorite_genre})")
        if abs(song.energy - user.target_energy) <= 0.2:
            reasons.append("energy is close to what you want")
        if (song.acousticness >= 0.5) == user.likes_acoustic:
            reasons.append("acoustic feel fits your taste")

        score = self._score(user, song)
        if not reasons:
            return f"'{song.title}' scores {score:.2f} but doesn't strongly match your preferences."
        return f"'{song.title}' scores {score:.2f} because it " + ", ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    numeric = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song = dict(row)
            song["id"] = int(song["id"])
            for key in numeric:
                song[key] = float(song[key])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    favorite_mood = user_prefs.get("mood", user_prefs.get("favorite_mood"))
    favorite_genre = user_prefs.get("genre", user_prefs.get("favorite_genre"))
    target_energy = user_prefs.get("energy", user_prefs.get("target_energy", 0.5))
    likes_acoustic = user_prefs.get("likes_acoustic", False)

    reasons: List[str] = []

    mood = 1.0 if song["mood"] == favorite_mood else 0.0
    if mood:
        reasons.append(f"matches your favorite mood ({favorite_mood})")

    genre = 1.0 if song["genre"] == favorite_genre else 0.0
    if genre:
        reasons.append(f"matches your favorite genre ({favorite_genre})")

    energy = 1.0 - abs(song["energy"] - target_energy)
    if abs(song["energy"] - target_energy) <= 0.2:
        reasons.append("energy is close to what you want")

    is_acoustic = song["acousticness"] >= 0.5
    acoustic = 1.0 if is_acoustic == likes_acoustic else 0.0
    if acoustic:
        reasons.append("acoustic feel fits your taste")

    weighted = (
        MOOD_WEIGHT * mood
        + GENRE_WEIGHT * genre
        + ENERGY_WEIGHT * energy
        + ACOUSTIC_WEIGHT * acoustic
    )
    return weighted / TOTAL_WEIGHT, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
