---
marp: true
theme: chapter-theme
paginate: true
html: true
math: mathjax
title: "Compiler-Derived Operator Views for Agentic AscendC Optimization"
description: "Overview deck for the repository: programming models, analysis, and structured views for an LLM agent that optimizes AscendC operators"
---

<style>
section {
  padding: 42px 48px;
  font-size: 26px;
}

h1 {
  font-size: 1.58em;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
}

h2 {
  font-size: 1.02em;
  margin: 0 0 11px 0;
}

h3 {
  font-size: 0.78em;
  margin: 0 0 8px 0;
}

p,
li {
  font-size: 0.72em;
  line-height: 1.34;
}

table {
  width: 100%;
  font-size: 0.53em;
  margin: 8px 0;
}

th,
td {
  padding: 7px 9px;
}

code {
  font-size: 0.88em;
}

pre {
  font-size: 0.54em;
  line-height: 1.24;
}

.lead {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.lead h1 {
  font-size: 1.92em;
  max-width: 1000px;
}

.subtitle {
  color: var(--light-text);
  font-size: 0.92em;
  line-height: 1.35;
  margin: 0 0 24px 0;
  max-width: 1020px;
}

.metric-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.metric {
  border: 1px solid var(--border);
  border-radius: 4px;
  min-height: 104px;
  padding: 14px 14px 12px 14px;
}

.metric strong {
  color: var(--primary);
  display: block;
  font-size: 1.24em;
  line-height: 1.05;
  margin-bottom: 8px;
}

.metric span {
  color: var(--light-text);
  display: block;
  font-size: 0.56em;
  line-height: 1.28;
}

.two-col {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}

.three-col {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 13px;
}

.four-col {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 11px;
}

.box {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 13px 15px;
  overflow: hidden;
}

.box h3 {
  line-height: 1.18;
}

.box p,
.box li {
  font-size: 0.61em;
  line-height: 1.34;
}

.box ul {
  margin: 0;
  padding-left: 18px;
}

.callout {
  border-left: 5px solid var(--accent3);
  background: rgba(237, 109, 0, 0.08);
  padding: 12px 16px;
  margin-top: 12px;
}

.callout p {
  margin: 0;
}

.source {
  position: absolute;
  left: 48px;
  bottom: 24px;
  right: 150px;
  color: var(--light-text);
  font-size: 0.46em;
  line-height: 1.35;
}

.small {
  color: var(--light-text);
  font-size: 0.56em;
  line-height: 1.28;
}

.pipeline {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
  align-items: stretch;
  margin-top: 18px;
}

.step {
  border: 1px solid var(--border);
  border-top: 5px solid var(--accent6);
  border-radius: 4px;
  min-height: 126px;
  padding: 12px;
}

.step strong {
  color: var(--primary);
  display: block;
  font-size: 0.75em;
  margin-bottom: 8px;
}

.step span {
  color: var(--light-text);
  display: block;
  font-size: 0.55em;
  line-height: 1.28;
}

.map {
  display: grid;
  grid-template-columns: 1.1fr 1.25fr 1.35fr 1.15fr 1.1fr;
  gap: 10px;
  align-items: stretch;
  margin-top: 14px;
}

.map-col {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 10px;
  min-height: 390px;
}

.map-col h3 {
  color: var(--primary);
  font-size: 0.62em;
  margin-bottom: 8px;
}

.map-item {
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent6);
  border-radius: 4px;
  padding: 8px 9px;
  margin-bottom: 8px;
  min-height: 54px;
}

.map-item strong {
  display: block;
  color: var(--text);
  font-size: 0.55em;
  line-height: 1.15;
}

.map-item span {
  color: var(--light-text);
  display: block;
  font-size: 0.46em;
  line-height: 1.22;
  margin-top: 3px;
}

.map-arrow {
  color: var(--accent3);
  font-weight: 700;
}

.compact-list li {
  font-size: 0.64em;
}

.tag {
  display: inline-block;
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--light-text);
  font-size: 0.46em;
  padding: 3px 6px;
  margin-right: 4px;
  margin-bottom: 5px;
}
</style>

<!-- _class: lead -->

# Compiler-Derived Operator Views for Agentic AscendC Optimization

