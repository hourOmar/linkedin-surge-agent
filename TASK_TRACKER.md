# TASK_TRACKER.md — ENTROGX LinkedIn Surge Agent (Mission A)

Tasks are ordered for sequential completion. Difficulty: **S** = small (<1hr), **M** = medium (1–3hrs), **L** = large (half day+).

## Phase 0 — Foundations & Environment Setup

### Task 1: Initialize repo scaffold
- **Purpose:** Create the base directory structure for backend and frontend
- **Difficulty:** S
- **Dependencies:** None
- **Expected files:** `backend/`, `frontend/`, `.gitignore` update, `scripts/`
- **Checklist:**
  - [ ] `backend/app/` with empty `api/`, `core/`, `services/`, `prompts/`, `knowledge/`, `models/`, `db/` subfolders
  - [ ] `frontend/` scaffolded via `npm create vite@latest -- --template react-ts`
  - [ ] `.gitignore` covers `venv/`, `node_modules/`, `.env`, `*.db`, `logs/`

### Task 2: Python environment + dependencies
- **Purpose:** Reproducible backend environment
- **Difficulty:** S
- **Dependencies:** Task 1
- **Expected files:** `backend/requirements.txt`, `backend/.env.example`
- **Checklist:**
  - [ ] `requirements.txt` includes `fastapi`, `uvicorn`, `pydantic-settings`, `google-genai`, `jinja2`, `sqlalchemy` (or plan to use `sqlite3`), `pytest`
  - [ ] `.env.example` documents `GOOGLE_API_KEY`, `MODEL_NAME`, etc. (no real secrets committed)

### Task 3: FastAPI hello-world + `/health`
- **Purpose:** Verify the backend boots and is reachable
- **Difficulty:** S
- **Dependencies:** Task 2
- **Expected files:** `backend/app/main.py`
- **Checklist:**
  - [ ] `uvicorn app.main:app --reload` runs without error
  - [ ] `GET /health` returns `{"status": "ok"}`

### Task 4: Vite React scaffold hitting `/health`
- **Purpose:** Verify frontend-backend connectivity end to end
- **Difficulty:** S
- **Dependencies:** Task 3
- **Expected files:** `frontend/src/App.tsx`
- **Checklist:**
  - [ ] Frontend dev server runs and fetches `/health` on load
  - [ ] Response is displayed somewhere visible (temporary debug text is fine)

### Task 5: Config/Settings via pydantic-settings
- **Purpose:** Centralize all configuration, no hardcoded values in services
- **Difficulty:** S
- **Dependencies:** Task 3
- **Expected files:** `backend/app/core/config.py`
- **Checklist:**
  - [ ] `Settings` class loads `GOOGLE_API_KEY`, `MODEL_NAME`, `MAX_REVISIONS`, `EVAL_THRESHOLD`, `DB_PATH`, `LOG_PATH` from `.env`
  - [ ] Settings importable as a singleton across the app

### Task 6: Gemini client wrapper + smoke test
- **Purpose:** Confirm real API connectivity before building anything on top of it
- **Difficulty:** S
- **Dependencies:** Task 5
- **Expected files:** `backend/app/services/llm_client.py`, a throwaway smoke-test script
- **Checklist:**
  - [ ] Wrapper exposes a single `generate(prompt, ...)` function using the Google Gen AI SDK
  - [ ] Manual smoke test returns a real Gemini response

## Phase 1 — Knowledge Base Construction

### Task 7: Draft `company_profile.md`
- **Purpose:** Encode ENTROGX's mission/vision/portfolio focus
- **Difficulty:** M
- **Dependencies:** Task 1; needs your source material
- **Expected files:** `backend/app/knowledge/company_profile.md`
- **Checklist:** [ ] Reviewed against official ENTROGX materials for accuracy

### Task 8: Transcribe `brand_voice.md` from official docs
- **Purpose:** Primary source of truth for tone — highest-leverage KB file
- **Difficulty:** M
- **Dependencies:** Task 1; needs your official brand voice documentation
- **Expected files:** `backend/app/knowledge/brand_voice.md`
- **Checklist:**
  - [ ] Directly sourced from official docs, not paraphrased from memory
  - [ ] Includes company-level "founder mindset" tone attributes (not person-specific)

### Task 9: Draft `target_audience.md` and `writing_style.md`
- **Purpose:** Give the agent audience personas and LinkedIn-specific formatting conventions
- **Difficulty:** M
- **Dependencies:** Task 1
- **Expected files:** `backend/app/knowledge/target_audience.md`, `backend/app/knowledge/writing_style.md`

### Task 10: Import real example posts
- **Purpose:** Give the LLM concrete style references, not just abstract rules
- **Difficulty:** S
- **Dependencies:** Needs your real past posts
- **Expected files:** `backend/app/knowledge/example_posts/*.md`
- **Checklist:** [ ] Each post tagged with type (thought-leadership/announcement/hot-take) and performance if known

### Task 11: Build `vocabulary.yaml`, `forbidden_words.yaml`, `cta_examples.yaml`, `hashtag_bank.yaml`
- **Purpose:** Machine-checkable brand guardrails
- **Difficulty:** M
- **Dependencies:** Tasks 8–10 inform content
- **Expected files:** the four YAML files listed
- **Checklist:** [ ] Forbidden words list includes generic B2B clichés and excessive emoji/hashtag patterns

### Task 12: Build the Knowledge Base loader
- **Purpose:** Load KB files into structured context for prompt assembly, with the founder-voice pluggable-slot design
- **Difficulty:** M
- **Dependencies:** Tasks 7–11
- **Expected files:** `backend/app/services/kb_loader.py`
- **Checklist:**
  - [ ] Loader scans `knowledge/` directory rather than hardcoding a file list
  - [ ] Each known filename maps to a named context slot
  - [ ] Missing files (e.g. `founder_voice.md`) are silently omitted, not errors

