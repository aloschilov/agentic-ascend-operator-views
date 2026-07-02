# Roadmap

## Phase 1 — Literature map

- Verify all links and add BibTeX.
- Create one article note per core source.
- Separate direct Ascend work from analogies in GPU/Triton/TVM/MLIR.

## Phase 2 — View schema

- Define a versioned JSON schema for operator knowledge views.
- Start with five views: semantic, tiling, pipeline, memory/liveness, performance evidence.
- Add examples for simple vector ops: abs, add, tanh, reduce_sum, rms_norm.

## Phase 3 — Extractor prototype

- Parse AscendC source patterns: CopyIn, Compute, CopyOut, TPipe/TQue, DataCopy.
- Extract queue and buffer information.
- Infer simple dataflow/dependence graph.
- Attach profiler evidence by source/view node.

## Phase 4 — Agent harness

- Compare raw-source prompting vs structured-view prompting.
- Restrict agent actions to legal transformations where possible.
- Record transformation provenance and regression history.

## Phase 5 — Evaluation

Suggested metrics:

- compile success;
- functional correctness;
- performance ratio to reference;
- number of iterations;
- agent cost/tokens;
- regression rate;
- explanation quality;
- motif reuse across operators.
