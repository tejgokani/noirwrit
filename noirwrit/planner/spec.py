"""Story questionnaire and spec.json.

Every field is optional. Blank fields are filled from period-appropriate pools
with a seeded RNG, avoiding names already used in earlier stories.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field

GENRES = ("noir", "classic_detective", "thriller")

QUESTIONS = [
    {"key": "chapters", "label": "How many chapters?", "type": "int", "default": 5, "min": 1, "max": 40},
    {"key": "genre", "label": "Genre", "type": "choice", "choices": list(GENRES), "default": "noir"},
    {"key": "vibe", "label": "Vibe", "type": "text", "placeholder": "rain-soaked, cynical, slow burn"},
    {"key": "setting", "label": "Setting", "type": "text", "placeholder": "a waterfront city"},
    {"key": "era", "label": "Era", "type": "text", "placeholder": "1920s"},
    {"key": "detective_type", "label": "Detective type", "type": "text", "placeholder": "private eye"},
    {"key": "detective_name", "label": "Detective name", "type": "text"},
    {"key": "victim", "label": "Victim", "type": "text", "placeholder": "a shipping clerk"},
    {"key": "culprit", "label": "Culprit", "type": "text", "placeholder": "the victim's partner"},
    {"key": "motive", "label": "Motive", "type": "text", "placeholder": "an insurance policy"},
    {"key": "twist", "label": "Twist", "type": "text", "placeholder": "the victim faked an earlier death"},
    {"key": "pov", "label": "Point of view", "type": "choice", "choices": ["first", "third"], "default": "first"},
    {"key": "tone", "label": "Tone", "type": "text", "placeholder": "hardboiled"},
    {"key": "chapter_words", "label": "Words per chapter", "type": "int", "default": 3000, "min": 500, "max": 8000},
]

POOLS = {
    "noir": {
        "setting": ["a waterfront city", "a rain-slick river town", "a city of speakeasies and fog",
                    "a mining town gone sour", "the docks and back rooms of a port city"],
        "era": ["1920s", "1928", "the late 1920s", "Prohibition years"],
        "detective_type": ["private eye", "agency operative", "ex-cop working for hire", "insurance investigator"],
        "vibe": ["rain-soaked and cynical", "smoky and tense", "cold and bitter", "fast and violent"],
        "tone": ["hardboiled", "terse and hardboiled", "weary and wry"],
        "places": ["the agency office", "a dockside warehouse", "a speakeasy on Front Street", "the Hotel Belvedere",
                   "a rooming house", "the police station", "a pier in the fog", "a pawnshop", "a nightclub"],
    },
    "classic_detective": {
        "setting": ["a country house in Surrey", "foggy London", "a cathedral town", "a seaside resort", "an Oxford college"],
        "era": ["1890s", "the Edwardian years", "1910s", "1920s"],
        "detective_type": ["consulting detective", "Scotland Yard inspector", "amateur sleuth", "village priest"],
        "vibe": ["genteel and uneasy", "fog-bound and cerebral", "orderly on the surface"],
        "tone": ["measured and observant", "dry and precise", "warm with a sharp edge"],
        "places": ["the drawing room", "the library", "the study", "the inn", "the railway station",
                   "the rectory", "the garden", "Baker Street rooms", "the coroner's office"],
    },
    "thriller": {
        "setting": ["a continental express train", "a port full of spies", "London under a threat", "a mountain hotel"],
        "era": ["1910s", "the years before the war", "1920s"],
        "detective_type": ["secret service agent", "reluctant amateur", "newspaper man", "gentleman adventurer"],
        "vibe": ["breathless", "paranoid and fast", "a race against time"],
        "tone": ["urgent", "taut", "brisk and dangerous"],
        "places": ["a railway carriage", "an embassy ballroom", "a harbour office", "a mountain pass",
                   "a cipher room", "a hotel lobby", "a back alley", "a moored yacht"],
    },
}

VICTIMS = ["a shipping clerk", "a wealthy widow", "a crooked alderman", "a nightclub singer", "a bank cashier",
           "a retired colonel", "a jeweller", "a bookmaker", "a young heiress", "a ship's captain", "a city councilman"]
CULPRITS = ["the victim's business partner", "the trusted secretary", "the grieving spouse", "the family doctor",
            "a police captain on the take", "the victim's brother", "the charming client", "the quiet lodger"]
MOTIVES = ["an insurance policy", "a blackmail letter", "a hidden inheritance", "a debt that could not be paid",
           "revenge for an old betrayal", "a stolen shipment", "a secret marriage", "a forged will"]
TWISTS = ["the first victim was not the intended target", "the client hired the detective to frame someone",
          "two people committed the crime without knowing about each other", "the victim faked an earlier death",
          "the key witness is the culprit's accomplice", "the murder weapon was planted twice",
          "the time of death was moved by an hour"]

FIRST = {
    "m": ["Sam", "Nick", "Frank", "Joe", "Eddie", "Walter", "Arthur", "Harry", "Jack", "Leo", "Vic", "Gus", "Ned",
          "Charles", "Edmund", "Hugh", "Percy", "Tom", "Ray", "Lou", "Dan", "Owen", "Felix", "Martin"],
    "f": ["Ruth", "Iris", "Mae", "Vera", "Nora", "Edith", "Alice", "Grace", "Lola", "Hazel", "Flora", "Clara", "Ada",
          "Della", "Irene", "Marion", "Opal", "Stella", "Violet", "Lena", "Pearl"],
}
LAST = ["Kade", "Marlow", "Brennan", "Doyle", "Hale", "Crane", "Vance", "Moran", "Sloane", "Rourke", "Galt", "Ashby",
        "Pryor", "Thorne", "Quill", "Ferris", "Mercer", "Lacey", "Blount", "Harrow", "Keene", "Wynn", "Corder",
        "Fenwick", "Dorsey", "Malloy", "Reardon", "Stroud", "Penrose", "Calloway", "Hatch", "Danner", "Shea"]


@dataclass
class Spec:
    chapters: int = 5
    genre: str = "noir"
    vibe: str = ""
    setting: str = ""
    era: str = ""
    detective_type: str = ""
    detective_name: str = ""
    victim: str = ""
    culprit: str = ""
    motive: str = ""
    twist: str = ""
    pov: str = "first"
    tone: str = ""
    chapter_words: int = 3000
    seed: int = 0
    premise: str = ""
    extra: dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_dict(cls, d: dict) -> Spec:
        known = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        s = cls(**known)
        s.chapters = int(s.chapters or 5)
        s.chapter_words = int(s.chapter_words or 3000)
        if s.genre not in GENRES:
            s.genre = "noir"
        return s


def make_name(rng: random.Random, used: set[str], gender: str | None = None) -> str:
    g = gender or rng.choice("mf")
    for _ in range(200):
        n = f"{rng.choice(FIRST[g])} {rng.choice(LAST)}"
        if n not in used and n.split()[1] not in {u.split()[-1] for u in used}:
            used.add(n)
            return n
    n = f"{rng.choice(FIRST[g])} {rng.choice(LAST)}-{len(used)}"
    used.add(n)
    return n


def fill(spec: Spec, used_names: set[str] | None = None) -> Spec:
    """Fill blanks from the genre pools. Deterministic for a given seed."""
    rng = random.Random(spec.seed)
    pool = POOLS[spec.genre]
    for key in ("setting", "era", "detective_type", "vibe", "tone"):
        if not getattr(spec, key):
            setattr(spec, key, rng.choice(pool[key]))
    spec.victim = spec.victim or rng.choice(VICTIMS)
    spec.culprit = spec.culprit or rng.choice(CULPRITS)
    spec.motive = spec.motive or rng.choice(MOTIVES)
    spec.twist = spec.twist or rng.choice(TWISTS)
    used = set(used_names or ())
    if not spec.detective_name:
        spec.detective_name = make_name(rng, used, "m" if rng.random() < 0.75 else "f")
    if not spec.premise:
        spec.premise = (f"In {spec.setting}, {spec.era}, {spec.detective_name}, a {spec.detective_type}, "
                        f"investigates the death of {spec.victim}.")
    return spec
