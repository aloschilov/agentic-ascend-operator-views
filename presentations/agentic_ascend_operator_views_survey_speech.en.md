# Spoken talk script for `agentic_ascend_operator_views_survey.en.marp.md`

Approximate duration: 22-26 minutes. This is a survey talk: it walks through four literature clusters and then synthesizes them. You can read it almost verbatim or use it as speaker notes.

## Slide 1. Title and framing

This talk is a survey of the research landscape around one question: how can compiler tools and program-analysis artifacts make AI-agentic operator optimization more effective, especially for AscendC operators on Ascend NPUs.

I have organized roughly thirty works into four clusters: Ascend and NPU-specific work, agentic kernel optimization, compiler IR and autotuning, and the classic foundations of program analysis. The thesis I will build toward is that the individual pieces already exist across these communities, but nobody has fused them into a single AI-facing view layer for AscendC - and that integration is the opportunity.

## Slide 2. Scope and method

Let me be explicit about how I read the literature. For every work I ask two questions: what does the optimizer actually see, and how does it decide. That lets me compare a benchmark, a compiler, and an RL system on the same terms.

The four clusters are: Cluster A, the Ascend domain itself with its baselines; Cluster B, agentic optimization - benchmarks, agents, and reinforcement-learning internalization; Cluster C, compiler IR and autotuning - the representations and search machinery; and Cluster D, program analysis - the classic foundations we can reuse.

Three cross-cutting axes run through the whole talk: what feedback is exposed to the optimizer, how knowledge is acquired, and how correctness is guaranteed.

## Slide 3. A taxonomy of the field

Here is the stack I will map everything onto. At the top, semantics: what the operator computes, captured by things like StableHLO and MLIR. Below that, the schedule or IR layer: how the computation is laid out, which is the territory of Halide, TVM, TensorIR, Tiramisu, Exo, Triton, and SDFG. Below that, analysis: data-flow, dependence and the program dependence graph, abstract interpretation, and graph learning like ProGraML. Then the agent loop: diagnose, edit, verify, as in KernelBench, Geak, CompilerGPT, and AscendOptimizer. And at the bottom, hardware feedback: roofline models, NPUMeter, and profiler-in-the-loop search.

Every system I discuss sits somewhere on this stack. The recurring weakness is that the layers are studied in isolation, and for AscendC the agent still consumes mostly raw source plus logs.

## Slide 4. Motivating evidence: the AscendC knowledge gap

Before the survey proper, here is why this problem is hard and specific. These are Pass@1 numbers from MultiKernelBench for single-shot operator generation. DeepSeek-R1 reaches 52.6% on CUDA but 1.4% on AscendC. Claude-Sonnet-4 is 47.0% versus 2.1%. Qwen3-235B in thinking mode is 44.2% versus 0.7%. So models that are genuinely strong on CUDA nearly fail on AscendC.

There are two structural causes. First, data scarcity: there are few open AscendC kernels and idioms, unlike the mature CUDA and Triton ecosystems. Second, the operator is a coupled artifact - a host tiling program plus a device kernel program, over an explicit UB, L1, L0 memory hierarchy. And compiler or profiler feedback typically shows symptoms, not the legal structural rewrite. This is the reason the whole survey matters: pretraining reuse, which is the engine behind CUDA agents, does not transfer, so other knowledge sources have to fill in.

## Slide 5. Cluster A - Ascend and NPU-specific work

Now the first cluster, the target domain. There are six works worth knowing. AscendOptimizer is the closest baseline: an episodic-experience agent with Optimization Rewind and a two-stage host and kernel design, training-free. AscendCraft is a programming-model contribution: DSL-guided transcompilation into AscendC that makes execution semantics explicit. AscendKernelGen is the diagnosis: a systematic study showing general LLMs struggle on NPU kernels without domain adaptation. MultiKernelBench is the benchmark, spanning GPU, NPU, and TPU, and it quantifies the gap we just saw. And two performance-model works: the ASPLOS 2025 "Squeezing Operator Performance" paper with a component-based roofline and bottleneck classification, and NPUMeter with analytical performance models for automatic optimization.

Together they cover the domain from three angles: generate, optimize, and measure or model.

## Slide 6. Deep dive - AscendOptimizer

AscendOptimizer deserves a deep dive because it is the closest baseline. Its mechanism has three parts. Optimization Rewind controllably deoptimizes strong kernels and keeps the motifs whose removal measurably slows the hardware, as reusable experience. Stage I does retrieval-guided kernel rewriting from a shared experience bank. Stage II does a hardware-in-the-loop evolutionary tiling search. And it is training-free: the experience lives outside the model weights.

The results, on 101 real AscendC operators from the cann-ops benchmark: a 1.21x geometric-mean speedup over the baseline, with 53.47% of operators beating their reference. On the hardest level-3 operators the geomean is 1.89, versus 1.38 for Best-of-N and 1.45 for OpenEvolve. The ablation shows retrieved experience lifts the geomean from 1.09 to 1.16, while tiling search alone reaches only 1.02. All on Ascend 910B2, CANN 8.3, at 230 hardware evaluations per operator.

