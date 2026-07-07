---
marp: true
theme: chapter-theme
paginate: true
html: true
math: mathjax
title: "Babble for PyAsc: Applicability to Learning DSL Abstractions"
description: "Overview deck on applying babble-2022 ideas to pyasc-fork: e-graphs, anti-unification, AscIR, and LLM helpers"
---

<style>
section {
  padding: 42px 48px;
  font-size: 26px;
}

h1 {
  font-size: 1.52em;
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
  font-size: 0.7em;
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
  line-height: 1.22;
}

.lead {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.lead h1 {
  font-size: 1.86em;
  max-width: 1000px;
}

.subtitle {
  color: var(--light-text);
  font-size: 0.92em;
  line-height: 1.35;
  margin: 0 0 24px 0;
  max-width: 1040px;
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
  border-radius: 4px;
  min-height: 118px;
  padding: 12px 12px;
  position: relative;
}

.step::after {
  content: ">";
  position: absolute;
  right: -9px;
  top: 43%;
  color: var(--accent3);
  font-weight: 700;
}

.step:last-child::after {
  content: "";
}

.step strong {
  color: var(--primary);
  display: block;
  font-size: 0.74em;
  line-height: 1.18;
  margin-bottom: 7px;
}

.step span {
  color: var(--light-text);
  display: block;
  font-size: 0.52em;
  line-height: 1.26;
}

.fit-table td:first-child {
  width: 27%;
  font-weight: 700;
}

.fit-table td:nth-child(2) {
  width: 18%;
  color: var(--primary);
  font-weight: 700;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 9px;
}

.tag {
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--light-text);
  font-size: 0.5em;
  line-height: 1;
  padding: 7px 9px;
  white-space: nowrap;
}

.map {
  display: grid;
  grid-template-columns: 1.05fr 1.3fr 1fr;
  gap: 14px;
  align-items: stretch;
  margin-top: 10px;
}

.lane {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px;
  min-height: 455px;
}

.lane h3 {
  color: var(--primary);
  margin-bottom: 10px;
}

.node {
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent3);
  border-radius: 4px;
  margin-bottom: 9px;
  padding: 9px 10px;
}

.node strong {
  display: block;
  font-size: 0.58em;
  line-height: 1.18;
  margin-bottom: 4px;
}

.node span {
  color: var(--light-text);
  display: block;
  font-size: 0.49em;
  line-height: 1.25;
}

.bridge {
  background: rgba(0, 146, 158, 0.08);
  border-color: rgba(0, 146, 158, 0.38);
}

.danger {
  border-left-color: var(--accent2);
}

.code-sample {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 10px;
}

.caption {
  color: var(--light-text);
  font-size: 0.5em;
  line-height: 1.26;
  margin-top: 7px;
}
</style>

<!-- _class: lead -->
# Babble for PyAsc

<p class="subtitle">Where library learning modulo theory can help PyAsc: from a corpus of Python/AscIR programs to LLM prompts, new DSL combinators, and checkable compiler rewrites.</p>

<div class="tag-row">
  <span class="tag">babble-2022</span>
  <span class="tag">e-graphs</span>
  <span class="tag">anti-unification</span>
  <span class="tag">PyAsc / AscIR</span>
  <span class="tag">LLM-assisted optimization</span>
</div>

<div class="source">Based on: <code>publications/files/babble-2022.pdf</code>, <code>publications/translations/babble-2022.md</code>, <code>/Users/aloschilov/articles-workspace/pyasc-fork</code>.</div>

---

# Short Takeaway

<div class="callout">
  <p><strong>Babble should be used in PyAsc not as a standalone latency optimizer, but as a layer for extracting reusable programming abstractions.</strong></p>
</div>

<div class="three-col" style="margin-top: 18px;">
  <div class="box">
    <h3>Good fit</h3>
    <ul>
      <li>recurring tile skeletons;</li>
      <li>equivalent indexing forms;</li>
      <li>canonicalization of AscTile / AscVF fragments;</li>
      <li>example selection for LLMs.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Must be constrained</h3>
    <ul>
      <li>side effects: memory, synchronization, queues;</li>
      <li>types, shapes, and memory locations;</li>
      <li>equivalences only where a verifier exists.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Does not replace</h3>
    <ul>
      <li>profiling on Ascend NPU;</li>
      <li>a performance cost model;</li>
      <li>manual CANN / Ascend C invariants.</li>
    </ul>
  </div>
