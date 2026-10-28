// Noirwrit front end. Plain JS, no network beyond this local server.
"use strict";

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const state = { view: "library", story: null, chapter: 1, storyData: null, poll: null, questions: [], match: null };

async function api(path, opts = {}) {
  const r = await fetch(path, { headers: { "Content-Type": "application/json" }, ...opts });
  if (!r.ok) {
    let msg = r.statusText;
    try { msg = (await r.json()).detail || msg; } catch (_) {}
    throw new Error(msg);
  }
  return r.headers.get("content-type")?.includes("json") ? r.json() : r;
}

function toast(msg, ms = 2600) {
  const t = $("#toast");
  t.textContent = msg;
  t.classList.remove("hidden");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.add("hidden"), ms);
}

function modal(html) {
  $("#modalBody").innerHTML = html;
  $("#modal").classList.remove("hidden");
  $("#modalClose").focus();
}
function closeModal() { $("#modal").classList.add("hidden"); }

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function fmtEta(s) {
  if (s == null) return "measuring speed";
  if (s < 60) return `${Math.max(1, Math.round(s))} s`;
  const m = Math.floor(s / 60), r = Math.round(s % 60);
  return m < 60 ? `${m} min ${r ? r + " s" : ""}`.trim() : `${Math.floor(m / 60)} h ${m % 60} min`;
}

// Persisted UI prefs (per browser). The app works without them.
const prefs = {
  get(k, d) { try { const v = localStorage.getItem("nw." + k); return v == null ? d : JSON.parse(v); } catch (_) { return d; } },
  set(k, v) { try { localStorage.setItem("nw." + k, JSON.stringify(v)); } catch (_) {} },
};

// Views ---------------------------------------------------------------------

function show(view) {
  state.view = view;
  $$(".view").forEach((v) => v.classList.toggle("active", v.id === "view-" + view));
  $$(".nav button").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  $("#crumb").textContent = { new: "New story", library: "Library", reader: state.storyData?.title || "Reader", memory: "Memory", settings: "Settings" }[view];
  if (view === "library") loadLibrary();
  if (view === "memory") loadMemory();
  if (view === "settings") loadSettings();
  if (view === "new") buildForm();
  prefs.set("view", view);
}

// New story -------------------------------------------------------------------

async function buildForm() {
  if (!state.questions.length) state.questions = (await api("/api/questions")).questions;
  const f = $("#specForm");
  if (f.dataset.built) return;
  f.innerHTML = state.questions.map((q) => {
    const id = "q_" + q.key;
    let input;
    if (q.type === "choice") input = `<select id="${id}" name="${q.key}">${q.choices.map((c) => `<option ${c === q.default ? "selected" : ""} value="${c}">${c.replace("_", " ")}</option>`).join("")}</select>`;
    else if (q.type === "int") input = `<input id="${id}" name="${q.key}" type="number" min="${q.min}" max="${q.max}" value="${q.default ?? ""}">`;
    else input = `<input id="${id}" name="${q.key}" placeholder="${esc(q.placeholder || "Noirwrit decides")}">`;
    return `<label for="${id}">${esc(q.label)}${input}</label>`;
  }).join("");
  f.dataset.built = "1";
  f.addEventListener("change", checkMatch);
}

function readSpec() {
  const spec = {};
  new FormData($("#specForm")).forEach((v, k) => { if (String(v).trim() !== "") spec[k] = v; });
  ["chapters", "chapter_words"].forEach((k) => { if (spec[k]) spec[k] = parseInt(spec[k], 10); });
  return spec;
}

async function checkMatch() {
  const res = await api("/api/match", { method: "POST", body: JSON.stringify({ spec: readSpec() }) });
  state.match = res.match;
  const box = $("#matchBox");
  if (!res.match) { box.classList.add("hidden"); return; }
  const m = res.match, st = m.story;
  box.innerHTML = `<strong>This looks like a story you already asked for${st ? `: “${esc(st.title)}”` : ""}.</strong>
    <div class="tags">Matching fields: ${m.matched.map((x) => `<span>${esc(x.replace("_", " "))}</span>`).join("") || "none"} <span class="muted">(${Math.round(m.score * 100)}% similar)</span></div>
    <div class="actions">
      <button data-mode="continue">Continue it</button>
      <button data-mode="vary">Vary it</button>
      <button data-mode="fresh" class="primary">Start fresh</button>
    </div>`;
  box.classList.remove("hidden");
  $$("button[data-mode]", box).forEach((b) => b.addEventListener("click", () => createStory(b.dataset.mode)));
}

