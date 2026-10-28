"""Story bible: characters, facts, timeline, clue ledger. Persisted per story."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

from noirwrit.memory.db import DB
from noirwrit.planner.outline import Beat, Outline


@dataclass
class Bible:
    story_id: int
    characters: dict[str, dict] = field(default_factory=dict)
    facts: list[str] = field(default_factory=list)
    timeline: list[dict] = field(default_factory=list)
    clues: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def from_outline(cls, story_id: int, outline: Outline) -> Bible:
        b = cls(story_id)
        for c in outline.cast:
            b.characters[c.name] = {"role": c.role, "description": c.description, "gender": c.gender,
                                    "alive": c.role != "victim", "dies_in_chapter": c.dies_in_chapter,
                                    "first_chapter": None}
        for c in outline.clues:
            b.clues[c.id] = {**asdict(c), "planted": False}
        victim = outline.char("victim")
        b.facts.append(f"{victim.name} ({victim.description}) is dead before the story opens.")
        return b

    # Persistence ----------------------------------------------------------

    def save(self, db: DB) -> None:
        conn = db.conn
        for name, data in self.characters.items():
            conn.execute(
                "INSERT INTO bible_entities(story_id, kind, name, data, first_chapter) VALUES (?, 'character', ?, ?, ?) "
                "ON CONFLICT(story_id, kind, name) DO UPDATE SET data=excluded.data, first_chapter=excluded.first_chapter",
                (self.story_id, name, json.dumps(data), data.get("first_chapter")),
            )
        for cid, data in self.clues.items():
            conn.execute(
                "INSERT INTO bible_entities(story_id, kind, name, data) VALUES (?, 'clue', ?, ?) "
                "ON CONFLICT(story_id, kind, name) DO UPDATE SET data=excluded.data",
                (self.story_id, cid, json.dumps(data)),
            )
        conn.execute(
            "INSERT INTO bible_entities(story_id, kind, name, data) VALUES (?, 'meta', 'facts_timeline', ?) "
            "ON CONFLICT(story_id, kind, name) DO UPDATE SET data=excluded.data",
            (self.story_id, json.dumps({"facts": self.facts, "timeline": self.timeline})),
        )
        conn.commit()

    @classmethod
    def load(cls, db: DB, story_id: int) -> Bible | None:
        rows = db.query("SELECT kind, name, data FROM bible_entities WHERE story_id=?", (story_id,))
        if not rows:
            return None
        b = cls(story_id)
        for r in rows:
            data = json.loads(r["data"])
            if r["kind"] == "character":
                b.characters[r["name"]] = data
            elif r["kind"] == "clue":
                b.clues[r["name"]] = data
            elif r["kind"] == "meta":
                b.facts = data.get("facts", [])
                b.timeline = data.get("timeline", [])
        return b

    # Updates --------------------------------------------------------------

    def update_after_scene(self, beat: Beat, text: str) -> None:
        for name in beat.characters:
            ch = self.characters.get(name)
            if ch and ch.get("first_chapter") is None:
                ch["first_chapter"] = beat.chapter
        for cid in beat.clues:
            if cid in self.clues and beat.kind != "reveal":
                self.clues[cid]["planted"] = True
        if beat.kind == "second_crime":
            for name, ch in self.characters.items():
                if ch.get("dies_in_chapter") == beat.chapter and ch["role"] != "victim":
                    ch["alive"] = False
                    self.facts.append(f"{name} was killed in chapter {beat.chapter}.")
        self.timeline.append({"chapter": beat.chapter, "scene": beat.num, "event": beat.summary})

    # Prompt slice ---------------------------------------------------------

    def slice_for(self, beat: Beat, max_items: int = 6) -> str:
        """Short prose list of the facts this beat needs."""
        lines = []
        for name in beat.characters[:max_items]:
            c = self.characters.get(name)
            if c:
                state = "" if c.get("alive", True) else " (dead)"
                lines.append(f"{name}, {c['description']}{state}.")
        for cid in beat.clues:
            c = self.clues.get(cid)
            if c:
                lines.append(f"Clue: {c['text']}.")
        lines += self.facts[-2:]
        return " ".join(lines)

    def full_names(self) -> list[str]:
        return list(self.characters)

    def is_dead(self, name: str, chapter: int, scene_kind: str = "") -> bool:
        c = self.characters.get(name)
        if not c:
            return False
        if c["role"] == "victim":
            return True
        died = c.get("dies_in_chapter")
        return bool(died) and (chapter > died or not c.get("alive", True))