</div>

<div class="source">Babble optimizes corpus compression through learned libraries; PyAsc still needs an external compile/run/profiler loop for performance prioritization.</div>

---

# What Babble Does

<p class="subtitle">Babble solves <em>library learning modulo theory</em>: it finds shared subprograms not only by syntactic matching, but also through equivalent rewrites.</p>

<div class="pipeline">
  <div class="step">
    <strong>Program corpus</strong>
    <span>many similar implementations that express the same ideas in different forms</span>
  </div>
  <div class="step">
    <strong>Equational theory</strong>
    <span>domain rules: associativity, commutativity, identities, rearrangements</span>
  </div>
  <div class="step">
    <strong>E-graph</strong>
    <span>a compact space of equivalent program forms</span>
  </div>
  <div class="step">
    <strong>Anti-unification</strong>
    <span>a shared pattern over multiple expressions, with parameters replacing differences</span>
  </div>
  <div class="step">
    <strong>Extraction</strong>
    <span>selecting abstractions that best compress the corpus</span>
  </div>
</div>

<div class="source">Babble: “Learning Better Abstractions with E-Graphs and Anti-Unification”, arXiv:2212.04596.</div>

---

# What PyAsc Already Has

<div class="two-col">
  <div class="box">
    <h3>Programming model</h3>
    <ul>
      <li><code>asc2</code>: tile-based Python API, closer to NumPy style.</li>
      <li><code>asc</code>: low-level 1:1 mapping to the Ascend C API.</li>
      <li><code>@asc2.jit</code> and <code>@asc.jit</code>: entry points into JIT compilation.</li>
      <li><code>GlobalTensor</code>, <code>LocalTensor</code>, <code>TensorLocation</code>: explicit memory model.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Compiler substrate</h3>
    <ul>
      <li>Python AST -> AscIR / MLIR.</li>
      <li>Dialects: <code>Asc</code>, <code>AscTile</code>, <code>AscVF</code>, <code>EmitAsc</code>.</li>
      <li>Transformations: lowering, sync, memory allocation, vector/cube rewrites.</li>
      <li>Codegen to Ascend C, then the Bisheng / CANN toolchain.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>This is almost an ideal setting for the Babble approach: a program corpus, typed IR, local rewrites, and compile-time verification.</p>
</div>

<div class="source">See <code>/Users/aloschilov/articles-workspace/pyasc-fork/README.md</code>, <code>AGENTS.md</code>, <code>docs/architecture_introduction.md</code>.</div>

---

# Where Babble Fits

<div class="map">
  <div class="lane">
    <h3>PyAsc corpus</h3>
    <div class="node">
      <strong>Python kernels</strong>
      <span><code>python/tutorials/asc2</code>, tests, docs examples</span>
    </div>
    <div class="node">
      <strong>Dumped AscIR</strong>
      <span>IR before and after key passes</span>
    </div>
    <div class="node">
      <strong>Generated Ascend C</strong>
      <span>optional downstream evidence</span>
    </div>
    <div class="node danger">
      <strong>Runtime traces</strong>
      <span>compile success, profiling, memory pressure</span>
    </div>
  </div>
  <div class="lane">
    <h3>Babble-style learner</h3>
    <div class="node bridge">
      <strong>Typed normalization</strong>
      <span>MLIR canonicalization + PyAsc-specific laws</span>
    </div>
    <div class="node bridge">
      <strong>E-graph saturation</strong>
      <span>equivalent forms of tile algebra, affine offsets, casts</span>
    </div>
    <div class="node bridge">
      <strong>E-graph anti-unification</strong>
      <span>shared patterns across non-identical kernels</span>
    </div>
    <div class="node bridge">
      <strong>Costed extraction</strong>
      <span>compression + typed validity + compile/profiler score</span>
    </div>
  </div>
  <div class="lane">
    <h3>Outputs</h3>
    <div class="node">
      <strong><code>asc2</code> helpers</strong>
      <span>DSL combinators for recurring tile patterns</span>
    </div>
    <div class="node">
      <strong>AscIR rewrites</strong>
      <span>canonicalization and optimization-pass candidates</span>
    </div>
    <div class="node">
      <strong>LLM memory</strong>
      <span>retrieval base of verified examples and counterexamples</span>
    </div>
    <div class="node danger">
      <strong>Review queue</strong>
      <span>humans accept only verified abstractions</span>
    </div>
  </div>