<p class="subtitle">How programming models and analysis tools can give an LLM not just code and logs, but a map of decisions: operator semantics, tiling, pipeline, memory, dependencies, legal actions, and evidence of performance.</p>

<div class="metric-row">
  <div class="metric"><strong>AscendC</strong><span>an operator consists of host-side tiling and a device-side kernel</span></div>
  <div class="metric"><strong>LLM</strong><span>struggles to see hidden constraints from raw C++</span></div>
  <div class="metric"><strong>Views</strong><span>structure knowledge for the agent's decisions</span></div>
  <div class="metric"><strong>Loop</strong><span>compile, verify, profile, learn from attempts</span></div>
</div>

---

# Why raw code is not enough

<div class="two-col">
  <div class="box">
    <h2>An AscendC operator is coupled</h2>
    <ul>
      <li><strong>Host tiling</strong>: shapes, tile sizes, block/core split, tails, launch parameters.</li>
      <li><strong>Device kernel</strong>: CopyIn/Compute/CopyOut, queues, UB/L1/L0, synchronization, vectorization.</li>
      <li>Performance depends on how data is fed in and how the kernel consumes it.</li>
    </ul>
  </div>
  <div class="box">
    <h2>The LLM sees a weak interface</h2>
    <ul>
      <li>Compiler errors and profiler logs often describe symptoms, not a legal rewrite.</li>
      <li>Public AscendC kernels are scarce, so there are fewer ready-made patterns in pretraining.</li>
      <li>Without an explicit model of legal actions, the agent easily makes an edit that compiles poorly or breaks semantics.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Repository hypothesis:</strong> the agent needs an AI-facing layer between source and actions, derived from the compiler, program analysis, the profiler, and a programming model.</p>
</div>

<p class="source">Context: README.md, docs/problem-statement.md, notes/01-ascend-npu.md.</p>

---

# The knowledge gap is real and measurable

<div class="two-col">
  <div class="box">
    <h2>One-shot AscendC generation collapses</h2>
    <p>MultiKernelBench reports Pass@1 for single-shot operator generation. Models that handle CUDA well nearly fail on AscendC.</p>
    <table>
      <thead><tr><th>Model</th><th>CUDA Pass@1</th><th>AscendC Pass@1</th></tr></thead>
      <tbody>
        <tr><td>DeepSeek-R1</td><td>52.6%</td><td>1.4%</td></tr>
        <tr><td>Claude-Sonnet-4</td><td>47.0%</td><td>2.1%</td></tr>
        <tr><td>Qwen3-235B (think)</td><td>44.2%</td><td>0.7%</td></tr>
      </tbody>
    </table>
  </div>
  <div class="box">
    <h2>Why this happens</h2>
    <ul>
      <li>Few open AscendC kernels to learn from, unlike CUDA/Triton.</li>
      <li>An operator is coupled: host tiling program + device kernel program.</li>
      <li>The explicit UB/L1/L0 hierarchy must be orchestrated by hand.</li>
      <li>Compiler and profiler feedback shows symptoms, not the structural rewrite.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>This is the empirical motivation for the whole repository: pretraining knowledge does not carry over to AscendC, so the agent needs a compiler-derived interface.</p>
</div>

<p class="source">Numbers: MultiKernelBench (arXiv:2507.17773), reported via AscendOptimizer (arXiv:2603.23566), Table 1.</p>

---

# The central idea: representations, not prompts

<div class="pipeline">
  <div class="step"><strong>1. Operator spec</strong><span>semantics, shapes, dtype, layout, tolerance</span></div>
  <div class="step"><strong>2. AscendC / IR</strong><span>host tiling, kernel, memory spaces, pipeline calls</span></div>
  <div class="step"><strong>3. Analysis views</strong><span>tiling, pipeline, liveness, dependence, performance evidence</span></div>
  <div class="step"><strong>4. Action space</strong><span>tile, split, reorder, buffer, vectorize, prefetch, validate</span></div>
  <div class="step"><strong>5. Agent loop</strong><span>LLM proposes legal edits; harness compiles, tests and profiles</span></div>
</div>

<div class="callout">
  <p>The goal is not to replace AscendC entirely, but to build a layer through which the LLM understands which decisions are legal at all and why they might speed the operator up.</p>
