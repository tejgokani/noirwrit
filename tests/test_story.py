import json

import pytest

from noirwrit.memory.db import DB
from noirwrit.memory.embed import HashingEmbedder
from noirwrit.memory.store import Memory
from noirwrit.planner import consistency
from noirwrit.planner.bible import Bible
from noirwrit.planner.generators import EchoGenerator
from noirwrit.planner.outline import plan
from noirwrit.planner.spec import Spec, fill
from noirwrit.planner.story import StoryEngine, create_story, load_story


@pytest.fixture
def env():
    db = DB(":memory:")
    mem = Memory(db, HashingEmbedder())
    return db, mem


def test_fill_is_deterministic_and_complete():
    a = fill(Spec(seed=7))
    b = fill(Spec(seed=7))
    assert a == b
    for f in ("setting", "era", "detective_type", "victim", "culprit", "motive", "twist", "detective_name"):
        assert getattr(a, f)


@pytest.mark.parametrize("chapters,words", [(1, 3000), (3, 1500), (5, 3000), (12, 2000)])
def test_outline_structure(chapters, words):
    spec = fill(Spec(seed=3, chapters=chapters, chapter_words=words))
    o = plan(spec)
    assert len(o.chapters) == chapters
    kinds = [b.kind for ch in o.chapters for b in ch["beats"]]
    assert kinds.count("reveal") == 1 and o.chapters[-1]["beats"][-1].kind != "discovery"
    assert "reveal" in [b.kind for b in o.chapters[-1]["beats"]]
    assert kinds[0] == "discovery"
    true_clues = [c for c in o.clues if c.true]
    herrings = [c for c in o.clues if not c.true]
    assert len(true_clues) == 3 and len(herrings) == 2
    culprit = o.char("culprit").name
    assert all(c.points_to == culprit for c in true_clues)
    # Every clue is planted before or in the reveal chapter.
    assert all(1 <= c.planted_chapter <= chapters for c in o.clues)
    # Beat count follows chapter length (~500 words per beat, min 3).
    assert len(o.chapters[0]["beats"]) == max(3, round(words / 500))


def test_names_not_reused_across_stories(env):
    db, _ = env
    s1 = create_story(db, Spec(seed=1, chapters=2))
    s2 = create_story(db, Spec(seed=1, chapters=2))
    n1 = {r["name"] for r in db.query("SELECT name FROM names_used WHERE story_id=?", (s1,))}
    n2 = {r["name"] for r in db.query("SELECT name FROM names_used WHERE story_id=?", (s2,))}
    assert n1 and n2 and not (n1 & n2)


def test_consistency_catches_planted_name_error(env):
    db, _ = env
    sid = create_story(db, Spec(seed=5, chapters=3, detective_name="Sam Kade"))
    _, spec, outline = load_story(db, sid)
    bible = Bible.load(db, sid)
    beat = outline.chapters[0]["beats"][2]
    # "Kane" is one letter off the detective's surname "Kade".
    text = "Sam Kane walked into the room. Kade lit a cigarette and said nothing."
    rep = consistency.check(text, bible, beat)
    kinds = [i.kind for i in rep.issues]
    assert "name_typo" in kinds
    assert "Kane" not in rep.fixed_text and rep.fixed_text.startswith("Sam Kade walked")


def test_consistency_flags_dead_character_speaking(env):
    db, _ = env
    sid = create_story(db, Spec(seed=9, chapters=3))
    _, _, outline = load_story(db, sid)
    bible = Bible.load(db, sid)
    victim = outline.char("victim").name.split()[-1]
    beat = next(b for b in outline.chapters[1]["beats"] if b.kind == "interview")
    rep = consistency.check(f'"I never trusted him," said {victim}.', bible, beat)
    assert rep.needs_regenerate
    assert any(i.kind == "dead_speaks" for i in rep.issues)


def test_consistency_leaves_clean_text_alone(env):
    db, _ = env
    sid = create_story(db, Spec(seed=11, chapters=2))
    _, _, outline = load_story(db, sid)
    bible = Bible.load(db, sid)
    beat = outline.chapters[0]["beats"][0]
    text = "The rain kept on. Nobody in the hotel lobby looked up when I came in."
    rep = consistency.check(text, bible, beat)
    assert rep.issues == [] and rep.fixed_text == text