async function createStory(mode = "fresh") {
  const btn = $("#createBtn");
  btn.disabled = true;
  try {
    const res = await api("/api/stories", { method: "POST", body: JSON.stringify({ spec: readSpec(), mode, match_spec_id: state.match?.spec_id ?? null }) });
    toast(mode === "continue" ? "Continuing your story" : "Planned. Writing chapter 1 now.");
    $("#matchBox").classList.add("hidden");
    state.match = null;
    await openStory(res.story_id, 1);
  } catch (e) { toast("Could not start: " + e.message, 4000); }
  finally { btn.disabled = false; }
}

// Library -------------------------------------------------------------------

async function loadLibrary() {
  const { stories } = await api("/api/stories");
  const el = $("#libraryList");
  if (!stories.length) {
    el.innerHTML = `<div class="panel">No stories yet. <button class="primary" id="emptyNew">Write your first</button></div>`;
    $("#emptyNew").onclick = () => show("new");
    return;
  }
  el.innerHTML = stories.map((s) => `
    <div class="card" data-id="${s.id}" tabindex="0">
      <h3>${esc(s.title)}</h3>
      <div class="meta">${s.done}/${s.chapters} chapters · ${s.words.toLocaleString()} words · ${new Date(s.created * 1000).toLocaleDateString()}</div>
      <div class="mini"><div style="width:${s.chapters ? (100 * s.done / s.chapters) : 0}%"></div></div>
      <div class="actions"><button data-act="open">Read</button><button data-act="pdf">PDF</button><button data-act="epub">EPUB</button><button data-act="del">Delete</button></div>
    </div>`).join("");
  $$(".card", el).forEach((c) => {
    const id = +c.dataset.id;
    c.addEventListener("click", async (ev) => {
      const act = ev.target.dataset?.act;
      if (act === "pdf" || act === "epub") { ev.stopPropagation(); return download(id, act, null); }
      if (act === "del") {
        ev.stopPropagation();
        if (confirm("Delete this story and what Noirwrit remembers of it?")) { await api(`/api/stories/${id}`, { method: "DELETE" }); loadLibrary(); }
        return;
      }
      openStory(id, prefs.get("pos." + id, 1));
    });
    c.addEventListener("keydown", (e) => { if (e.key === "Enter") openStory(id, prefs.get("pos." + id, 1)); });
  });
}

// Reader ----------------------------------------------------------------------

async function openStory(id, chapter = 1) {
  typer.stop();
  state._sameChapter = false;
  state._lastText = null;
  state.story = id;
  state.storyData = await api(`/api/stories/${id}`);
  state.chapter = Math.min(chapter, state.storyData.chapters.length);
  prefs.set("story", id);
  show("reader");
  renderChapterList();
  await loadChapter();
}

function renderChapterList() {
  const d = state.storyData;
  if (!d) { $("#chapterList").innerHTML = ""; return; }
  $("#chapterList").innerHTML = `<div class="muted small" style="padding:4px 8px 8px">${esc(d.title)}</div>` + d.chapters.map((c) => `
    <button class="ch ${c.num === state.chapter ? "active" : ""}" data-n="${c.num}" title="${esc(c.status)}">
      <span class="n">${c.num}</span><span class="t">${esc(c.title)}</span><span class="dot ${c.status}"></span>
    </button>`).join("");
  $$("#chapterList .ch").forEach((b) => b.addEventListener("click", () => goChapter(+b.dataset.n)));
}

function renderText(text, status) {
  const box = $("#chapterText");
  if (!text) {
    box.innerHTML = `<p class="placeholder">${status === "done" ? "This chapter is empty." : "This chapter is being written. Finished scenes appear here as they land."}</p>`;
    return;
  }
  box.innerHTML = text.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean).map((p) => `<p>${esc(p)}</p>`).join("");
}

