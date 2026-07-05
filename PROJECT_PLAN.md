# PROJECT_PLAN.md — ENTROGX LinkedIn Surge Agent (Mission A)

## 1. Objective

Build an AI agent that helps the ENTROGX Media team create high-quality LinkedIn **posts** and **comment replies** aligned with ENTROGX's brand voice. Version 1 generates content **for human review only** — it never publishes to LinkedIn directly.

## 2. About ENTROGX

ENTROGX is an AI-native venture studio focused on energy innovation, sustainability, AI, and emerging technologies. Brand values: founder mindset, clarity over cleverness, professional B2B communication, innovation, sustainability, energy transition, high-quality execution. All generated content must reflect this identity.

## 3. Evaluation Criteria (what the agent is graded on)

| # | Criterion | What it means for the agent |
|---|---|---|
| 1 | **Content Strategy & Planning** | Alignment with B2B tone and ENTROGX brand voice |
| 2 | **Visual Design Quality** | Professional, scroll-stopping assets (V1: a structured visual brief a designer can execute) |
| 3 | **Engagement Outcomes** | Content designed to earn comments, reshares, saves from a B2B audience |
| 4 | **Messaging Precision** | Founder-voice-aligned clarity and effective calls-to-action |

Everything in this plan is designed to directly serve these four criteria — see `TECH_STACK.md` and `ARCHITECTURE.md` for how each system layer maps back to them.

## 4. Locked Design Decisions

| Decision | Choice |
|---|---|
| Backend | Python + FastAPI |
| Frontend | React (Vite + TypeScript) — kept intentionally simple/MVP-scoped |
| Deployment (V1) | Local only, single user, no auth, no hosting |
| LLM | Google AI Studio (Gemini API via Google Gen AI SDK) |
| Visual output (V1) | Text-only structured visual brief — no image generation |
| Knowledge Base primary source | Official ENTROGX brand voice documentation |
| Founder voice | Not attempted in V1. `founder_voice.md` is a reserved, pluggable slot — added later with zero architecture changes |
| LinkedIn publishing | Out of scope entirely for V1 (human copies approved content manually) |

## 5. Project Phases