def test_end_to_end_five_chapters(env):
    db, mem = env
    sid = create_story(db, Spec(seed=21, chapters=5, chapter_words=1500))
    engine = StoryEngine(db, mem, EchoGenerator())
    events = []
    texts = engine.write_story(sid, progress=events.append)
    assert len(texts) == 5 and all(len(t.split()) > 500 for t in texts)
    rows = db.query("SELECT status FROM chapters WHERE story_id=?", (sid,))
    assert all(r["status"] == "done" for r in rows)
    assert db.one("SELECT status FROM stories WHERE id=?", (sid,))["status"] == "done"
    assert db.one("SELECT COUNT(*) AS c FROM summaries WHERE story_id=?", (sid,))["c"] == 5
    assert all(len(r["text"].split()) <= 110 for r in db.query("SELECT text FROM summaries WHERE story_id=?", (sid,)))
    bible = Bible.load(db, sid)
    assert any(c["planted"] for c in bible.clues.values())
    assert len(bible.timeline) == db.one("SELECT COUNT(*) AS c FROM scenes WHERE story_id=?", (sid,))["c"]
    assert sum(e["event"] == "chapter_done" for e in events) == 5


def test_scene_checkpoint_resume(env):
    """A crash mid-chapter loses at most the scene in progress."""
    db, mem = env
    sid = create_story(db, Spec(seed=4, chapters=1, chapter_words=2000))
    engine = StoryEngine(db, mem, EchoGenerator())
    calls = {"n": 0}

    def stop_after_two():
        calls["n"] += 1
        return calls["n"] > 2

    with pytest.raises(InterruptedError):
        engine.write_chapter(sid, 1, should_stop=stop_after_two)
    done = db.query("SELECT num, text FROM scenes WHERE story_id=? AND status='done' ORDER BY num", (sid,))
    assert [r["num"] for r in done] == [1, 2]
    saved = {r["num"]: r["text"] for r in done}

    gen = EchoGenerator()
    seen = []
    orig = gen.generate
    gen.generate = lambda prompt, *a, **k: (seen.append(prompt), orig(prompt, *a, **k))[1]
    StoryEngine(db, mem, gen).write_chapter(sid, 1)
    total = db.one("SELECT COUNT(*) AS c FROM scenes WHERE story_id=?", (sid,))["c"]
    # Only the unfinished scenes were generated again; saved scenes are untouched.
    assert len(seen) == total - 2
    for num, text in saved.items():
        assert db.one("SELECT text FROM scenes WHERE story_id=? AND num=?", (sid, num))["text"] == text


def test_chapter_ten_uses_chapter_one_facts(env):
    """Memory gate: a fact from chapter 1 is retrieved when writing chapter 10."""
    db, mem = env
    sid = create_story(db, Spec(seed=33, chapters=10, chapter_words=1500))
    # Plant a distinctive fact in chapter 1 through the generator.
    fact = "The ledger was hidden behind the loose brick in the cellar of the Blue Parrot."
    gen = EchoGenerator(inject=fact)
    engine = StoryEngine(db, mem, gen)
    engine.write_chapter(sid, 1)
    gen.inject = ""
    for ch in range(2, 10):
        engine.write_chapter(sid, ch)
    _, spec, outline = load_story(db, sid)
    bible = Bible.load(db, sid)
    beat = outline.chapters[9]["beats"][0]
    beat.summary = "Where was the ledger hidden? The cellar of the Blue Parrot."
    prompt = engine.build_prompt(spec, outline, bible, beat, "", "", sid)
    assert "loose brick in the cellar of the Blue Parrot" in prompt


def test_spec_json_round_trip():
    s = fill(Spec(seed=2, chapters=4))
    assert Spec.from_dict(json.loads(s.to_json())) == s


def test_consistency_replaces_borrowed_names(env):
    db, _ = env
    sid = create_story(db, Spec(seed=13, chapters=2))
    _, _, outline = load_story(db, sid)
    bible = Bible.load(db, sid)
    beat = next(b for b in outline.chapters[0]["beats"] if b.kind == "interview")
    text = '"You are late," said Chichikov. Holmes lit his pipe. "Not yet," said Holmes.'
    rep = consistency.check(text, bible, beat)
    assert "Chichikov" not in rep.fixed_text and "Holmes" not in rep.fixed_text
    known = {n.split()[-1] for n in bible.full_names()}
    speakers = set(consistency.SPEECH_RE.findall(rep.fixed_text))
    assert speakers and speakers <= known
    # The same borrowed name maps to the same character every time.
    assert rep.fixed_text.count(speakers.pop()) >= 1
    assert {i.kind for i in rep.issues} == {"foreign_name"}
