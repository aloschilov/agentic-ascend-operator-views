---
marp: true
theme: chapter-theme
paginate: true
html: true
math: mathjax
title: "Compiler Tools and Program Analysis for AI-Agentic AscendC Operator Optimization: A Survey"
description: "Survey deck across the repository bibliography: Ascend/NPU works, agentic kernel optimization, compiler IR and autotuning, and program-analysis foundations, synthesized into compiler-derived operator views."
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
  font-size: 0.5em;
  margin: 8px 0;
}

th,
td {
  padding: 6px 8px;
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
  font-size: 1.78em;
  max-width: 1040px;
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
  font-size: 0.6em;
  line-height: 1.32;
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

.refs {
  columns: 2;
  column-gap: 28px;
}

.refs p {
  font-size: 0.5em;
  line-height: 1.3;
  margin: 0 0 6px 0;
  break-inside: avoid;
}
</style>

<!-- _class: lead -->

# Compiler Tools and Program Analysis for AI-Agentic AscendC Operator Optimization

<p class="subtitle">A survey across four literature clusters: Ascend/NPU-specific work, agentic kernel optimization, compiler IR / scheduling / autotuning, and program-analysis foundations - synthesized toward compiler-derived operator knowledge views.</p>

<div class="metric-row">
  <div class="metric"><strong>4 clusters</strong><span>Ascend, agents, compiler IR, analysis</span></div>
  <div class="metric"><strong>~30 works</strong><span>from the repository bibliography plus adjacent references</span></div>
  <div class="metric"><strong>1 question</strong><span>how do compiler artifacts make agentic operator tuning work?</span></div>
  <div class="metric"><strong>1 gap</strong><span>no unified AI-facing view layer for AscendC</span></div>
</div>

---

# Scope and method of this survey

<div class="two-col">
  <div class="box">
    <h2>Guiding question</h2>
    <p>How can compiler tools and program-analysis artifacts make AI-agentic ML operator optimization more effective, especially for AscendC operators on Ascend NPUs?</p>
    <p>We read each work as an answer to: <em>what does the optimizer see, and how does it decide?</em></p>
  </div>
  <div class="box">
    <h2>How works are organized</h2>
    <ul>
      <li><strong>Cluster A - Ascend/NPU:</strong> the target domain and its baselines.</li>
      <li><strong>Cluster B - Agentic optimization:</strong> benchmarks, agents, RL internalization.</li>
      <li><strong>Cluster C - Compiler IR / autotuning:</strong> representations and search.</li>
      <li><strong>Cluster D - Program analysis:</strong> classic foundations to reuse.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Cross-cutting axes used throughout: <strong>what feedback is exposed</strong> (code / errors / profiling / structured views), <strong>how knowledge is acquired</strong> (pretraining, search, RL, episodic experience), and <strong>how correctness is guaranteed</strong>.</p>
</div>

<p class="source">Sources: README.md, docs/problem-statement.md, bibliography/reading-list.md, notes/01-05.</p>

---

# A taxonomy of the field

<div class="pipeline">
  <div class="step"><strong>Semantics</strong><span>StableHLO, MLIR: what the operator computes, dtype/layout/tolerance</span></div>
  <div class="step"><strong>Schedule / IR</strong><span>Halide, TVM, TensorIR, Tiramisu, Exo, Triton, SDFG: how it is laid out</span></div>
  <div class="step"><strong>Analysis</strong><span>data-flow, dependence/PDG, abstract interpretation, ProGraML</span></div>
  <div class="step"><strong>Agent loop</strong><span>KernelBench, Geak, CompilerGPT, AscendOptimizer: diagnose, edit, verify</span></div>
  <div class="step"><strong>Hardware feedback</strong><span>roofline, NPUMeter, profiler-in-the-loop search</span></div>
</div>

<div class="callout">
  <p>Every surveyed system sits somewhere on this stack. The recurring weakness: layers are studied in isolation, and for AscendC the agent still consumes mostly raw source plus logs.</p>
</div>

---

# Motivating evidence: the AscendC knowledge gap

<div class="two-col">
  <div class="box">
    <h2>One-shot generation collapses on AscendC</h2>
    <table>
      <thead><tr><th>Model</th><th>CUDA Pass@1</th><th>AscendC Pass@1</th></tr></thead>
      <tbody>
        <tr><td>DeepSeek-R1</td><td>52.6%</td><td>1.4%</td></tr>
        <tr><td>Claude-Sonnet-4</td><td>47.0%</td><td>2.1%</td></tr>
        <tr><td>Qwen3-235B (think)</td><td>44.2%</td><td>0.7%</td></tr>
      </tbody>
    </table>
    <p>MultiKernelBench Pass@1: models strong on CUDA nearly fail on AscendC.</p>
  </div>
  <div class="box">
    <h2>Two structural causes</h2>
    <ul>
      <li><strong>Data scarcity:</strong> few open AscendC kernels/idioms vs the mature CUDA/Triton ecosystem.</li>
      <li><strong>Coupled artifact:</strong> host tiling program + device kernel program, with an explicit UB/L1/L0 hierarchy.</li>
      <li>Compiler/profiler feedback shows symptoms, not the legal structural rewrite.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>This gap is the reason the survey exists: pretraining reuse - the engine behind CUDA agents - largely fails to transfer, so other knowledge sources must fill in.</p>
</div>

<p class="source">MultiKernelBench (arXiv:2507.17773); numbers via AscendOptimizer (arXiv:2603.23566), Table 1.</p>

---

# Cluster A - Ascend / NPU-specific work

<table>
  <thead>
    <tr><th>Work</th><th>Role</th><th>Key contribution for this topic</th></tr>
  </thead>
  <tbody>
    <tr><td>AscendOptimizer (2026)</td><td>closest baseline</td><td>episodic-experience agent; Optimization Rewind; host/kernel two-stage; training-free</td></tr>
    <tr><td>AscendCraft (2026)</td><td>programming model</td><td>DSL-guided transcompilation to AscendC; makes execution semantics explicit</td></tr>
    <tr><td>AscendKernelGen (2026)</td><td>diagnosis</td><td>systematic study: general LLMs struggle on NPU kernels without domain adaptation</td></tr>
    <tr><td>MultiKernelBench (2025)</td><td>benchmark</td><td>multi-platform (GPU/NPU/TPU) generation benchmark; quantifies the gap</td></tr>
    <tr><td>Squeezing Operator Perf., ASPLOS'25</td><td>performance model</td><td>component-based roofline & bottleneck classification for Ascend operators</td></tr>
    <tr><td>NPUMeter (2026)</td><td>performance model</td><td>analytical performance models for automatic Ascend operator optimization</td></tr>
  </tbody>
</table>

<div class="callout">
  <p>Together they show the domain from three angles: <strong>generate</strong> (Craft, KernelGen), <strong>optimize</strong> (AscendOptimizer), and <strong>measure/model</strong> (roofline, NPUMeter, MultiKernelBench).</p>
</div>

<p class="source">arXiv:2603.23566, 2601.22760, 2601.07160, 2507.17773; DOI 10.1145/3676641.3716243, 10.1145/3820380. See notes/01-ascend-npu.md.</p>

---

# Deep dive - AscendOptimizer, the closest baseline

<div class="two-col">
  <div class="box">
    <h2>Mechanism</h2>
    <ul>
      <li><strong>Optimization Rewind:</strong> controllably deoptimize strong kernels; keep motifs whose removal measurably slows hardware as reusable experience.</li>
      <li><strong>Stage I:</strong> retrieval-guided kernel rewrite from a shared experience bank.</li>
      <li><strong>Stage II:</strong> hardware-in-the-loop evolutionary tiling search.</li>
      <li>Training-free; experience lives outside model weights.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Results (101 real AscendC operators)</h2>
    <ul>
      <li>1.21x geomean over the cann-ops baseline; 53.47% beat their reference.</li>
      <li>Level-3 GM 1.89 vs 1.38 BoN / 1.45 OpenEvolve.</li>
      <li>Ablation: experience lifts GM 1.09 to 1.16; tiling-only only 1.02.</li>
      <li>Ascend 910B2, CANN 8.3, 230 hardware evals per operator.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Takeaway for the survey: episodic experience works, but it is stored as free-form records. It is <em>not</em> yet anchored to compiler-derived structural views - the opening this repository targets.</p>
</div>

<p class="source">AscendOptimizer (arXiv:2603.23566), Tables 1-3, Figures 1, 3, 6.</p>

---

# Cluster B - Agentic kernel optimization (1/2)

<div class="two-col">
  <div class="box">
    <h2>Benchmarks & metrics</h2>
    <ul>
      <li><strong>KernelBench:</strong> "can LLMs write fast GPU kernels?"; introduces the fast_p metric family.</li>
      <li><strong>TritonBench:</strong> Triton operator generation; even a friendly DSL is hard when performance matters.</li>
      <li><strong>MultiKernelBench:</strong> cross-platform GPU/NPU/TPU coverage.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Agents & compiler bridges</h2>
    <ul>
      <li><strong>Geak:</strong> agentic feedback loop for AMD Triton kernels.</li>
      <li><strong>CompilerGPT:</strong> feeds compiler optimization reports to an LLM - the closest analogue to compiler-to-AI views.</li>
      <li><strong>Code Optimization survey:</strong> broad framing of LLM-for-code-optimization challenges.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Common pattern: iterate with execution feedback beats one-shot prompting. Common limit: the interface is still code + errors + profiler text, not a structured legal-action space.</p>
</div>

<p class="source">arXiv:2502.10517, 2502.14752, 2507.23194, 2506.06227, 2501.01277. See notes/02-agentic-kernel-optimization.md.</p>

---

# Cluster B - Agentic kernel optimization (2/2)

<div class="three-col">
  <div class="box">
    <h2>Multi-agent & profiling-guided</h2>
    <ul>
      <li>Astra - multi-agent GPU kernel perf</li>
      <li>PRAGMA - profiling-reasoned agents</li>
      <li>CudaForge - hardware-feedback agent</li>
      <li>TritonForge - profiling-guided Triton</li>
      <li>GPU Kernel Scientist; StitchCUDA</li>
    </ul>
  </div>
  <div class="box">
    <h2>Evolutionary search</h2>
    <ul>
      <li>KernelEvolve - agentic kernels at Meta scale</li>
      <li>EvoEngineer - CUDA code evolution</li>
      <li>OpenEvolve - open evolutionary coding agent (baseline)</li>
    </ul>
  </div>
  <div class="box">
    <h2>RL / SFT internalization</h2>
    <ul>
      <li>Kevin - multi-turn RL for CUDA</li>
      <li>CUDA-L1 / CUDA-L2 - contrastive RL</li>
      <li>AutoTriton, TritonRL - RL for Triton</li>
      <li>Seed-Coder - data self-curation</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Two acquisition philosophies: <strong>internalize into weights</strong> (RL/SFT, needs many code-performance pairs) vs <strong>externalize as experience/search</strong> (training-free). Knowledge-scarce NPUs push toward the latter.</p>
</div>

<p class="source">Adjacent references from AscendOptimizer's related work (arXiv:2509.07506, 2511.06345, 2511.01884, 2512.09196, 2506.20807, 2603.02637, 2512.23236, 2510.03760, 2507.11948, 2507.14111, 2512.02551, 2507.05687, 2510.17891, 2506.03524).</p>

---

# Cluster C - Compiler IR, scheduling, autotuning

<div class="three-col">
  <div class="box">
    <h2>Algorithm / schedule split</h2>
    <ul>
      <li>Halide - decouple algorithm from schedule</li>
      <li>Tiramisu - polyhedral, layers + communication</li>
      <li>Exo - user-schedulable accelerators</li>
      <li>Triton / TileLang - tile-centric models</li>
    </ul>
  </div>
  <div class="box">
    <h2>Tensor programs & search</h2>
    <ul>
      <li>TVM - end-to-end optimizing compiler</li>
      <li>AutoTVM - learned cost models</li>
      <li>Ansor - hierarchical search space</li>
      <li>MetaSchedule - probabilistic programs</li>
      <li>TensorIR - tensorized program IR</li>
    </ul>
  </div>
  <div class="box">
    <h2>Infra & data-centric IR</h2>
    <ul>
      <li>MLIR - multi-level dialect infra</li>
      <li>StableHLO - portable operator semantics</li>
      <li>DaCe / SDFG - data movement & double buffering as transforms</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>These supply the vocabulary for AI-facing views: <strong>schedule actions</strong> (tile, split, reorder, vectorize, double-buffer), <strong>semantic upper layer</strong>, and <strong>data-centric</strong> movement graphs.</p>
</div>

<p class="source">arXiv:2002.11054, 1802.04799, 1805.08166, 2006.06762, 2205.13603, 2207.04296, 1902.10345, 1804.10694; Halide (PLDI'13), Triton (MAPL'19), Exo (PLDI'22), StableHLO spec. See notes/03-compiler-ir-autotuning.md.</p>

---

# IR & scheduling systems compared

<table>
  <thead>
    <tr><th>System</th><th>Core abstraction</th><th>Search / tuning</th><th>What this repo borrows</th></tr>
  </thead>
  <tbody>
    <tr><td>Halide / Tiramisu</td><td>algorithm vs schedule</td><td>manual / autoscheduler / polyhedral</td><td>separate semantics from schedule</td></tr>
    <tr><td>TVM / Ansor / MetaSchedule</td><td>tensor program + schedule</td><td>learned cost model, evolutionary, probabilistic</td><td>schedule actions as structured choices</td></tr>
    <tr><td>TensorIR</td><td>tensorized loop-nest IR</td><td>schedule primitives + tuning</td><td>block/loop-level legal transforms</td></tr>
    <tr><td>Triton / TileLang / Exo</td><td>tile-centric / user-schedulable</td><td>compiler + user hints</td><td>tile as first-class object</td></tr>
    <tr><td>MLIR / StableHLO</td><td>multi-level IR / semantics</td><td>n/a (infrastructure)</td><td>dialects for views; semantic contract</td></tr>
    <tr><td>DaCe / SDFG</td><td>data-centric dataflow graph</td><td>graph transformations</td><td>data movement & liveness as first-class</td></tr>
  </tbody>
</table>

<p class="source">Synthesis of Cluster C; mapped to the candidate view schema in notes/05-ascend-toolchain-views.md.</p>

---

# Cluster D - Program-analysis foundations

<table>
  <thead>
    <tr><th>Foundation</th><th>Year</th><th>Provides</th><th>Maps to view</th></tr>
  </thead>
  <tbody>
    <tr><td>Kildall - unified data-flow</td><td>1973</td><td>reaching defs, constants, ranges</td><td>tiling-parameter / semantic view</td></tr>
    <tr><td>Cousot - abstract interpretation</td><td>1977</td><td>sound invariants, ranges, alignment</td><td>UB-capacity / tail-correctness contracts</td></tr>
    <tr><td>Ferrante et al. - PDG</td><td>1987</td><td>data/control dependence</td><td>dependence / legality view</td></tr>
    <tr><td>ProGraML - graph ML on code</td><td>2020</td><td>attributed program graphs</td><td>operator knowledge graph</td></tr>
  </tbody>
</table>

<div class="callout">
  <p>The key survey insight: liveness, dependence, ranges and legality are <em>solved problems</em> in compilers. For AscendC they can be repackaged as agent-facing views instead of reinvented.</p>
</div>

<p class="source">DOI 10.1145/512927.512945, POPL'77, DOI 10.1145/24039.24041, arXiv:2003.10536. See notes/04-program-analysis.md.</p>

---

# Cross-cutting axis 1 - what the optimizer sees

<div class="pipeline">
  <div class="step"><strong>Raw code</strong><span>most LLM prompting baselines</span></div>
  <div class="step"><strong>+ compiler errors</strong><span>iterative agents (Geak, CudaForge)</span></div>
  <div class="step"><strong>+ profiling text</strong><span>PRAGMA, TritonForge, AscendOptimizer</span></div>
  <div class="step"><strong>+ compiler reports</strong><span>CompilerGPT</span></div>
  <div class="step"><strong>+ structured views</strong><span>this repository's target</span></div>
</div>

<div class="callout">
  <p>The field moves left-to-right, but stops short of a full structured, legality-aware view layer. AscendOptimizer reaches "profiling text + episodic experience"; the roofline and NPUMeter work supplies the missing performance-model piece.</p>
</div>

---

# Cross-cutting axis 2 - evaluation methodology

<div class="two-col">
  <div class="box">
    <h2>Shared metric language</h2>
    <ul>
      <li><strong>Pass@1 / compile success</strong> - can it even generate valid code (MultiKernelBench, KernelBench).</li>
      <li><strong>speedup vs reference</strong> - ratio to a baseline implementation.</li>
      <li><strong>fast_p</strong> - fraction of ops beating a speedup threshold p (KernelBench, AscendOptimizer).</li>
      <li><strong>evaluation budget</strong> - hardware evals counted as wall-clock cost.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Correctness discipline</h2>
    <ul>
      <li>CPU reference + absolute/relative tolerance (CANN policies).</li>
      <li>compile / correctness / profile as one hardware evaluation.</li>
      <li>regression rate and stability of baseline latency.</li>
      <li>transductive autotuning, not zero-shot predictive claims.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Convergent methodology across clusters makes the proposed view-based system directly comparable: reuse fast_p, speedup, and a fixed evaluation budget.</p>
</div>

<p class="source">KernelBench (arXiv:2502.10517), AscendOptimizer (arXiv:2603.23566) Sec. 4; docs/problem-statement.md evaluation sketch.</p>

---

# Cross-cutting axis 3 - how knowledge is acquired

<div class="four-col">
  <div class="box">
    <h2>Pretraining reuse</h2>
    <p>Works well for CUDA/Triton; collapses on AscendC (Table 1).</p>
  </div>
  <div class="box">
    <h2>Search / evolution</h2>
    <p>Ansor, MetaSchedule, OpenEvolve, HITL tiling; strong but budget-hungry.</p>
  </div>
  <div class="box">
    <h2>RL / SFT</h2>
    <p>Kevin, CUDA-L1/L2, AutoTriton; needs many code-performance pairs.</p>
  </div>
  <div class="box">
    <h2>Episodic experience</h2>
    <p>AscendOptimizer's rewind bank; training-free, transferable motifs.</p>
  </div>
</div>

<div class="callout">
  <p>Missing fifth source: <strong>compiler-derived structural knowledge</strong> - liveness, dependence, tiling and legality extracted statically and handed to the agent, complementing the four above.</p>
</div>

---

# The synthesis gap

<div class="two-col">
  <div class="box">
    <h2>What the literature already gives us</h2>
    <ul>
      <li>schedule/semantic abstractions (Cluster C);</li>
      <li>reusable static analyses (Cluster D);</li>
      <li>agent loops with execution feedback (Cluster B);</li>
      <li>Ascend baselines, benchmarks, performance models (Cluster A).</li>
    </ul>
  </div>
  <div class="box">
    <h2>What is missing</h2>
    <ul>
      <li>a single AI-facing layer that fuses them for AscendC;</li>
      <li>legality/contracts exposed to the agent explicitly;</li>
      <li>profiling evidence tied to IR/view nodes;</li>
      <li>experience anchored to structured views, not free text.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Thesis of the survey:</strong> the pieces exist across four communities; the contribution opportunity is their integration into compiler-derived operator knowledge views.</p>
</div>

---

# Proposed synthesis - compiler-derived operator views

<div class="three-col">
  <div class="box"><h3>1. Semantic view</h3><p>op family, shapes, dtype, layout, broadcast/reduction, tolerance.</p></div>
  <div class="box"><h3>2. Tiling view</h3><p>axes, tile sizes, core split, tail policy, buffer footprint, legal actions.</p></div>
  <div class="box"><h3>3. Pipeline view</h3><p>CopyIn/Compute/CopyOut, queues, overlap, double-buffer legality, stalls.</p></div>
</div>

<div class="three-col" style="margin-top: 12px;">
  <div class="box"><h3>4. Memory / liveness</h3><p>GM/UB/L1/L0, live ranges, peak bytes, alignment, reuse, conflicts.</p></div>
  <div class="box"><h3>5. Dependence / legality</h3><p>def-use, data/control deps, alias/effect, legal vs illegal with reasons.</p></div>
  <div class="box"><h3>6. Performance evidence</h3><p>bottleneck class, component utilization, affected nodes, ranked actions.</p></div>
</div>

<div class="callout">
  <p>Plus a <strong>7. provenance view</strong>: action, expected benefit, correctness, performance, regression - so episodic experience becomes anchored to view nodes and contracts.</p>
</div>

<p class="source">Candidate schema from notes/05-ascend-toolchain-views.md and docs/problem-statement.md.</p>

---

# Research agenda and open problems

<div class="two-col">
  <div class="box">
    <h2>Open research questions</h2>
    <ul>
      <li>Which IR/tooling artifacts can an Ascend pipeline realistically expose?</li>
      <li>Which classic analyses transfer directly vs need adaptation?</li>
      <li>What programming-model additions make AscendC inherently more AI-comprehensible?</li>
      <li>Do views beat raw source on success, correctness, speed, and explanation quality?</li>
    </ul>
  </div>
  <div class="box">
    <h2>Minimal first artifact</h2>
    <ul>
      <li>one operator, one shape, one dtype;</li>
      <li>5-7 views + 6-10 legal actions;</li>
      <li>schema, extractor, action checker, harness, agent protocol;</li>
      <li>three-way ablation: raw / +profiling / +views.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Evaluation reuses the field's own yardsticks: compile success, speedup, fast_p, iterations, regression rate, motif transferability.</p>
</div>

<p class="source">docs/problem-statement.md (research questions and evaluation sketch); roadmap.md.</p>

---

# Conclusions

<div class="three-col">
  <div class="box">
    <h2>1. The gap is real</h2>
    <p>AscendC breaks the pretraining-reuse recipe that powers CUDA agents; other knowledge sources are required.</p>
  </div>
  <div class="box">
    <h2>2. The parts exist</h2>
    <p>Schedules, analyses, agent loops, and Ascend performance models are all mature - but siloed across four communities.</p>
  </div>
  <div class="box">
    <h2>3. Integration is the opportunity</h2>
    <p>Compiler-derived operator views can fuse them into one AI-facing interface with legality and provenance.</p>
  </div>
</div>

<div class="callout">
  <p><strong>One line:</strong> the survey maps four literatures onto a single target - compiler-derived operator knowledge views for agentic AscendC optimization.</p>
</div>

---

# References (1/2)

<div class="refs">
  <p><strong>Ascend / NPU.</strong> AscendOptimizer, arXiv:2603.23566. AscendCraft, arXiv:2601.22760. AscendKernelGen, arXiv:2601.07160. MultiKernelBench, arXiv:2507.17773. Squeezing Operator Performance (ASPLOS'25), DOI 10.1145/3676641.3716243. NPUMeter, DOI 10.1145/3820380.</p>
  <p><strong>Agentic optimization.</strong> KernelBench, arXiv:2502.10517. TritonBench, arXiv:2502.14752. Geak, arXiv:2507.23194. CompilerGPT, arXiv:2506.06227. Code Optimization survey, arXiv:2501.01277.</p>
  <p><strong>Adjacent agents.</strong> Astra 2509.07506; PRAGMA 2511.06345; CudaForge 2511.01884; TritonForge 2512.09196; GPU Kernel Scientist 2506.20807; StitchCUDA 2603.02637; KernelEvolve 2512.23236; EvoEngineer 2510.03760.</p>
  <p><strong>RL / SFT.</strong> Kevin 2507.11948; CUDA-L1 2507.14111; CUDA-L2 2512.02551; AutoTriton 2507.05687; TritonRL 2510.17891; Seed-Coder 2506.03524. OpenEvolve (github: algorithmicsuperintelligence/openevolve).</p>
</div>

---

# References (2/2)

<div class="refs">
  <p><strong>Compiler IR / scheduling / autotuning.</strong> MLIR, arXiv:2002.11054. StableHLO spec (openxla.org/stablehlo). TVM, arXiv:1802.04799. Learning to Optimize Tensor Programs (AutoTVM), arXiv:1805.08166. Ansor, arXiv:2006.06762. MetaSchedule, arXiv:2205.13603. TensorIR, arXiv:2207.04296. Triton (MAPL'19). Halide (PLDI'13 / CACM). Exo (PLDI'22). DaCe/SDFG, arXiv:1902.10345. Tiramisu, arXiv:1804.10694. TileLang, arXiv:2504.17577.</p>
  <p><strong>Program analysis.</strong> Kildall, A Unified Approach to Global Program Optimization, DOI 10.1145/512927.512945 (1973). Cousot &amp; Cousot, Abstract Interpretation, POPL'77. Ferrante et al., The Program Dependence Graph and Its Use in Optimization, DOI 10.1145/24039.24041 (1987). ProGraML, arXiv:2003.10536.</p>
  <p><strong>Repository materials.</strong> README.md; docs/problem-statement.md; notes/01-05; bibliography/reading-list.md; bibliography/articles.yaml; publications/translations/ascendoptimizer-2026.md.</p>
</div>
