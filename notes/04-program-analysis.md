# Notes: Program-analysis foundations

## Why this cluster matters

The proposed AI-facing operator views can reuse classic compiler analysis rather than inventing everything from scratch.

## Reusable analyses

### Data-flow analysis

Use for:

- reaching definitions;
- live variable / buffer liveness;
- available expressions;
- constant propagation;
- value/range propagation for tiling parameters.

### Dependence analysis / PDG

Use for:

- data/control dependence graph;
- legal reordering constraints;
- pipeline dependency view;
- explaining why a transformation is illegal.

### Abstract interpretation

Use for:

- shape/range/alignment invariants;
- UB capacity safety;
- tail correctness;
- monotonic fixed-point summaries of loop/kernel behavior.

### Loop and polyhedral analysis

Use for:

- affine accesses;
- loop-carried dependencies;
- tiling legality;
- fusion/interchange/reorder legality.

### Graph representations for ML over code

ProGraML is a useful precedent for representing programs as attributed graphs with control, data, and call relations. For Ascend, this can be specialized into an operator knowledge graph with pipeline and memory-space annotations.
