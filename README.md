# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real recommendation systems like Spotify combine collaborative filtering (based on what similar users like) and content-based filtering (based on song attributes). This project implements only content-based filtering, since we only have song attribute data. My recommender prioritizes mood match most heavily, followed by genre match and energy closeness, with acoustic preference weighted least.

This simulation's `Song` and `UserProfile` objects use:
- `genre`, `mood` — categorical, must match exactly
- `energy` — numeric (0-1), scored by closeness to target
- `acousticness` — numeric (0-1), thresholded at 0.5 to infer whether a song "feels acoustic"

### Algorithm Recipe
- Mood match: +3.0 (exact match only)
- Genre match: +2.0 (exact match only)
- Energy closeness: +2.0 × (1 - |song.energy - target_energy|)
- Acoustic preference match: +1.0 (song treated as "acoustic" if acousticness ≥ 0.5)
- Total normalized by dividing by 8.0

### Potential Bias
This system uses exact-match equality for genre and mood, so it can't express genre
"adjacency" — a metal song and an EDM song score identically low against a rock
profile (both 0.36), even though metal is sonically closer to rock. The scorer
also lets mood outweigh genre (weight 3 vs 2), so a pop song matching mood can
outscore a rock-adjacent genre that doesn't share the exact mood. In short: this
recommender rewards exact taste matches well, but treats every "near miss" the
same as a "total miss."

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output


### Profile 1 — High-Energy Pop
`{"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.9, "likes_acoustic": False}`

```
Loaded songs: 18

Top recommendations:

Sunrise City - Score: 0.98
Because: mood match (+3.0), genre match (+2.0), energy closeness (+1.8), acoustic match (+1.0)

Rooftop Lights - Score: 0.71
Because: mood match (+3.0), energy closeness (+1.7), acoustic match (+1.0)

Gym Hero - Score: 0.62
Because: genre match (+2.0), energy closeness (+1.9), acoustic match (+1.0)

Storm Runner - Score: 0.37
Because: energy closeness (+2.0), acoustic match (+1.0)

Concrete Kingdom - Score: 0.37
Because: energy closeness (+2.0), acoustic match (+1.0)
```

### Profile 2 — Chill Lofi
`{"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.3, "likes_acoustic": True}`

```
Loaded songs: 18

Top recommendations:

Library Rain - Score: 0.99
Because: mood match (+3.0), genre match (+2.0), energy closeness (+1.9), acoustic match (+1.0)

Midnight Coding - Score: 0.97
Because: mood match (+3.0), genre match (+2.0), energy closeness (+1.8), acoustic match (+1.0)

Spacewalk Thoughts - Score: 0.74
Because: mood match (+3.0), energy closeness (+2.0), acoustic match (+1.0)

Focus Flow - Score: 0.60
Because: genre match (+2.0), energy closeness (+1.8), acoustic match (+1.0)

Letters to Autumn - Score: 0.37
Because: energy closeness (+2.0), acoustic match (+1.0)
```

### Profile 3 — Deep Intense Rock
`{"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.9, "likes_acoustic": False}`

```
Loaded songs: 18

Top recommendations:

Storm Runner - Score: 1.00
Because: mood match (+3.0), genre match (+2.0), energy closeness (+2.0), acoustic match (+1.0)

Gym Hero - Score: 0.74
Because: mood match (+3.0), energy closeness (+1.9), acoustic match (+1.0)

Concrete Kingdom - Score: 0.37
Because: energy closeness (+2.0), acoustic match (+1.0)

Circuit Sunrise - Score: 0.36
Because: energy closeness (+1.9), acoustic match (+1.0)

Ironclad Dawn - Score: 0.36
Because: energy closeness (+1.9), acoustic match (+1.0)
```

### Profile 4 — The Contradiction (adversarial)
`{"favorite_genre": "classical", "favorite_mood": "melancholic", "target_energy": 0.95, "likes_acoustic": False}`

```
Loaded songs: 18

Top recommendations:

Nocturne in Ash - Score: 0.70
Because: mood match (+3.0), genre match (+2.0)

Rainwater Blues - Score: 0.48
Because: mood match (+3.0)

Ironclad Dawn - Score: 0.37
Because: energy closeness (+2.0), acoustic match (+1.0)

Circuit Sunrise - Score: 0.37
Because: energy closeness (+2.0), acoustic match (+1.0)

Gym Hero - Score: 0.37
Because: energy closeness (+2.0), acoustic match (+1.0)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Experiment: doubled energy weight (2→4), halved genre weight (2→1)**

Even with energy weighted 2x higher than its original value, the "Contradiction" 
profile (target_energy: 0.95) still ranked the lowest-energy song (Nocturne in Ash, 
energy 0.24) first — 0.57 vs 0.55 for the closest energy-matched competitor, a 0.02 
margin. This shows the bias isn't simply a matter of energy being underweighted: it's 
that mood/genre are binary exact-matches while energy is continuous, so a categorical 
hit is worth more per point spent than a numeric near-miss, almost regardless of the 
weight ratio.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



