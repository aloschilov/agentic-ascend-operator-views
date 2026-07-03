# Spoken talk script for `agentic_ascend_operator_views_overview.en.marp.md`

Approximate duration: 12-15 minutes. The text is written for an overview talk: you can read it almost verbatim, or use it as speaker notes.

## Slide 1. Compiler-Derived Operator Views for Agentic AscendC Optimization

Today I want to present the general idea of this repository: how to make the optimization of AscendC operators more understandable for LLM agents.

The main point is simple: it is not enough to give the agent raw C++ code, compiler errors, and profiler text. For AscendC this is especially painful, because an operator consists of two coupled parts. On one side there is host-side tiling, where you decide how to split the data, how to distribute work across cores, and how to handle tails. On the other side there is the device-side kernel, where CopyIn, Compute, CopyOut, queues, buffers, synchronization, and vectorization live.

So the goal of the repository is to build an intermediate AI-facing layer. It should give the agent not just text, but structured views: operator semantics, tiling, pipeline, memory, dependencies, legal actions, and evidence from the profiler.

## Slide 2. Why raw code is not enough

The problem is that an AscendC operator is coupled. Performance depends not only on how well the kernel is written, but also on how the host part feeds data into that kernel.

If the agent sees only the source and the compiler log, it is forced to guess the hidden structure: which buffers are alive simultaneously, which dependencies forbid reordering, where there is a tail policy, where UB capacity is already at the limit, and which profiler counter corresponds to which part of the code.

In CUDA or Triton the model often has more ready-made examples from the open ecosystem. For AscendC there are fewer such examples, so simply relying on the model's knowledge is risky. We need an interface that makes the domain constraints explicit.

## Slide 3. The central idea: representations, not prompts

Here is the overall pipeline.

At the input there is an operator specification: shapes, dtype, layout, numerical contract. There is AscendC or an intermediate representation where host tiling and the device kernel are already visible. Then an extractor builds analysis views: tiling, pipeline, memory/liveness, dependencies, performance evidence.

From these views an action space is formed. That is, the agent is offered not arbitrary "try to improve the code," but legal actions: change tile size, split, reorder, enable double buffering, change the granularity of data movement, change the tail policy, and so on.

After that the agent makes an edit, the harness compiles, checks correctness, profiles, and stores the result as evidence.

## Slide 4. System map: where the pieces live

This is the central diagram of the presentation.

On the left are the inputs: operator spec, AscendC source, compiler IR, and profiler traces. This is the raw material.

The next layer is the programming model. Here we separate semantics, schedule, data movement, and contracts. This matters because the LLM must understand not only the text of a function, but also what is part of the computation, what is part of the schedule, and what is a hardware constraint.

The third layer is the analysis views. Here concrete representations appear: tiling view, pipeline view, memory/liveness, dependence/legality, and performance evidence.

Then comes the layer of LLM decisions: diagnose, retrieve, plan action, patch. And on the right, the verification loop: compile, verify, profile, provenance.

The main message of the diagram: the agent does not jump directly from "raw code" to "patch." Between them there is a layer of structured knowledge.

## Slide 5. Programming models: what to make visible

Now let's break down the programming model.

The first layer is semantic. It answers the question: what does the operator actually compute? Here we need shapes, dtype, layout, broadcast and reduction semantics, and numerical tolerance.

The second layer is the schedule. This is the classic lesson of Halide, Tiramisu, TensorIR: you must separate what is computed from how it is laid out. For Ascend this means representing tile, split, reorder, vectorize, unroll, and other decisions separately.

The third layer is data movement. For Ascend this is critical: GM, UB, L1, L0, CopyIn, Compute, CopyOut, queues, and synchronization should not be scattered C++ code, but objects of the model.

In addition, contracts matter: preconditions, invariants, unsupported regimes, alignment and capacity rules. And finally, we need an action vocabulary, so that the agent chooses from legal transformations.

## Slide 6. Analysis tools: how to help the LLM

Here are the classic program analyses that can be reused.

Data-flow analysis gives definitions, uses, constants, and ranges. This helps avoid guessing tiling parameters.

Liveness analysis shows which buffers are alive simultaneously and where the peak memory pressure is. This matters for UB reuse, double buffering, and memory placement.

