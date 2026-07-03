# Spoken talk script for `agentic_ascend_operator_views_overview.en.marp.md`

Approximate duration: 15-18 minutes. The text is written for an overview talk: you can read it almost verbatim, or use it as speaker notes.

## Slide 1. Compiler-Derived Operator Views for Agentic AscendC Optimization

Today I want to present the general idea of this repository: how to make the optimization of AscendC operators more understandable for LLM agents.

The main point is simple: it is not enough to give the agent raw C++ code, compiler errors, and profiler text. For AscendC this is especially painful, because an operator consists of two coupled parts. On one side there is host-side tiling, where you decide how to split the data, how to distribute work across cores, and how to handle tails. On the other side there is the device-side kernel, where CopyIn, Compute, CopyOut, queues, buffers, synchronization, and vectorization live.

So the goal of the repository is to build an intermediate AI-facing layer. It should give the agent not just text, but structured views: operator semantics, tiling, pipeline, memory, dependencies, legal actions, and evidence from the profiler.

## Slide 2. Why raw code is not enough

The problem is that an AscendC operator is coupled. Performance depends not only on how well the kernel is written, but also on how the host part feeds data into that kernel.

If the agent sees only the source and the compiler log, it is forced to guess the hidden structure: which buffers are alive simultaneously, which dependencies forbid reordering, where there is a tail policy, where UB capacity is already at the limit, and which profiler counter corresponds to which part of the code.

In CUDA or Triton the model often has more ready-made examples from the open ecosystem. For AscendC there are fewer such examples, so simply relying on the model's knowledge is risky. We need an interface that makes the domain constraints explicit.

## Slide 3. The knowledge gap is real and measurable

Before the design, let me show that this is not a hypothetical problem. This slide uses real numbers from MultiKernelBench, as reported in the AscendOptimizer paper.

The table is Pass@1 for single-shot operator generation. Look at the contrast: DeepSeek-R1 reaches 52.6% on CUDA but only 1.4% on AscendC. Claude-Sonnet-4 is 47.0% versus 2.1%. Qwen3-235B in thinking mode is 44.2% versus 0.7%. So models that are genuinely strong on CUDA nearly fail on AscendC.

This is not just a syntax problem. There are few open AscendC kernels to learn from, the operator is a coupled two-part artifact, the UB/L1/L0 memory hierarchy has to be orchestrated by hand, and compiler or profiler feedback usually points at symptoms, not at the structural rewrite that would fix them. This is the empirical motivation for the whole repository: pretraining knowledge does not carry over, so the agent needs a compiler-derived interface.

## Slide 4. The central idea: representations, not prompts

Here is the overall pipeline.

At the input there is an operator specification: shapes, dtype, layout, numerical contract. There is AscendC or an intermediate representation where host tiling and the device kernel are already visible. Then an extractor builds analysis views: tiling, pipeline, memory/liveness, dependencies, performance evidence.

From these views an action space is formed. That is, the agent is offered not arbitrary "try to improve the code," but legal actions: change tile size, split, reorder, enable double buffering, change the granularity of data movement, change the tail policy, and so on.

After that the agent makes an edit, the harness compiles, checks correctness, profiles, and stores the result as evidence.

## Slide 5. System map: where the pieces live

This is the central diagram of the presentation.

On the left are the inputs: operator spec, AscendC source, compiler IR, and profiler traces. This is the raw material.

The next layer is the programming model. Here we separate semantics, schedule, data movement, and contracts. This matters because the LLM must understand not only the text of a function, but also what is part of the computation, what is part of the schedule, and what is a hardware constraint.

The third layer is the analysis views. Here concrete representations appear: tiling view, pipeline view, memory/liveness, dependence/legality, and performance evidence.

Then comes the layer of LLM decisions: diagnose, retrieve, plan action, patch. And on the right, the verification loop: compile, verify, profile, provenance.

The main message of the diagram: the agent does not jump directly from "raw code" to "patch." Between them there is a layer of structured knowledge.

## Slide 6. Programming models: what to make visible

Now let's break down the programming model.

The first layer is semantic. It answers the question: what does the operator actually compute? Here we need shapes, dtype, layout, broadcast and reduction semantics, and numerical tolerance.

The second layer is the schedule. This is the classic lesson of Halide, Tiramisu, TensorIR: you must separate what is computed from how it is laid out. For Ascend this means representing tile, split, reorder, vectorize, unroll, and other decisions separately.

The third layer is data movement. For Ascend this is critical: GM, UB, L1, L0, CopyIn, Compute, CopyOut, queues, and synchronization should not be scattered C++ code, but objects of the model. This is exactly the data-centric view that systems like DaCe and its SDFG representation make first-class.

