# Notes: Ascend / NPU-specific sources

## Why this cluster matters

This is the closest cluster to the proposed work. The central question is not only whether an agent can generate AscendC code, but whether it can understand and optimize the coupled host-tiling + device-kernel structure that determines Ascend operator performance.

## Key papers

### AscendOptimizer

Link: https://arxiv.org/abs/2603.23566

Use as the closest direct baseline for agentic AscendC optimization. It frames the problem as a two-fold knowledge bottleneck: limited public AscendC examples and coupled host/kernel performance structure.

Important takeaways for this repo:

- host-side tiling and data movement should be represented explicitly;
- kernel-side scheduling/pipelining needs separate but connected treatment;
- execution feedback can be turned into reusable optimization experience;
- a future system can improve on this by exposing compiler-derived structured views rather than relying only on episodic feedback.

### AscendCraft

Link: https://arxiv.org/abs/2601.22760

Use as evidence that a DSL layer can make Ascend execution semantics more accessible to LLMs.

Important takeaways:

- raw AscendC is too domain-specific and sparse in training data;
- a lightweight DSL can hide non-essential complexity while preserving execution semantics;
- this supports the programming-model side of the topic.

### AscendKernelGen

Link: https://arxiv.org/abs/2601.07160

Use as evidence that general-purpose LLMs struggle with NPU kernel generation without domain adaptation and execution feedback.

### Squeezing Operator Performance Potential for the Ascend Architecture

Link: https://cs.nju.edu.cn/tianchen/lunwen/2025/asplos25-yuhang.pdf

Use as the performance-analysis foundation. Its component-based roofline abstraction is a strong candidate for the performance evidence view.

Candidate views derived from this paper:

- component utilization view;
- MTE/compute bottleneck view;
- insufficient parallelism vs inefficient component classification;
- pipeline status view;
- targeted optimization strategies tied to bottleneck class.
