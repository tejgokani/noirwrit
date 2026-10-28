"""Rule-based outline planner: cast, clue ledger, and beats per chapter.

Structure: the crime and the hook, an investigation that plants true clues and
red herrings, a midpoint twist, the red herring exposed, then the reveal that
ties every true clue to the culprit. Plot logic lives here, not in the weights.
"""

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass, field

from noirwrit.planner.spec import POOLS, Spec, make_name

WORDS_PER_BEAT = 500

CLUE_TEMPLATES = [
    "a matchbook from {place}", "a torn railway ticket", "mud of an unusual colour on a shoe",
    "a letter with the last page missing", "a key that fits no door in the house", "a stopped wristwatch",
    "cigarette ash of a brand {culprit_short} smokes", "a pawn ticket", "a telephone number written on a cuff",
    "a bank book with one large withdrawal", "a smear of greasepaint", "a glove for the left hand only",
    "a receipt dated the night of the murder", "a photograph with one face cut out",
]


@dataclass
class Character:
    name: str
    role: str  # detective | victim | culprit | suspect | witness | ally
    description: str
    gender: str = "m"
    alive: bool = True
    dies_in_chapter: int | None = None


@dataclass
class Clue:
    id: str
    text: str
    points_to: str  # character name
    true: bool
    planted_chapter: int = 0
    revealed_chapter: int = 0


@dataclass
class Beat:
    chapter: int
    num: int
    kind: str
    summary: str
    lead: str
    characters: list[str]
    place: str
    clues: list[str] = field(default_factory=list)
    target_words: int = WORDS_PER_BEAT


@dataclass
class Outline:
    title: str
    cast: list[Character]
    clues: list[Clue]
    chapters: list[dict]  # {num, title, beats: [Beat]}

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "cast": [asdict(c) for c in self.cast],
            "clues": [asdict(c) for c in self.clues],
            "chapters": [{"num": ch["num"], "title": ch["title"], "beats": [asdict(b) for b in ch["beats"]]}
                         for ch in self.chapters],
        }

    @classmethod
    def from_dict(cls, d: dict) -> Outline:
        return cls(
            title=d["title"],
            cast=[Character(**c) for c in d["cast"]],
            clues=[Clue(**c) for c in d["clues"]],
            chapters=[{"num": ch["num"], "title": ch["title"], "beats": [Beat(**b) for b in ch["beats"]]}
                      for ch in d["chapters"]],
        )

    def by_role(self, role: str) -> list[Character]:
        return [c for c in self.cast if c.role == role]

    def char(self, role: str) -> Character:
        return self.by_role(role)[0]


TITLE_PATTERNS = {
    "noir": ["The {thing} on {street}", "Dead Man's {thing}", "{city} Blues", "The {adj} Kiss", "Night of the {thing}"],
    "classic_detective": ["The {adj} {thing}", "The Affair at {house}", "The {thing} of {house}", "Murder at {house}"],
    "thriller": ["The {adj} Cipher", "Express to {city}", "The {thing} Conspiracy", "Seven Hours to {city}"],
}
TITLE_WORDS = {
    "thing": ["Ledger", "Glove", "Key", "Ticket", "Matchbook", "Photograph", "Telegram", "Pearl", "Locket", "Revolver"],
    "street": ["Front Street", "Pier Nine", "Mercer Lane", "the Waterfront", "Dock Road"],
    "city": ["Harbor City", "Port Royal", "Kingsbridge", "Marlow", "Calais"],
    "adj": ["Crimson", "Silent", "Second", "Crooked", "Last", "Painted", "Broken"],
    "house": ["Ashby Hall", "Thornfield Grange", "Crane Court", "the Belvedere", "Penrose House"],
}


def make_title(rng: random.Random, genre: str) -> str:
    pat = rng.choice(TITLE_PATTERNS[genre])
    return pat.format(**{k: rng.choice(v) for k, v in TITLE_WORDS.items()})


def _short(name: str) -> str:
    return name.split()[-1]


