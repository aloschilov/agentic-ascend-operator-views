# Notes: LLM / agentic kernel optimization

## Why this cluster matters

This cluster shows that kernel generation needs more than prompting. Correctness, compilation, and performance improve when the system includes execution feedback, profiling, benchmarks, and domain-specific constraints.

## Key sources

### KernelBench

Link: https://arxiv.org/abs/2502.10517

Useful for benchmark design and metric framing. The `fast_p` idea maps naturally to Ascend operator evaluation: correct kernel plus speed threshold relative to baseline/reference.

### TritonBench

Link: https://arxiv.org/abs/2502.14752

Useful as a GPU/Triton analogue. It highlights that even a relatively friendly DSL such as Triton remains difficult for LLMs when performance matters.

### GEAK

Link: https://arxiv.org/abs/2507.23194

Useful as an agentic feedback-loop baseline for Triton/AMD. It motivates comparing direct prompting vs iterative agentic generation.

### CompilerGPT

Link: https://arxiv.org/abs/2506.06227

Important because it uses compiler optimization reports as a bridge between compiler analysis and LLM action. The proposed Ascend work can be positioned as a domain-specific extension where the reports become richer structured operator views.

## Gap for this repo

Most LLM kernel systems still expose either code, tests, compiler errors, or profiling feedback. The research gap is to expose a structured, domain-aware representation of the operator and its legal optimization space.