## Phase 2 — Prompt Library & LLM Client

### Task 13: `system_prompt.md` + Jinja rendering utility
- **Purpose:** Core persona injected into every call, with conditional founder-voice block
- **Difficulty:** S
- **Dependencies:** Task 12
- **Expected files:** `backend/app/prompts/system_prompt.md`, rendering helper in `services/`
- **Checklist:** [ ] Contains `{% if founder_voice %}...{% endif %}` block

### Task 14: `post_generator.md` prompt + first orchestrator call
- **Purpose:** First real end-to-end generation
- **Difficulty:** M
- **Dependencies:** Tasks 6, 12, 13
- **Expected files:** `backend/app/prompts/post_generator.md`, `backend/app/services/orchestrator.py` (initial version)
- **Checklist:** [ ] Renders with real KB context and returns a plausible LinkedIn post draft

### Task 15: `hook_generator.md`, `hashtag_generator.md`, `visual_brief_generator.md`
- **Purpose:** Supporting generation prompts
- **Difficulty:** M
- **Dependencies:** Task 14
- **Expected files:** the three prompt files

### Task 16: `comment_reply_generator.md`
- **Purpose:** Second content type
- **Difficulty:** S
- **Dependencies:** Task 14

## Phase 3 — Evaluation Layer

### Task 17: `content_evaluator.md` + structured score parsing
- **Purpose:** Score drafts on the 4 rubric dimensions with a machine-parseable output
- **Difficulty:** M
- **Dependencies:** Task 14
- **Expected files:** `backend/app/prompts/content_evaluator.md`, `backend/app/services/evaluator.py`
- **Checklist:** [ ] Output reliably parses as JSON with the 4 score fields + rationale

### Task 18: `content_improver.md` + revision loop
- **Purpose:** Auto-revise low-scoring drafts before showing them to a human
- **Difficulty:** M
- **Dependencies:** Task 17
- **Expected files:** `backend/app/prompts/content_improver.md`, revision loop logic in `orchestrator.py`
- **Checklist:** [ ] Loop capped at `MAX_REVISIONS`; never blocks reaching the human reviewer

## Phase 4 — Persistence, Logging, API

### Task 19: SQLite schema + history persistence
- **Purpose:** Audit trail of every generation and its outcome
- **Difficulty:** M
- **Dependencies:** Task 5
- **Expected files:** `backend/app/db/models.py`, `backend/app/db/session.py`
- **Checklist:** [ ] Table stores input, draft, scores, revision count, status (approved/rejected/pending)

### Task 20: JSON-lines logging through the orchestrator
- **Purpose:** Debuggability of prompt/model behavior over time
- **Difficulty:** S
- **Dependencies:** Task 14
- **Expected files:** `backend/app/core/logging.py`, `logs/agent.log`
- **Checklist:** [ ] Every LLM call logs prompt version, model, tokens, latency, eval scores

### Task 21: API routers — `/generate/post`, `/generate/reply`, `/history`
- **Purpose:** Expose the orchestrator over HTTP
- **Difficulty:** M
- **Dependencies:** Tasks 14–20
- **Expected files:** `backend/app/api/generate.py`, `backend/app/api/history.py`, Pydantic schemas in `backend/app/models/`
- **Checklist:** [ ] All endpoints tested via curl/Postman end-to-end

## Phase 5 — Frontend

### Task 22: New Content form page
- **Purpose:** Input capture UI
- **Difficulty:** M
- **Dependencies:** Task 21
- **Expected files:** `frontend/src/pages/NewContent.tsx`, `frontend/src/api/client.ts`, `frontend/src/types/`

### Task 23: Draft Review page
- **Purpose:** Core review/approve UI — the human checkpoint
- **Difficulty:** L
- **Dependencies:** Task 22
- **Expected files:** `frontend/src/pages/ReviewDraft.tsx`, `frontend/src/components/DraftCard.tsx`, `ScoreBadge.tsx`, `VisualBriefPanel.tsx`
- **Checklist:** [ ] Shows copy, hook variants, hashtags, visual brief, and rubric scores; supports edit/approve/reject/regenerate

### Task 24: History page
- **Purpose:** Browse past generations
- **Difficulty:** M
- **Dependencies:** Task 21
- **Expected files:** `frontend/src/pages/History.tsx`

## Phase 6 — Testing & QA

### Task 25: Backend unit tests
- **Purpose:** Guard against silent regressions in deterministic logic
- **Difficulty:** M
- **Dependencies:** Tasks 12, 17, 21
- **Expected files:** `backend/tests/test_kb_loader.py`, `test_orchestrator.py`, `test_evaluator.py`
- **Checklist:** [ ] KB loader tests cover the missing-file (pluggable slot) case explicitly

### Task 26: Manual rubric QA pass
- **Purpose:** Human validation that the agent actually performs well on the 4 criteria, not just that the code runs
- **Difficulty:** M
- **Dependencies:** Full pipeline working
- **Checklist:** [ ] ≥10 generations reviewed by hand against the rubric; notes captured on KB/prompt gaps found

## Phase 7 — Documentation & Demo Prep

### Task 27: Finalize docs and capture examples
- **Purpose:** Grading-ready deliverable
- **Difficulty:** S
- **Dependencies:** All prior tasks
- **Expected files:** `examples/` populated with best sample outputs; all five root docs updated to match final implementation
- **Checklist:** [ ] Demo walkthrough runs start-to-finish in under 5 minutes