</div>

---

# System map: where the pieces live

<div class="map">
  <div class="map-col">
    <h3>Inputs</h3>
    <div class="map-item"><strong>Operator spec</strong><span>op, shape, dtype, layout, reference</span></div>
    <div class="map-item"><strong>AscendC source</strong><span>host tiling + device kernel</span></div>
    <div class="map-item"><strong>Compiler IR</strong><span>lowering artifacts, loops, buffers</span></div>
    <div class="map-item"><strong>Profiler traces</strong><span>latency, stalls, component utilization</span></div>
  </div>
  <div class="map-col">
    <h3>Programming model</h3>
    <div class="map-item"><strong>Semantic layer</strong><span>what is computed, the numerical contract</span></div>
    <div class="map-item"><strong>Schedule IR</strong><span>how the computation is spread over tiles and cores</span></div>
    <div class="map-item"><strong>Data movement model</strong><span>GM/UB/L1/L0, CopyIn/Compute/CopyOut</span></div>
    <div class="map-item"><strong>Contracts</strong><span>invariants, preconditions, legal actions</span></div>
  </div>
  <div class="map-col">
    <h3>Analysis and views</h3>
    <div class="map-item"><strong>Tiling view</strong><span>axis, tile sizes, tail policy, core split</span></div>
    <div class="map-item"><strong>Pipeline view</strong><span>queues, buffers, overlap, double buffering</span></div>
    <div class="map-item"><strong>Memory/liveness</strong><span>live ranges, capacity pressure, reuse</span></div>
    <div class="map-item"><strong>Dependence/legality</strong><span>def-use, alias/effect, reorder constraints</span></div>
    <div class="map-item"><strong>Performance evidence</strong><span>bottleneck class, affected nodes, confidence</span></div>
  </div>
  <div class="map-col">
    <h3>LLM decisions</h3>
    <div class="map-item"><strong>Diagnose</strong><span>pick the bottleneck and affected view nodes</span></div>
    <div class="map-item"><strong>Retrieve</strong><span>similar episodes and motifs</span></div>
    <div class="map-item"><strong>Plan action</strong><span>choose a legal transformation</span></div>
    <div class="map-item"><strong>Patch</strong><span>edit kernel, tiling, or schedule</span></div>
  </div>
  <div class="map-col">
    <h3>Verification loop</h3>
    <div class="map-item"><strong>Compile</strong><span>CANN toolchain, diagnostics</span></div>
    <div class="map-item"><strong>Verify</strong><span>CPU reference, tolerance, invariants</span></div>
    <div class="map-item"><strong>Profile</strong><span>real device feedback</span></div>
    <div class="map-item"><strong>Provenance</strong><span>change, expected benefit, actual result</span></div>
  </div>
</div>

<p class="source">The diagram connects README.md, docs/problem-statement.md, and notes/05-ascend-toolchain-views.md.</p>

---

# Programming models: what to make visible

<div class="three-col">
  <div class="box">
    <h2>1. Semantic layer</h2>
    <p>Op type, ranks, shapes, layouts, broadcast/reduction semantics, tolerance.</p>
    <p><span class="tag">StableHLO-like</span><span class="tag">operator contract</span></p>
  </div>
  <div class="box">
    <h2>2. Schedule layer</h2>
    <p>Separate "what we compute" from "how we lay it out": tile, split, reorder, vectorize, unroll.</p>
    <p><span class="tag">Halide</span><span class="tag">Tiramisu</span><span class="tag">TensorIR</span></p>
  </div>
  <div class="box">
    <h2>3. Data movement layer</h2>
    <p>Make GM/UB/L1/L0, CopyIn/Compute/CopyOut, and queues first-class objects.</p>
    <p><span class="tag">SDFG</span><span class="tag">Ascend pipeline</span></p>
  </div>
</div>

<div class="three-col" style="margin-top: 14px;">
  <div class="box">
    <h2>4. Host tiling as data</h2>
    <p>Not an opaque C++ function, but a structured set of decisions: axis, tile sizes, blockDim, tail policy.</p>
  </div>
  <div class="box">
    <h2>5. Contracts</h2>
    <p>Preconditions, invariants, unsupported regimes, alignment and capacity rules.</p>
  </div>
  <div class="box">
    <h2>6. Action vocabulary</h2>
    <p>The LLM picks an action from a vocabulary instead of writing an arbitrary optimization blindly.</p>
  </div>