In addition, contracts matter: preconditions, invariants, unsupported regimes, alignment and capacity rules. And finally, we need an action vocabulary, so that the agent chooses from legal transformations.

## Slide 7. Analysis tools: how to help the LLM

Here are the classic program analyses that can be reused. These are not new inventions - they have decades of foundations behind them.

Data-flow analysis, going back to Kildall in 1973, gives definitions, uses, constants, and ranges. This helps avoid guessing tiling parameters.

Liveness analysis shows which buffers are alive simultaneously and where the peak memory pressure is. This matters for UB reuse, double buffering, and memory placement.

Dependence analysis and the Program Dependence Graph, from Ferrante and colleagues in 1987, help understand what can be reordered and what cannot. For the agent this is especially valuable: it can propose reorder or fusion only where it is legal.

Loop and polyhedral analysis are useful for affine accesses, tiling legality, and loop-carried dependencies. Abstract interpretation, from Cousot in 1977, is the foundation for sound ranges and invariants.

Profiler evidence links low-level counters to an understandable bottleneck class and affected nodes. On Ascend there is concrete prior work here, such as the component-based roofline analysis published at ASPLOS 2025. The agent should see not just "a bad counter," but "here is the stage or buffer where the problem arises."

## Slide 8. Techniques worth building into the system

There are four techniques on this slide.

The first is Optimization Rewind. The idea is to take a strong implementation, remove an optimization motif from it in a controlled way, run it on hardware, and see whether it got worse. If it got worse, then the reverse change is a useful optimization pattern. Such experience can be saved and later reused.

The second technique is hardware-in-the-loop tiling. Tiling is hard to derive fully statically, because legality depends on shapes, alignment, buffer capacity, and the behavior of real hardware. Therefore a tiling candidate must be compiled, checked, and profiled on the device.

The third is retrieval-guided rewrite. The agent first diagnoses the bottleneck, then retrieves similar episodes, looks at applicability and avoid rules, and only then rewrites the code.

The fourth is a constrained action space. This is a way not to ask the LLM to "make it faster," but to give it a set of legal actions and preconditions.

## Slide 9. How the LLM decides with views

Here is the decision loop.

First, the agent observes the operator view, diagnostics, and profiling summary. Then it localizes the problem: it should be tied to a loop, buffer, pipeline stage, or tiling node. Then a legal action is selected and preconditions are checked. After that the agent makes a patch, and the result is stored in provenance and the experience bank.

Example question: can I increase the tile size without overflowing UB and without violating the tail policy? Without views this is almost a guess. With views the answer is assembled from the tiling view, memory/liveness, shape/range invariants, and profiler evidence.

## Slide 10. What sets this apart from AscendOptimizer

AscendOptimizer is the closest baseline for this topic, and it is worth grounding in its actual results. On a benchmark of 101 real AscendC operators from the cann-ops repository, it reaches a geometric-mean speedup of 1.21x over the open baseline, and 53.47% of operators beat their reference. On the hardest level-3 operators the geomean is 1.89, versus 1.38 for Best-of-N and 1.45 for OpenEvolve at the same evaluation budget. The ablation is telling: retrieved experience lifts the geomean from 1.09 to 1.16, while tiling search alone reaches only 1.02. All of this is measured on Ascend 910B2 with CANN 8.3, at 230 hardware evaluations per operator.

It already demonstrates several strong ideas: it builds an experience bank via Optimization Rewind, uses retrieval for kernel rewrite, tunes host-side tiling from hardware feedback, and requires no model fine-tuning.

Our extension in this repository is to add a structured layer before the agent action. Not just "there is experience," but experience tied to compiler-derived views. Not just "the profiler said it is slow," but a bottleneck linked to a specific node in the pipeline, memory, or dependence view. Not just "the model rewrote the code," but an action from a legal action space with an explanation of why it is legal.

## Slide 11. Real example: cross-operator motif transfer

Let me make this concrete with a real case from the AscendOptimizer paper, because it shows why structured experience matters.

The source operator is clip_by_value_v2. During Optimization Rewind, the system removes a motif it calls "consolidated loop with conditional tail" - where separate tail handling is folded into a single loop using a conditional like i equals last, choose tailNum, otherwise partNum. When you remove this motif, pipeline stalls rise by 28.6% and latency moves from 56 microseconds to 75 microseconds. So the motif itself is worth about 25%, and hardware validation confirms it.

