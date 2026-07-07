# Linked reading list

## 1. Ascend / NPU-specific

- [AscendOptimizer: Episodic Agent for Ascend NPU Operator Optimization](https://arxiv.org/abs/2603.23566) — closest direct match: agentic AscendC operator optimization, host-side tiling, kernel scheduling/pipelining.
- [AscendCraft: Automatic Ascend NPU Kernel Generation via DSL-Guided Transcompilation](https://arxiv.org/abs/2601.22760) — DSL-guided AscendC generation; important for AI-friendly programming model design.
- [AscendKernelGen: A Systematic Study of LLM-Based Kernel Generation for Neural Processing Units](https://arxiv.org/abs/2601.07160) — domain-specific kernel generation/evaluation for Ascend NPUs.
- [MultiKernelBench: A Multi-Platform Benchmark for Kernel Generation](https://arxiv.org/abs/2507.17773) — benchmark across Nvidia GPU, Huawei NPU, and Google TPU.
- [Squeezing Operator Performance Potential for the Ascend Architecture](https://cs.nju.edu.cn/tianchen/lunwen/2025/asplos25-yuhang.pdf) — component-based roofline and bottleneck analysis for Ascend operators.
- [NPUMeter: Automatic Operator Optimization for Ascend NPU with Accurate Analytical Performance Models](https://dl.acm.org/doi/10.1145/3820380) — added as to-verify source for Ascend performance modeling / automatic optimization.

## 2. LLM / agentic kernel optimization

- [KernelBench: Can LLMs Write Efficient GPU Kernels?](https://arxiv.org/abs/2502.10517) — benchmark for fast and correct GPU kernels.
- [TritonBench: Benchmarking Large Language Model Capabilities for Generating Triton Operators](https://arxiv.org/abs/2502.14752) — Triton operator generation benchmark.
- [Geak: Introducing Triton Kernel AI Agent & Evaluation Benchmarks](https://arxiv.org/abs/2507.23194) — agentic Triton generation for AMD GPUs.
- [CompilerGPT: Leveraging Large Language Models for Analyzing and Acting on Compiler Optimization Reports](https://arxiv.org/abs/2506.06227) — compiler reports as LLM input for optimization.
- [Language Models for Code Optimization: Survey, Challenges and Future Directions](https://arxiv.org/abs/2501.01277) — broad survey.

## 3. Programming-model induction

- [DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning](https://arxiv.org/abs/2006.08381) — learns reusable symbolic abstractions from solved programs.
- [Stitch: Top-Down Synthesis for Library Learning](https://arxiv.org/abs/2211.16605) — extracts reusable functions from corpora.
- [LILO: Learning Interpretable Libraries by Compressing and Documenting Code](https://arxiv.org/abs/2310.19791) — combines LLM-guided synthesis, symbolic compression, and documentation.
- [Babble: Learning Better Abstractions with E-Graphs and Anti-Unification](https://arxiv.org/abs/2212.04596) — abstraction learning modulo equivalence rules.
- [AutoDSL: Automated Domain-Specific Language Design for Structural Representation of Procedures with Constraints](https://arxiv.org/abs/2406.12324) — automated constrained DSL design.
- [Grammar Prompting for Domain-Specific Language Generation with Large Language Models](https://arxiv.org/abs/2305.19234) — grammars as an LLM-facing constraint layer.
- [HYSYNTH: LLM-guided surrogate grammars for program synthesis](https://arxiv.org/abs/2405.15880) — surrogate grammar induction for synthesis.
- [Mathematical discoveries from program search with large language models](https://www.nature.com/articles/s41586-023-06924-6) — FunSearch/evaluator-driven program evolution.
- [Evolution through Large Models](https://arxiv.org/abs/2206.08896) — LLMs as mutation operators in evolutionary search.
- [AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) — evaluator-driven code evolution at scale.
- [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) — growing executable skill library.
- [Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753) — policy code assembled from available APIs.
- [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691) — planning constrained by skill affordances.
- [Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931) — evolved reward programs.
- [MimIR: Extensible and type-safe IR with typed axioms and plugins](https://arxiv.org/abs/2411.07443) — typed IR model for DSL-level abstractions.

## 4. Algebraic programming-model induction

- [CuTe Layout Representation and Algebra](https://arxiv.org/abs/2603.02298) — formalizes CuTe-style layout algebra.
- [Categorical Foundations for CuTe Layouts](https://arxiv.org/abs/2601.05972) — categorical account of CuTe layouts.
- [Modeling Layout Abstractions Using Integer Set Relations](https://arxiv.org/abs/2511.10374) — integer-set view of layout abstractions.
- [egg: Fast and Extensible Equality Saturation](https://arxiv.org/abs/2004.03082) — e-graph substrate for rewrite search.
- [STOKE: Stochastic Superoptimization](https://arxiv.org/abs/1211.0557) — low-level superoptimization over target instructions.
- [Faster sorting algorithms discovered using deep reinforcement learning](https://www.nature.com/articles/s41586-023-06004-9) — AlphaDev/low-level algorithm discovery.
- [ARISE: Automatic RISC-V Instruction Set Extension](https://arxiv.org/abs/2508.07725) — ISA extension induction from assembly patterns.

## 5. Compiler IR, scheduling, autotuning

- [MLIR: A Compiler Infrastructure for the End of Moore's Law](https://arxiv.org/abs/2002.11054)
- [StableHLO Specification](https://openxla.org/stablehlo/spec)
- [TVM: An Automated End-to-End Optimizing Compiler for Deep Learning](https://arxiv.org/abs/1802.04799)
- [Learning to Optimize Tensor Programs](https://arxiv.org/abs/1805.08166)
- [Ansor: Generating High-Performance Tensor Programs for Deep Learning](https://arxiv.org/abs/2006.06762)
- [Tensor Program Optimization with Probabilistic Programs](https://arxiv.org/abs/2205.13603)
- [TensorIR: An Abstraction for Automatic Tensorized Program Optimization](https://arxiv.org/abs/2207.04296)
- [Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations](https://research.ibm.com/publications/triton-an-intermediate-language-and-compiler-for-tiled-neural-network-computations)
- [Halide: decoupling algorithms from schedules for high-performance image processing](https://cacm.acm.org/research/halide/)
- [Exo: A Usable User-Schedulable Programming Language for Accelerators](https://people.csail.mit.edu/yuka/pdf/exo_pldi2022_full.pdf)
- [Stateful Dataflow Multigraphs: A Data-Centric Model for Performance Portability on Heterogeneous Architectures](https://arxiv.org/abs/1902.10345)
- [Tiramisu: A Polyhedral Compiler for Expressing Fast and Portable Code](https://arxiv.org/abs/1804.10694)

## 6. Program analysis foundations

- [A Unified Approach to Global Program Optimization](https://dl.acm.org/doi/10.1145/512927.512945) — Kildall/data-flow analysis.
- [Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml)
- [The Program Dependence Graph and Its Use in Optimization](https://dl.acm.org/doi/10.1145/24039.24041)
- [ProGraML: Graph-based Deep Learning for Program Optimization and Analysis](https://arxiv.org/abs/2003.10536)