async function loadChapter() {
  if (!state.story) return;
  const c = await api(`/api/stories/${state.story}/chapters/${state.chapter}`);
  const d = state.storyData;
  $("#readerStory").textContent = d.title;
  $("#readerTitle").textContent = `Chapter ${c.num}`;
  $("#chapterTitle").textContent = c.title;
  $("#crumb").textContent = `${d.title} · Chapter ${c.num}`;
  const key = `${state.story}:${state.chapter}`;
  const typingHere = typer.active && typer.key === key;
  if (!typingHere) {
    const mode = typingMode();
    const wantType = (mode === "live" && c.status !== "done") || (mode === "always" && !typer.typedOnce.has(key));
    if (wantType) {
      typer.start(state.story, state.chapter, c);
    } else if (state._lastText !== c.text) {
      const scrollKeep = $("#main").scrollTop;
      renderText(c.text, c.status);
      state._lastText = c.text;
      $("#main").scrollTop = state._sameChapter ? scrollKeep : 0;
    }
  }
  state._sameChapter = true;
  updateProgress(c);
  prefs.set("pos." + state.story, state.chapter);
  schedulePoll(c.status === "done" ? 6000 : 2000);
}

function updateProgress(c) {
  const box = $("#progressBox");
  const d = state.storyData;
  if (c.status === "done") {
    box.classList.add("hidden");
  } else {
    box.classList.remove("hidden");
    $("#progressFill").style.width = c.percent + "%";
    const live = c.live && c.live.scene ? ` · scene ${c.live.scene} of ${c.live.of}` : "";
    const word = { queued: "Queued", pending: "Not started", writing: "Writing", failed: "Failed" }[c.status] || c.status;
    $("#progressText").textContent = `${word}${live} · ${Math.round(c.percent)}% · about ${fmtEta(c.eta_s)} left`;
    $("#sceneDots").innerHTML = c.scenes.map((s) => `<span class="${s.status === "done" ? "done" : (c.live && c.live.scene === s.num ? "writing" : "")}" title="Scene ${s.num}: ${esc(s.kind)}"></span>`).join("");
  }
  // Next chapter state: ready, writing with ETA, or not started.
  const next = d.chapters[state.chapter];
  const ns = $("#nextState"), nb = $("#nextBtn");
  $("#prevBtn").disabled = state.chapter <= 1;
  if (!next) { ns.textContent = "The end."; nb.disabled = true; nb.textContent = "Next chapter →"; return; }
  nb.disabled = false;
  if (next.status === "done") { ns.textContent = "Next chapter is ready."; nb.textContent = "Next chapter →"; }
  else if (next.status === "writing" || next.status === "queued") { ns.textContent = `Next chapter ${next.status === "writing" ? "is being written" : "is queued"}, about ${fmtEta(next.eta_s)}.`; nb.textContent = "Next chapter →"; }
  else { ns.textContent = "Next chapter not started."; nb.textContent = "Write next chapter →"; }
}

async function goChapter(n) {
  const d = state.storyData;
  if (!d || n < 1 || n > d.chapters.length) return;
  const target = d.chapters[n - 1];
  if (target.status === "pending" || target.status === "failed") {
    await api(`/api/stories/${state.story}/chapters/${n}/generate`, { method: "POST" });
  }
  typer.stop();
  state.chapter = n;
  state._lastText = null;
  state._sameChapter = false;
  await refreshStory();
  await loadChapter();
}

async function refreshStory() {
  if (!state.story) return;
  state.storyData = await api(`/api/stories/${state.story}`);
  renderChapterList();
}

function schedulePoll(ms) {
  clearTimeout(state.poll);
  state.poll = setTimeout(async () => {
    try {
      if (state.view === "reader" && state.story && !document.hidden) { await refreshStory(); await loadChapter(); }
      else schedulePoll(ms);
      refreshStatus();
    } catch (_) { schedulePoll(5000); }
  }, ms);
}

// Typewriter -------------------------------------------------------------------
// Live chapters stream in over Server-Sent Events, one scene at a time. Each scene
// keeps the text the server has sent (target) and the text typed so far (shown);
// a timer types the difference at a reading pace, pausing at punctuation.

const SPEEDS = { slow: 22, natural: 45, fast: 110, instant: Infinity };
const typingMode = () => prefs.get("typing", "live");          // live | always | off
const typingSpeed = () => SPEEDS[prefs.get("typingSpeed", "natural")] ?? 45;

