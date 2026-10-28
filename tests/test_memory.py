import time

import pytest

from noirwrit.memory.db import DB
from noirwrit.memory.embed import HashingEmbedder
from noirwrit.memory.store import Memory, chunk_text, match_spec

DOCS = {
    "harbor": "The harbor smelled of tar and diesel. Fishing boats knocked against the pilings while gulls fought over scraps. "
              "Down at Pier Nine the night watchman kept a lantern and a bottle under his stool.",
    "poison": "Arsenic in the tea, the coroner said. A slow poison, given over weeks, in the cup she drank every evening "
              "before bed. The chemist on Mercer Lane had sold it as rat poison.",
    "train": "The express left Victoria at nine. In the dining car a man in a grey coat read the same page of his newspaper "
             "for an hour, watching the compartment door through the reflection in the window.",
    "money": "The bank book showed a single withdrawal of four thousand dollars, made the morning of the murder, "
             "in small bills, signed by a hand that was not quite the dead man's.",
}


@pytest.fixture
def mem():
    db = DB(":memory:")
    return Memory(db, HashingEmbedder())


def _story(db, title="Test"):
    sid = db.add_spec({"genre": "noir"})
    return db.execute("INSERT INTO stories(created, spec_id, title) VALUES (?, ?, ?)", (time.time(), sid, title)).lastrowid


def test_chunker_size_and_overlap():
    words = " ".join(f"word{i}" for i in range(2000))
    chunks = chunk_text(words, size=500, overlap=50)
    assert len(chunks) >= 4
    # Consecutive chunks share text at the seam.
    a, b = chunks[0].split(), chunks[1].split()
    assert set(a[-10:]) & set(b[:80])


def test_ingest_any_size(mem, tmp_path):
    big = "\n\n".join(DOCS.values()) * 300  # ~20k words
    n = mem.ingest_text(big, source="pasted")
    assert n > 20
    f = tmp_path / "notes.md"
    f.write_text("# Notes\n\n" + DOCS["poison"])
    assert mem.ingest_file(f) >= 1
    assert mem.db.one("SELECT COUNT(*) AS c FROM chunks")["c"] == n + 1


def test_retrieval_accuracy(mem):
    for name, text in DOCS.items():
        mem.ingest_text(text, source=name)
    queries = {
        "harbor": "watchman at the pier with gulls and fishing boats",
        "poison": "who bought the arsenic from the chemist",
        "train": "man in a grey coat on the express dining car",
        "money": "large withdrawal from the bank in small bills",
    }
    correct = sum(mem.search(q, k=1)[0].source == want for want, q in queries.items())
    assert correct == len(queries)


def test_retrieval_scoped_to_story(mem):
    s1, s2 = _story(mem.db, "one"), _story(mem.db, "two")
    mem.ingest_text(DOCS["poison"], source="s1", story_id=s1, kind="scene")
    mem.ingest_text(DOCS["poison"] + " Again.", source="s2", story_id=s2, kind="scene")
    hits = mem.search("arsenic in the tea", k=5, story_id=s1, include_global=False)
    assert hits and all(h.story_id == s1 for h in hits)


def test_novelty_flags_duplicate_and_passes_fresh(mem):
    old = _story(mem.db, "old")
    chapter = " ".join(DOCS.values()) * 3
    mem.ingest_text(chapter, source="old", story_id=old, kind="chapter")
    new = _story(mem.db, "new")

    dup = mem.novelty(chapter, story_id=new)
    assert not dup.novel
    assert dup.max_cosine > 0.85 and dup.ngram_overlap > 0.5
    assert dup.closest_story == old

    # Light edits still read as a copy.
    edited = chapter.replace("harbor", "port").replace("arsenic", "strychnine")
    assert not mem.novelty(edited, story_id=new).novel

    fresh = ("Snow lay on the mountain hotel. The concierge had a scar and a Swiss passport, and the countess "
             "in room twelve had not come down to dinner for three nights. Someone had cut the telephone line.")
    rep = mem.novelty(fresh, story_id=new)
    assert rep.novel, rep.reason


def test_novelty_ignores_own_story(mem):
    sid = _story(mem.db)
    mem.ingest_text(DOCS["train"] * 4, source="mine", story_id=sid, kind="chapter")
    assert mem.novelty(DOCS["train"] * 4, story_id=sid).novel


def test_spec_match():
    emb = HashingEmbedder()
    stored = [
        (1, {"genre": "noir", "setting": "a waterfront city", "era": "1920s", "victim": "a shipping clerk",
             "culprit": "the business partner", "motive": "an insurance policy"}),
        (2, {"genre": "classic_detective", "setting": "a country house", "era": "1890s", "victim": "a colonel"}),
    ]
    new = {"genre": "noir", "setting": "a waterfront city", "era": "1920s", "victim": "a shipping clerk",
           "culprit": "the business partner", "motive": "insurance money"}
    m = match_spec(new, stored, emb)
    assert m and m["spec_id"] == 1
    assert {"genre", "setting", "era", "victim"} <= set(m["matched"])
    assert match_spec({"genre": "thriller", "setting": "a mountain hotel", "era": "1910s"}, stored, emb) is None
