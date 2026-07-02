# Notes: Compiler IR, scheduling, and autotuning

## Why this cluster matters

This cluster supplies design patterns for representing operators, schedules, transformations, search spaces, and hardware-specific lowering.

## Key ideas to reuse

### Algorithm/schedule separation

Halide and Tiramisu show that separating what is computed from how it is scheduled is a strong design pattern. For Ascend, this suggests separating:

- operator semantics;
- tiling strategy;
- memory placement;
- CopyIn/Compute/CopyOut pipeline;
- synchronization and double buffering.

### Tensor IR and schedule actions

TVM, Ansor, MetaSchedule, and TensorIR provide precedents for exposing schedule transformations as structured actions rather than arbitrary source edits.

Candidate Ascend schedule actions:

- choose tile size;
- split work across cores;
- choose UB buffer layout;
- enable/disable double buffering;
- reorder pipeline stages where legal;
- change vectorization/unrolling;
- change tail handling;
- adjust GM/UB movement granularity;
- modify queue depth.

### Data-centric IR

DaCe/SDFG is especially relevant because Ascend performance often depends on data movement and overlap. SDFG-style views suggest making data movement and dependencies first-class.

### MLIR/StableHLO

MLIR is relevant as a general infrastructure for dialects and multi-level IR. StableHLO is relevant as a semantic upper-level operator view, not as a full performance model.