</div>

---

# Applicability by PyAsc Layer

<table class="fit-table">
  <thead>
    <tr>
      <th>Layer</th>
      <th>Fit</th>
      <th>Why</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>asc2</code> tile API</td>
      <td>High</td>
      <td>Many pure expressions over tile values; load/compute/store, map, reduce, and matmul skeletons recur.</td>
    </tr>
    <tr>
      <td><code>AscTile</code> / <code>AscVF</code></td>
      <td>High</td>
      <td>A typed MLIR layer is convenient for e-graphs, canonicalization, and shape/location constraint checks.</td>
    </tr>
    <tr>
      <td><code>asc</code> low-level API</td>
      <td>Medium</td>
      <td>Useful patterns exist, but memory, synchronization, and queues require an effect-aware theory.</td>
    </tr>
    <tr>
      <td>Ascend C codegen</td>
      <td>Medium</td>
      <td>Good as a validation target; noisier as the main learning layer because of boilerplate.</td>
    </tr>
    <tr>
      <td>Latency tuning</td>
      <td>Low without profiling</td>
      <td>Babble selects compact libraries, not guaranteed-fast kernels.</td>
    </tr>
  </tbody>
</table>

---

# Which Equivalence Theory to Use

<div class="two-col">
  <div class="box">
    <h3>Safe starting zone</h3>
    <ul>
      <li>index arithmetic and offsets;</li>
      <li>associativity and commutativity for approved ops;</li>
      <li>identity rewrites: <code>x + 0</code>, <code>x * 1</code>;</li>
      <li>shape-preserving casts and broadcasts;</li>
      <li>equivalent forms of tile slicing.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Only with guards</h3>
    <ul>
      <li><code>copy_in</code> / <code>copy_out</code>: memory location and layout;</li>
      <li>sync elimination / movement;</li>
      <li>buffer reuse and allocation movement;</li>
      <li>matmul decomposition through L1/L0A/L0B;</li>
      <li>any rules with order-sensitive side effects.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Practical criterion: a rule enters the Babble theory only if it can be checked by the MLIR verifier, type/shape constraints, and compile-only tests.</p>
</div>

---

# What Abstractions Could Be Learned

<div class="three-col">
  <div class="box">
    <h3>Python DSL helpers</h3>
    <ul>
      <li><code>block_tiles(size, cores)</code></li>
      <li><code>load_tile(gm, offset, shape)</code></li>
      <li><code>store_tile(tile, gm, offset)</code></li>
      <li><code>vector_map(fn, *tiles)</code></li>
      <li><code>tile_reduce(fn, tile)</code></li>
    </ul>
  </div>
  <div class="box">
    <h3>IR patterns</h3>
    <ul>
      <li>redundant cast/fold;</li>
      <li>common mask elimination;</li>
      <li>copy-in split through L1;</li>
      <li>load/compute/store fusion;</li>
      <li>canonical offsets.</li>
    </ul>
  </div>
  <div class="box">
    <h3>LLM examples</h3>
    <ul>
      <li>typical skeletons;</li>
      <li>counterexamples for unsafe rewrites;</li>
      <li>verified lowering traces;</li>
      <li>performance annotations;</li>
      <li>review checklists.</li>
    </ul>
  </div>
</div>

<div class="source">Idea: do not ask the LLM to “guess” the idiom; give it mined, verified, domain-grounded abstractions.</div>

---

# Example: From Similar Kernels to a Helper

<div class="code-sample">
  <div>

```python
@asc2.jit
def vadd(x_ptr, y_ptr, out_ptr, size, tile_size):
    x_gm = asc2.global_tensor(x_ptr, [size])
    y_gm = asc2.global_tensor(y_ptr, [size])
    out_gm = asc2.global_tensor(out_ptr, [size])

    for i in range(size // tile_size):
        off = i * tile_size
        x = asc2.copy_in(x_gm, [off], [tile_size])
        y = asc2.copy_in(y_gm, [off], [tile_size])
        out = x + y
        asc2.copy_out(out, out_gm, [off])
```

  <div class="caption">Original recurring skeleton: tile loop + load + compute + store.</div>
  </div>
  <div>