</div>

<p class="source">Lineage: StableHLO / MLIR (arXiv:2002.11054), Halide, TensorIR (arXiv:2207.04296), Tiramisu (arXiv:1804.10694), Exo, DaCe/SDFG (arXiv:1902.10345), Triton / TileLang.</p>

---

# Analysis tools: how to help the LLM

<table>
  <thead>
    <tr>
      <th>Analysis</th>
      <th>What it gives the agent</th>
      <th>Decisions that become safer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data-flow</td>
      <td>definitions, uses, constants, ranges</td>
      <td>expression rewriting, propagation, validating tiling parameters</td>
    </tr>
    <tr>
      <td>Liveness</td>
      <td>live ranges, peak buffer pressure</td>
      <td>UB reuse, double buffering, memory placement</td>
    </tr>
    <tr>
      <td>Dependence / PDG</td>
      <td>data/control dependencies, alias/effect facts</td>
      <td>reorder, fuse, split, pipeline overlap without breaking semantics</td>
    </tr>
    <tr>
      <td>Loop / polyhedral</td>
      <td>affine accesses, loop-carried dependencies</td>
      <td>tile, interchange, vectorize, tail handling</td>
    </tr>
    <tr>
      <td>Profiler evidence</td>
      <td>bottleneck class and affected source/view nodes</td>
      <td>pick an action by root cause, not by counter name</td>
    </tr>
  </tbody>
</table>

<p class="source">Foundations: Kildall data-flow (1973), Cousot abstract interpretation (1977), Program Dependence Graph (1987), ProGraML (arXiv:2003.10536); Ascend evidence: ASPLOS'25 roofline. See notes/04-program-analysis.md and notes/05-ascend-toolchain-views.md.</p>

---

# Techniques worth building into the system

<div class="four-col">
  <div class="box">
    <h2>Optimization Rewind</h2>
    <ul>
      <li>take a strong implementation;</li>
      <li>remove a motif in a controlled way;</li>
      <li>if it got slower, keep the reverse rewrite as experience.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Hardware-in-the-loop tiling</h2>
    <ul>
      <li>mutate the tiling;</li>
      <li>compile + correctness;</li>
      <li>real-device profile;</li>
      <li>survivor update.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Retrieval-guided rewrite</h2>
    <ul>
      <li>diagnose the bottleneck;</li>
      <li>find similar episodes;</li>
      <li>rewrite the code respecting applicability and avoid rules.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Constrained action space</h2>
    <ul>
      <li>legal actions from views;</li>
      <li>precondition checks;</li>
      <li>explanation: why the edit is legal.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>The key link:</strong> the techniques provide the agent loop, and compiler-derived views shrink the space of random edits and make each attempt explainable.</p>
</div>

---

# How the LLM decides with views

<div class="pipeline">
  <div class="step"><strong>Observe</strong><span>operator view + diagnostics + profiling summary</span></div>
  <div class="step"><strong>Localize</strong><span>the bottleneck is tied to a loop, buffer, stage, or tiling node</span></div>
  <div class="step"><strong>Select</strong><span>the agent picks a legal action and checks preconditions</span></div>
  <div class="step"><strong>Patch</strong><span>the kernel, tiling template, or schedule representation changes</span></div>
  <div class="step"><strong>Learn</strong><span>the result goes into provenance and the experience bank</span></div>
</div>

<div class="two-col" style="margin-top: 16px;">
  <div class="box">
    <h2>Example agent question</h2>
    <p>"Can I increase the tile size without overflowing UB and without violating the tail policy?"</p>
  </div>
  <div class="box">
    <h2>Which views answer it</h2>
    <p>Tiling view + memory/liveness + shape/range invariants + profiler evidence.</p>
  </div>
</div>

---

# What sets this apart from AscendOptimizer

