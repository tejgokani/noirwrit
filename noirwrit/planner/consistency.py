"""Consistency pass: names, timeline, and clue references checked against the bible.

Auto-fixes what is safe to fix (a misspelled known name) and asks for a
regenerate when it is not (a dead character speaking, a clue cited before it
was planted).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from noirwrit.planner.bible import Bible
from noirwrit.planner.outline import Beat

TITLES = r"(?:Mr|Mrs|Miss|Ms|Dr|Inspector|Sergeant|Lieutenant|Captain|Detective|Officer|Colonel|Lady|Lord|Sir|Father)"
TITLED_NAME_RE = re.compile(rf"\b{TITLES}\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)")
FULL_NAME_RE = re.compile(r"\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b")
SPEECH_RE = re.compile(r'"[^"]{2,300}?"\s*,?\s*(?:said|asked|told|answered|replied|whispered|snapped)\s+([A-Z][a-z]+)')
SPEECH_RE2 = re.compile(r'([A-Z][a-z]+)\s+(?:said|asked|answered|replied|whispered|snapped)\b')

# Words that look like names at the start of a phrase but are not people.
NOT_NAMES = {
    "The", "This", "That", "Then", "There", "When", "What", "Where", "Who", "Why", "How", "And", "But", "Yes", "Not",
    "Front", "Street", "Hotel", "Police", "City", "Harbor", "North", "South", "East", "West", "Monday", "Tuesday",
    "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "January", "February", "March", "April", "June", "July",
    "August", "September", "October", "November", "December", "Christmas", "God", "Lord", "Scotland", "Yard",
    "London", "England", "America", "New", "York", "Chicago", "San", "Francisco", "Pier", "Dock", "Road", "Lane",
    "Hall", "House", "Court", "Grange", "Station", "Square", "Park", "Club", "Bar", "Cafe",
}


PRONOUNS = {"He", "She", "They", "We", "You", "It", "His", "Her", "Their", "Someone", "Nobody", "Everyone"}

# Well-known characters from the public domain training books. A base model
# remembers them; a Noirwrit story should not borrow them.
FAMOUS = {
    "Holmes", "Watson", "Lestrade", "Moriarty", "Hudson", "Mycroft", "Poirot", "Hastings", "Japp", "Marple",
    "Tuppence", "Wimsey", "Bunter", "Lupin", "Ganimard", "Sholmes", "Spade", "Archer", "Gutman", "Cairo",
    "Carrados", "Hewitt", "Thorndyke", "Kennedy", "Dupin", "Cuff", "Chichikov", "Pickwick", "Copperfield",
    "Crisparkle", "Utterson", "Jekyll", "Hyde", "Dracula", "Harker", "Quatermain", "Tarzan", "Carter",
}


def edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


@dataclass
class Issue:
    kind: str  # name_typo | dead_speaks | clue_early | unknown_name
    detail: str
    fixable: bool
    fix: tuple[str, str] | None = None


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)
    fixed_text: str = ""

    @property
    def needs_regenerate(self) -> bool:
        return any(not i.fixable and i.kind in ("dead_speaks", "clue_early") for i in self.issues)

    def summary(self) -> str:
        return "; ".join(f"{i.kind}: {i.detail}" for i in self.issues) or "ok"


def _known_parts(bible: Bible) -> tuple[set[str], set[str], dict[str, str]]:
    firsts, lasts, full = set(), set(), {}
    for name in bible.full_names():
        parts = name.split()
        firsts.add(parts[0])
        lasts.add(parts[-1])
        full[name] = name
    return firsts, lasts, full


def check(text: str, bible: Bible, beat: Beat) -> Report:
    rep = Report(fixed_text=text)
    firsts, lasts, full = _known_parts(bible)
    known_tokens = firsts | lasts

    # 1. Names: a capitalized token one or two edits from a known name part is a typo.
    candidates: set[str] = set()
    for m in FULL_NAME_RE.finditer(text):
        candidates.update([m.group(1), m.group(2)])
    for m in TITLED_NAME_RE.finditer(text):
        candidates.update(m.group(1).split())
    for tok in sorted(candidates):
        if tok in known_tokens or tok in NOT_NAMES:
            continue
        best, dist = None, 9
        for k in known_tokens:
            d = edit_distance(tok, k)
            if d < dist:
                best, dist = k, d
        if best and dist <= (1 if len(best) <= 4 else 2) and tok[0] == best[0]:
            rep.issues.append(Issue("name_typo", f"{tok} -> {best}", True, (tok, best)))
    for iss in rep.issues:
        if iss.fix:
            rep.fixed_text = re.sub(rf"\b{re.escape(iss.fix[0])}\b", iss.fix[1], rep.fixed_text)

    # 1b. Foreign names: a speaker or titled name the bible does not know (often a
    # character remembered from the training books) is mapped to someone in this beat.
    # Famous public domain characters are replaced wherever they appear.
    typo_from = {i.fix[0] for i in rep.issues if i.fix}
    foreign: list[str] = []
    for rx in (SPEECH_RE, SPEECH_RE2, TITLED_NAME_RE):
        for m in rx.finditer(rep.fixed_text):
            for tok in m.group(1).split():
                if tok not in known_tokens and tok not in NOT_NAMES and tok not in PRONOUNS and tok not in typo_from \
                        and not re.fullmatch(TITLES, tok) \
                        and tok not in foreign:
                    foreign.append(tok)
    for tok in sorted(FAMOUS & set(re.findall(r"\b[A-Z][a-z]+\b", rep.fixed_text))):
        if tok not in known_tokens and tok not in foreign:
            foreign.append(tok)
    if foreign:
        def usable(n: str) -> bool:
            role = bible.characters[n]["role"]
            return role not in ("victim", "detective") and not bible.is_dead(n, beat.chapter)

        # Beat characters first, then the rest of the living cast, one per borrowed name.
        pool = [n.split()[-1] for n in beat.characters if n in bible.characters and usable(n)]
        pool += [n.split()[-1] for n in bible.full_names() if usable(n) and n.split()[-1] not in pool]
        if not pool:
            pool = [n.split()[-1] for n in bible.full_names() if bible.characters[n]["role"] == "detective"]
        for i, tok in enumerate(foreign):
            new = pool[i % len(pool)] if pool else "the stranger"
            rep.issues.append(Issue("foreign_name", f"{tok} -> {new}", True, (tok, new)))
            rep.fixed_text = re.sub(rf"\b{re.escape(tok)}\b", new, rep.fixed_text)

    # 2. Timeline: dead characters do not speak (except in a reveal or reflection, as memory).
    if beat.kind not in ("reveal", "reflection", "aftermath"):
        speakers = {m.group(1) for m in SPEECH_RE.finditer(rep.fixed_text)}
        speakers |= {m.group(1) for m in SPEECH_RE2.finditer(rep.fixed_text)}
        for name in bible.full_names():
            parts = set(name.split())
            if bible.is_dead(name, beat.chapter) and parts & speakers:
                rep.issues.append(Issue("dead_speaks", f"{name} speaks in chapter {beat.chapter}", False))

    # 3. Clues: a true clue's exact text should not appear before its planted chapter.
    low = rep.fixed_text.lower()
    for cid, c in bible.clues.items():
        if c["true"] and not c.get("planted") and beat.chapter < c["planted_chapter"] and cid not in beat.clues:
            if c["text"].lower() in low:
                rep.issues.append(Issue("clue_early", f"{cid} '{c['text']}' cited before chapter {c['planted_chapter']}", False))
    return rep
