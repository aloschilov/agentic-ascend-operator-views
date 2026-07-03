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
- [`presentations/agentic_ascend_operator_views_survey.en.marp.md`](presentations/agentic_ascend_operator_views_survey.en.marp.md) — English survey deck across the full bibliography (Ascend/NPU, agentic optimization, compiler IR/autotuning, program analysis).
- [`presentations/agentic_ascend_operator_views_survey.ru.marp.md`](presentations/agentic_ascend_operator_views_survey.ru.marp.md) — Russian survey deck (same content in Russian).
- [`presentations/agentic_ascend_operator_views_survey_speech.en.md`](presentations/agentic_ascend_operator_views_survey_speech.en.md) — English spoken-talk script for the survey deck.
- [`presentations/agentic_ascend_operator_views_survey_speech.ru.md`](presentations/agentic_ascend_operator_views_survey_speech.ru.md) — Russian spoken-talk script for the survey deck.
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

This repository stores links, metadata, working notes, and vendored PDF copies of the linked publications (listed below). A few sources are only available as HTML pages (Cousot 1977, StableHLO spec, Triton 2019); those, plus the download manifest, remain local-only and are not committed.

To (re)download everything for local offline reading, run:

```bash
python3 tools/download_publications.py
```

Downloaded PDFs are written to `publications/files/`; non-PDF downloads and the manifest are ignored by git.

## Vendored publication PDFs

Full-text PDFs of the linked papers are committed under [`publications/files/`](publications/files/).

Ascend / NPU-specific:

- [AscendOptimizer: Episodic Agent for Ascend NPU Operator Optimization](publications/files/ascendoptimizer-2026.pdf)
- [AscendCraft: Automatic Ascend NPU Kernel Generation via DSL-Guided Transcompilation](publications/files/ascendcraft-2026.pdf)
- [AscendKernelGen: LLM-Based Kernel Generation for Neural Processing Units](publications/files/ascendkernelgen-2026.pdf)
- [MultiKernelBench: A Multi-Platform Benchmark for Kernel Generation](publications/files/multikernelbench-2025.pdf)
- [Squeezing Operator Performance Potential for the Ascend Architecture (ASPLOS'25)](publications/files/ascend-roofline-2025.pdf)

Agentic kernel optimization:

- [KernelBench: Can LLMs Write Efficient GPU Kernels?](publications/files/kernelbench-2025.pdf)
- [TritonBench: Benchmarking LLM Capabilities for Generating Triton Operators](publications/files/tritonbench-2025.pdf)
- [Geak: Triton Kernel AI Agent & Evaluation Benchmarks](publications/files/geak-2025.pdf)
- [CompilerGPT: LLMs for Analyzing and Acting on Compiler Optimization Reports](publications/files/compilergpt-2025.pdf)
- [Language Models for Code Optimization: Survey, Challenges and Future Directions](publications/files/codeopt-survey-2025.pdf)

Compiler IR, scheduling, autotuning:

- [MLIR: A Compiler Infrastructure for the End of Moore's Law](publications/files/mlir-2020.pdf)
- [TVM: An Automated End-to-End Optimizing Compiler for Deep Learning](publications/files/tvm-2018.pdf)
- [Learning to Optimize Tensor Programs (AutoTVM)](publications/files/autotvm-2018.pdf)
- [Ansor: Generating High-Performance Tensor Programs for Deep Learning](publications/files/ansor-2020.pdf)
- [Tensor Program Optimization with Probabilistic Programs (MetaSchedule)](publications/files/metaschedule-2022.pdf)
- [TensorIR: An Abstraction for Automatic Tensorized Program Optimization](publications/files/tensorir-2022.pdf)
- [Halide: Decoupling Algorithms from Schedules](publications/files/halide-2017.pdf)
- [Exo: A Usable User-Schedulable Programming Language for Accelerators](publications/files/exo-2022.pdf)
- [Stateful Dataflow Multigraphs (DaCe/SDFG)](publications/files/dace-sdfg-2019.pdf)
- [Tiramisu: A Polyhedral Compiler for Expressing Fast and Portable Code](publications/files/tiramisu-2018.pdf)

Program-analysis foundations:

- [A Unified Approach to Global Program Optimization (Kildall, 1973)](publications/files/kildall-1973.pdf)
- [The Program Dependence Graph and Its Use in Optimization (1987)](publications/files/pdg-1987.pdf)
- [ProGraML: Graph-based Deep Learning for Program Optimization and Analysis](publications/files/programl-2020.pdf)

> These PDFs are third-party publications included for research convenience; copyright remains with the original authors and publishers.