<div class="two-col">
  <div class="box">
    <h2>AscendOptimizer as a baseline</h2>
    <ul>
      <li>builds an experience bank via Optimization Rewind;</li>
      <li>uses retrieval for kernel rewrite;</li>
      <li>tunes host-side tiling from hardware feedback;</li>
      <li>works training-free.</li>
    </ul>
  </div>
  <div class="box">
    <h2>The extension in this repository</h2>
    <ul>
      <li>add compiler-derived views before the agent action;</li>
      <li>represent legality and contracts explicitly;</li>
      <li>link profiling evidence to nodes in the IR/views;</li>
      <li>make the programming model more AI-facing.</li>
    </ul>
  </div>
</div>

<div class="metric-row">
  <div class="metric"><strong>101</strong><span>real AscendC operators from the cann-ops benchmark</span></div>
  <div class="metric"><strong>1.21x</strong><span>geomean speedup over the open baseline (53.47% beat their reference)</span></div>
  <div class="metric"><strong>1.89 GM</strong><span>on hardest level-3 ops vs 1.38 BoN / 1.45 OpenEvolve</span></div>
  <div class="metric"><strong>Ablation</strong><span>experience lifts GM 1.09 to 1.16; tiling-only reaches only 1.02</span></div>
</div>

<p class="source">AscendOptimizer (arXiv:2603.23566), Tables 2-3; Ascend 910B2, CANN 8.3, 230 hardware evals per operator.</p>

---

# Real example: cross-operator motif transfer

<div class="two-col">
  <div class="box">
    <h2>Source operator: clip_by_value_v2</h2>
    <p>Optimization Rewind removes a "consolidated loop with conditional tail" motif and measures the damage on hardware.</p>
    <ul>
      <li>separate tail handling folded into one loop with <code>(i==last) ? tailNum : partNum</code>;</li>
      <li>removing it raises pipeline stalls by 28.6%;</li>
      <li>latency moves 56 us -> 75 us, so the motif is worth ~25%.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Target operator: upsample_nearest_exact3d</h2>
    <p>Structurally unrelated, initial 156 us. Profiling localizes a GatherData hot path with vector-pipeline stalls.</p>
    <ul>
      <li>retrieval pulls the motif mined from clip_by_value_v2;</li>
      <li>the same loop consolidation is applied to GatherData;</li>
      <li>first big drop: 156 us -> 145 us.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Counterfactual:</strong> given only an oracle bottleneck description but no retrieved experience, just 1 of 100 attempts reaches 145 us - even when Ascend C Best Practices docs are added. Structured, transferable experience is the missing link from diagnosis to the right rewrite.</p>
</div>

<p class="source">AscendOptimizer (arXiv:2603.23566), Section 4.4 and Figure 3.</p>

---

# Real example: a rewind-derived experience record

<div class="two-col">
  <div class="box">
    <h2>Operator eye: remove redundant scattered zero writes</h2>

```json
{
  "op": "eye",
  "canonical_family": "kernel.memory.scatter",
  "root_mechanism": "Output is already zero-initialized;
     only diagonal values need explicit writes.",
  "causal_chain": "remove scattered zero writes ->
     fewer L2 misses -> higher bandwidth ->
     shorter vector critical path",
  "reusable_when": ["Eye-like diagonal init",
     "Output buffer guaranteed zero-initialized"],
  "avoid_when": ["Buffer not known to be zero-initialized"]
}
```

  </div>
  <div class="box">
    <h2>Why this shape matters</h2>
    <ul>
      <li>Every record ties a code diff to a bottleneck, a causal mechanism, and profiler evidence.</li>
      <li>L2 read hit rate: 0.02% -> 87.5%; task duration recovers from 925 ms to 1.19 ms once redundant writes are removed.</li>
      <li>Retrieval keys, reusable_when and avoid_when make the episode transferable and safe.</li>
      <li>This is exactly the "experience tied to view nodes and contracts" that structured views should standardize.</li>
    </ul>
  </div>
</div>

<p class="source">AscendOptimizer (arXiv:2603.23566), Figure 6 / Appendix B.4.</p>

---

# Experimental framing

