# Automatic discovery of a CuTe-like algebraic programming model

## Working formulation

A stronger version of automatic DSL discovery is **automatic discovery of the algebraic structure of the domain**.

If the desired result is something at the level of CuTe DSL, then the goal is not merely to discover a set of commands such as `copy_tile`, `split_axis`, or `make_buffer`. The goal is to discover a structured algebraic programming model:

```text
objects:
  Shape, Layout, Tensor, Tile, ThreadLayout, MemorySpace, PipelineStage

operations:
  compose, product, divide, tile, coalesce, complement, inverse, project, partition

laws:
  associativity, identity, invertibility, compatibility, normal forms, equivalence rules

semantics:
  logical coordinate -> physical index
  logical tile -> memory movement
  pipeline stage -> resource/effect transition

lowering:
  algebraic expression -> target implementation
```

## DSL vs algebraic programming model

A command-style DSL exposes useful functions. An algebraic programming model exposes objects, closed operations, laws, equivalence rules, normal forms, verifiers, cost semantics, and lowering rules.

The difference matters because agentic optimization needs reasoning:

- whether two schedules are equivalent;
- whether a layout transformation preserves coverage;
- whether a tile decomposition is compatible with memory alignment;
- whether a pipeline transformation violates dependencies;
- whether double buffering is legal under buffer-lifetime constraints;
- whether an expression can be normalized and lowered efficiently.

## CuTe-level criteria

A CuTe-level result should contain at least:

1. carrier objects;
2. a closed set of operations;
3. algebraic laws and rewrite rules;
4. equivalence checking or equality saturation;
5. normal forms;
6. verifier constraints;
7. cost semantics;
8. lowering rules;
9. examples and documentation;
10. a way to reject unsound or unhelpful constructs.

## Candidate algebras for Ascend

A direct copy of CuTe is not enough for Ascend. The central structures differ. An Ascend-oriented algebraic programming model probably needs several coupled algebras.

| Algebra | What it models | Example operations |
| --- | --- | --- |
| Layout algebra | logical tensor to physical memory/index mapping | compose, product, tile, coalesce, inverse, swizzle |
| Tiling algebra | host-side work decomposition | split_axis, core_partition, tile_shape, tail_policy |
| Memory movement algebra | GM/UB/L1/L0 transfers | promote, copy_tile, vectorized_copy, align, pad |
| Pipeline algebra | CopyIn/Compute/CopyOut concurrency | sequence, overlap, double_buffer, barrier |
| Queue/event algebra | TPipe/TQue/event behavior | enqueue, dequeue, wait, signal, token |
| Effect/resource algebra | lifetimes, ownership, hazards, capacity | allocate, release, reuse, noalias, capacity_check |
| Cost algebra | performance model | bytes, cycles, stalls, bandwidth, occupancy |

## Discovery pipeline

```text
1. collect low-level implementations
2. build semantic traces and IR graphs
3. lift code into a raw term/graph representation
4. mine recurring structures and motifs
5. propose candidate abstractions and operations
6. propose candidate laws and preconditions
7. validate with property tests, SMT, symbolic execution, compiler verifiers, and profilers
8. store accepted laws in an e-graph / rewrite system
9. add type/effect/resource constraints
10. implement lowering rules
11. evaluate synthesis, optimization, verification, and performance
```

LLMs should act as proposers, namers, generalizers, documenters, and search guides. They should not be the final judges. The judges are the compiler, verifier, tests, profilers, solvers, and equality engines.

## Example target expression

A useful Ascend-oriented algebraic layer might let an agent work with expressions like this:

```text
pipeline =
  double_buffer(
    sequence(
      copy(GM[A] -> UB[A_tile]),
      compute(vector_add, UB[A_tile], UB[B_tile] -> UB[C_tile]),
      copy(UB[C_tile] -> GM[C])
    )
  )

schedule =
  core_partition(axis=N, cores=K)
  . tile(axis=M, size=T)
  . guard_tail(predicate)
```

Then the system can run:

```text
verify(schedule, pipeline) -> OK / violation
cost(schedule, pipeline) -> predicted bottleneck
rewrite(schedule, pipeline) -> equivalent improved schedule
lower(schedule, pipeline) -> AscendC / MLIR / ISA target code
```

## Research gap

The relevant literature already covers parts of this:

- CuTe shows a mature human-designed layout algebra.
- E-graphs and equality saturation provide machinery for equivalence classes and rewrite exploration.
- LILO, Stitch, and Babble learn reusable abstractions from examples.
- AscendCraft and AscendOptimizer show target-aware LLM/agent loops for Ascend.

The gap is automatic induction of the algebra itself: objects, operations, laws, normal forms, verifiers, cost semantics, and lowering rules from low-level target programs and execution evidence.