const typer = {
  active: false, key: null, story: null, chapter: null, scenes: new Map(), es: null, timer: null,
  done: false, budget: 0, last: 0, typedOnce: new Set(), instant: new Set(),

  start(story, chapter, c) {
    this.stop();
    Object.assign(this, { active: true, story, chapter, key: `${story}:${chapter}`, scenes: new Map(), done: false,
      budget: 0, last: performance.now(), instant: new Set() });
    $("#chapterText").innerHTML = "";
    $("#skipTyping").classList.remove("hidden");
    if (c.status === "done") {
      // "Every chapter" mode on a finished chapter: type the whole text.
      this.scene(1).target = c.text;
      this.done = true;
    } else {
      // Scenes already finished when the chapter is opened appear at once; new text types out.
      (c.scenes || []).forEach((s) => { if (s.status === "done") this.instant.add(s.num); });
      this.connect();
    }
    this.timer = setInterval(() => this.tick(), 30);
  },

  connect() {
    const es = new EventSource(`/api/stories/${this.story}/chapters/${this.chapter}/stream`);
    this.es = es;
    es.addEventListener("scene", (e) => {
      const d = JSON.parse(e.data);
      const s = this.scene(d.num);
      s.target = d.text;
      if (this.instant.has(d.num)) { s.shown = d.text; this.render(s); }
    });
    es.addEventListener("status", (e) => updateLiveStatus(JSON.parse(e.data)));
    es.addEventListener("end", (e) => {
      es.close();
      if (JSON.parse(e.data).reason === "done") { this.done = true; refreshStory(); }
      else if (this.active) setTimeout(() => this.active && this.connect(), 1000);
    });
    es.onerror = () => { es.close(); if (this.active && !this.done) setTimeout(() => this.active && this.connect(), 2000); };
  },

  scene(num) {
    if (!this.scenes.has(num)) {
      const el = document.createElement("div");
      el.className = "scene";
      el.dataset.n = num;
      const box = $("#chapterText");
      const after = [...box.children].find((x) => +x.dataset.n > num);
      box.insertBefore(el, after || null);
      this.scenes.set(num, { num, target: "", shown: "", el });
    }
    return this.scenes.get(num);
  },

  ordered() { return [...this.scenes.values()].sort((a, b) => a.num - b.num); },

  render(s, caret = false) {
    const paras = s.shown.split(/\n\s*\n/);
    s.el.innerHTML = paras.map((p, i) => `<p>${esc(p.trim())}${caret && i === paras.length - 1 ? '<span class="caret"></span>' : ""}</p>`).join("");
  },

  tick() {
    const now = performance.now();
    const dt = Math.min((now - this.last) / 1000, 0.25);
    this.last = now;
    const cps = typingSpeed();
    const main = $("#main");
    const follow = main.scrollHeight - main.scrollTop - main.clientHeight < 140;
    let touched = null;
    if (cps === Infinity) {
      this.ordered().forEach((s) => { if (s.shown !== s.target) { s.shown = s.target; this.render(s); } });
    } else {
      this.budget = Math.min(this.budget + cps * dt * (0.8 + Math.random() * 0.4), cps * 0.3);
      while (this.budget >= 1) {
        const s = this.ordered().find((x) => x.shown !== x.target);
        if (!s) break;
        if (!s.target.startsWith(s.shown)) {
          // The cleaned text changed behind the cursor (a name fix): rewind to the common prefix.
          let k = 0;
          while (k < s.shown.length && s.shown[k] === s.target[k]) k++;
          s.shown = s.target.slice(0, k);
        }
        const ch = s.target[s.shown.length];
        if (ch === undefined) break;
        s.shown += ch;
        this.budget -= 1;
        if (".!?".includes(ch)) this.budget -= 9;
        else if (",;:".includes(ch)) this.budget -= 3;
        else if (ch === "\n") this.budget -= 5;
        touched = s;
      }
      if (touched) {
        this.ordered().forEach((s) => { if (s !== touched && s.el.querySelector(".caret")) this.render(s); });
        this.render(touched, true);
      }
    }
    if (follow && touched) main.scrollTop = main.scrollHeight;
    const pending = this.ordered().some((s) => s.shown !== s.target);
    if (!pending && this.done) this.finish();
  },

  skip() {
    this.ordered().forEach((s) => { s.shown = s.target; this.render(s); });
    if (this.done) this.finish();
  },

  finish() {
    const text = this.ordered().map((s) => s.target).join("\n\n");
    this.ordered().forEach((s) => this.render(s));
    this.typedOnce.add(this.key);
    state._lastText = text;
    this.stop();
  },

  stop() {
    clearInterval(this.timer);
    if (this.es) this.es.close();
    Object.assign(this, { active: false, timer: null, es: null });
    $("#skipTyping")?.classList.add("hidden");
  },
};