<table>
  <thead>
    <tr>
      <th>Configuration</th>
      <th>What the agent sees</th>
      <th>What we test</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Raw source + logs</td>
      <td>AscendC, compiler errors, test failures, profiler text</td>
      <td>the lower baseline point</td>
    </tr>
    <tr>
      <td>Source + profiling summaries</td>
      <td>structured latency and bottleneck summaries</td>
      <td>how much clean diagnostics buys</td>
    </tr>
    <tr>
      <td>Source + operator views</td>
      <td>semantic, tiling, pipeline, memory, dependence, legal actions</td>
      <td>the value of an AI-facing compiler layer</td>
    </tr>
  </tbody>
</table>

<div class="three-col">
  <div class="box"><h2>Correctness</h2><p>compile success, CPU reference, tolerance, regression rate</p></div>
  <div class="box"><h2>Performance</h2><p>speedup, fast_p, iterations, hardware-evaluation budget</p></div>
  <div class="box"><h2>Reasoning</h2><p>legality explanations, motif transfer, provenance quality</p></div>
</div>

---

# A minimal research artifact

<div class="pipeline">
  <div class="step"><strong>Schema</strong><span>JSON views for semantic, tiling, pipeline, memory, dependence, performance</span></div>
  <div class="step"><strong>Extractor</strong><span>parse AscendC/IR + static analysis + profiler ingestion</span></div>
  <div class="step"><strong>Action checker</strong><span>legal/illegal transformations with reasons</span></div>
  <div class="step"><strong>Harness</strong><span>compile, run, compare, profile, archive evidence</span></div>
  <div class="step"><strong>Agent protocol</strong><span>prompt templates, retrieval, provenance, dashboard</span></div>
</div>

<div class="callout">
  <p>The first useful slice: one operator, one shape, one dtype, 5-7 views, 6-10 legal actions, and a reproducible compile/verify/profile loop.</p>
</div>

---

# Prior art this builds on

<div class="three-col">
  <div class="box">
    <h2>Programming models &amp; schedules</h2>
    <ul>
      <li>Halide, TVM, Ansor, TensorIR, Tiramisu, Exo</li>
      <li>Triton, TileLang - tile-centric models</li>
      <li>StableHLO, MLIR - semantics + multi-level IR</li>
      <li>DaCe / SDFG - data-centric, double buffering</li>
    </ul>
  </div>
  <div class="box">
    <h2>Program analysis</h2>
    <ul>
      <li>Kildall data-flow analysis (1973)</li>
      <li>Cousot abstract interpretation (1977)</li>
      <li>Program Dependence Graph (1987)</li>
      <li>ProGraML - graph ML over programs</li>
    </ul>
  </div>
  <div class="box">
    <h2>Agentic kernel optimization</h2>
    <ul>
      <li>KernelBench, TritonBench, Geak</li>
      <li>CompilerGPT - compiler reports as input</li>
      <li>Ascend: AscendOptimizer, AscendCraft, AscendKernelGen</li>
      <li>Ascend perf: MultiKernelBench, ASPLOS'25 roofline</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>The gap these leave: schedules, analyses, and agent loops exist separately. This repository asks how to fuse them into compiler-derived views that a single agent consumes for AscendC.</p>
</div>

<p class="source">Full links: bibliography/reading-list.md and bibliography/articles.yaml (AscendOptimizer arXiv:2603.23566, MultiKernelBench arXiv:2507.17773, AscendCraft arXiv:2601.22760, AscendKernelGen arXiv:2601.07160).</p>

---

# Conclusions

<div class="three-col">
  <div class="box">
    <h2>1. The LLM needs an interface</h2>
    <p>Raw AscendC hides semantics, constraints, and resource trade-offs. Views turn that into data.</p>
  </div>
  <div class="box">
    <h2>2. Analysis lowers risk</h2>
    <p>Dependence, liveness, ranges, and legality checks reduce the number of pointless or dangerous edits.</p>
  </div>
  <div class="box">
    <h2>3. Experience becomes transferable</h2>
    <p>Optimization Rewind and provenance are stronger when tied to view nodes, bottleneck classes, and action contracts.</p>
  </div>
</div>

<div class="callout">
  <p><strong>Project statement:</strong> compiler-derived operator knowledge views for agentic AscendC optimization.</p>
</div>

<p class="source">Core materials: README.md, docs/problem-statement.md, notes/01-05, publications/translations/ascendoptimizer-2026.md.</p>