Now take a structurally unrelated operator, upsample_nearest_exact3d, starting at 156 microseconds. Profiling localizes a GatherData hot path with vector-pipeline stalls. Retrieval pulls the motif that was mined from clip_by_value_v2, and the same loop consolidation is applied to GatherData. That produces the first big drop, from 156 to 145 microseconds.

Here is the striking part, the counterfactual. If you give the optimizer only an oracle description of the bottleneck but no retrieved experience, only 1 attempt in 100 reaches 145 microseconds - and it is still 1 in 100 even when you add the official Ascend C Best Practices documentation. So structured, transferable experience is the missing link from diagnosis to the right rewrite. That is precisely what compiler-derived views aim to standardize.

## Slide 12. Real example: a rewind-derived experience record

This slide shows what one experience record actually looks like, again a real one from the paper, for the operator eye.

The record captures more than a code diff. It has a canonical family - here kernel.memory.scatter. It has a root mechanism: the output is already zero-initialized, so only diagonal values need explicit writes. It has a causal chain: remove scattered zero writes, get fewer L2 misses, get higher bandwidth, get a shorter vector critical path. And it has reusable-when and avoid-when conditions.

The profiler evidence is dramatic: the L2 read hit rate goes from 0.02% to 87.5%, and task duration recovers from about 925 milliseconds down to about 1.19 milliseconds once the redundant writes are removed. The point is the shape of this record: it ties a concrete rewrite to a bottleneck, a mechanism, and hardware evidence, plus retrieval keys and safety conditions. This is exactly the "experience tied to view nodes and contracts" that a structured views layer should standardize, rather than leaving it as free-form text.

## Slide 13. Experimental framing

Such an approach should be evaluated not only by speedup.

There are three configurations. The first is raw source plus logs: the agent sees the code, compilation errors, test failures, and profiler text. This is the baseline.

The second is source plus profiling summaries. Here the agent gets structured diagnostics, but not yet full compiler-derived views.

The third is source plus operator views: semantic, tiling, pipeline, memory, dependence, and legal actions. This is exactly where the value of the AI-facing compiler layer is tested.

The metrics also fall into groups: correctness, performance, and reasoning. For us the important ones are compile success, functional correctness, speedup, fast_p, number of iterations, regression rate, the quality of explanations, and motif transferability.

## Slide 14. A minimal research artifact

A minimal useful artifact does not have to cover all of AscendC at once.

It is enough to take one operator, one shape, one dtype, and build a small but reproducible slice. It should contain a schema for the views, an extractor, an action checker, a harness, and an agent protocol.

It is important that every run leaves evidence: which views were built, which action the agent chose, which patch it applied, whether it compiled, whether correctness passed, what the profiler said, and which result went into provenance.

Exactly this kind of slice can then be expanded: add more operators, more shapes, more actions, and more techniques like Optimization Rewind.

## Slide 15. Prior art this builds on

I want to be explicit that this idea sits on top of a lot of real work, not in a vacuum.

For programming models and schedules there is Halide, TVM, Ansor, TensorIR, Tiramisu, and Exo; tile-centric models like Triton and TileLang; semantic and multi-level IR like StableHLO and MLIR; and the data-centric SDFG model from DaCe, which already treats data movement and double buffering as transformations.

For program analysis there are the classic foundations: Kildall's data-flow analysis, Cousot's abstract interpretation, the Program Dependence Graph, and more recent graph-based machine learning over programs like ProGraML.

For agentic kernel optimization there is KernelBench, TritonBench, and Geak; CompilerGPT, which feeds compiler reports to an agent; and, on Ascend specifically, AscendOptimizer, AscendCraft, and AscendKernelGen, plus the MultiKernelBench benchmark and the ASPLOS 2025 roofline analysis.

The gap they leave is that schedules, analyses, and agent loops mostly exist separately. This repository asks how to fuse them into compiler-derived views that a single agent consumes for AscendC. All links are in the bibliography folder.

## Slide 16. Conclusions

Finally, there are three conclusions.

First: the LLM needs an interface. Raw AscendC hides too many domain constraints, and the MultiKernelBench numbers show the gap is real.

Second: classic program analysis lowers risk. Dependence, liveness, range analysis, and legality checks help the agent avoid dangerous edits.

Third: experience becomes transferable when it is tied to the structure of the program. Optimization Rewind, retrieval, and provenance are especially strong when every experience record is tied to view nodes, bottleneck classes, and action contracts - as the clip_by_value_v2 and eye examples showed.

In one phrase, the project can be formulated as: compiler-derived operator knowledge views for agentic AscendC optimization.