Dependence analysis and the PDG help understand what can be reordered and what cannot. For the agent this is especially valuable: it can propose reorder or fusion only where it is legal.

Loop and polyhedral analysis are useful for affine accesses, tiling legality, and loop-carried dependencies.

Profiler evidence links low-level counters to an understandable bottleneck class and affected nodes. That is, the agent sees not just "a bad counter," but "here is the stage or buffer where the problem arises."

## Slide 7. Techniques worth building into the system

There are four techniques on this slide.

The first is Optimization Rewind. The idea is to take a strong implementation, remove an optimization motif from it in a controlled way, run it on hardware, and see whether it got worse. If it got worse, then the reverse change is a useful optimization pattern. Such experience can be saved and later reused.

The second technique is hardware-in-the-loop tiling. Tiling is hard to derive fully statically, because legality depends on shapes, alignment, buffer capacity, and the behavior of real hardware. Therefore a tiling candidate must be compiled, checked, and profiled on the device.

The third is retrieval-guided rewrite. The agent first diagnoses the bottleneck, then retrieves similar episodes, looks at applicability and avoid rules, and only then rewrites the code.

The fourth is a constrained action space. This is a way not to ask the LLM to "make it faster," but to give it a set of legal actions and preconditions.

## Slide 8. How the LLM decides with views

Here is the decision loop.

First, the agent observes the operator view, diagnostics, and profiling summary. Then it localizes the problem: it should be tied to a loop, buffer, pipeline stage, or tiling node. Then a legal action is selected and preconditions are checked. After that the agent makes a patch, and the result is stored in provenance and the experience bank.

Example question: can I increase the tile size without overflowing UB and without violating the tail policy? Without views this is almost a guess. With views the answer is assembled from the tiling view, memory/liveness, shape/range invariants, and profiler evidence.

## Slide 9. What sets this apart from AscendOptimizer

AscendOptimizer is the closest baseline for this topic. It already demonstrates several strong ideas: it builds an experience bank via Optimization Rewind, uses retrieval for kernel rewrite, tunes host-side tiling from hardware feedback, and requires no model fine-tuning.

Our extension in this repository is to add a structured layer before the agent action. Not just "there is experience," but experience tied to compiler-derived views. Not just "the profiler said it is slow," but a bottleneck linked to a specific node in the pipeline, memory, or dependence view. Not just "the model rewrote the code," but an action from a legal action space with an explanation of why it is legal.

## Slide 10. Experimental framing

Such an approach should be evaluated not only by speedup.

There are three configurations. The first is raw source plus logs: the agent sees the code, compilation errors, test failures, and profiler text. This is the baseline.

The second is source plus profiling summaries. Here the agent gets structured diagnostics, but not yet full compiler-derived views.

The third is source plus operator views: semantic, tiling, pipeline, memory, dependence, and legal actions. This is exactly where the value of the AI-facing compiler layer is tested.

The metrics also fall into groups: correctness, performance, and reasoning. For us the important ones are compile success, functional correctness, speedup, fast_p, number of iterations, regression rate, the quality of explanations, and motif transferability.

## Slide 11. A minimal research artifact

A minimal useful artifact does not have to cover all of AscendC at once.

It is enough to take one operator, one shape, one dtype, and build a small but reproducible slice. It should contain a schema for the views, an extractor, an action checker, a harness, and an agent protocol.

It is important that every run leaves evidence: which views were built, which action the agent chose, which patch it applied, whether it compiled, whether correctness passed, what the profiler said, and which result went into provenance.

Exactly this kind of slice can then be expanded: add more operators, more shapes, more actions, and more techniques like Optimization Rewind.

## Slide 12. Conclusions

Finally, there are three conclusions.

First: the LLM needs an interface. Raw AscendC hides too many domain constraints.

Second: classic program analysis lowers risk. Dependence, liveness, range analysis, and legality checks help the agent avoid dangerous edits.

Third: experience becomes transferable when it is tied to the structure of the program. Optimization Rewind, retrieval, and provenance are especially strong when every experience record is tied to view nodes, bottleneck classes, and action contracts.

In one phrase, the project can be formulated as: compiler-derived operator knowledge views for agentic AscendC optimization.