| # | Phase | Why Necessary | What We Build | Key Deliverables | Files | Best Practices | Complete When |
|---|---|---|---|---|---|---|---|
| 0 | **Foundations & Environment Setup** | Nothing else can start without a working skeleton and verified API access | Repo scaffold, Python venv, Google AI Studio API key wired, FastAPI "hello world", Vite app calling it | Working local dev loop | `backend/app/main.py`, `frontend/` scaffold, `.env.example`, `requirements.txt`, `package.json` | Never commit real API keys; use `.env` + `.gitignore`; pin dependency versions | `GET /health` returns 200, visible from the React app |
| 1 | **Knowledge Base Construction** | Content quality on all 4 rubric categories depends more on KB quality than on code | Structured Markdown/YAML files transcribing the official brand voice docs, audience personas, vocabulary, real example posts | Populated `backend/app/knowledge/` | `company_profile.md`, `brand_voice.md`, `target_audience.md`, `writing_style.md`, `vocabulary.yaml`, `forbidden_words.yaml`, `cta_examples.yaml`, `hashtag_bank.yaml`, `example_posts/*.md` | Keep each file single-purpose and short enough to fully inject into a prompt; cite the source doc at the top of each file | A human unfamiliar with ENTROGX can read the KB and correctly describe its voice |
| 2 | **Prompt Library & LLM Client** | Prompts are the actual "agent logic" — must be versioned, testable, and separate from app code | Jinja2-templated prompt files + a thin Gemini client wrapper (model, retries, token/cost logging) | Working prompt render + Gemini call | `backend/app/prompts/*.md`, `backend/app/services/llm_client.py` | One prompt = one file; no prompt text inline in Python; wrapper is the only place that calls the Google Gen AI SDK | Every prompt template renders with KB context and returns a valid Gemini response in a scratch script |
| 3 | **Core Agent Orchestration (Backend)** | Wires KB + prompts + LLM into the actual generation pipeline behind an API | FastAPI routers + orchestrator service implementing the generate → evaluate → revise loop | Working `/generate/*` endpoints | `backend/app/api/*.py`, `backend/app/services/orchestrator.py` | Orchestrator has no HTTP knowledge; routers have no LLM knowledge — keep layers separated | `POST /generate/post` returns a draft + eval scores end-to-end via curl/Postman |
| 4 | **Evaluation Layer** | The assignment is graded on 4 rubric dimensions — the agent should self-check before a human ever sees a draft | LLM-as-judge module scoring drafts 0–10 on the 4 categories + rationale + revision trigger | Working evaluator + improver loop | `backend/app/services/evaluator.py`, `content_evaluator.md`, `content_improver.md` | Force structured JSON output from the evaluator; cap revision iterations to avoid runaway loops/cost | Evaluator returns scores matching the 4 rubric categories on a sample draft |
| 5 | **Frontend Review UI** | Human-in-the-loop approval is a hard requirement — nothing may auto-publish | Simple React SPA: input form, draft review screen (copy + hooks + visual brief + scores), approve/reject/edit, history list | Working browser UI | `frontend/src/pages/*`, `frontend/src/api/client.ts` | Keep components small and few; no state-management library; TypeScript types mirror backend Pydantic schemas | A user can go from "enter topic" to "approve draft" fully in-browser |
| 6 | **Logging, Config, Persistence** | Needed to debug prompt quality over time and keep an audit trail | Structured JSON-lines logging, Pydantic `Settings`, SQLite history store | Working persistence + logs | `backend/app/core/config.py`, `backend/app/db/*.py`, `logs/` | Log prompt version + model + tokens + latency + eval scores for every call; never log secrets | Every generation is logged and persisted to SQLite |
| 7 | **Testing & QA** | Prevent silent prompt/logic regressions as KB and prompts evolve | Unit tests for KB loader/orchestrator; manual rubric QA pass | Passing test suite + QA notes | `backend/tests/*` | Test the KB loader and evaluator parsing deterministically; treat LLM output tests as smoke tests, not exact-match assertions | `pytest` green; ≥10 sample generations manually reviewed against the rubric |
| 8 | **Documentation & Demo Prep** | This is a graded internship deliverable — presentation matters | Finalize all five docs, write a short demo script, capture best example outputs | Final docs + `examples/` | repo-root `.md` files, `examples/` | Keep docs in sync with actual code by the end of the build, not just at the start | You can demo start-to-finish in under 5 minutes using the docs as a script |
| 9+ | **Future (not built now)** | Explicitly out of scope for V1 | LinkedIn API, Canva/image-gen, multi-user auth, cloud deploy, engagement-analytics feedback loop, vector/RAG KB, real founder-voice modeling | — | — | — | — |

## 6. MVP Definition

### Version 1 (Must Build)
- Topic/goal input form (post or comment reply)
- Post Generator, Comment Reply Generator, Hook Generator, Hashtag Generator, Visual Brief Generator (text-only)
- Content Evaluator scoring the 4 rubric dimensions
- Content Improver auto-revision loop (capped iterations)
- Review UI: view draft, inline edit, approve/reject/regenerate
- SQLite history log of every generation and its outcome
- Basic structured logging + centralized config

**Why these and only these:** this set directly and completely targets the four graded categories using a text-only visual brief (avoiding image-generation scope) and a static, direct-injection knowledge base (avoiding RAG/vector-DB scope). It is a complete, demoable, human-in-the-loop system.

### Future Versions (Explicitly Deferred)
| Feature | Why deferred |
|---|---|
| Carousel/multi-slide generator | Extra content type, not required to hit the 4 criteria with a single post format |
| Real AI image generation / Canva integration | New external API, cost, and prompt-to-image tuning — the rubric can be met with a strong text brief |
| LinkedIn API (scheduling/auto-publish) | The assignment explicitly requires human-review-only; building this now works against the spec |
| Engagement-analytics feedback loop | Requires the LinkedIn API and real post history first |
| Multi-user auth & roles | Not needed for a local, single-user V1 |
| Vector-DB/RAG knowledge base | Current KB is small enough for direct context injection; adds complexity with no current benefit |
| Real founder-voice modeling | No real founder writing samples exist yet; the KB is designed so this drops in later with no refactor (see `ARCHITECTURE.md` §5) |
| Cloud deployment | V1 is local-only by design; hosting adds auth/secrets-management scope not needed for the internship deliverable |

## 7. Roadmap

The granular, ordered task breakdown lives in `TASK_TRACKER.md`. At a glance, build order follows the phase table in §5 above: environment → knowledge base → prompts/LLM client → orchestration → evaluation → frontend → persistence/logging → testing → documentation.
