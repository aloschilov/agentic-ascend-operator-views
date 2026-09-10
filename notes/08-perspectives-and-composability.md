# Execution perspectives and composability

These are references for research hypotheses, not an implemented induction method or certificates for Ascend transformations. Version and licence checks: 2026-09-10.

## Modular GPU Programming with Typed Perspectives

Manya Bansal, Daniel Sainati, Joseph W. Cutler, Saman Amarasinghe and Jonathan Ragan-Kelley. arXiv:2511.11939v1, 14 November 2025. [Source](https://arxiv.org/abs/2511.11939v1); [unchanged PDF](../publications/files/prism-typed-perspectives-2511.11939v1.pdf); [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Copyright remains with the authors. No endorsement is implied.

Prism exposes cooperative execution through typed perspectives; Bundl supplies a formal core. Read sections 2–4 for perspectives, code/memory interfaces and the safety argument, then the limitations. This is a high-priority reference for deciding which execution requirements belong in a graph's types.

Project interpretation: represent execution group, participation requirements and memory-access scope separately. Do not identify a GPU warp with an Ascend core. The paper does not discharge CANN-specific obligations for queue expansion, DMA completion, event generations or AIC/AIV handoff.

SHA-256: `b92338ba20a39fa214f2c027062127f2ad86150853c2f24724915e1ce1ce6504`.

## A Programming Paradigm for Spatiotemporal Composability

Yifan Shi, Wei Zhang and Tianyi Cui. arXiv:2608.25512v1, 26 August 2026. [Source](https://arxiv.org/abs/2608.25512v1); [arXiv PDF](https://arxiv.org/pdf/2608.25512v1); [listed licence](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html).

The setting is dynamic components: revertible effects, reactive coeffects and mediated context. Prioritize sections 3.3–3.4 for observational equivalence and independence, and section 6 for limitations. The complete 92-page calculus is optional for the current extraction bottleneck.

Project interpretation: useful discipline for stating observations and independence conditions. It does not make DMA reversible or establish that disjoint writes suffice for reordering asynchronous operations. Buffer ownership, resource capacity and visible completion remain separate obligations.

The listed licence grants distribution rights to arXiv, not a general redistribution licence. Therefore the full text is downloaded for local reading as `publications/files/spatiotemporal-composability-2608.25512v1.pdf`, excluded from Git, and represented publicly by links and these notes. Additional permission would be needed before vendoring it here.

SHA-256: `390775dbc9debdcf2ed1b076eed013387ca057630be3cb594617b2b742e48cf0`.

## Reading outcome

Read Prism first; use composability as a later check on the formulation of guarded laws. Neither paper replaces source-grounded effect extraction or simulator counterexamples. Keep abstraction discovery, correctness of expansion, and legality of graph transformations as different claims.