def plan(spec: Spec, used_names: set[str] | None = None) -> Outline:
    rng = random.Random(spec.seed * 7919 + 1)
    used = set(used_names or ()) | {spec.detective_name}
    pool = POOLS[spec.genre]
    places = list(pool["places"])
    rng.shuffle(places)

    det = Character(spec.detective_name, "detective", spec.detective_type)
    vic_g = rng.choice("mf")
    victim = Character(make_name(rng, used, vic_g), "victim", spec.victim, vic_g, alive=False, dies_in_chapter=0)
    cul_g = rng.choice("mf")
    culprit = Character(make_name(rng, used, cul_g), "culprit", spec.culprit, cul_g)
    herring = Character(make_name(rng, used), "suspect", "a suspect with a motive and no alibi")
    other = Character(make_name(rng, used), "suspect", "a nervous associate of the victim")
    witness = Character(make_name(rng, used), "witness", "a witness who saw more than they say")
    ally = Character(make_name(rng, used, "m"), "ally",
                     "a police lieutenant" if spec.genre != "thriller" else "a contact in the service")
    cast = [det, victim, culprit, herring, other, witness, ally]

    clue_texts = list(CLUE_TEMPLATES)
    rng.shuffle(clue_texts)
    fmt = {"place": places[0], "culprit_short": _short(culprit.name)}
    clues = [Clue(f"C{i + 1}", clue_texts[i].format(**fmt), culprit.name, True) for i in range(3)]
    clues += [Clue(f"R{i + 1}", clue_texts[3 + i].format(**fmt), herring.name, False) for i in range(2)]

    n = max(1, spec.chapters)
    beats_per = max(3, round(spec.chapter_words / WORDS_PER_BEAT))
    words_per_beat = max(150, spec.chapter_words // beats_per)
    mid = max(1, math.ceil(n / 2))

    # Spread clue plants across the chapters before the last one.
    plant_chapters = list(range(1, max(n, 2)))
    for i, c in enumerate(clues):
        c.planted_chapter = plant_chapters[i % len(plant_chapters)] if n > 1 else 1
        c.revealed_chapter = n

    # A second victim at the midpoint keeps the middle moving (only for 4+ chapters).
    if n >= 4:
        other.alive = True
        other.dies_in_chapter = mid

    chapters = []
    for ch in range(1, n + 1):
        kinds = _chapter_kinds(ch, n, mid, beats_per)
        beats = []
        for b, kind in enumerate(kinds, 1):
            place = places[(ch * beats_per + b) % len(places)]
            planted = [c for c in clues if c.planted_chapter == ch]
            beat_clues = []
            if kind in ("clue", "search") and planted:
                beat_clues = [planted[(b - 1) % len(planted)].id]
            if kind == "reveal":
                beat_clues = [c.id for c in clues]
            beats.append(_make_beat(spec, ch, b, kind, place, cast, clues, beat_clues, words_per_beat, rng))
        chapters.append({"num": ch, "title": _chapter_title(rng, kinds), "beats": beats})

    return Outline(make_title(rng, spec.genre), cast, clues, chapters)


def _chapter_kinds(ch: int, n: int, mid: int, k: int) -> list[str]:
    if n == 1:
        base = ["discovery", "hire", "interview", "clue", "red_herring", "confront", "reveal", "aftermath"]
    elif ch == 1:
        base = ["discovery", "hire", "scene", "clue", "interview", "reflection"]
    elif ch == n:
        base = ["gather", "confront", "reveal", "struggle", "aftermath", "reflection"]
    elif ch == n - 1 and n >= 3:
        base = ["interview", "red_herring_exposed", "clue", "trap", "danger", "reflection"]
    elif ch == mid:
        base = ["interview", "search", "twist", "second_crime", "danger", "reflection"]
    else:
        base = ["interview", "clue", "red_herring", "search", "danger", "reflection"]
    if k <= len(base):
        # Keep the k most important beats, in story order.
        ranked = sorted(range(len(base)), key=lambda i: BEAT_PRIORITY.index(base[i]))
        keep = sorted(ranked[:k])
        return [base[i] for i in keep]
    filler = ["interview", "clue", "search", "reflection"]
    return base[:-1] + [filler[i % len(filler)] for i in range(k - len(base))] + base[-1:]


# Most important first. Used when a short chapter cannot fit every beat.
BEAT_PRIORITY = [
    "reveal", "discovery", "confront", "twist", "second_crime", "red_herring_exposed", "clue", "search", "hire",
    "interview", "aftermath", "red_herring", "danger", "trap", "gather", "struggle", "scene", "reflection",
]


def _chapter_title(rng: random.Random, kinds: list[str]) -> str:
    names = {
        "discovery": ["A Body in the Rain", "The Call", "First Light"], "twist": ["The Wrong Corpse", "Turnabout"],
        "reveal": ["The Last Card", "Accounts Settled"], "red_herring_exposed": ["A Lie Comes Apart", "The Alibi"],
        "second_crime": ["Another One", "Blood on the Stair"], "danger": ["A Gun in the Dark", "Close Call"],
    }
    for k in kinds:
        if k in names:
            return rng.choice(names[k])
    return rng.choice(["Questions", "Footwork", "Old Debts", "Small Hours", "Loose Ends", "Wet Pavement"])


def _make_beat(spec: Spec, ch: int, num: int, kind: str, place: str, cast: list[Character],
               clues: list[Clue], beat_clues: list[str], words: int, rng: random.Random) -> Beat:
    det, victim, culprit, herring, other, witness, ally = cast
    clue_by = {c.id: c for c in clues}
    clue_txt = ", ".join(clue_by[c].text for c in beat_clues) if beat_clues else "something out of place"
    first = spec.pov == "first"
    subj = "I" if first else _short(det.name)
    my = "my" if first else ("his" if det.gender == "m" else "her")
    d, v, cu, h, o, w, a = (_short(c.name) for c in cast)
    suspect = rng.choice([cu, h, o]) if kind == "interview" else h

    table = {
        "discovery": (f"{victim.name} is found dead at {place}.",
                      f"They found {victim.name} at {place}, and by the time {subj} got there the rain had washed away most of what mattered."),
        "hire": (f"{det.name} is drawn into the case.",
                 f"The client sat across from {'me' if first else d} and said the police had it wrong about {v}."),
        "scene": (f"{det.name} studies the scene at {place}.",
                  f"{subj} went back to {place} alone, because a place remembers things that people forget."),
        "clue": (f"{det.name} finds {clue_txt}.", f"It was {clue_txt}, and {subj} turned it over in {my} hand for a long time."),
        "search": (f"{det.name} searches {place} and finds {clue_txt}.",
                   f"{subj} searched {place} the slow way, drawer by drawer, until {subj} found {clue_txt}."),
        "interview": (f"{det.name} questions {suspect} at {place}.",
                      f"{suspect} did not want to talk, but {subj} had come a long way to {place} and {subj} was in no hurry to leave."),
        "red_herring": (f"Evidence seems to point to {herring.name}.",
                        f"Everything {subj} had so far pointed at {h}, and that was exactly what bothered {'me' if first else 'him'}."),
        "red_herring_exposed": (f"{herring.name}'s alibi holds; the false trail is exposed.",
                                f"{h} had been lying, but not about the thing that mattered."),
        "twist": (f"Twist: {spec.twist}.", f"Then {subj} understood that {spec.twist}, and the whole case turned over like a card."),
        "second_crime": (f"{other.name} is killed before {pronoun(other)} can talk.",
                         f"{o} never got the chance to tell {'me' if first else d} what {pronoun(other)} knew."),
        "danger": (f"Someone tries to stop {det.name} at {place}.",
                   f"The first shot went wide, and {subj} was on the floor of {place} before the second one came."),
        "reflection": (f"{det.name} thinks over the case.",
                       f"Later, with a drink {subj} did not want, {subj} laid the pieces out in {my} head one more time."),
        "trap": (f"{det.name} sets a trap for the killer.", f"{subj} told {a} what {subj} wanted, and {a} said {subj} was crazy, and then he agreed."),
        "gather": (f"{det.name} brings the suspects together at {place}.",
                   f"They were all there at {place}: {cu}, {h}, {w}, and {a} by the door."),
        "confront": (f"{det.name} confronts {culprit.name}.", f"{subj} looked at {cu} and said, \"You were there that night.\""),
        "reveal": (f"Reveal: {culprit.name} did it, motive {spec.motive}. The true clues: "
                   + "; ".join(c.text for c in clues if c.true) + ".",
                   f"\"It was {spec.motive},\" {subj} said. \"It was always {spec.motive}.\""),
        "struggle": (f"{culprit.name} makes a last desperate move.", f"{cu} went for the gun, and {subj} went for {cu}."),
        "aftermath": (f"The case closes; {ally.name} takes {culprit.name} away.",
                      f"{a} took {cu} out into the rain, and {subj} stood there a while longer."),
    }
    summary, lead = table.get(kind, table["reflection"])
    names = [c.name for c in cast if _short(c.name) in summary + lead or c.name in summary + lead]
    return Beat(ch, num, kind, summary, lead, names, place, beat_clues, words)


def pronoun(c: Character) -> str:
    return "he" if c.gender == "m" else "she"
