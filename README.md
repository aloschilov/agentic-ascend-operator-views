# Compiler-Derived Operator Knowledge Views for Agentic AscendC Optimization

This repository is a structured exploration space for the topic:

> How can compiler tools and program-analysis artifacts make AI-agentic ML operator optimization more effective, especially for AscendC operators?

The central hypothesis is that AI agents should not optimize raw AscendC source code alone. They should consume structured, compiler-derived operator knowledge views: semantic operator information, tiling parameters, CopyIn/Compute/CopyOut pipeline structure, memory-space and buffer-liveness information, dependence graphs, legal transformation actions, and profiling-based bottleneck evidence.

## Repository map

- [`docs/problem-statement.md`](docs/problem-statement.md) — cleaned research/problem statement.
- [`docs/initial-prompt-commentary.ru.md`](docs/initial-prompt-commentary.ru.md) — Russian translation and critique of the original formulation.
- [`bibliography/reading-list.md`](bibliography/reading-list.md) — human-readable linked bibliography.
- [`bibliography/articles.yaml`](bibliography/articles.yaml) — structured metadata for linked articles and docs.
- [`publications/README.md`](publications/README.md) — instructions for local-only downloaded copies of linked publications.
- [`notes/01-ascend-npu.md`](notes/01-ascend-npu.md) — Ascend/NPU-specific sources.
- [`notes/02-agentic-kernel-optimization.md`](notes/02-agentic-kernel-optimization.md) — LLM/agentic kernel optimization sources.
- [`notes/03-compiler-ir-autotuning.md`](notes/03-compiler-ir-autotuning.md) — compiler IR, tensor IR, scheduling, autotuning.
- [`notes/04-program-analysis.md`](notes/04-program-analysis.md) — static analysis, dependence graphs, dataflow, abstract interpretation.
- [`notes/05-ascend-toolchain-views.md`](notes/05-ascend-toolchain-views.md) — candidate AI-facing compiler/toolchain views.
- [`presentations/agentic_ascend_operator_views_overview.en.marp.md`](presentations/agentic_ascend_operator_views_overview.en.marp.md) — English overview Marp deck for compiler-derived operator views and agentic AscendC optimization.
- [`presentations/agentic_ascend_operator_views_overview.ru.marp.md`](presentations/agentic_ascend_operator_views_overview.ru.marp.md) — Russian overview Marp deck (same content in Russian).
- [`presentations/agentic_ascend_operator_views_overview_speech.en.md`](presentations/agentic_ascend_operator_views_overview_speech.en.md) — English spoken-talk script for the overview deck.
- [`presentations/agentic_ascend_operator_views_overview_speech.ru.md`](presentations/agentic_ascend_operator_views_overview_speech.ru.md) — Russian spoken-talk script for the overview deck.
- [`templates/article-note.md`](templates/article-note.md) — template for per-paper notes.
- [`roadmap.md`](roadmap.md) — next steps for turning the topic into a concrete research artifact.

## Short positioning

Existing LLM coding frameworks often expose agents to raw source code, compiler errors, logs, and profiling output. For AscendC, this is not enough because performance depends on coupled host-side tiling and device-side kernel scheduling/pipelining, including memory movement, queues, synchronization, and explicit pipeline overlap.

A stronger architecture is:

```text
AscendC source / operator spec / compiler IR
        -> static-analysis extractor
        -> semantic + tiling + pipeline + memory + dependence + profiling views
        -> constrained agent action space
        -> compile / verify / profile loop
        -> optimized kernel + explanation + reusable motifs
```

## What is stored here

This repository stores links, metadata, and working notes. It does not vendor full PDFs or copyrighted article text.

For local offline reading, run:

```bash
python3 tools/download_publications.py
```

Downloaded files are written to `publications/files/` and ignored by git.