The takeaway for this survey: episodic experience works, but it is stored as free-form records. It is not yet anchored to compiler-derived structural views - and that is precisely the opening this repository targets.

## Slide 7. Cluster B - agentic kernel optimization, part one

The second cluster is agentic optimization. First the benchmarks and metrics. KernelBench asks whether LLMs can write fast GPU kernels and introduces the fast_p metric family. TritonBench targets Triton operator generation and shows that even a friendly DSL is hard when performance matters. MultiKernelBench, which we already saw, adds cross-platform coverage.

Then the agents and compiler bridges. Geak is an agentic feedback loop for AMD Triton kernels. CompilerGPT is especially relevant: it feeds compiler optimization reports to an LLM, which is the closest existing analogue to a compiler-to-AI view. And there is a broad survey of LLMs for code optimization that frames the challenges.

The common pattern across this cluster is that iterating with execution feedback beats one-shot prompting. The common limit is that the interface is still code plus errors plus profiler text, not a structured, legal-action space.

## Slide 8. Cluster B - agentic kernel optimization, part two

The agentic space is broader than the curated core, so here is the wider landscape from AscendOptimizer's related work. On multi-agent and profiling-guided systems: Astra, PRAGMA, CudaForge, TritonForge, GPU Kernel Scientist, and StitchCUDA. On evolutionary search: KernelEvolve at Meta scale, EvoEngineer for CUDA code evolution, and OpenEvolve, which is used as a baseline. And on internalization through learning: Kevin with multi-turn RL, CUDA-L1 and CUDA-L2 with contrastive RL, AutoTriton and TritonRL, and Seed-Coder with data self-curation.

The important contrast is two acquisition philosophies. One internalizes optimization into model weights via RL or SFT, which needs many code-performance pairs. The other externalizes it as experience or search, training-free. Knowledge-scarce hardware like NPUs pushes strongly toward the second philosophy - which is exactly why AscendOptimizer is training-free.

## Slide 9. Cluster C - compiler IR, scheduling, autotuning

The third cluster gives us the representational vocabulary. Three sub-groups. First, algorithm and schedule separation: Halide, which decouples algorithm from schedule; Tiramisu, a polyhedral compiler with explicit layers and communication; Exo, for user-schedulable accelerators; and the tile-centric models, Triton and TileLang. Second, tensor programs and search: TVM as an end-to-end optimizing compiler, AutoTVM with learned cost models, Ansor with a hierarchical search space, MetaSchedule with probabilistic programs, and TensorIR as a tensorized program IR. Third, infrastructure and data-centric IR: MLIR for multi-level dialects, StableHLO for portable operator semantics, and DaCe with its SDFG, which treats data movement and double buffering as transformations.

These supply the exact vocabulary an AI-facing view needs: schedule actions like tile, split, reorder, vectorize, and double-buffer; a semantic upper layer; and data-centric movement graphs.

## Slide 10. IR and scheduling systems compared

To make the cluster concrete, here is a comparison. Halide and Tiramisu give us the algorithm-versus-schedule split, tuned manually or by autoschedulers or polyhedrally; we borrow the idea of separating semantics from schedule. TVM, Ansor, and MetaSchedule model a tensor program plus schedule with learned, evolutionary, or probabilistic search; we borrow schedule actions as structured choices. TensorIR gives a tensorized loop-nest IR with schedule primitives; we borrow block and loop-level legal transforms. Triton, TileLang, and Exo are tile-centric or user-schedulable; we borrow the tile as a first-class object. MLIR and StableHLO are infrastructure and semantics; we borrow dialects for views and the semantic contract. And DaCe with SDFG is a data-centric dataflow graph; we borrow data movement and liveness as first-class citizens.

## Slide 11. Cluster D - program-analysis foundations

The fourth cluster is the oldest and, I think, the most under-used here. Kildall's 1973 unified data-flow analysis gives reaching definitions, constants, and ranges, which map to tiling-parameter and semantic views. Cousot's 1977 abstract interpretation gives sound invariants, ranges, and alignment facts, which map to UB-capacity and tail-correctness contracts. The 1987 program dependence graph by Ferrante and colleagues gives data and control dependence, which maps directly to a dependence and legality view. And ProGraML, from 2020, represents programs as attributed graphs, which maps to an operator knowledge graph.

The key insight is this: liveness, dependence, ranges, and legality are solved problems in compilers. For AscendC we can repackage them as agent-facing views instead of reinventing them.

## Slide 12. Cross-cutting axis one - what the optimizer sees

Now the synthesis. The first cross-cutting axis is a spectrum of what the optimizer is shown. On the far left, raw code, which is most LLM prompting baselines. Then plus compiler errors, as in iterative agents like Geak and CudaForge. Then plus profiling text, as in PRAGMA, TritonForge, and AscendOptimizer. Then plus compiler reports, which is CompilerGPT. And on the far right, plus structured views, which is this repository's target.