function updateLiveStatus(d) {
  if (!state.storyData) return;
  const box = $("#progressBox");
  if (d.status === "done") { box.classList.add("hidden"); return; }
  box.classList.remove("hidden");
  $("#progressFill").style.width = d.percent + "%";
  const live = d.live && d.live.scene ? ` · scene ${d.live.scene} of ${d.live.of}` : "";
  $("#progressText").textContent = `Writing${live} · ${Math.round(d.percent)}% · about ${fmtEta(d.eta_s)} left`;
}

// Export, print, Kindle ----------------------------------------------------

function download(id, fmt, chapter) {
  const q = new URLSearchParams({ fmt });
  if (chapter) q.set("chapter", chapter);
  const a = document.createElement("a");
  a.href = `/api/stories/${id}/export?${q}`;
  a.download = "";
  document.body.appendChild(a);
  a.click();
  a.remove();
  toast(`Exporting ${fmt.toUpperCase()}…`);
}

function exportCurrent() {
  if (!state.story) return toast("Open a story first");
  const chapter = $("#exportScope").value === "chapter" ? state.chapter : null;
  download(state.story, $("#exportFormat").value, chapter);
}

async function printCurrent() {
  if (!state.story) return toast("Open a story first");
  const chapter = $("#exportScope").value === "chapter" ? state.chapter : null;
  try {
    const q = chapter ? `?chapter=${chapter}` : "";
    const r = await api(`/api/stories/${state.story}/print${q}`, { method: "POST" });
    toast("Opened in Preview. Press Cmd+P to print.", 4000);
    return r;
  } catch (e) { toast(e.message, 4000); }
}

async function kindle() {
  if (!state.story) return toast("Open a story first");
  try {
    const chapter = $("#exportScope").value === "chapter" ? state.chapter : null;
    const r = await api(`/api/stories/${state.story}/kindle`, { method: "POST", body: JSON.stringify({ chapter }) });
    const check = r.epubcheck == null ? "epubcheck not installed, so the file was not validated." : (r.epubcheck.ok ? "Validated with epubcheck." : "epubcheck reported problems.");
    modal(`<h3>Ready for Kindle</h3>
      <p>Saved <code>${esc(r.path)}</code>. ${check}</p>
      <p>Amazon's Send to Kindle takes EPUB. Pick one way to send it:</p>
      <ol>${r.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>
      ${r.calibre ? `<p class="muted">${esc(r.calibre)}</p>` : ""}
      <p class="muted small">Noirwrit never sends email or uploads anything itself.</p>`);
  } catch (e) { toast(e.message, 4000); }
}

// Memory ----------------------------------------------------------------------

async function loadMemory() {
  const m = await api("/api/memory");
  const parts = [`<p class="muted small">${m.total_chunks.toLocaleString()} chunks remembered · ${m.names_used} names used across stories (never reused).</p>`];
  if (m.context_sources.length) {
    parts.push(`<div class="panel"><h3>Your context</h3>${m.context_sources.map((s) => `<div class="row"><span style="flex:1">${esc(s.source)} <span class="muted small">(${s.chunks} chunks)</span></span><button data-forget="${esc(s.source)}">Forget</button></div>`).join("")}</div>`);
  }
  for (const s of m.stories) {
    parts.push(`<div class="mem-story"><h3>${esc(s.title)}</h3>
      <div class="mem-grid">${s.characters.map((c) => `<div><div class="role">${esc(c.role)}${c.alive === false ? " · dead" : ""}</div>${esc(c.name)}<div class="muted small">${esc(c.description)}</div></div>`).join("")}</div>
      <div class="mem-grid" style="margin-top:8px">${s.clues.map((c) => `<div><div class="role">${c.true ? "clue" : "red herring"} ${esc(c.id)}${c.planted ? " · planted" : ""}</div>${esc(c.text)}</div>`).join("")}</div>
      ${s.summaries.map((x) => `<p class="small"><span class="muted">Ch ${x.chapter_num}.</span> ${esc(x.text)}</p>`).join("")}
    </div>`);
  }
  $("#memoryBody").innerHTML = parts.join("");
  $$("[data-forget]").forEach((b) => b.addEventListener("click", async () => {
    await api(`/api/memory/sources/${encodeURIComponent(b.dataset.forget)}`, { method: "DELETE" });
    loadMemory();
  }));
}

