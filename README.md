# Project Sentinel

**An autonomous AI agent that detects production errors, diagnoses the root cause, writes and tests a fix, and reports back — all without a human in the loop until final approval.**

Think of it as a night-shift engineer: when your app throws an error log, Sentinel wakes up, reads the traceback, searches your actual codebase for the relevant code, writes a fix, runs your real test suite against it in an isolated sandbox, retries if it fails, and produces a clear post-mortem report — all before a human ever needs to look at it.

---

## What it does

1. **Watches** a directory for new error logs (`watchdog`)
2. **Triages** the traceback to extract exception type, file, and function
3. **Retrieves** relevant code context from the codebase using AST-based chunking + vector search (ChromaDB), following function call chains across multiple files
4. **Plans** a fix using a local LLM (Qwen2.5-Coder via Ollama) with structured, schema-validated output (Pydantic)
5. **Generates a patch** — potentially spanning multiple files — also schema-validated
6. **Checks the patch** against a safety guardrail layer (blocks dangerous patterns like `rm -rf`, `os.system`, `eval`)
7. **Requests human approval** before anything touches a real file — no patch is ever auto-applied
8. **Applies the patch atomically** (all files succeed or none do)
9. **Verifies the fix** by running the real test suite inside a network-isolated, resource-capped Docker sandbox
10. **Self-corrects** — if tests fail, the failure is fed back to the planner, which tries again (up to 3 attempts)
11. **Reports** the full story — error, root cause, diff, test results — as a markdown post-mortem
12. **Traces everything** — every LLM call, tool call, and decision is logged via Arize Phoenix for full auditability

## Architecture

```
Watchdog → Triage → ChromaDB (RAG) → LLM Planner → Patch Generator
                                                          ↓
                                                   Safety Guardrails
                                                          ↓
                                                  Human Approval Gate
                                                          ↓
                                              Docker-Sandboxed Verify
                                                    ↓           ↑
                                              Post-Mortem    (retry loop,
                                                Report        max 3x)
```

Built as a [LangGraph](https://github.com/langchain-ai/langgraph) state machine — the retry loop is a real cycle in the graph, not a wrapper script.

## Tech stack

| Component | Tool |
|---|---|
| Orchestration | LangGraph |
| LLM | Qwen2.5-Coder, served locally via Ollama |
| Structured output | Pydantic V2 |
| Retrieval | ChromaDB + AST-based code chunking |
| Sandbox | Docker (network-isolated, resource-capped) |
| Test execution | pytest |
| Observability | Arize Phoenix (OpenTelemetry) |
| File watching | watchdog |

Everything runs **locally** — no source code ever leaves the machine, which matters for a tool with read/write access to a real codebase.

## Why these design choices

- **Human approval before any write.** The agent reasons, patches, and verifies — but a human always has final say before a change lands on disk.
- **Plain-code safety guardrails, not prompt-based ones.** Dangerous patterns are blocked by a regex layer, never left to the LLM's judgment alone.
- **Docker sandbox, not a bare subprocess.** Test runs have no network access and capped memory/CPU — a bad patch can't exfiltrate data or take down the host.
- **Atomic multi-file patches.** A fix touching multiple files either fully applies or fully rolls back — never a half-applied state.
- **Structured output everywhere.** Every LLM response is validated against a Pydantic schema, so a malformed response fails loudly instead of silently corrupting downstream state.

## Benchmark

Tested against a corpus of 10 hand-written bugs spanning off-by-one errors, type errors, missing null checks, boolean logic inversions, wrong exception handling, and multi-file bugs. See `benchmark/results/` for the current scorecard.

## Setup

```bash
git clone <your-repo-url>
cd sentinel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Pull the local model (requires Ollama: https://ollama.com)
ollama pull qwen2.5-coder:7b
ollama serve &

# Start observability
phoenix serve &

# Build the sandbox image
docker build -t sentinel-sandbox -f Dockerfile.sandbox .

# Index your target codebase
python src/index_repo.py

# Start the agent
python src/main.py
```

Drop a `.log` file into `data/inbox/` to trigger a run. View live traces at `http://localhost:6006`.

## Status

Built as a 7-day solo project. Core loop, multi-file patching, human approval gate, and Docker sandboxing are working end to end. See `benchmark/results/` for current accuracy numbers.

## Roadmap

- [ ] Slack / GitHub PR integration for approval (currently CLI-based)
- [ ] Support for languages beyond Python
- [ ] Hybrid local-model + frontier-model escalation policy
- [ ] Expanded benchmark corpus

---

