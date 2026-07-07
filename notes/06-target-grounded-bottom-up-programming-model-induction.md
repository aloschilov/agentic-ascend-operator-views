# Target-grounded bottom-up programming-model induction

## Working formulation

**Target-grounded bottom-up programming-model induction** asks how to automatically form a programming model when the lower target is already known: an ISA, AscendC, CUDA, MLIR dialect, runtime API, another language, a robot/controller API, or a set of cooperating controllers.

The intended output is not just a new DSL syntax. The output is an evolving programming-model basis:

- primitives;
- combinators;
- types;
- contracts;
- resource/effect semantics;
- lowering rules;
- verifiers;
- examples and documentation;
- cost models;
- reusable optimization motifs.

The central hypothesis is that an induced programming model should be accepted only if it improves synthesis, optimization, verification, interpretability, reuse, or performance compared with direct programming of the lower target.

## Why this matters for agentic operator optimization

Raw target code is too large and too unstructured for reliable LLM-agent optimization. A good programming model should expose the domain structure the agent must reason about:

```text
known target programs / traces / profiles
        -> pattern mining and lifting
        -> candidate abstractions
        -> typed constructs and contracts
        -> lowering rules
        -> compile / test / profile validation
        -> accepted programming-model basis
```

For AscendC, the recurring patterns are not only arithmetic operators. They include host-side tiling, core partitioning, GM/UB memory movement, CopyIn/Compute/CopyOut pipelines, double buffering, TPipe/TQue usage, synchronization, alignment, tail handling, and profiling-driven bottleneck motifs.

## Literature clusters

### 1. Library learning and abstraction invention

DreamCoder, Stitch, LILO, Babble, AbstractBeam, and related systems learn reusable abstractions from solved programs. This is the closest foundation for growing a programming-model basis from examples.

The key limitation is that learned abstractions often remain library-level and are not promoted into a compiler-backed programming model with type/effect semantics, lowering, verification, and performance contracts.

### 2. DSL and grammar induction

AutoDSL, Grammar Prompting, HYSYNTH, HyGenar, Text2DSL, and related work address grammar design, formal DSL generation, constrained generation, and surrogate grammars for program synthesis.

These works are relevant because they show how to make a language interface friendly to LLM generation. However, most systems assume that the DSL skeleton or grammar family is already substantially known.

### 3. Evolutionary program discovery

FunSearch, Evolution through Large Models, AlphaEvolve, STOP, LLaMEA, and CodeEvolve show how LLMs can be used inside evolutionary search loops with evaluator feedback.

The missing step for this topic is to evolve not only programs but also the reusable programming-model basis: primitives, laws, transformations, schedule templates, verifiers, and cost-model features.

### 4. Skill-library formation over known APIs and controllers

Voyager, Code as Policies, SayCan, Eureka, Lifelong Robot Library Learning, SkillX, HASP, CODESKILL, and similar systems learn or accumulate executable skills over a known API or controller substrate.

This is conceptually close to programming-model induction when the lower target is a controller API rather than an ISA or compiler IR. The gap is compiler-grade semantics: types, effects, resource constraints, aliasing, proof obligations, and target-aware lowering.

### 5. Compiler and IR substrate

MLIR, MimIR, CoCompiler, AscendCraft, and AscendOptimizer are relevant because a serious induced programming model needs an extensible IR, typed operations, verifier rules, and progressive lowering.

A useful rule of thumb: library learning can suggest the abstractions, but compiler infrastructure must make them first-class and safe.

## Proposed evaluation

Compare three modes:

1. **Raw target programming:** LLM edits AscendC/CUDA/MLIR directly.
2. **Helper-library programming:** LLM uses a hand-written helper API.
3. **Induced programming model:** LLM uses learned primitives, laws, verifiers, lowering rules, and cost semantics.

Measure:

- correctness rate;
- number of failed compile/test iterations;
- performance relative to reference;
- search-space reduction;
- reuse of discovered constructs;
- explanation quality;
- human interpretability;
- robustness across operator families.

## Research gap

Existing work usually learns libraries, generates DSL code, evolves programs, or optimizes target code. The open problem is to automatically induce and evolve a compiler-backed programming model from low-level programs, compiler artifacts, and execution evidence.
