# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**  

---

## 2. Intended Use  

This recommender takes a user's stated music taste (favorite genre, favorite mood, 
target energy, and an acoustic preference) and ranks a fixed catalog of songs by how 
well each one matches. It's a classroom simulation, not a production system — it 
assumes the user's stated preferences are complete and static, and it has no way to 
learn from listening behavior or feedback over time.

**Not intended for**: real users, real deployment, or any decision where getting 
a bad recommendation has real consequences. It has no safeguards against confidently 
recommending something that contradicts a stated preference (see Limitations), so it 
should not be treated as more reliable than it actually is.

---

## 3. How the Model Works  

Every song gets scored against the user's profile using four factors: whether the 
genre matches exactly, whether the mood matches exactly, how close the song's energy 
level is to what the user wants, and whether the song's "acoustic-ness" matches the 
user's stated preference. Each factor is worth a different number of points — mood 
matters most, then genre and energy equally, then the acoustic preference least — and 
the points are added up and scaled to a score between 0 and 1. Songs are then sorted 
from highest to lowest score, and the top few are shown to the user along with a 
plain-language explanation of which factors it matched on.

---

## 4. Data  

The catalog has 18 songs, starting from 10 in the original starter file and expanded 
with 8 more covering genres and moods that weren't represented yet (hip-hop, folk, 
classical, metal, R&B, country, EDM, blues; moods like angry, nostalgic, melancholic, 
triumphant, dreamy, energetic). Even after expanding, most genres and moods still only 
appear in one song each — only pop and lofi have more than one entry. There's no 
audio, lyrics, or actual listening-history data; every feature is a hand-assigned 
number or label.

---

## 5. Strengths  

The system works best for users whose taste maps cleanly onto a single genre/mood 
combination that's well represented in the catalog — the Deep Intense Rock profile 
is a good example, landing a confident top match (score 1.00) because rock, intense, 
high energy, and non-acoustic all line up on one real song. It also correctly 
separates opposite tastes: High-Energy Pop and Chill Lofi profiles produced almost 
entirely different top-5 lists, which matches intuition. The explanation strings are 
genuinely useful — they let you see exactly which factors drove a score instead of 
treating the ranking as a black box.

---

## 6. Limitations and Bias 

This recommender uses exact-string matching for genre and mood (75% of the total 
score), so it can never give partial credit to musically adjacent choices — a pop 
fan scores zero on indie pop or synthwave, even though these are close in style. 
This is a textbook filter-bubble mechanism: it only re-serves the one label already 
in the user's profile, with no way to explore related tastes.

The dataset also makes this worse for niche users: most genres and moods appear in 
only one song, so a user with an uncommon combination (e.g. metal/triumphant) can 
never earn a real mood or genre match, and their ranking collapses onto energy 
proximity alone — the system effectively can't represent their taste.

Finally, energy scores show an unexpected "dead zone": the catalog has no songs 
between energy 0.46 and 0.72, so a user targeting mid-range energy (~0.5, which is 
also this system's default when unspecified) is maximally distant from almost every 
song in the catalog and is systematically under-served compared to high- or 
low-energy listeners.

---

## 7. Evaluation  


I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an 
adversarial profile ("The Contradiction") designed to expose weaknesses.

- **High-Energy Pop vs. Chill Lofi**: the two profiles produced almost opposite 
  top results (Sunrise City/high-energy pop vs. Library Rain/low-energy lofi), 
  which makes sense — mood and genre are on opposite ends for these two, and 
  energy targets (0.9 vs 0.3) pull toward different songs. This is where the 
  system works as intended.

- **Deep Intense Rock**: produced a clean, confident top pick (Storm Runner, 
  score 1.00) with a perfect match on all four factors — the easiest case for 
  the recommender because rock/intense/high-energy/non-acoustic all line up on 
  one song in the catalog.

- **The Contradiction (classical/melancholic/energy 0.95)**: this is the most 
  surprising result. Despite explicitly asking for high energy, the top pick 
  (Nocturne in Ash) is the catalog's *lowest*-energy song, because mood+genre 
  match (5 of 8 points) outweighs a total energy miss. I even doubled the energy 
  weight (2→4) and the same song still won, by a margin of only 0.02 — showing 
  the bias comes from binary vs. continuous scoring, not just weight size.

**In plain language**: this recommender is good at finding songs that match a 
user's stated genre and mood exactly, but it will confidently recommend something 
that contradicts an explicit numeric preference (like energy) if the categorical 
labels match strongly enough. It doesn't know when it's giving someone the opposite 
of what they asked for — it just adds up points.

---

## 8. Future Work  

- Replace exact-match genre/mood with a similarity table (e.g. rock and metal count 
  as a partial match) so near-misses aren't scored the same as total misses.
- Add a diversity term to the ranking step so recommendations don't collapse onto a 
  single label the user already stated, reducing the filter-bubble effect.
- Detect "no real match" cases (e.g. a genre/mood not in the catalog at all) and 
  say so explicitly instead of confidently returning low-scoring songs.
- Fix the explanation/score mismatch — always show a reason for every point actually 
  earned, including partial energy credit, not just close matches.

---

## 9. Personal Reflection

The biggest learning moment was realizing that doubling the energy weight barely 
changed the "Contradiction" test result (0.02-point margin) — I expected weight 
adjustments to fix the bias, but the real problem was that mood/genre give all-or-
nothing points while energy gives partial credit, so no amount of weight-tuning could 
fully fix it. That's a different kind of bug than I expected to find.

AI tools (Claude Code) helped most with implementation speed — writing the scoring 
logic, running multiple test profiles, and finding biases I hadn't thought to look 
for (like the "dead zone" in mid-range energy values, which I never would have 
noticed just by eyeballing the CSV). I had to double-check it most closely when it 
made claims about *why* a result happened — one of its early explanations for a score 
was actually slightly wrong about which term contributed the points, and re-reading 
the code myself caught it.

What surprised me most is how "confident" and human the recommendations feel even 
though the underlying logic is just adding up four numbers. Scores like 0.98 or 1.00 
read as authoritative, but they're really just exact-match booleans plus one distance 
calculation — there's no understanding of music at all, just arithmetic dressed up as 
taste.

If I extended this project, I'd start with a genre/mood similarity table instead of 
exact matching, since that's the single change most likely to fix the biases I found.