async function ingest() {
  const fd = new FormData();
  fd.append("text", $("#ingestText").value);
  fd.append("source", $("#ingestSource").value || "pasted text");
  const f = $("#ingestFile").files[0];
  if (f) fd.append("file", f);
  const r = await fetch("/api/memory/ingest", { method: "POST", body: fd });
  const j = await r.json();
  $("#ingestResult").textContent = r.ok ? `Remembered ${j.chunks} chunks.` : (j.detail || "Failed");
  if (r.ok) { $("#ingestText").value = ""; $("#ingestFile").value = ""; loadMemory(); }
}

async function memSearch() {
  const q = $("#memQuery").value.trim();
  if (!q) return;
  const { hits } = await api(`/api/memory/search?q=${encodeURIComponent(q)}`);
  $("#memHits").innerHTML = hits.map((h) => `<div class="hit"><div class="muted small">${esc(h.source)} · ${h.score.toFixed(2)}</div>${esc(h.text.slice(0, 400))}…</div>`).join("") || `<p class="muted">Nothing found.</p>`;
}

// Settings ------------------------------------------------------------------

async function loadSettings() {
  const { settings, models } = await api("/api/settings");
  const sel = $("#modelSelect");
  sel.innerHTML = `<option value="">Best available</option>` + models.map((m) => `<option value="${esc(m.path)}">${esc(m.name)} (${m.kind}, ${m.size_mb} MB)</option>`).join("");
  const f = $("#settingsForm");
  for (const [k, v] of Object.entries(settings)) {
    const el = f.elements[k];
    if (!el) continue;
    if (el.type === "checkbox") el.checked = !!v; else el.value = v ?? "";
  }
  f.elements.ui_typing.value = typingMode();
  f.elements.ui_typingSpeed.value = prefs.get("typingSpeed", "natural");
  const st = await api("/api/status");
  $("#aboutBox").innerHTML = `Noirwrit ${esc(st.version)} · model: ${esc(st.model)} · embedder: ${esc(st.embedder)} · speed: ${st.tok_per_s || "not measured yet"} tok/s · works offline.`;
}

async function saveSettings(e) {
  e.preventDefault();
  const f = $("#settingsForm"), body = {};
  prefs.set("typing", f.elements.ui_typing.value);
  prefs.set("typingSpeed", f.elements.ui_typingSpeed.value);
  for (const el of f.elements) {
    if (!el.name || el.name.startsWith("ui_")) continue;
    if (el.type === "checkbox") body[el.name] = el.checked;
    else if (el.type === "number") body[el.name] = parseFloat(el.value);
    else body[el.name] = el.value || null;
  }
  await api("/api/settings", { method: "POST", body: JSON.stringify(body) });
  $("#settingsSaved").textContent = "Saved.";
  setTimeout(() => ($("#settingsSaved").textContent = ""), 2000);
}

// Status ----------------------------------------------------------------------

async function refreshStatus() {
  try {
    const s = await api("/api/status");
    const q = s.queue || {};
    const run = s.running ? `Writing ch ${s.running.chapter}${s.running.scene ? `, scene ${s.running.scene}/${s.running.of}` : ""}` : "Idle";
    $("#statusBox").innerHTML = `${run}<br>${q.queued || 0} queued · ${s.tok_per_s || "–"} tok/s<br><span title="${esc(s.model)}">${s.worker_alive ? "Worker running" : "Worker stopped"}</span>`;
  } catch (_) {}
}

// Theme, reader mode, shortcuts ------------------------------------------------

function setTheme(t) {
  document.documentElement.dataset.theme = t;
  $("#themeBtn").textContent = t === "dark" ? "Light" : "Dark";
  prefs.set("theme", t);
}
function toggleReaderMode() {
  const on = !$("#app").classList.contains("reader-mode");
  if (on && state.view !== "reader") show("reader");
  $("#app").classList.toggle("reader-mode", on);
  $("#readerModeBtn").textContent = on ? "Exit reader" : "Reader mode";
}

