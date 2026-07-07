# Compiler-Derived Operator Knowledge Views for Agentic AscendC Optimization

This repository is a structured exploration space for the topic:

> How can compiler tools and program-analysis artifacts make AI-agentic ML operator optimization more effective, especially for AscendC operators?

The central hypothesis is that AI agents should not optimize raw AscendC source code alone. They should consume structured, compiler-derived operator knowledge views: semantic operator information, tiling parameters, CopyIn/Compute/CopyOut pipeline structure, memory-space and buffer-liveness information, dependence graphs, legal transformation actions, and profiling-based bottleneck evidence.

## Repository map

- [`docs/problem-statement.md`](docs/problem-statement.md) — cleaned research/problem statement.
- [`docs/initial-prompt-commentary.ru.md`](docs/initial-prompt-commentary.ru.md) — Russian translation and critique of the original formulation.
- [`docs/visual-roadmaps.md`](docs/visual-roadmaps.md) — high-level Russian visual maps for the harness, bottom-up programming-model induction, and CuTe-like algebraic DSL discovery.
- [`bibliography/reading-list.md`](bibliography/reading-list.md) — human-readable linked bibliography.
- [`bibliography/articles.yaml`](bibliography/articles.yaml) — structured metadata for linked articles and docs.
- [`bibliography/programming-model-induction.yaml`](bibliography/programming-model-induction.yaml) — structured links for bottom-up programming-model induction and algebraic programming-model discovery.
- [`publications/README.md`](publications/README.md) — instructions for local-only downloaded copies of linked publications.
- [`notes/01-ascend-npu.md`](notes/01-ascend-npu.md) — Ascend/NPU-specific sources.
- [`notes/02-agentic-kernel-optimization.md`](notes/02-agentic-kernel-optimization.md) — LLM/agentic kernel optimization sources.
- [`notes/03-compiler-ir-autotuning.md`](notes/03-compiler-ir-autotuning.md) — compiler IR, tensor IR, scheduling, autotuning.
- [`notes/04-program-analysis.md`](notes/04-program-analysis.md) — static analysis, dependence graphs, dataflow, abstract interpretation.
- [`notes/05-ascend-toolchain-views.md`](notes/05-ascend-toolchain-views.md) — candidate AI-facing compiler/toolchain views.
- [`notes/06-target-grounded-bottom-up-programming-model-induction.md`](notes/06-target-grounded-bottom-up-programming-model-induction.md) — target-grounded bottom-up programming-model induction with LLMs.
- [`notes/07-algebraic-programming-model-induction.md`](notes/07-algebraic-programming-model-induction.md) — automatic discovery of a CuTe-like algebraic programming model.
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

## Visual roadmaps

- [Harness for AI Agentic Operator Code Analysis & Programming Model](docs/visual-roadmaps.md#1-harness-for-ai-agentic-operator-code-analysis--programming-model)
- [Bottom-up programming-model induction with LLMs](docs/visual-roadmaps.md#2-bottom-up-programming-model-induction-with-llms)
- [Automatic discovery of a CuTe-level algebraic programming model](docs/visual-roadmaps.md#3-automatic-discovery-of-a-cute-level-algebraic-programming-model)

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

This repository stores links, metadata, working notes, and vendored PDF copies of the linked publications (listed below). A few sources are only available as HTML pages (Cousot 1977, StableHLO spec, Triton 2019, AlphaDev 2023); those, plus the download manifest, remain local-only and are not committed.

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

Programming-model induction:

- [DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning](publications/files/dreamcoder-2020.pdf)
- [Stitch: Top-Down Synthesis for Library Learning](publications/files/stitch-2022.pdf)
- [LILO: Learning Interpretable Libraries by Compressing and Documenting Code](publications/files/lilo-2023.pdf)
- [Babble: Learning Better Abstractions with E-Graphs and Anti-Unification](publications/files/babble-2022.pdf)
- [AutoDSL: Automated Domain-Specific Language Design](publications/files/autodsl-2024.pdf)
- [Grammar Prompting for Domain-Specific Language Generation with LLMs](publications/files/grammar-prompting-2023.pdf)
- [HYSYNTH: LLM-guided surrogate grammars for program synthesis](publications/files/hysynth-2024.pdf)
- [Mathematical discoveries from program search with large language models (FunSearch)](publications/files/funsearch-2023.pdf)
- [Evolution through Large Models](publications/files/evolution-through-large-models-2022.pdf)
- [AlphaEvolve: A coding agent for scientific and algorithmic discovery](publications/files/alphaevolve-2025.pdf)
- [Voyager: An Open-Ended Embodied Agent with Large Language Models](publications/files/voyager-2023.pdf)
- [Code as Policies: Language Model Programs for Embodied Control](publications/files/code-as-policies-2022.pdf)
- [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](publications/files/saycan-2022.pdf)
- [Eureka: Human-Level Reward Design via Coding Large Language Models](publications/files/eureka-2023.pdf)
- [MimIR: Extensible and type-safe IR with typed axioms and plugins](publications/files/mimir-2024.pdf)

Algebraic programming-model induction:

- [CuTe Layout Representation and Algebra](publications/files/cute-layout-algebra-2026.pdf)
- [Categorical Foundations for CuTe Layouts](publications/files/cute-categorical-foundations-2026.pdf)
- [Modeling Layout Abstractions Using Integer Set Relations](publications/files/integer-set-layout-abstractions-2025.pdf)
- [egg: Fast and Extensible Equality Saturation](publications/files/egg-2020.pdf)
- [STOKE: Stochastic Superoptimization](publications/files/stoke-2012.pdf)
- [ARISE: Automatic RISC-V Instruction Set Extension](publications/files/arise-2025.pdf)

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