The field is clearly moving left to right, but it stops short of a full structured, legality-aware view layer. AscendOptimizer reaches profiling text plus episodic experience, and the roofline and NPUMeter work supplies the missing performance-model piece - but no one has assembled the whole right end.

## Slide 13. Cross-cutting axis two - evaluation methodology

The second axis is evaluation, and here the field is encouragingly convergent. There is a shared metric language: Pass@1 and compile success for whether valid code is even produced; speedup versus a reference implementation; fast_p, the fraction of operators beating a speedup threshold; and an explicit evaluation budget, counting hardware evaluations as wall-clock cost.

There is also a shared correctness discipline: a CPU reference with absolute and relative tolerance following CANN policies; treating compile, correctness, and profile together as one hardware evaluation; tracking regression rate and baseline stability; and framing the work as transductive autotuning rather than making zero-shot predictive claims. This convergence is good news, because it means a view-based system can be evaluated with exactly the same yardsticks.

## Slide 14. Cross-cutting axis three - how knowledge is acquired

The third axis is knowledge acquisition, and there are four established sources. Pretraining reuse, which works for CUDA and Triton but collapses on AscendC as we saw. Search and evolution, like Ansor, MetaSchedule, OpenEvolve, and hardware-in-the-loop tiling, which is strong but budget-hungry. RL and SFT, like Kevin and CUDA-L1 and L2, which needs many code-performance pairs. And episodic experience, like AscendOptimizer's rewind bank, which is training-free and transferable.

My claim is that there is a missing fifth source: compiler-derived structural knowledge - liveness, dependence, tiling, and legality extracted statically and handed to the agent. It complements the four above rather than replacing them.

## Slide 15. The synthesis gap

So here is the gap stated plainly. What the literature already gives us: schedule and semantic abstractions from Cluster C; reusable static analyses from Cluster D; agent loops with execution feedback from Cluster B; and Ascend baselines, benchmarks, and performance models from Cluster A.

What is missing: a single AI-facing layer that fuses them for AscendC; legality and contracts exposed to the agent explicitly; profiling evidence tied to IR and view nodes; and experience anchored to structured views rather than free text. The thesis of this survey is that the pieces exist across four communities, and the contribution opportunity is their integration into compiler-derived operator knowledge views.

## Slide 16. Proposed synthesis - compiler-derived operator views

Concretely, the synthesis is a small set of views. A semantic view: op family, shapes, dtype, layout, broadcast and reduction, tolerance. A tiling view: axes, tile sizes, core split, tail policy, buffer footprint, and legal actions. A pipeline view: CopyIn, Compute, CopyOut, queues, overlap, double-buffer legality, and stalls. A memory and liveness view: the GM, UB, L1, L0 hierarchy, live ranges, peak bytes, alignment, reuse, and conflicts. A dependence and legality view: def-use chains, data and control dependencies, alias and effect facts, and legal versus illegal transformations with reasons. And a performance evidence view: bottleneck class, component utilization, affected nodes, and ranked actions.

Plus a seventh, a provenance view: the action taken, expected benefit, correctness result, performance result, and regression status - so that episodic experience finally becomes anchored to view nodes and contracts, instead of living as free text.

## Slide 17. Research agenda and open problems

That leads to a concrete agenda. The open research questions: which IR and tooling artifacts can an Ascend pipeline realistically expose; which classic analyses transfer directly versus need adaptation; what programming-model additions make AscendC inherently more AI-comprehensible; and, the empirical one, do views actually beat raw source on success rate, correctness, speed, and explanation quality.

And a minimal first artifact to test this: one operator, one shape, one dtype; five to seven views and six to ten legal actions; a schema, extractor, action checker, harness, and agent protocol; and a three-way ablation comparing raw source, source plus profiling, and source plus views. Crucially, evaluation reuses the field's own yardsticks - compile success, speedup, fast_p, iterations, regression rate, and motif transferability.

## Slide 18. Conclusions

Three conclusions. First, the gap is real: AscendC breaks the pretraining-reuse recipe that powers CUDA agents, so other knowledge sources are required. Second, the parts exist: schedules, analyses, agent loops, and Ascend performance models are all mature, but siloed across four research communities. Third, integration is the opportunity: compiler-derived operator views can fuse them into one AI-facing interface with explicit legality and provenance.

In one line: this survey maps four literatures onto a single target - compiler-derived operator knowledge views for agentic AscendC optimization.

## Slides 19-20. References

The final two slides collect the full reference list, grouped by cluster: the Ascend and NPU works; the agentic optimization benchmarks and agents, including the broader adjacent and reinforcement-learning references; the compiler IR, scheduling, and autotuning systems; and the program-analysis foundations. All arXiv identifiers and DOIs are listed there, and the repository materials - the notes, the problem statement, and the AscendOptimizer translation - are cited at the end for anyone who wants to follow up.