const SHORTCUTS = [
  ["→ or j", "Next chapter"], ["← or k", "Previous chapter"], ["r", "Reader mode"], ["t", "Light or dark theme"],
  ["[", "Show or hide the chapter sidebar"], ["n", "New story"], ["l", "Library"], ["g", "Reader"], ["m", "Memory"],
  ["s", "Settings"], ["e", "Export"], ["p", "Print"], ["f", "Finish typing (show the rest now)"], ["Esc", "Close dialog or leave reader mode"], ["?", "This help"],
];

function keys(e) {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const tag = (e.target.tagName || "").toLowerCase();
  if (["input", "textarea", "select"].includes(tag)) { if (e.key === "Escape") e.target.blur(); return; }
  const k = e.key;
  const map = {
    ArrowRight: () => state.view === "reader" && goChapter(state.chapter + 1), j: () => state.view === "reader" && goChapter(state.chapter + 1),
    ArrowLeft: () => state.view === "reader" && goChapter(state.chapter - 1), k: () => state.view === "reader" && goChapter(state.chapter - 1),
    r: toggleReaderMode, t: () => setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark"),
    "[": toggleSidebar, n: () => show("new"), l: () => show("library"),
    g: () => show("reader"), m: () => show("memory"), s: () => show("settings"), e: exportCurrent, p: printCurrent,
    f: () => typer.active && typer.skip(),
    "?": () => modal(`<h3>Keyboard shortcuts</h3>${SHORTCUTS.map(([a, b]) => `<div class="row"><span class="kbd">${a}</span> ${b}</div>`).join("")}`),
    Escape: () => { if (!$("#modal").classList.contains("hidden")) closeModal(); else if ($("#app").classList.contains("reader-mode")) toggleReaderMode(); },
  };
  if (map[k]) { e.preventDefault(); map[k](); }
}

const narrow = () => matchMedia("(max-width: 760px)").matches;
function closeDrawer() {
  $("#app").classList.remove("sidebar-open");
  document.querySelector(".scrim")?.remove();
}
function toggleSidebar() {
  if (!narrow()) { $("#app").classList.toggle("no-sidebar"); return; }
  if ($("#app").classList.contains("sidebar-open")) { closeDrawer(); return; }
  $("#app").classList.add("sidebar-open");
  const scrim = document.createElement("div");
  scrim.className = "scrim";
  scrim.addEventListener("click", closeDrawer);
  document.body.appendChild(scrim);
}

// Wire up ---------------------------------------------------------------------

function init() {
  setTheme(prefs.get("theme", "dark"));
  $$(".nav button").forEach((b) => b.addEventListener("click", () => show(b.dataset.view)));
  $("#createBtn").addEventListener("click", () => createStory(state.match ? "fresh" : "fresh"));
  $("#nextBtn").addEventListener("click", () => goChapter(state.chapter + 1));
  $("#prevBtn").addEventListener("click", () => goChapter(state.chapter - 1));
  $("#exportBtn").addEventListener("click", exportCurrent);
  $("#printBtn").addEventListener("click", printCurrent);
  $("#kindleBtn").addEventListener("click", kindle);
  $("#themeBtn").addEventListener("click", () => setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark"));
  $("#readerModeBtn").addEventListener("click", toggleReaderMode);
  $("#toggleSidebar").addEventListener("click", toggleSidebar);
  // On narrow screens, picking anything in the drawer closes it.
  $("#sidebar").addEventListener("click", (e) => { if (e.target.closest("button") && narrow()) closeDrawer(); });
  $("#helpBtn").addEventListener("click", () => keys({ key: "?", target: document.body, preventDefault() {} }));
  $("#modalClose").addEventListener("click", closeModal);
  $("#skipTyping").addEventListener("click", () => typer.skip());
  $("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") closeModal(); });
  $("#ingestBtn").addEventListener("click", ingest);
  $("#memSearchBtn").addEventListener("click", memSearch);
  $("#memQuery").addEventListener("keydown", (e) => { if (e.key === "Enter") memSearch(); });
  $("#settingsForm").addEventListener("submit", saveSettings);
  document.addEventListener("keydown", keys);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) schedulePoll(200); });

  refreshStatus();
  setInterval(refreshStatus, 5000);
  const last = prefs.get("story", null);
  const view = prefs.get("view", "library");
  if (last && view === "reader") openStory(last, prefs.get("pos." + last, 1)).catch(() => show("library"));
  else show(view === "reader" ? "library" : view);
}

init();
