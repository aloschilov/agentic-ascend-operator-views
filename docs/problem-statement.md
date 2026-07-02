# Problem statement

## Working title

**Compiler-Derived Operator Knowledge Views for Agentic AscendC Optimization**

## Motivation

LLM-based coding agents can generate and modify accelerator kernels, but raw-source prompting is a weak interface for performance optimization. It forces the agent to infer domain structure from syntax, compiler errors, and profiler logs. For AscendC operators this is especially fragile: performance depends on host-side tiling, device-side kernel scheduling, explicit data movement, queues, synchronization, and pipeline overlap.

## Core idea

Build a harness that extracts structured, compiler-derived knowledge views from AscendC source, operator metadata, compiler artifacts, and profiling output. The AI agent receives these views together with a constrained set of legal optimization actions instead of editing arbitrary code blindly.

## Candidate views

1. **Operator semantic view** — op type, tensor ranks/shapes, dtypes, layouts, broadcast/reduction semantics, numerical constraints.
2. **Tiling view** — axes, tile sizes, block split, core split, tail handling, host tiling parameters.
3. **Pipeline view** — CopyIn / Compute / CopyOut stages, queue operations, synchronization, stage overlap, double-buffering opportunities.
4. **Memory-space view** — GM/UB/L1/L0/L0C usage, buffer liveness, alignment, reuse, capacity pressure.
5. **Dependence view** — def-use chains, data/control dependencies, alias/effect information, legal reordering constraints.
6. **Loop/polyhedral view** — loop nests, affine accesses, dependence vectors, legal transformations.
7. **Action-space view** — legal schedule transformations such as tile, split, reorder, double-buffer, vectorize, unroll, fuse, prefetch.
8. **Performance evidence view** — profiler counters, bottleneck classification, component utilization, MTE/compute imbalance, latency breakdown.
9. **Transformation provenance view** — what was changed, why, expected benefit, actual result, regression status.

## Research questions

1. Which intermediate representations and analysis artifacts can an Ascend compilation/tooling pipeline expose for AI-driven operator tuning?
2. Which classical program-analysis techniques can be reused directly: dataflow analysis, dependence analysis, liveness, alias/effect analysis, loop analysis, polyhedral analysis?
3. What additional programming-model abstractions, annotations, or schedule-level constructs are needed to make AscendC operators inherently more comprehensible to AI systems?
4. Does providing structured compiler-derived views improve agent success rate, correctness, performance, and explanation quality compared with raw-source-code prompting?

## Evaluation sketch

Compare three configurations:

1. **Raw source + logs**: the agent sees source code, compiler errors, test failures, and profiler text.
2. **Source + profiling summaries**: the agent also gets structured latency and bottleneck summaries.
3. **Source + compiler-derived operator views**: the agent gets semantic, tiling, pipeline, memory, dependence, and legal-action views.

Metrics:

- compile success;
- functional correctness;
- speedup / ratio to reference;
- number of iterations;
- regression rate;
- explanation quality;
- transferability of optimization motifs across operators.