```python
def elementwise_tile_loop(ins, out, size, tile_size, fn):
    for off in tile_offsets(size, tile_size):
        tiles = [load_tile(t, off, tile_size) for t in ins]
        result = fn(*tiles)
        store_tile(result, out, off)

@asc2.jit
def vadd(...):
    elementwise_tile_loop([x_gm, y_gm], out_gm,
                          size, tile_size,
                          lambda x, y: x + y)
```

  <div class="caption">Babble-like output: candidate abstraction, then compile/test/profiler validation.</div>
  </div>
</div>

---

# MVP Pipeline for pyasc-fork

<div class="pipeline">
  <div class="step">
    <strong>1. Corpus</strong>
    <span>collect <code>asc2</code> tutorials, tests, docs examples, and dumped MLIR snapshots</span>
  </div>
  <div class="step">
    <strong>2. Normalize</strong>
    <span>AST/MLIR normalization: names, constants, offsets, canonical ops</span>
  </div>
  <div class="step">
    <strong>3. Learn</strong>
    <span>e-graph saturation + anti-unification for pure-ish fragments</span>
  </div>
  <div class="step">
    <strong>4. Validate</strong>
    <span>type/shape verifier, compile-only tests, optional runtime checks</span>
  </div>
  <div class="step">
    <strong>5. Feed LLM</strong>
    <span>retrieval cards: abstraction, examples, guards, failed rewrites</span>
  </div>
</div>

<div class="callout">
  <p>The first goal should not be “speed up everything”; it should be “assemble a small library of verified PyAsc idioms that an LLM can apply and explain”.</p>
</div>

---

# Where Analysis Tooling Is Needed

<div class="four-col">
  <div class="box">
    <h3>Static shape/type</h3>
    <p>Check that a learned abstraction preserves dtype, rank, shape, tensor location, and const-expression constraints.</p>
  </div>
  <div class="box">
    <h3>Effect model</h3>
    <p>Separate pure tile expressions from order-sensitive operations: memory copies, flags, queues, barriers.</p>
  </div>
  <div class="box">
    <h3>IR diffing</h3>
    <p>Compare before/after: which AscIR ops disappear, which appear, and whether the lowering path changes.</p>
  </div>
  <div class="box">
    <h3>Profiler score</h3>
    <p>Rank library compression together with compile success, latency, memory footprint, and generated-code size.</p>
  </div>
</div>

<div class="tag-row">
  <span class="tag">MLIR verifier</span>
  <span class="tag">pass snapshots</span>
  <span class="tag">CANN compile</span>
  <span class="tag">msprof / runtime profiling</span>
  <span class="tag">LLM retrieval</span>
</div>

---

# Risks

<div class="three-col">
  <div class="box">
    <h3>Unsound rewrites</h3>
    <p>Arithmetic equivalence does not imply equivalence in the presence of memory, sync, and layout constraints.</p>
  </div>
  <div class="box">
    <h3>E-graph blowup</h3>
    <p>AscIR and tile expressions can grow quickly; start with one kernel family.</p>
  </div>
  <div class="box">
    <h3>Wrong objective</h3>
    <p>Corpus compression may hurt readability or latency; the cost model must account for real checks.</p>
  </div>
</div>

<div class="callout">
  <p>Guardrail: Babble proposes candidates; the PyAsc compiler, tests, and profiler decide whether a candidate becomes DSL/API/pass material.</p>
</div>

---

# Recommendation

<div class="two-col">
  <div class="box">
    <h3>Do now</h3>
    <ul>
      <li>start with <code>asc2</code> vector/tile kernels;</li>
      <li>learn common skeletons from Python AST and AscTile IR;</li>
      <li>build retrieval cards for the LLM;</li>
      <li>check every abstraction through a compile-only pipeline.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Defer</h3>
    <ul>
      <li>sync/memory scheduling rewrites without an effect model;</li>
      <li>automatic modification of low-level <code>asc</code> kernels;</li>
      <li>performance claims without hardware runs;</li>
      <li>a broad rule theory for all dialects at once.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Best first result:</strong> a mined library of 10-20 PyAsc idioms with examples, guards, and links to passing compile/runtime evidence.</p>
</div>

<div class="source">Next practical artifact: an extractor prototype for <code>python/tutorials/asc2</code> + “pattern / guard / rewrite / validation” cards.</div>
