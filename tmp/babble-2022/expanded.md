<div class="CCSXML">

\<ccs2012\> \<concept\> \<concept_id\>10011007.10011006.10011008.10011009.10011012\</concept_id\> \<concept_desc\>Software and its engineering Functional languages\</concept_desc\> \<concept_significance\>500\</concept_significance\> \</concept\> \<concept\> \<concept_id\>10011007.10011074.10011092.10011782\</concept_id\> \<concept_desc\>Software and its engineering Automatic programming\</concept_desc\> \<concept_significance\>500\</concept_significance\> \</concept\> \</ccs2012\>

</div>

# Introduction

Abstraction is the key to managing software complexity. Experienced programmers routinely extract common functionality into libraries of reusable abstractions to express their intent more clearly and concisely. What if this process of extracting useful abstractions from code could be automated? *Library learning* seeks to answer this question with techniques to compress a given corpus of programs by extracting common structure into reusable library functions. Library learning has many potential applications from refactoring and decompilation , to modeling human cognition , and speeding up program synthesis by specializing the target language to a chosen problem domain .

Consider the simple library learning task in <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>. On the left, <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>a shows a corpus of three programs in a <span class="smallcaps">2d cad</span> DSL from . Each program corresponds to a picture composed of regular polygons, each of which is made of multiple rotated line segments. On the right, <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>b shows a learned library with a single function (named `f0`) that abstracts away the construction of scaled regular polygons. The three input programs can then be refactored into a more concise form using the learned `f0`. Whether `f0` is the “best” abstraction for this corpus is generally hard to quantify. For this paper, we follow <span class="smallcaps">DreamCoder</span>  and use *compression* as a metric for library learning, *i.e.*, the goal is to reduce the total size of the corpus in AST nodes (from 208 to 72 <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>). Importantly, the total size of the corpus includes the size of the library: this prevents library learning from generating too many overly-specific functions, and instead biases it towards more general and reusable abstractions.

<figure id="fig:polygons">
<embed src="figures/polygons.pdf" />
<figcaption>Example of library learning. Initial corpus A contains three graphical programs from the “nuts &amp; bolts” dataset of <span class="citation" data-cites="cogsci-dataset"></span>. Corpus B is the output of library learning with a single learned function for a scaled polygon, and the original programs refactored using this function.</figcaption>
</figure>

Library learning can be phrased as a program synthesis problem structured in two phases: *generating* candidate abstractions, and then *selecting* those abstractions that produce the best (smallest) refactored corpus. The state-of-the-art technique, implemented in <span class="smallcaps">DreamCoder</span> , suffers from two primary limitations that hinder scaling library learning to larger and more realistic inputs.

- Candidate generation is not ***precise***: <span class="smallcaps">DreamCoder</span> generates many candidate abstractions that cannot be useful, slowing down the selection phase and the algorithm as a whole.

- The technique is purely syntactic and hence not ***robust*** to superficial variation. For example, a human programmer would immediately know that the terms $`2 + 1`$ and $`1 + 3`$ can be refactored using the abstraction $`\lambda x \ \mathbf{\shortrightarrow}\ x + 1`$, because addition commutes; a purely syntactic library learning approach cannot generate this abstraction.

In this paper we propose *library learning modulo (equational) theories* (LLMT)—a new library learning algorithm that addresses both of the above limitations.

***Precise Candidate Generation via Anti-Unification.*** To make candidate generation more precise, LLMT leverages two key observations:

- Useful abstractions must be used in the corpus at least twice. For example, in a corpus of two programs $`2 + 1`$ and $`3 + 1`$, there is no need to consider $`\lambda x \ \mathbf{\shortrightarrow}\ 3 + x`$ because it can only be used in one place, and hence would only increase the size of the corpus.

- Abstractions should be “as concrete as possible” for a given corpus. For example, in the same corpus with $`2 + 1`$ and $`3 + 1`$, the abstraction $`\lambda x \ \mathbf{\shortrightarrow}\ x + 1`$ is superior to the more general $`\lambda x\ y \ \mathbf{\shortrightarrow}\ x + y`$, since both apply to the same two terms, but applying the latter is more expensive (it requires two arguments).

In other words, a useful abstraction corresponds to the least general *pattern* that matches some pair of subterms from the original corpus; such a pattern can be computed via *anti-unification* (AU) . For example, anti-unifying $`2 + 1`$ and $`3 + 1`$ yields the pattern $`X + 1`$, and the desired candidate library function $`\lambda x \ \mathbf{\shortrightarrow}\ x + 1`$ can be derived by abstracting over the pattern variable $`X`$. Similarly, in <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>, the abstraction `f0` can be derived by anti-unifying, for example, the blue and the brown subterms of the corpus.

***Robustness via E-Graphs.*** To make candidate generation more robust, LLMT additionally takes as input a *domain-specific equational theory* and uses it to find programs that are semantically equivalent to the original corpus, but share the most syntactic structure. For example, in the domain of arithmetic, we expect the theory to contain the equation $`X + Y  \equiv Y + X`$, which states that addition is commutative. Given the corpus with terms $`2 + 1`$ and $`1 + 3`$, this rule can be used to rewrite the second term in to $`3 + 1`$, enabling the discovery of the common abstraction $`\lambda x \ \mathbf{\shortrightarrow}\ x + 1`$.

The main challenge with this approach is to search over the large space of programs that are semantically equivalent to the original corpus. To this end, LLMT relies on the *e-graph* data structure and the *equality saturation* technique  to compute and represent the space of semantically equivalent programs. To enable efficient library learning over this space, we propose a new candidate generation algorithm that efficiently computes the set of all anti-unifiers between pairs of sub-terms represented by an e-graph, using dynamic programming.

Finally, *selecting* the optimal library in this setting reduces to the problem of *extracting* the smallest term out of an e-graph in the presence of common sub-expressions. This problem is extremely computationally intensive in its general form, and existing approaches have limited scalability . Instead we propose *targeted subexpression elimination*: a novel e-graph extraction algorithm that uses domain-specific knowledge to reduce the search space and readily supports approximation via beam search to trade off accuracy and efficiency.

<figure id="fig:arch">
<embed src="figures/arch.pdf" />
<figcaption><span class="smallcaps">babble</span> architecture overview</figcaption>
</figure>

***<span class="smallcaps">babble</span>.*** We have implemented LLMT in <span class="smallcaps">babble</span>, a tool built on top of the <span class="smallcaps">egg</span> e-graph library . The overview of the <span class="smallcaps">babble</span>’s workflow is shown in <a href="#fig:arch" data-reference-type="ref+label" data-reference="fig:arch">2</a>, with gray boxes representing existing techniques and black boxes representing our contributions.

We evaluated <span class="smallcaps">babble</span> on benchmarks from two sources: compression tasks extracted from <span class="smallcaps">DreamCoder</span> runs  and <span class="smallcaps">2d cad</span> programs used to evaluate concept learning in humans . Our evaluation shows that <span class="smallcaps">babble</span> outperforms <span class="smallcaps">DreamCoder</span> on its own benchmarks, achieving better compression in orders of magnitude less time. Adding domain-specific rewrites improves compression even further. We also show that <span class="smallcaps">babble</span> scales to the larger <span class="smallcaps">2d cad</span> corpora, which is beyond reach of <span class="smallcaps">DreamCoder</span>. We also present and discuss a selection of abstractions learned by <span class="smallcaps">babble</span>, demonstrating that the LLMT approach can learn functions that match human intuition.

***Contributions.*** In summary, this paper makes the following contributions:

- *library learning modulo equational theory*: a library learning algorithm that can incorporate an arbitrary domain-specific equational theory to make learning robust to syntactic variations;

- *e-graph anti-unification*: an algorithm that efficiently generates the set of candidate abstractions using the mechanism of anti-unification extended from terms to e-graphs;

- *targeted common subexpression elimination*: a new approximate algorithm for extracting the best term from an e-graph in the presence of common sub-expressions.

# Overview

We illustrate LLMT via a running example building on <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>. The input corpus in <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a> is written in a <span class="smallcaps">2d cad</span> DSL by , which features the following primitives:

|  |  |
|---:|:---|
| `line` | a line segment from the origin (0, 0) to the point (1, 0) |
| $`\mbox{\lstinline^combine^}(F_1,\ F_2)`$ | the union of figures $`F_1`$ and $`F_2`$ |
| $`\mbox{\lstinline^xform^}(F,\ \tau)`$ | applying transformation $`\tau`$ to figure $`F`$ |
| $`\mbox{\lstinline^repeat^}(F,\ 0,\ \tau)`$ | the empty figure |
| $`\mbox{\lstinline^repeat^}(F,\ n+1,\ \tau)`$ | $`\mbox{\lstinline^combine^}(F,\ \ensuremath{\mbox{\lstinline^xform^}(\ensuremath{\mbox{\lstinline^repeat^}(F,\ n,\ \tau)},\ \tau)})`$, similar to a “fold” |

A transformation $`\tau`$ is a 4-tuple $`\ensuremath{[s, \theta, t_x, t_y]}`$ denoting uniformly scaling by a factor of $`s`$, rotating by $`\theta`$ radians, and translating by $`(t_x,\ t_y)`$ in the $`x`$ and $`y`$ directions respectively. For example, the green hexagon in <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a> is implemented as:
``` math
\ensuremath{\mbox{\lstinline^xform^}(
    \ensuremath{\mbox{\lstinline^repeat^}(
      \ensuremath{\mbox{\lstinline^xform^}(
        \mbox{\lstinline^line^}
      ,\ 
        \ensuremath{[1, 0, -0.5, 0.5 / \tan(\pi / 6)]}
      )}
    ,\ 6,\ 
      \ensuremath{[1, 2\pi/6, 0, 0]}
    )}
  ,\ 
    \ensuremath{[2, 0, 0, 0]}
  )}
```
That is, a hexagon side $`\ensuremath{\mbox{\lstinline^xform^}(\mbox{\lstinline^line^},\ \ensuremath{[1, 0, -0.5, 0.5 / \tan(\pi / 6)]})}`$ is repeated six times, each time rotated by another $`2\pi/6`$ radians, and the resulting unit hexagon is scaled by $`2`$.

Taking a closer look at the two blue hexagons in <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>, however, we notice something peculiar. The two occurrences of $`\mbox{\lstinline^xform^}(\mbox{\lstinline^repeat^} \ldots,\ \ensuremath{[1, 0, 0, 0]})`$ in <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a> are no-ops: they merely scale a figure $`F`$ by a factor of 1 and neither rotate nor translate it. These redundant transformations would likely not be there had the code been written by hand or decompiled from a lower-level representation (by a tool like <span class="smallcaps">Szalinski</span> );[^1] and yet, they are crucial if we hope to learn the optimal abstraction $`f_0`$ with a purely syntactic technique.

<a href="#fig:llmt" data-reference-type="ref+label" data-reference="fig:llmt">3</a> shows a simplified and “more natural” version of the corpus from <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>, which eliminates these no-op transformations. As illustrated in the figure, this causes a purely syntactic technique to learn a different function, $`f_1`$, which abstracts over an *unscaled* unit polygon. Because the scaling transformation is now outside the abstraction, it must be repeated five times. As a result, although the simplified input corpus C from <a href="#fig:llmt" data-reference-type="ref+label" data-reference="fig:llmt">3</a> is *smaller* than the original corpus A (196 AST nodes instead of 208), its compressed version D is *larger* (81 AST nodes instead of 72)! In other words, syntactic library learning is not robust with respect to semantics-preserving code variations.

<figure id="fig:llmt">
<embed src="figures/polygons-simplified.pdf" />
<figcaption>Difference between syntactic library learning and LLMT. Here the initial corpus C is the simplified version of corpus A from <a href="#fig:polygons" data-reference-type="ref+label" data-reference="fig:polygons">1</a>, with the redundant transformations on the blue subterms removed (unchanged terms are shown as ellipses). With this modification, syntactic techniques would learn an inferior abstraction <span class="math inline"><em>f</em><sub>1</sub></span>, leading to corpus D, while LLMT still learns the better abstraction <span class="math inline"><em>f</em><sub>0</sub></span>. </figcaption>
</figure>

In contrast, our tool <span class="smallcaps">babble</span> can take the simplified corpus C as input and still discover, in a fraction of a second, the scaled polygon abstraction $`f_0`$, yielding the compressed corpus B of size 72. In the rest of this section, we illustrate how <span class="smallcaps">babble</span> achieves this using our new algorithm, *library learning modulo equational theory* (LLMT).

***Simplified DSL.*** In the rest of this section we use a tailored version of the <span class="smallcaps">2d cad</span> DSL with the following additional constructs:

|  |  |
|---:|:---|
| $`\mbox{\lstinline^scale^}(F,\ s)`$ | scale $`F`$ by a factor of $`s`$ |
| $`\mbox{\lstinline^repRot^}(F,\ n,\ \theta)`$ | a special case of `repeat` that only performs rotation between iterations |
| $`\mbox{\lstinline^side^}(n)`$ | a side of a regular unit $`n`$-gon |

These are expressible in the original DSL, and could be even discovered with library learning, given an appropriate corpus; we treat them as primitives here for the sake of simplifying presentation.

## Representing Equivalent Terms with E-Graphs

To exploit equivalences during library learning, <span class="smallcaps">babble</span> takes as input a domain-specific equational theory. For our running example, let us assume that the theory contains a single equation:
``` math
\begin{equation}
  F \equiv\ensuremath{\mbox{\lstinline^scale^}(F,\ 1)} \label{eq:unit-xform}
\end{equation}
```
which stipulates that any figure $`F`$ is equivalent to itself scaled by one. With this equation in hand, it is possible to “rewrite” corpus C into corpus A, and from there learn the optimal compressed corpus B by purely syntactic techniques. The challenge is that there are infinitely many alternative corpora C may be rewritten to; how do we know which to pick to maximize syntactic alignment, and thus the chance of discovering an optimal abstraction?

Instead of trying to guess the best equivalent corpus or enumerating them one by one, <span class="smallcaps">babble</span> uses *equality saturation* . Equality saturation takes as input a term $`t`$ and a set of rewrite rules, and finds the space of all terms equivalent to $`t`$ under the given rules; this is possible due to the high degree of sharing provided by the *e-graph* data structure, which can compactly represent the resulting space.

<a href="#fig:egraph" data-reference-type="ref+label" data-reference="fig:egraph">4</a> (left) shows the e-graph built by equality saturation for the blue term in <a href="#fig:llmt" data-reference-type="ref+label" data-reference="fig:llmt">3</a>—represented in the simplified DSL as $`\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(6)},\ 6,\ 2\pi/6)`$—using the rewrite rule <a href="#eq:unit-xform" data-reference-type="eqref" data-reference="eq:unit-xform">[eq:unit-xform]</a>. The blue part of the graph represents the original term, and the gray part is added by equality saturation. The solid rectangles in the e-graph denote *e-nodes* (which are similar to regular AST nodes), while the dashed rectangles denote *e-classes* (which represent equivalence classes of terms). Importantly, the edges in the e-graph go from e-nodes to e-classes, which enables compact representation of programs with variation in sub-terms: for example, making e-class $`c_1`$ the first child of the `repRot` node, enables it to represent both terms $`\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(6)},\ 6,\ 2\pi/6)`$ and $`\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^side^}(6)},\ 1)},\ 6,\ 2\pi/6)`$ without duplicating their common parts. Furthermore, because e-graphs can have cycles, they can also represent infinite sets of terms: for example, the e-class $`c_1`$ represents all terms of the form: $`\mbox{\lstinline^side^}(6)`$, $`\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^side^}(6)},\ 1)`$, $`\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^side^}(6)},\ 1)},\ 1)`$, etc. Because this e-graph represents the space of *all* equivalent terms up to the rewrite <a href="#eq:unit-xform" data-reference-type="eqref" data-reference="eq:unit-xform">[eq:unit-xform]</a>, the term we seek for library learning, namely $`\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(6)},\ 6,\ 2\pi/6)},\ 1)`$, is also represented in the e-class $`c_0`$.

<figure id="fig:egraph">
<div class="minipage">
<embed src="figures/egraph-blue.pdf" />
</div>
<div class="minipage">
<embed src="figures/egraph-new.pdf" />
</div>
<figcaption>(Left) An e-graph representing the space of all programs equivalent the blue term in <a href="#fig:llmt" data-reference-type="ref+label" data-reference="fig:llmt">3</a> under rule <a href="#eq:unit-xform" data-reference-type="eqref" data-reference="eq:unit-xform">[eq:unit-xform]</a>. (Right) An e-graph with both the blue and the brown terms from <a href="#fig:llmt" data-reference-type="ref+label" data-reference="fig:llmt">3</a> after equality saturation. All terms are written in the simplified DSL. </figcaption>
</figure>

## Candidate Generation via E-Graph Anti-Unification

After building an e-graph from the given corpus by running equality saturation with the given equational theory, the next step in library learning is to generate candidate patterns that capture syntactic similarities across the corpus. The challenge is to generate sufficiently few candidates to make library learning tractable, but sufficiently many to achieve good compression. We illustrate candidate generation using the e-graph in <a href="#fig:egraph" data-reference-type="ref+label" data-reference="fig:egraph">4</a> (right), which represents the part of our corpus consisting of the (saturated) blue and brown terms. Recall that the optimal pattern—which corresponds to the scaled polygon abstraction $`f_0`$—is:
``` math
\begin{equation}
  P_0 = \ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(X)},\ X,\ 2\pi/X)},\ Y)}\label{eq:p0}
\end{equation}
```

Prior work on <span class="smallcaps">DreamCoder</span> generates patterns by picking a random fragment from the corpus, and then replacing arbitrarily chosen subterms with pattern variables. For example, to generate the pattern $`P_0`$, <span class="smallcaps">DreamCoder</span> needs to pick the entire brown subterm as a fragment, and then decide to abstract over its subterms $`8`$ and $`2`$. This approach successfully restricts the set of candidates from all syntactically valid patterns to only those that have at least one match in the corpus; however, since there are too many ways to select the subterms to abstract over, this space is still too large to explore exhaustively beyond small corpora of short programs. In <span class="smallcaps">babble</span>, this problem is exacerbated by equality saturation, since the e-graph often contains exponentially or infinitely more programs than the original corpus.

***Generality Filters.*** To further prune the set of viable candidates in <span class="smallcaps">babble</span>, we identify two classes of patterns that can be safely discarded, either because they are too concrete or too abstract. First, a pattern like $`\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(8)},\ X,\ 2\pi/8)`$ can be discarded because it is *too concrete* for this corpus: the corresponding abstraction can be applied only once, essentially replacing the sole matching term, $`\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(8)},\ 8,\ 2\pi/8)`$ with $`(\lambda x \ \mathbf{\shortrightarrow}\ \ensuremath{\mbox{\lstinline^repeat^}(\ensuremath{\mbox{\lstinline^side^}(8)},\ x,\ 2\pi/8)})\ 8`$, which only adds more AST nodes to the corpus. Second, a pattern like $`\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(X)},\ X,\ Y)`$ can be discarded because it is *too abstract* for this corpus: everywhere it matches, a more concrete pattern $`\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(X)},\ X,\ 2\pi/X)`$ would also match; using the more concrete pattern leads to better compression, since the actual arguments in its applications are both fewer and smaller: `f 6 2pi/6` and `f 8 2pi/8` vs. `f 6` and `f 8`.

Thus, our ***first key insight*** is to restrict the set of candidates to the most concrete patterns that match some pair of subterms in the (saturated) corpus.[^2] For example, pattern $`P_0`$ is the most concrete pattern that matches the two terms
``` math
\begin{gather}
    \ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(6)},\ 6,\ 2\pi/6)},\ 1)}\label{eq:hex}\\
    \ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(8)},\ 8,\ 2\pi/8)},\ 2)}\label{eq:oct}
\end{gather}
```
represented in <a href="#fig:egraph" data-reference-type="ref+label" data-reference="fig:egraph">4</a> by the e-classes $`c_0`$ and $`c_2`$, respectively.

***Term Anti-Unification.*** Computing the most concrete pattern that matches two given terms is known as *anti-unification* (AU) . AU works by a simple top-down traversal of the two terms, replacing any mismatched constructors by pattern variables. For example, to anti-unify the terms <a href="#eq:hex" data-reference-type="eqref" data-reference="eq:hex">[eq:hex]</a> and <a href="#eq:oct" data-reference-type="eqref" data-reference="eq:oct">[eq:oct]</a>, we start from the root of both terms; since both AST nodes share the same constructor `scale`, it becomes part of the pattern and we recurse into the children. We eventually encounter a mismatch, where the term on the left is `6` and the term on the right is `8`; so we create a fresh pattern variable $`X`$ and remember the *anti-substitution* $`\sigma = \{(\mbox{\lstinline^6^}, \mbox{\lstinline^8^}) \mapsto X\}`$. When we encounter a mismatch in the denominator of the angle, we look up the pair of mismatched terms $`(\mbox{\lstinline^6^}, \mbox{\lstinline^8^})`$ in $`\sigma`$; because we already created a variable for this pair, we simply return the existing variable $`X`$. The final mismatch is $`(\mbox{\lstinline^1^}, \mbox{\lstinline^2^})`$ in the second child of `scale`; since this pair is not yet in $`\sigma`$, we create a second pattern variable, $`Y`$. At this point, the resulting anti-unifier is the pattern $`P_0`$ <a href="#eq:p0" data-reference-type="eqref" data-reference="eq:p0">[eq:p0]</a>.

Anti-unifying a single pair of terms is simple and efficient. However, in LLMT we want to anti-unify *all pairs of subterms* that can occur *in any corpus* equivalent (modulo the given equational theory) to the original[^3]. Explicitly enumerating all equivalent corpora represented by the e-graph and then performing AU on each pair of subterms is infeasible. Instead, <span class="smallcaps">babble</span> performs anti-unification directly on the e-graph.

***From Terms to E-Classes.*** We first explain how to anti-unify two e-classes. This operation takes as input a pair of e-classes and returns a set of *dominant anti-unifiers*, *i.e.* a set of patterns that (1) match both e-classes, and (2) is guaranteed to include the best abstraction among the most concrete patterns that match pairs of terms represented by the two e-classes.

Consider computing $`\mathsf{AU}(c_1, c_4)`$ for the e-classes $`c_1`$ and $`c_4`$ in the e-graph from <a href="#fig:egraph" data-reference-type="ref+label" data-reference="fig:egraph">4</a> (right). AU still proceeds as a top-down traversal, but in this context we must check whether two e-classes have any constructors *in common*. In this case they do: both a `side` constructor and a `scale` constructor. Let us first pick the two `side` constructors and recurse into their only child, computing $`\mathsf{AU}(\{\mbox{\lstinline^6^}\}, \{\mbox{\lstinline^8^}\})`$. These two e-classes have no matching constructors, so AU simply returns a pattern variable, similarly to term anti-unification; this yields the first pattern for $`c_1`$ and $`c_4`$: $`\mbox{\lstinline^side^}\ X`$.

Recall, however, that $`c_1`$ and $`c_4`$ also have matching `scale` constructors. This is where things get interesting: these constructors are involved in a *cycle* (their first child is the parent e-class itself). If we let AU follow this cycle, the set of anti-unifiers becomes infinite:
``` math
\mathsf{AU}(c_1, c_4) = \{\mbox{\lstinline^side^}\ X\} \cup \{\mbox{\lstinline^scale^}\ p\ 1 \mid p \in \mathsf{AU}(c_1, c_4)\}
```
Fortunately, we can show that $`\mbox{\lstinline^side^}\ X`$ *dominates* all the other patterns from this set, because their pattern variables—in this case, just $`X`$—match the same e-classes, but they are also larger (in <a href="#sec:egraphs" data-reference-type="ref+label" data-reference="sec:egraphs">4</a> we show how this domination relation lets us prune other patterns, not just those caused by cycles). Hence $`\mathsf{AU}(c_1, c_4)`$ simply returns $`\{\mbox{\lstinline^side^}\ X\}`$.

Following the same logic for the root e-classes of the two polygons, $`c_0`$ and $`c_2`$, $`\mathsf{AU}(c_0, c_2)`$ yields that pattern $`P_0`$ <a href="#eq:p0" data-reference-type="eqref" data-reference="eq:p0">[eq:p0]</a>, which is required to learn the optimal abstraction.

***From E-Classes to E-Graphs.*** To obtain the set of all candidate abstractions, we need to perform anti-unification over all pairs of e-classes in the e-graph. Clearly, these computations have overlapping subproblems (for example, we have to compute $`\mathsf{AU}(c_1, c_4)`$ as part of $`\mathsf{AU}(c_0, c_2)`$ and $`\mathsf{AU}(c_0, c_3)`$). To avoid duplicating work, <span class="smallcaps">babble</span> uses an efficient dynamic programming algorithm that processes all pairs of e-classes in a bottom-up fashion.

## Candidate Selection via Targeted Common Subexpression Elimination

We now illustrate the final step of library learning in <span class="smallcaps">babble</span>: given the set of candidate abstractions generated by e-graph anti-unification, the goal is to pick a subset that gives the best compression for the corpus as a whole. For example, the candidates generated for the corpus from <a href="#fig:llmt" data-reference-type="ref+label" data-reference="fig:llmt">3</a> include:
``` math
\begin{array}{rcll}
f_0 &=& \lambda x\ y \ \mathbf{\shortrightarrow}\ \ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(x)},\ x,\ 2\pi/x)},\ y)} &\quad \text{scaled regular $x$-gon} \\[2pt]
f_1 &=& \lambda x \ \mathbf{\shortrightarrow}\ \ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(x)},\ x,\ 2\pi/x)} &\quad \text{regular $x$-gon} \\[2pt]
f_2 &=& \lambda y \ \mathbf{\shortrightarrow}\ \ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(6)},\ 6,\ 2\pi/6)},\ y)} &\quad \text{scaled hexagon}
\end{array}
```
It is not immediately clear which abstraction is better: $`f_0`$ matches more terms than $`f_2`$, but $`f_2`$ requires fewer arguments (so if we have enough scaled hexagons in the corpus and only one octagon, it might be better to leave the octagon un-abstracted). On the other hand, $`f_1`$ might be better, since it does not introduce the redundant transformation on the blue hexagons. Finally, if we pick $`f_0`$ *and* $`f_2`$ together, we can also abstract the definition of $`f_2`$ as $`f_0\ 6`$, thereby getting additional reuse! As you can see, candidate selection is highly non-trivial, since it needs to take into account the choice between different equivalent programs in the e-graph, and the fact that some abstractions can be defined using others.

<figure id="fig:beam">
<embed src="figures/beam.pdf" />
<figcaption>The e-graph from <a href="#fig:egraph" data-reference-type="ref+label" data-reference="fig:egraph">4</a> (right) with applications of <span class="math inline"><em>f</em><sub>0</sub></span> and <span class="math inline"><em>f</em><sub>1</sub></span> depicted in red. We show the unchanged parts of the graph representing the unit hexagon and octagon as corresponding shapes; we also omit some of the gray e-nodes added in the previous stage.</figcaption>
</figure>

***Reduction to E-Graph Extraction.*** To overcome this difficulty, we once again leverage e-graph and equality saturation. Our ***second key insight*** is that selecting the optimal subset of abstractions can be reduced to the problem of extracting the smallest term from an e-graph in the presence of common sub-expressions.

To illustrate this reduction, let us limit our attention to only two candidate abstractions, $`f_0`$ and $`f_1`$, defined above. <span class="smallcaps">babble</span> converts each of the candidate patterns and its corresponding abstraction into a rewrite rule that introduces a *local* $`\lambda`$-abstraction followed by application into the corpus; for our two abstractions these rules are:
``` math
\begin{align}
\ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(X)},\ X,\ 2\pi/X)},\ Y)} &\Rightarrow f_0\ X\ Y\label{eq:rw1}\\ 
  \ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(X)},\ X,\ 2\pi/X)} &\Rightarrow f_1\ X \label{eq:rw2}
\end{align}
```
The result of applying these rules to the e-graph from <a href="#fig:egraph" data-reference-type="ref+label" data-reference="fig:egraph">4</a> (right) is shown in <a href="#fig:beam" data-reference-type="ref+label" data-reference="fig:beam">5</a>. For example, you can see that the e-class $`c_2`$ (which represents the scale-2 octagon) now stores an alternative representation: $`f_0\  8\ 2`$. The e-class $`c_0`$ (unit hexagon) has representations using either $`f_0`$ or $`f_1`$, because this class matches both rewrite rules <a href="#eq:rw1" data-reference-type="eqref" data-reference="eq:rw1">[eq:rw1]</a> and <a href="#eq:rw2" data-reference-type="eqref" data-reference="eq:rw2">[eq:rw2]</a> above. Note also that because the definitions of the $`\lambda`$-abstractions are also stored in the e-graph, equality saturation can use the above rewrite rules inside their bodies, to make one function use another: for example, one term stored for the definition of $`f_0`$ is
``` math
\lambda x\ y \ \mathbf{\shortrightarrow}\ \ensuremath{\mbox{\lstinline^scale^}(f_1\ x,\ y)}.
```

Once we have built the version of the e-graph with local lambdas for all the candidate abstractions, all that is left is to extract the smallest term out of this e-graph. The tricky part is that we want to count the size of the duplicated lambdas only once. For example, in <a href="#fig:beam" data-reference-type="ref+label" data-reference="fig:beam">5</a>, $`f_0`$ is applied twice (in $`c_0`$ and $`c_2`$); if term extraction were to choose both of these e-nodes, we want to treat their first child (the definition of $`f_0`$) as a common sub-expression, whose size contributes to the final expression only once. Intuitively, this is because we can “float” these lambdas into top-level `let`-bindings, thereby defining $`f_0`$ only once, and replacing each local lambda with a name.

Extraction with common sub-expressions is a known but notoriously hard problem, which is traditionally reduced to integer linear programming (ILP) . Because the scalability of the ILP approach is very limited, we have developed a custom extraction algorithm, which scales better by using domain-specific knowledge and approximation.

***Extraction Algorithm.*** The main idea for making extraction more efficient is that for library learning we are only interested in sharing a certain type of sub-terms: namely, the $`\lambda`$-abstractions. Hence for each e-class we only need to keep track of the the best term for each possible library (*i.e.* each subset of $`\lambda`$-abstractions). More precisely, for each e-class and library, we keep track of (1) the smallest size of the library (2) the smallest size of the program refactored using this library (counting the $`\lambda`$-abstractions as a single node). We compute and propagate this information bottom-up through the e-graph. Once this information is computed for the root e-class (that represents the entire corpus), we can simply choose the library with the smallest total size.

For example, for the e-class $`c_2`$ from <a href="#fig:beam" data-reference-type="ref+label" data-reference="fig:beam">5</a>, with the empty library $`\emptyset`$, the size of library is 0 and the size of the smallest program ($`\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(8)},\ 8,\ 2\pi/8)},\ 2)`$) is 9; with the library $`\{f_0\}`$, the size of the library is 9 and the size of the smallest program ($`f_0\ 2\ 8`$) is 3; while with the library $`\{f_1\}`$, the size of the library is 7 and the size of the smallest program ($`\mbox{\lstinline^scale^}(f_1\ 8,\ 2)`$) is 4. Clearly for this e-class introducing library functions is not paying off yet ($`0 + 9 < 7 + 4 < 9 + 3`$), since each one can be only used once. This situation changes, however, as we move up towards the root. Already for the parent e-class of $`c_0`$ and $`c_2`$, the cost of introducing $`\{f_0\}`$ and $`\{f_1\}`$ is amortized: the size of the smallest program is 17 with the empty library and 7 with either $`\{f_0\}`$ or $`\{f_1\}`$, so $`\{f_1\}`$ is already worthwhile to introduce ($`9 + 7 < 0 + 17`$). Including even more programs with scaled polygons eventually makes the library $`\{f_0\}`$ the most profitable of the four subsets.

Since in a larger corpus, keeping track of all subsets of candidate abstractions is not feasible, <span class="smallcaps">babble</span> provides a way to trade off scalability and precision by using a *beam search* approach.

# Library Learning over Terms

In this section we formalize the problem of library learning over a corpus of terms and motivate our first core contribution: generating candidate abstractions via anti-unification. <a href="#sec:egraphs" data-reference-type="ref+label" data-reference="sec:egraphs">4</a> generalizes this formalism to library learning over an e-graph. For simplicity of exposition, our formalization of library learning is *first order*, that is, the initial corpus does not itself contain any $`\lambda`$-abstractions, and all the learned abstractions are first-order functions (the <span class="smallcaps">babble</span> implementation does not have this limitation).

## Preliminaries

***Terms.*** A *signature* $`\Sigma`$ is a set of constructors, each associated with an arity. $`\mathcal{T}(\Sigma)`$ denotes the set of *terms* over $`\Sigma`$, defined as the smallest set containing all $`s(t_1,\dots,t_k)`$ where $`s \in \Sigma`$, $`k = \mathsf{arity}(s)`$, and $`t_1,\dots,t_k\in\mathcal{T}(\Sigma)`$. We abbreviate nullary terms of the form $`s()`$ as $`s`$. The *size* of a term $`\mathsf{size}(t)`$ is defined in the usual way (as the number of constructors in the term). We use $`\mathsf{subterms}(t)`$ to denote the set of all subterms of $`t`$ (including $`t`$ itself). We assume that $`\Sigma`$ contains a dedicated *variadic* tuple constructor, written $`\langle t_1, \ldots, t_n \rangle`$, which we use to represent a corpus of programs as a single term ($`\langle \rangle`$ does not contribute to the size of a term).

***Patterns.*** If $`\mathcal{X}`$ is a denumerable set of variables, $`\mathcal{T}(\Sigma,\mathcal{X})`$ is a set of *patterns*, *i.e.* terms that can contain variables from $`\mathcal{X}`$. A pattern is *linear* if each of its variables occurs only once: $`\forall X \in \mathsf{vars}(p) . \mathsf{occurs}(X, p) = 1`$. A *substitution* $`\sigma = [{X_1} \mapsto {p_1}, \ldots, {X_n} \mapsto {p_n}]`$ is a mapping from variables to patterns. We write $`{\sigma}({p})`$ to denote the application of $`\sigma`$ to pattern $`p`$, which is defined in the standard way. We define the size of a substitution $`\mathsf{size}(\sigma)`$ as the total size of its right-hand sides.

A pattern $`p`$ is more general than (or *matches*) $`p'`$, written $`p' \sqsubseteq p`$, if there exists $`\sigma`$ such that $`p' = {\sigma}({p})`$; we will denote such a $`\sigma`$ by $`\mathsf{match}(p',p)`$. For example $`X + 1 \sqsubseteq X + Y`$ with $`\mathsf{match}(X + 1,X + Y) = [{Y} \mapsto {1}]`$. The relation $`\sqsubseteq`$ is a partial order on patterns, and induces an equivalence relation $`p_1 \sim p_2 \triangleq p_1 \sqsubseteq p_2 \wedge p_2 \sqsubseteq p_1`$ (equivalence up to variable renaming). In the following, we always distinguish patterns only up to this equivalence relation.

The *join* of two patterns $`p_1 \sqcup p_2`$—also called their *anti-unifier*—is the least general pattern that matches both $`p_1`$ and $`p_2`$; the join is unique up to $`\sim`$. Note that $`\langle \mathcal{T}(\Sigma,\mathcal{X}), \sqsubseteq, \sqcup, \top = X \rangle`$ is a join semi-lattice (part of Plotkin’s *subsumption lattice* ). Consequently, the join can be generalized to an arbitrary set of patterns.

A *context* $`\mathcal{C}`$ is a pattern with a single occurrence of a distinguished variable $`\circ`$. We write $`\mathcal{C}[p]`$—$`p`$ in context $`\mathcal{C}`$—as a syntactic sugar for $`{[{\circ} \mapsto {p}]}({\mathcal{C}})`$. A *rewrite rule* $`R`$ is a pair of patterns, written $`p_1 \Rightarrow p_2`$. Applying a rewrite rule $`R`$ to a term or pattern $`p`$, written $`{R}({p})`$ is defined in the standard way: $`{R}({p}) = {(\mathsf{match}(p,p_1))}({p_2})`$ if $`p \sqsubseteq p_1`$ and undefined otherwise. A pattern $`p`$ can be *re-written in one step* into $`q`$ using a rule $`R`$, written $`p \rightarrow^{R}_1 q`$, if there exists a context $`\mathcal{C}`$ such that $`p = \mathcal{C}[p']`$ and $`q = \mathcal{C}[{R}({p'})]`$. The reflexive-transitive closure of this relation is the *rewrite relation* $`\rightarrow^{\mathcal{R}}`$, where $`\mathcal{R}`$ is a set of rewrite rules.

***Compressed Terms.*** Compressed terms $`\hat{\mathcal{T}}(\Sigma,\mathcal{X})`$ are of the form:
``` math
\hat{t} ::= X   \mid   s(\hat{t}_1,\ldots,\hat{t}_k)     \mid (\lambda X_1 \ldots X_n \ \mathbf{\shortrightarrow}\ \hat{t})\ \hat{t}_1\ \ldots\ \hat{t}_n
```
In other words, compressed terms may contain applications of a $`\lambda`$-abstraction with zero or more binders to the same number of arguments. Note that this is a first-order language in the sense that all abstractions are fully applied. Importantly, we define $`\mathsf{size}(\hat{t})`$ in such a way that multiple occurrences of a $`\lambda`$-abstraction are *only counted once*. For simplicity of accounting, the size of an application $`(\lambda \overline{X} \ \mathbf{\shortrightarrow}\ \hat{t}_1)\ \overline{\hat{t}_2}`$ is defined as $`\mathsf{size}(\hat{t}_1) + \sum{\overline{\mathsf{size}(\hat{t}_2)}}`$, that is, abstraction nodes themselves do not add to the size.[^4]

*Beta-reduction* on compressed terms, denoted $`\hat{t}_1 \rightarrow^{\beta}_1\hat{t}_2`$, is defined in the usual way:
``` math
(\lambda \overline{X} \ \mathbf{\shortrightarrow}\ \hat{t}_1)\ \overline{\hat{t}_2}  \rightarrow^{\beta}_1{[\overline{X \mapsto \hat{t}_2}]}({\hat{t}_1})
```
where substitution on compressed terms is the standard capture-avoiding substitution for $`\lambda`$-calculus. Note that because our language is first-order and has no built-in recursion, it is strongly normalizing (the proof of this statement, as well as other proofs omitted from this section, can be found in the supplementary material). Hence, the order of $`\beta`$-reductions is irrelevant, and without loss of generality we can define *evaluation* on compressed terms, $`\hat{t}_1 \rightarrow^{\beta}\hat{t}_2`$, to follow applicative order, *i.e.* innermost $`\beta`$-redexes are reduced first. As a result, any application reduced during evaluation has the form $`(\lambda \overline{X} \ \mathbf{\shortrightarrow}\ p_1)\ \overline{p_2}`$, that is, neither the body $`p_1`$ nor the actual arguments $`\overline{p_2}`$ contain any redexes (and hence any $`\lambda`$-abstractions). This simplifies several aspects of our formalization; for example, there is no need for $`\alpha`$-renaming, since with no binders in $`p_1`$, no variable capture can occur.

***Problem Statement.*** We can now formalize the *library learning problem* as follows: given a term $`t \in \mathcal{T}(\Sigma)`$, the goal is to find the smallest compressed term $`\hat{t} \in \hat{\mathcal{T}}(\Sigma,\mathcal{X})`$ that evaluates to $`t`$ (*i.e.*$`\hat{t} \rightarrow^{\beta}t`$). The reason such $`\hat{t}`$ may be smaller than $`t`$, is that it may contain multiple occurrences of the same $`\lambda`$-abstraction (applied to different arguments), whose size is only counted once. An example is shown in <a href="#fig:lib-learning-example" data-reference-type="ref+label" data-reference="fig:lib-learning-example">6</a>.

Although in full generality the solution might include nested lambdas with free variables (defined in the outer lambdas), in the rest of the paper we restrict our attention to *global library learning*, where all lambdas are closed terms. This is motivated by the purpose of library learning to discover reusable abstraction for a given problem domain. The solution in <a href="#fig:lib-learning-example" data-reference-type="ref+label" data-reference="fig:lib-learning-example">6</a> already has this form.

<figure id="fig:lib-learning-example">
<div class="minipage">
<p><span class="math display">$$\begin{align*}
      \langle &amp;f(g(a) + g(a)) + (g(1) + h(2))\\
      ,\ &amp;f(g(b) + g(b)) + (g(3) + h(4))\\
      ,\ &amp;g(5) + h(6) \rangle
\end{align*}$$</span></p>
</div>
<div class="minipage">
<p><span class="math display">$$\begin{align*}
      &amp;\langle \hat{f}_2\ g(a)\ 1\ 2, \hat{f}_2\ g(b)\ 2\ 3, \hat{f}_1\ 5\ 6\rangle\quad \text{where}\\
      &amp;\hat{f}_1 = \lambda Y\ Z \ \mathbf{\shortrightarrow}\ g(Y) + h(Z)\\
      &amp;\hat{f}_2 = \lambda X\ Y\ Z \ \mathbf{\shortrightarrow}\ f(X + X) + \hat{f}_1\ Y\ Z
\end{align*}$$</span></p>
</div>
<figcaption>Library learning. Left: initial term (size 29). Right: an optimal solution with two abstractions, one of which uses the other (size 26). A solution with <span class="math inline">$\hat{f}_2 = \lambda X\ Y\ Z \ \mathbf{\shortrightarrow}\ f(g(X) + g(X)) + \hat{f}_1\ Y\ Z$</span> also has size 26.</figcaption>
</figure>

## Pattern-Based Library Learning

At a high-level, our approach to library learning is to use *patterns* that occur in the original corpus as candidate bodies for $`\lambda`$-abstractions in the compressed corpus. Looking at the example in <a href="#fig:lib-learning-example" data-reference-type="ref+label" data-reference="fig:lib-learning-example">6</a>, it is not immediately obvious that using just the patterns from the original corpus is sufficient, since the body of $`f_2`$ contains an application of $`f_1`$. Perhaps surprisingly, this is not an issue: the key idea is that we can compress $`t`$ into $`\hat{t}`$ by inverting the evaluation $`\hat{t} \rightarrow^{\beta}t`$, and because the evaluation order is applicative, the rewritten sub-term at every step will not contain any $`\beta`$-redexes.

***Compression.*** More formally, given a pattern $`p`$, let us define its *compression rule* (or $`\kappa`$-rule for short) as the rewrite rule
``` math
\kappa(p) \; \triangleq \; p \Rightarrow (\lambda \overline{X} \ \mathbf{\shortrightarrow}\ p)\ \overline{X} \quad \text{where}\quad \overline{X} = \mathsf{vars}(p)
```
In other words, $`\kappa(p)`$ will replace any term matching $`p`$ with an application of a function whose body is *exactly* $`p`$. For example, if $`p = g(Y) + h(Z)`$, its $`\kappa`$-rule is $`g(Y) + h(Z) \Rightarrow (\lambda Y\ Z \ \mathbf{\shortrightarrow}\ g(Y) + h(Z))\ Y\ Z`$. Note that on the right-hand side of this rule only the *free* occurrences of $`Y`$ and $`Z`$ will be substituted during rewriting; the bound $`Y`$ and $`Z`$ will be left unchanged, following the usual semantics of substitution for $`\lambda`$-calculus. For example, this rule can rewrite the third term in <a href="#fig:lib-learning-example" data-reference-type="ref+label" data-reference="fig:lib-learning-example">6</a> (left) as follows:
``` math
g(5) + h(6) \;\rightarrow^{\kappa(g(Y) + h(Z))}_1\; (\lambda Y\ Z \ \mathbf{\shortrightarrow}\ g(Y) + h(Z))\ 5\ 6
```
A sequence of $`\kappa`$-rewrites $`t \rightarrow^{\kappa(p_1)}_1 \dots \rightarrow^{\kappa(p_n)}_1 \hat{t}`$, where all $`p_i \in \mathcal{P}`$, is called a *compression* of $`t`$ into $`\hat{t}`$ using patterns $`\mathcal{P}`$ and written $`t \rightarrow^{\kappa(\mathcal{P})} \hat{t}`$. We can now show that the library learning problem is equivalent to finding the smallest compression of $`t`$ using only patterns that occur in $`t`$.

<div class="theorem">

For any term $`t \in \mathcal{T}(\Sigma)`$ and compressed term $`\hat{t} \in \hat{\mathcal{T}}(\Sigma,\mathcal{X})`$:

<div class="description">

If $`t`$ compresses into $`\hat{t}`$, then $`\hat{t}`$ evaluates to $`t`$: $`\forall \mathcal{P}. t \rightarrow^{\kappa(\mathcal{P})} \hat{t} \Longrightarrow \hat{t} \rightarrow^{\beta}t`$.

If $`\hat{t}`$ is a solution to the (global) library learning problem, then $`t`$ compresses into $`\hat{t}`$ using only patterns that have a match in $`t`$: $`\hat{t} \in \mathop{\mathrm{arg\,min}}_{\hat{t}' \rightarrow^{\beta}t} \mathsf{size}(\hat{t}') \Longrightarrow t \rightarrow^{\kappa(\mathcal{P})} \hat{t}`$, where $`\mathcal{P}= \{p \in \mathcal{T}(\Sigma,\mathcal{X}) \mid t' \in \mathsf{subterms}(t) , t' \sqsubseteq p\}`$.

</div>

<span id="thm:pat-lib-learning" data-label="thm:pat-lib-learning"></span>

</div>

The proof can be found in the supplementary material.

***Example.*** Consider once again the library learning problem in <a href="#fig:lib-learning-example" data-reference-type="ref+label" data-reference="fig:lib-learning-example">6</a>. Here the set of patterns used to compress the original corpus into the solution on the right is:
``` math
p_1 = g(Y) + h(Z)\quad\quad\quad
  p_2 = f(X + X) + g(Y) + h(Z)
```
Rewriting the first term of the corpus proceeds in two steps (the redexes of $`\kappa`$-steps are highlighted):
``` math
\begin{multline*}
  \textcolor{darkblue}{f(g(a) + g(a)) + (g(1) + h(2))}    \;\rightarrow^{\kappa(p_2)}_1\\     
  (\lambda X\ Y\ Z \ \mathbf{\shortrightarrow}\ f(X + X) + \textcolor{darkblue}{g(Y) + h(Z)})\ g(a)\ g(a)\ (g(1) + h(2))\;\rightarrow^{\kappa(p_1)}_1\\ 
  (\lambda X\ Y\ Z\ \ \mathbf{\shortrightarrow}\ f(X + X) + (\lambda Y\ Z \ \mathbf{\shortrightarrow}\ g(Y) + h(Z))\ Y\ Z)\ g(a)\ g(a)\ (g(1) + h(2))
\end{multline*}
```
In other words, we first rewrite the entire term using $`p_2`$, and then rewrite inside the body of the introduced abstraction using $`p_1`$ (note that this order of compression is the inverse of the applicative evaluation order). The second term of the corpus compresses analogously; the third term compresses in a single step using $`p_1`$. Although this is not obvious from the rewrite sequence above, the resulting compressed corpus is indeed smaller than the original thanks to sharing of both $`\lambda`$-abstractions, as illustrated on the right of <a href="#fig:lib-learning-example" data-reference-type="ref+label" data-reference="fig:lib-learning-example">6</a>.

***Library Learning as Term Rewriting.*** Theorem <a href="#thm:pat-lib-learning" data-reference-type="ref" data-reference="thm:pat-lib-learning">[thm:pat-lib-learning]</a> reduces library learning to a *term rewriting* problem. Namely, given a term $`t`$ and a finite set of rewrite rules $`\mathcal{R}= \{\kappa(p) \mid  t' \in \mathsf{subterms}(t) , t' \sqsubseteq p\}`$, our goal is to find a minimal-size term $`\hat{t}`$ such that $`t \rightarrow^{\mathcal{R}} \hat{t}`$, which is a standard formulation in term rewriting. Unfortunately, this particular problem is notoriously difficult because (a) the rule set $`\mathcal{R}`$ is very large for any non-trivial term $`t`$, and (b) our $`\mathsf{size}`$ function is non-local (it takes sharing into account) In the rest of this section we discuss how we can prune the rule set $`\mathcal{R}`$ to reduce it to a tractable size. <a href="#sec:beam" data-reference-type="ref+label" data-reference="sec:beam">5</a> discusses how we tackle the remaining term rewriting problem using the *equality saturation* technique .

## Pruning Candidate Patterns

In this section, we discuss which patterns can be discarded from consideration when constructing the set of $`\kappa`$-rules $`\mathcal{R}`$ for the term rewriting problem.

***Cost of a Pattern.*** Consider a compression $`t \rightarrow^{\kappa(\mathcal{P})} \hat{t}`$ where each pattern $`p \in \mathcal{P}`$ is used some number $`n`$ times, with substitutions $`\sigma^p_1, \ldots, \sigma^p_n`$. We can break down the total amount of compression into contributions of individual patterns:
``` math
\mathsf{size}(\hat{t}) - \mathsf{size}(t) = \sum_{p \in \mathcal{P}} \mathsf{cost}(p, \{\sigma^p_1, \dots \sigma^p_n\})
```
The cost of a pattern $`p`$, in turn, consists of three components. The cost of *introducing* the abstraction is the size of its body, *i.e.*$`\mathsf{size}(p)`$. The cost of using an abstraction—$`\textsf{use}(p, \sigma)`$ <a href="#eq:use" data-reference-type="eqref" data-reference="eq:use">[eq:use]</a>—includes the application itself and the size of the arguments. The cost saved by using an abstraction—$`\textsf{save}(p, \sigma)`$ <a href="#eq:save" data-reference-type="eqref" data-reference="eq:save">[eq:save]</a>—is just the cost of the term matched by $`p`$ (*i.e.* the redex of the corresponding $`\kappa`$-step).
``` math
\begin{align}
\textsf{use}(p, \sigma) &= 1 + \sum_{X \in \mathsf{vars}(p)} \mathsf{size}(\sigma(X)) \label{eq:use} \\
  \textsf{save}(p, \sigma) &= \mathsf{size}({\sigma}({p})) = 
  \mathsf{size}(p) + \sum_{X \in \mathsf{vars}(p)} \mathsf{occurs}(X, p) \cdot (\mathsf{size}(\sigma(X)) - 1)\label{eq:save}
\end{align}
```
The total cost of $`p`$ is the cost of introducing the abstraction paid a single time, plus the cost of each use, minus what you save for each application:
``` math
\begin{equation}
  \textsf{cost}(p, \{\sigma_1,\ldots,\sigma_n\}) 
  = \mathsf{size}(p) + \sum_{\sigma_i} (\textsf{use}(p, \sigma_i) - \textsf{save}(p, \sigma_i))
\end{equation}
```
When $`p`$ is linear (all $`\mathsf{occurs}(X, p) = 1`$), the cost depends only on $`n`$ but not on the substitutions $`\sigma_i`$:
``` math
\begin{align}
  \textsf{cost}(p, \{\sigma_1,\ldots,\sigma_n\}) 
  &= \mathsf{size}(p) + \sum_{\sigma_i} \left(
    1 - \mathsf{size}(p) + |\mathsf{vars}(p)|
  \right) \\
  &= \mathsf{size}(p) + n \cdot \left(
    1 - \mathsf{size}(p) + |\mathsf{vars}(p)|
  \right)
\end{align}
```
We can show that a pattern $`p`$ with a *non-negative* cost can be safely discarded, that is: there exists another compression using only $`\mathcal{P}\setminus \{p\}`$, whose result is at least as small.

***Trivial Patterns.*** Based on this analysis, any linear pattern $`p`$ with $`\mathsf{skeleton}(p) \leq 1`$ can be discarded, where $`\mathsf{skeleton}(p) = \mathsf{size}(p) - |\mathsf{vars}(p)|`$ is the size of $`p`$’s “skeleton”, *i.e.* it’s body without the variables. Intuitively, the skeleton of $`p`$ is simply too small to pay for introducing an application. In this case, $`\mathsf{cost}(p,\_) > 0`$ *independently* of how many times it is used. We refer to such patterns as *trivial*. Examples of trivial patterns are $`X`$ and $`X + Y`$.

***Patterns with a Single Match.*** We can show that patterns with only a single match in the corpus can also be discarded. If $`p`$ has a single match in $`t`$, then it can appear *at most once* in any compression of $`t`$. If $`p`$ is linear, $`\mathsf{cost}(p, \_) = 1 + |\mathsf{vars}(p)|`$, which is always positive, so $`p`$ can be discarded. But what about non-linear patterns, where even a single $`\kappa`$-step can decrease size thanks to variable reuse? It turns out that any non-linear pattern with a single match can always be replaced by a nullary pattern (with no variables) that is more optimal.

Without loss of generality, assume that $`p`$ has a single variable $`X`$ that occurs $`m > 1`$ times, and let its sole $`\kappa`$-step be $`{\sigma}({p}) \rightarrow^{\kappa(p)}_1  (\lambda X \ \mathbf{\shortrightarrow}\ p)\  {\sigma}({X})`$. The size of the right-hand side is $`\mathsf{size}(p) + 1 + \mathsf{size}({\sigma}({X}))`$, or, rewritten in terms of $`p`$’s skeleton: $`1 + (\mathsf{skeleton}(p) + m) + \mathsf{size}({\sigma}({X}))`$. Instead, we can rewrite the same redex $`{\sigma}({p}) \rightarrow^{\{R\}} p'`$ using $`m`$ applications of the rule $`R \;\triangleq\; {\sigma}({X}) \Rightarrow (\lambda \epsilon \ \mathbf{\shortrightarrow}\ {\sigma}({X}))\ \epsilon`$. This is a $`\kappa`$-rule for a *nullary* pattern $`{\sigma}({X})`$ with no variables (hence the corresponding $`\lambda`$-abstraction has zero binders). The size of $`p'`$ obtained in this way is $`\mathsf{size}({\sigma}({X})) + m + \mathsf{skeleton}(p)`$ (where the former is the size of the shared $`\lambda`$-abstraction, $`m`$ is the number of applications, and $`\mathsf{skeleton}(p)`$ is the size of the term around the applications). As you can see, this term is one smaller than the one we get by applying $`p`$. Intuitively, this result says that instead of using a non-linear pattern that occurs only once, it is better to perform common sub-expression elimination.

***Parameterization Lattice.*** Eliminating from consideration all patterns with fewer than two matches in the corpus suggests an algorithm for generating a complete set $`\mathcal{P}`$ of candidate patterns: (1) start from the set $`\mathcal{P}^2(t) = \{t_1 \sqcup t_2 \mid t_i \in \mathsf{subterms}(t)\}`$ of all pairwise joins of subterms of the input program, (2) explore all elements of the subsumption semi-lattice above those patterns, by gradually replacing sub-patterns with variables, until we hit trivial patterns at the top of the lattice. We will refer to this semi-lattice above $`\mathcal{P}^2(t)`$ as the *parametrization lattice* of $`t`$, denoted $`\mathcal{P}(t)`$. A fragment of $`\mathcal{P}(t)`$ for $`t = \langle f(a+b), f(a+c), f(b+c)\rangle`$ is shown in <a href="#fig:lattice" data-reference-type="ref+label" data-reference="fig:lattice">7</a> (left).

<figure id="fig:lattice">
<div class="minipage">
<embed src="figures/lattice-1.pdf" />
</div>
<div class="minipage">
<embed src="figures/lattice-2.pdf" />
</div>
<figcaption>Left: fragment of the parametrization lattice for the term <span class="math inline"><em>t</em> = ⟨<em>f</em>(<em>a</em> + <em>b</em>), <em>f</em>(<em>a</em> + <em>c</em>), <em>f</em>(<em>b</em> + <em>c</em>)⟩</span>; only filled black circles correspond to candidate patterns: hollow circles match fewer than two terms and gray circles are trivial. Right: an example where is it insufficient to consider pairwise joins to obtain an optimal pattern.</figcaption>
</figure>

***Approximation.*** In practice, computing the set $`\mathcal{P}^2(t)`$ is feasible: although there are quadratically many pairs of subterms, most of them do not have a common constructor at the root, and hence their join is trivially $`X`$. An example is the join of $`t`$ with any of its subterms in <a href="#fig:lattice" data-reference-type="ref+label" data-reference="fig:lattice">7</a> (left). Unfortunately, generalizing the patterns from $`\mathcal{P}^2(t)`$ according to the parameterization lattice (<a href="#fig:lattice" data-reference-type="ref+label" data-reference="fig:lattice">7</a>) is expensive. For this reason, <span class="smallcaps">babble</span> adopts an approximation and simply uses $`\mathcal{P}^2(t)`$ as the set of candidates.

This approximation makes our pattern generation theoretically incomplete. Consider a pattern $`p \in \mathcal{P}(t)\setminus \mathcal{P}^2(t)`$; there are two reasons why we might need $`p`$ in the optimal compression of $`t`$:

1.  there is *no* $`p' \in \mathcal{P}^2(t)`$ with the same set of matches as $`p`$, or

2.  there is such a $`p'`$ but it has *few enough matches* that its larger size does not pay off.

The first kind of incompleteness occurs when $`p`$ matches a set of subterms $`t_1, \ldots, t_n`$ ($`n > 2`$), whose join is distinct from all their pairwise joins (otherwise some $`t_i \sqcup t_j \in \mathcal{P}^2(t)`$ would also match all $`t_1, \ldots, t_n`$). An example is shown in <a href="#fig:lattice" data-reference-type="ref+label" data-reference="fig:lattice">7</a> (right), where the three subterms in question are $`f(a+a)`$, $`f(a+c)`$, and $`f(c+c)`$. In this case, an optimal compression might use the pattern $`f(X+Y)`$ to rewrite all three subterms, but our approximation would only include the patterns $`f(a+X)`$, $`f(X+X)`$, and $`f(X+c)`$, each of which can rewrite only two of the three subterms.

The second kind of incompleteness occurs when there exists $`p' \in \mathcal{P}^2(t)`$ that has the same set of matches as $`p`$, despite being strictly more specific, and yet using $`p'`$ instead of $`p`$ still doe not pay off. The understand when this happens, consider the difference in costs between $`p`$ and $`p'`$, assuming that they are both used to rewrite the same $`n`$ subterms (*i.e.* their <span class="sans-serif">save</span> cost is the same):
``` math
\begin{align*}
  \mathsf{cost}(p', \overline{\sigma'}) - \mathsf{cost}(p, \overline{\sigma}) &= \mathsf{size}(p') - \mathsf{size}(p) + \sum_i (\mathsf{use}(p', \sigma'_i) - \mathsf{use}(p, \sigma_i))\\
  &= \mathsf{size}(p') - \mathsf{size}(p) + \sum_i (\mathsf{size}(\sigma'_i) - \mathsf{size}(\sigma_i))
\end{align*}
```
Because $`p'`$ is strictly more specific than $`p`$, we know that $`\mathsf{size}(p') \geq \mathsf{size}(p)`$, but all its substitutions $`\sigma'_i`$ must be strictly smaller than $`\sigma_i`$. Hence, with enough uses, $`p'`$ is bound to become more compressive than $`p`$; when there are just a few uses, however, $`p`$ can be more optimal. For example, consider the corpus $`\langle \mathcal{C}[f(1,2,3)],  \mathcal{C}[f(4,5,6)]\rangle`$, where $`\mathcal{C}`$ is some sufficiently large context. Here, a more general pattern $`p = \mathcal{C}[X]`$ is more optimal than the more specific $`p' = \mathcal{C}[f(X,Y,Z)]`$, because $`\mathsf{size}(p') - \mathsf{size}(p) = 3`$, each use of $`p'`$ is only one node cheaper, and there are only two uses.

Despite the lack of theoretical completeness guarantees, we argue that restricting candidate patterns to $`\mathcal{P}^2(t)`$ is a reasonable trade-off. Note, that the counter-examples above are quite contrived, and they no longer apply once the corpus contains sufficiently many and sufficiently diverse instances of a pattern (for example, adding $`f(b,b)`$ to the first corpus would make $`f(X,Y)`$ appear in $`\mathcal{P}^2(t)`$, and adding just one more occurrence of $`p'`$ into the second corpus would make it as optimal as $`p`$). Our empirical evaluation confirms that this approximation works well in practice.

# Library Learning modulo Equational Theory

<figure id="fig:syntax">
<div class="minipage">
<p><strong>Syntax</strong> <span class="math display">$$\begin{array}{rll}
      \text{e-class ids} &amp; a,b &amp;\in \mathcal{I} \\
      \text{e-nodes}     &amp; n \ensuremath{\mathrel{\mathord{:}\mathord{:=}}}s(a_1, \ldots, a_k)  &amp;\in N\\
      \text{e-classes}   &amp; c \ensuremath{\mathrel{\mathord{:}\mathord{:=}}}\{n_1, \ldots, n_m\} &amp;\in C     
    \end{array}$$</span></p>
</div>
<div class="minipage">
<p><strong>Denotation</strong> <span class="math inline">⟦⋅⟧: <em>N</em> → 2<sup>𝒯(<em>Σ</em>)</sup></span>, <span class="math inline">⟦⋅⟧: <em>C</em> → 2<sup>𝒯(<em>Σ</em>)</sup></span> <span class="math display">$$\begin{array}{rl}
      \\
      \llbracket s(a_1, \ldots, a_k) \rrbracket &amp;= \{s(t_1, \ldots, t_k) \mid t_i \in \llbracket M(a_i) \rrbracket\}\\
      \llbracket \{n_1, \ldots, n_m\} \rrbracket &amp;= \bigcup_{i \in [1,m]} \llbracket n_i \rrbracket
    \end{array}$$</span></p>
</div>
<figcaption>Syntax, metavariables, and denotation for the components of an e-graph. Here <span class="math inline"><em>s</em> ∈ <em>Σ</em></span> and <span class="math inline"><em>k</em> = arity(<em>s</em>)</span>.</figcaption>
</figure>

***E-Graphs.*** Let $`\mathcal{I}`$ be a denumerable set of *e-class ids*. An *e-graph* $`\mathcal{G}`$ is a triple $`\langle C, M, r\rangle`$, where $`C`$ is a set of *e-classes*, $`M\colon \mathcal{I} \to C`$ is an *e-class map*. and $`r\in \mathcal{I}`$ is the root class id. An *e-class* $`c \in C`$ is a set of *e-nodes* $`n \in N`$, and an e-node is a constructor applied to e-class ids. The syntax of e-classes and e-nodes is summarized in <a href="#fig:syntax" data-reference-type="ref+label" data-reference="fig:syntax">8</a> (left). An e-graph has to satisfy the *congruence invariant*, which states that the e-graph has no two identical e-nodes (or alternatively, that all e-classes are disjoint).[^5]

The *denotation* of an *e-graph*—the set of terms it represents—is the denotation of its root e-class $`\llbracket M(r) \rrbracket`$, where the denotation of e-classes and e-nodes is defined mutually-recursively in <a href="#fig:syntax" data-reference-type="ref+label" data-reference="fig:syntax">8</a> (right). Note that the denotation can be infinite if the e-graph has cycles. An e-graph induces an equivalence relation $`\equiv^{\mathcal{G}}`$, where $`t_1 \equiv^{\mathcal{G}}t_2`$ iff there exists an e-class $`c \in C`$ such that $`t_1 \in \llbracket c \rrbracket \wedge t_2\in \llbracket c \rrbracket`$.

E-graphs provide means to *extract* the cheapest term from an e-class according to some cost function: $`\mathsf{extract}_{\mathsf{cost}}(a) = \mathop{\mathrm{arg\,min}}_{t\in \llbracket M(a) \rrbracket} \mathsf{cost}(t)`$. If $`\mathsf{cost}`$ is *local*, meaning that the cost of a term can be computed from the costs of its immediate children, extraction can be done efficiently by a greedy algorithm, which recursively extracts the best term from each e-class.

***E-Matching.*** E-matching is a generalization of pattern matching to e-graphs, where matching an e-class $`c`$ against a pattern $`p`$ yields a set of *e-class substitutions* $`\theta\colon \mathcal{X}\to \mathcal{I}`$ such that $`{\theta}({p})`$ is a “subgraph” of $`c`$. To formalize this notion, we introduce *partial terms* $`\pi \in \mathcal{T}(\Sigma,\mathcal{I})`$, which are terms whose leaves can be e-class ids (or, alternatively, patterns with e-class ids for variables). The containment relation $`{\pi} \prec {a}`$ for some e-class id $`a`$ is defined as follows:
``` math
{a} \prec {a} \quad\quad\quad
{s(\pi_1, \ldots, \pi_k)} \prec {a}\ \text{iff}\ s(a_1, \ldots, a_k) \in M(a) \wedge {\pi_i} \prec {a_i}
```
With this definition, a pattern $`p`$ matches an e-class $`a`$, $`a \sqsubseteq p`$, if there exists an e-class substitution $`\theta`$, such that $`{{\theta}({p})} \prec {a}`$. We denote the set of such substitutions as $`\mathsf{matches}(a,p)`$.

***Rewriting and Equality Saturation.*** Equality saturation (EqSat)  takes as input a term $`t`$ and a set of equations that induce an equivalence relation $`\equiv`$, and produces an e-graph $`\mathcal{G}`$ such that $`\llbracket \mathcal{G} \rrbracket = \{t' \mid t \equiv t'\}`$ and $`t \equiv t'`$ iff $`t \equiv^{\mathcal{G}}t'`$. The core idea of EqSat is to convert equations into rewrite rules and apply them to the e-graph in a non-destructive way: so that the original term and the rewritten terms are both represented in the same e-class. Applying a rewrite rule $`p_1 \Rightarrow p_2`$ to an e-class $`a`$ works as follows: for each $`\theta \in \mathsf{matches}(a,p_1)`$, we obtain the rewritten partial term $`\pi' = {\theta}({p_2})`$ and then add this partial term to the same e-class $`a`$, restoring the congruence invariant (*i.e.* merging e-classes that now have identical e-nodes).

## Top-Level Algorithm

<figure id="fig:algo-llmt">
<div class="sourceCode" id="cb1" data-commentstyle="\small\ttfamily\textcolor{gray}" data-basicstyle="\small\ttfamily" data-xleftmargin="2.5em" data-numbers="left"><pre class="sourceCode numberSource numberLines"><code class="sourceCode"><span id="cb1-1"><a href="#cb1-1"></a># Original term $t$, set of equational rewrite rules $\ruleset_\semeq$, maximum library size $N$</span>
<span id="cb1-2"><a href="#cb1-2"></a>def LLMT($t$, $R_\semeq$, $N$):</span>
<span id="cb1-3"><a href="#cb1-3"></a>    # EqSat phase:</span>
<span id="cb1-4"><a href="#cb1-4"></a>    $\mathcal{G}$ = egraph($t$)                            # initialize with a single term $t$</span>
<span id="cb1-5"><a href="#cb1-5"></a>    $\mathcal{G}$ = eqSat($\mathcal{G}, \ruleset_\semeq$)  # $\mathcal{G}$ represents all terms that are $\semeq t$</span>
<span id="cb1-6"><a href="#cb1-6"></a></span>
<span id="cb1-7"><a href="#cb1-7"></a>    # candidate generation phase:</span>
<span id="cb1-8"><a href="#cb1-8"></a>    $\patset$ = AU($\mathcal{G}$)                          # generate candidate patterns by anti-unification</span>
<span id="cb1-9"><a href="#cb1-9"></a>    $\ruleset_\kappa$ = $\{\kappa(p) \mid p \in \patset\}$ # construct a compression rule from every pattern</span>
<span id="cb1-10"><a href="#cb1-10"></a>    $\mathcal{G}&#39;$ = eqSat($\mathcal{G}, \ruleset_\kappa$) # $\mathcal{G}&#39;$ represents all ways to compress $\mathcal{G}$</span>
<span id="cb1-11"><a href="#cb1-11"></a></span>
<span id="cb1-12"><a href="#cb1-12"></a>    # candidate selection phase:</span>
<span id="cb1-13"><a href="#cb1-13"></a>    $\ruleset&#39;$ = select_library($\mathcal{G}&#39;, N$)        # select the best $N$ rules from $\ruleset_\kappa$ using beam search</span>
<span id="cb1-14"><a href="#cb1-14"></a>    $\mathcal{G}&#39;&#39;$  = eqSat($\mathcal{G}, R&#39;$)            # $\mathcal{G}&#39;&#39;$ represents all ways to compress $\mathcal{G}$ using the optimal library          </span>
<span id="cb1-15"><a href="#cb1-15"></a>    return extract($\mathcal{G}&#39;&#39;$)                        # extract the smallest compressed term from $\mathcal{G}&#39;&#39;$</span></code></pre></div>
<figcaption>The top-level LLMT algorithm.</figcaption>
</figure>

We can formalize the problem of *library learning modulo equational theory* (LLMT) as follows: given a term $`t`$ and a set of equations that induce an equivalence relation $`\equiv`$, the goal is to find a compressed term $`\hat{t} \in \hat{\mathcal{T}}(\Sigma,\mathcal{X})`$, such that $`\hat{t} \rightarrow^{\beta}t' \equiv t`$ (for some $`t'`$), and $`\hat{t}`$ has a minimal size.

Our top-level algorithm `LLMT` is depicted in <a href="#fig:algo-llmt" data-reference-type="ref+label" data-reference="fig:algo-llmt">9</a>. This algorithm takes as input the original corpus $`t`$ and the equational theory, represented as a set of require rules $`\mathcal{R}_\equiv`$ (another input to the algorithm is the maximum size of the library; this parameter is introduced for the sake of efficiency, as we explain in <a href="#sec:beam" data-reference-type="ref+label" data-reference="sec:beam">5</a>). As the first step (lines 4–5), `LLMT` applies EqSat to obtain an e-graph $`\mathcal{G}`$ that represents all terms $`t'`$ such that $`t' \equiv t`$. This reduces the LLMT problem to library learning over an e-graph: *i.e.* the goal is to find a minimal-size compressed term $`\hat{t}`$, such that $`\hat{t} \rightarrow^{\beta}t'`$ for some $`t' \in \llbracket \mathcal{G} \rrbracket`$. Similarly to <a href="#sec:au" data-reference-type="ref+label" data-reference="sec:au">3</a>, we take a pattern-based approach to this problem, that is, we select a set $`\mathcal{P}`$ of *candidate patterns* and then perform compression rewrites using these patterns.

The rest of the algorithm is split into two phases: *candidate generation* and *candidate selection*. Candidate generation (lines 8–10) first computes the set of candidate patterns $`\mathcal{P}`$ using the anti-unification mechanism extended to e-graphs. Then it creates a compression rule ($`\kappa`$-rule, see <a href="#sec:au" data-reference-type="ref+label" data-reference="sec:au">3</a>) from each candidate pattern, and once again applies EqSat to obtain a new e-graph $`\mathcal{G}'`$. This new e-graph represents all possible ways to compress the terms from $`\mathcal{G}`$ using patterns in $`\mathcal{P}`$. Finally, the candidate selection phase (lines 13–15) selects the optimal subset of compression rules $`\mathcal{R}'`$, constructs an e-graph $`\mathcal{G}''`$ that represents all possible compressions using only the selected compression rules, and finally extracts the smallest compressed term from this e-graph.

The rest of this section focuses on the candidate generation via e-graph anti-unification (line 8). The candidate selection functions `select\_library` and `extract` are discussed in <a href="#sec:beam" data-reference-type="ref+label" data-reference="sec:beam">5</a>.

## Candidate Generation via E-Graph Anti-Unification

The goal of candidate generation is to find a set of patterns that are useful for compression. Following the discussion in <a href="#sec:au" data-reference-type="ref+label" data-reference="sec:au">3</a>, we restrict our attention to patterns $`\mathsf{AU}(t_1, t_2)`$, where $`t_1`$ and $`t_2`$ are subterms of some $`t \in \llbracket \mathcal{G} \rrbracket`$. The naïve approach is to enumerate all such $`t`$, and for each one, perform anti-unification on all pairs of subterms; this is suboptimal at best, and impossible at worst (when $`\llbracket \mathcal{G} \rrbracket`$ is infinite). Hence in this section we show how to compute a finite set of candidate patterns directly on the e-graph, without discarding any optimal patterns.

***E-Class Anti-Unification.*** Let us first consider anti-unification of two e-classes, $`\mathsf{AU}(a,b)`$, which takes as input e-class ids $`a`$ and $`b`$ and returns a set of patterns. We define $`\mathsf{AU}(a,b) = \mathsf{AU}(\epsilon \vdash a,b)`$, where $`\mathsf{AU}(\Gamma \vdash a,b)`$ is an auxiliary function that additionally takes into account a *context* $`\Gamma`$. A context is a list of pairs of e-classes that have been visited while computing the AU, and is required to prevent infinite recursion in case of cycles in the e-graph.

<figure id="fig:ecau">
<p><strong>E-node Anti-Unification</strong> <span class="math inline">AU(<em>Γ</em> ⊢ <em>n</em><sub>1</sub>, <em>n</em><sub>2</sub>)</span> <span class="math display">$$\begin{array}{rl}
    \mathsf{AU}(\Gamma, (a,b) \vdash s(a_1,\ldots,a_k),s(b_1,\ldots,b_k)) &amp;= \{s(p_1,\ldots,p_k) \mid p_i \in \mathsf{AU}(\Gamma \vdash a_i,b_i)\}\\
    \mathsf{AU}(\Gamma, (a,b) \vdash s_1(\ldots),s_2(\ldots)) &amp;= \{X_{a,b}\} \quad\text{if}\ s_1 \neq s_2\\
    \end{array}$$</span> <strong>E-class Anti-Unification</strong> <span class="math inline">AU(<em>Γ</em> ⊢ <em>a</em>, <em>b</em>)</span> <span class="math display">$$\begin{array}{rl}
    \mathsf{AU}(\Gamma \vdash a,b) &amp;= \emptyset \quad\text{if}\ (a,b) \in \Gamma\\
\mathsf{AU}(\Gamma \vdash a,b) &amp;= \textcolor{darkblue}{\mathsf{dominant}} \left(
       \bigcup_{n_a \in M(a), n_b \in M(b)} \mathsf{AU}(\Gamma, (a, b) \vdash n_a,n_b) 
    \right)
  \end{array}$$</span></p>
<figcaption>E-class anti-unification defined as two mutually-recursive functions of e-nodes and e-class ids.</figcaption>
</figure>

<a href="#fig:ecau" data-reference-type="ref+label" data-reference="fig:ecau">10</a> defines this operation using two mutually recursive functions that anti-unify e-classes and e-nodes. Note that e-node AU is always invoked in a non-empty context. The first equation anti-unifies two e-nodes with the same constructor: in this case, we recursively anti-unify their child e-classes and return the cross-product of the results. The second equation applies to e-nodes with different constructors: as in term AU, this results in a pattern variable. A nice side-effect of dealing with e-graphs is that we need not keep track of the anti-substitution to guarantee that each pair of subterms maps to the same variable: because any duplicate terms are represented by the same e-class, we can simply use the e-class ids $`a`$ and $`b`$ in the name of the pattern variable $`X_{a,b}`$.

The second block of equations defines anti-unification of e-classes (let us first ignore the <span style="color: darkblue">dominant</span> which will be explained shortly). The first equation applies when $`a`$ and $`b`$ have already been visited: in this case, we break the cycle and return the empty set. Otherwise, the last equation anti-unifies all pairs of e-nodes from the two e-classes in an updated context and merges the results. Note that this will add a pattern variable unless all e-nodes in both e-classes have the same constructor; we have omitted this detail in <a href="#sec:overview" data-reference-type="ref+label" data-reference="sec:overview">2</a> for simplicity, but this is implemented in <span class="smallcaps">babble</span> and often yields more optimal patterns. For example, consider anti-unifying $`c_1`$ and $`c_2`$ from <a href="#fig:egraph" data-reference-type="ref+label" data-reference="fig:egraph">4</a> (right): although they have the constructor `scale` in common, $`X`$ is actually a better pattern for abstracting these two e-classes than $`\mbox{\lstinline^scale^}\  X\ Y`$, because the total size of the actual arguments to pattern $`X`$ ($`\ensuremath{\mbox{\lstinline^side^}(6)}`$ and $`\ensuremath{\mbox{\lstinline^scale^}(\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(8)},\ 8,\ 2\pi/8)},\ 2)}`$) is the same as those to the pattern $`\mbox{\lstinline^scale^}\  X\ Y`$ ($`\ensuremath{\mbox{\lstinline^side^}(6)}`$, $`1`$, $`\ensuremath{\mbox{\lstinline^repRot^}(\ensuremath{\mbox{\lstinline^side^}(8)},\ 8,\ 2\pi/8)}`$, and $`2`$), and the pattern $`X`$ itself is smaller. This happens because the class $`c_1`$ represents several different terms, and the term “compatible with” $`X`$ in this case is smaller than the term “compatible wit” $`\mbox{\lstinline^scale^}\  X\ Y`$.

***Dominant Patterns.*** Recall that $`\mathsf{AU}(a,b)`$ produces patterns with variable names $`X_{a_i,b_i}`$, which record the e-class ids they abstract; let us refer to such a pattern $`p`$ as *uniquely matched* and define $`\theta_l(p) = \{\overline{X_{a_i,b_i} \mapsto a_i}\}`$ and $`\theta_r(p) = \{\overline{X_{a_i,b_i} \mapsto b_i}\}`$; these substitutions are necessarily among $`\mathsf{matches}(a,p)`$ and $`\mathsf{matches}(b,p)`$, respectively. Given two uniquely matched patterns $`p_1,p_2 \in \mathsf{AU}(a,b)`$, we say that $`p_1`$ *dominates* $`p_2`$ in the context of $`(a,b)`$ if (1) $`\mathsf{vars}(p_1) \subseteq \mathsf{vars}(p_2)`$, and (2) $`\mathsf{size}(p_1) \leq \mathsf{size}(p_2)`$. We can show that if $`p_1`$ dominates $`p_2`$, then we can safely discard $`p_2`$ from the set of candidate patterns. First, since $`p_1`$ is no larger than $`p_2`$, the definition of its $`\lambda`$-abstraction is also no larger. Second, given a term $`t_a\in \llbracket a \rrbracket`$, compressing this term using $`p_1`$ vs $`p_2`$, requires choosing actual arguments from $`\mathsf{range}(\theta_l(p_1))`$ vs $`\mathsf{range}(\theta_l(p_2))`$; because the former is a subset of the latter, the first application can always be made no larger (symmetric argument applies for $`t_b\in \llbracket b \rrbracket`$).

Hence it is sufficient that $`\mathsf{AU}(a,b)`$ only returns the set of *dominant patterns* (*i.e.* a pattern dominated by any pattern in the set can be discarded). This is what the function $`\textcolor{darkblue}{\mathsf{dominant}}`$ does in the last equation of <a href="#fig:ecau" data-reference-type="ref+label" data-reference="fig:ecau">10</a>. This pruning technique is especially helpful in the presence of equational theories. Suppose our theory contains the equation $`X + Y \equiv Y + X`$, and that the original term $`t`$ contains subterms $`1 + 2`$ and $`3 + 1`$. After saturation, the e-graph will represent $`1 + 2`$ and $`2 + 1`$ in some e-class $`a`$ and $`3 + 1`$ and $`1 + 3`$ in another e-class $`b`$; $`\mathsf{AU}(a,b)`$ will then produce both patterns $`X + 1`$ and $`1 + X`$, but it is clearly redundant to have both, since they match the same e-classes with the same substitutions $`\theta`$. Pruning of dominated patterns will eliminate one of them.

***Avoiding Cycles.*** Interestingly enough, the same notion of dominant patterns justifies why we need not follow cycles in the e-graph when computing $`\mathsf{AU}(a,b)`$, or, alternatively, why a finite set of candidate patterns is sufficient to compress any term in $`\llbracket \mathcal{G} \rrbracket`$, even if this set is infinite. Removing the first equation that short-circuits cycles can only lead to solutions $`p'`$ of the form
``` math
p' = {[X \mapsto p]}({q})
```
where $`p \in \mathsf{AU}(a,b)`$ is another solution, and $`q`$ is some context, added by the cycle. It is clear that any such $`p'`$ is dominated by $`p`$, and hence can be discarded.

***E-Graph Anti-Unification.*** The algorithm $`\mathsf{AU}(a,b)`$ computes a set of patterns that can be used to compress terms represented by the e-classes $`a`$ and $`b`$. Our ultimate goal, however, is to compute candidate patterns for abstracting *all subterms* of some $`t \in \llbracket \mathcal{G} \rrbracket`$. The most straightforward way to achieve this is to apply $`\mathsf{AU}(a,b)`$ to all pairs of e-classes in $`\mathcal{G}`$. We can do better, however: some pairs of e-classes need not be considered, because they cannot occur together in a single term $`t`$. For an example, consider the following e-graph, with $`\mathcal{I} = \mathbb{N}`$ and $`r = 0`$:
``` math
0 \mapsto \{f(1),g(2)\}\quad 1\mapsto\{g(3)\} \quad 2\mapsto \{f(3)\} \quad 3\mapsto \{a\}
```
This e-graph can result, for example, by rewriting a term $`f(g(a))`$ using an equation $`f(g(X)) \equiv g(f(X))`$. In this e-graph, the e-classes $`1`$ and $`2`$ (representing $`g(a)`$ and $`f(a)`$, respectively) clearly cannot *co-occur* in the same term: since the e-graph only represents two terms, $`f(g(a))`$ and $`g(f(a))`$.

To formalize this intuition, we define the co-occurrence relation between two e-class ids as follows. An e-class $`a`$ is a *sibling* of $`b`$ if there is an e-node that has both $`a`$ and $`b`$ as children. An e-class $`a`$ is an *ancestor* of $`b`$ if $`a = b`$ or $`b`$ is a child of some e-node $`n \in M(c)`$ and $`a`$ is an ancestor of $`c`$; $`a`$ is a *proper ancestor* of $`b`$ if $`a`$ is an ancestor of $`b`$ and $`a \neq b`$. Two e-classes $`a`$ and $`b`$ are *co-occurring* if (1) one of them is a proper ancestor of another, or (2) they have ancestors that are siblings.

Finally, to compute the set $`\mathsf{AU}(\mathcal{G})`$ of all candidate patterns for an e-graph $`\mathcal{G}`$, `LLMT` first computes the co-occurrence relation between all e-classes in $`\mathcal{G}`$, and then computes $`\mathsf{AU}(a,b)`$ of all pairs of e-classes that are co-occurring. As mentioned in <a href="#sec:overview" data-reference-type="ref+label" data-reference="sec:overview">2</a>, we use a dynamic programming algorithm that memoizes the results of $`\mathsf{AU}(a,b)`$ to avoid recomputation.

# Candidate Selection via E-Graph Extraction

After generating candidate abstractions, the `LLMT` algorithm invokes `select_library` to pick the subset of candidate patterns that can best be used to compress the input corpus. This section describes our approach to selecting the optimal library dubbed *targeted common subexpression elimination*.

***Library Selection as E-Graph Extraction.*** Recall that candidate selection starts with an e-graph $`\mathcal{G}'`$, which represents all the ways of compressing the initial corpus and its equivalent terms using the candidate patterns $`\mathcal{P}`$. We will refer to a subset $`\mathcal{L}\subset \mathcal{P}`$ as a *library*. The optimal size of an e-class $`c`$ compressed with $`\mathcal{L}`$ can be computed as the sum of the sizes of (1) the smallest term $`t\in \llbracket c \rrbracket`$ using only the library functions in $`\mathcal{L}`$ and where $`\lambda`$-abstractions do not count toward the size of $`t`$, and (2) the smallest version of each $`p \in \mathcal{L}`$. Note that the cost of defining an abstraction in $`\mathcal{L}`$ is only counted once, and that abstractions in $`\mathcal{L}`$ can be used to compress other abstractions in $`\mathcal{L}`$. Our goal is to find $`\mathcal{L}`$ such that the root e-class compressed with $`\mathcal{L}`$ has the smallest size.

Given a *particular* library, we can find the size of the smallest term via a relatively straightforward top-down traversal of the e-graph. Hence, a naïve approach to library selection would be to enumerate all subsets of $`\mathcal{P}`$ and pick the one that produces the smallest term at the root. Unfortunately, this approach becomes intractable as the size of $`\mathcal{P}`$ grows.

<figure id="fig:costset">
<p><strong>E-node cost set</strong> <span class="math inline">costset<sub><em>N</em></sub>(<em>n</em>)</span> <span class="math display">$$\begin{array}{rl}
    \mathsf{costset}_N(s()) &amp;= \{ (\emptyset, 1) \} \\
    \mathsf{costset}_N(s(\overline{a_i})) &amp;= \{ (\mathcal{L}, u + 1) \mid (\mathcal{L}, u) \in \mathsf{cross}(\overline{a_i}) \} \\
\mathsf{costset}_N((\lambda \overline{X} \ \mathbf{\shortrightarrow}\ a)\ b) &amp;= \mathsf{addlib}(a, \mathsf{costset}(a), \mathsf{costset}(b)) \\
    \end{array}$$</span></p>
<p><strong>E-class cost set</strong> <span class="math inline">costset(<em>a</em>)</span> <span class="math display">$$\begin{array}{rl}
    \mathsf{costset}(\{ \overline{n_j} \}) &amp;= \ensuremath{\textcolor{darkred}{\mathsf{prune}}}(\ensuremath{\textcolor{darkblue}{\mathsf{reduce}}}(\bigcup \overline{\mathsf{costset}_N(n_j)})) \\
  \end{array}$$</span></p>
<p><strong>Auxiliary definitions</strong> <span class="math inline">cross</span>, <span class="math inline">addlib</span>, <span class="math inline">$\ensuremath{\textcolor{darkblue}{\mathsf{reduce}}}$</span>, <span class="math inline">$\ensuremath{\textcolor{darkred}{\mathsf{prune}}}$</span> <span class="math display">$$\begin{array}{rl}
    \mathsf{cross}(z_1, z_2) &amp;= \ensuremath{\textcolor{darkred}{\mathsf{prune}}}(\ensuremath{\textcolor{darkblue}{\mathsf{reduce}}}(\{ (\mathcal{L}_1 \cup \mathcal{L}_2, u_1 + u_2) \mid (\mathcal{L}_1, u_1) \in z_1, (\mathcal{L}_2, u_2) \in z_2 \})) \\
    \mathsf{addlib}(a, z_1, z_2) &amp;= \ensuremath{\textcolor{darkred}{\mathsf{prune}}}(\ensuremath{\textcolor{darkblue}{\mathsf{reduce}}}(\{ (\mathcal{L}_1 \cup \mathcal{L}_2 \cup \{ a \}, u_2) \mid (\mathcal{L}_1, u_1) \in z_1, (\mathcal{L}_2, u_2) \in z_2 \})) \\
    \ensuremath{\textcolor{darkblue}{\mathsf{reduce}}}(z) &amp;= \{ (\mathcal{L}_1, u_1) \in z \mid \forall (\mathcal{L}_2, u_2) \in z \setminus (\mathcal{L}_1, u_1).\ \mathcal{L}_1 \subset \mathcal{L}_2 \lor u_1 &lt; u_2 \} \\
    \ensuremath{\textcolor{darkred}{\mathsf{prune}}}(N, K, z) &amp;=  \ensuremath{\mathsf{top\_k}}(\{(\mathcal{L}, u) \in z \mid |\mathcal{L}| \leq N \}, K)\\
  \end{array}$$</span></p>
<figcaption>Cost set propagation, defined as two mutually recursive functions. Blue text corresponds to the partial order reduction optimization and red text corresponds to the beam approximation. <span class="math inline">top_k(<em>S</em>, <em>K</em>)</span> is a helper function that returns top <span class="math inline"><em>K</em></span> elements from the sorted set <span class="math inline"><em>S</em></span>.</figcaption>
</figure>

***Exploiting Partial Shared Structure.*** Instead, <span class="smallcaps">babble</span> selects the optimal library using a bottom-up dynamic programming algorithm. To this end, it associates each e-node and e-class with a *cost set*, which is a set of pairs $`(\mathcal{L}, u)`$ where $`\mathcal{L}`$ is a library and $`u`$ is the *use cost* of this library, *i.e.* the size of the smallest term represented by the e-node / e-class if it is allowed to use $`\mathcal{L}`$ (excluding the size of $`\mathcal{L}`$ itself). Cost sets are propagated up the e-graph using the rules shown in <a href="#fig:costset" data-reference-type="ref+label" data-reference="fig:costset">11</a>. The base case is a nullary e-node $`s()`$, which cannot use any library functions and whose size is always $`1`$. For an e-node that has children, <span class="smallcaps">babble</span> computes the $`\mathsf{cross}`$ product over the cost sets of all its child e-classes. Finally, for an application e-node $`(\lambda \overline{X} \ \mathbf{\shortrightarrow}\ a)\ b`$, the cost set *must include* the library function $`a`$ (in addition to some combination of libraries from the cost sets of $`a`$ and $`b`$); note that the use cost of the abstraction node only includes the use cost of $`b`$, since abstraction bodies are excluded from the use cost.

To compute the cost set of an e-class, <span class="smallcaps">babble</span> takes the union of the cost sets of all its e-nodes. However, doing this naively would result in the size of the cost set growing exponentially. To mitigate this, we define a *partial order reduction* ($`\ensuremath{\textcolor{darkblue}{\mathsf{reduce}}}`$), which only prunes provably sub-optimal cost sets. Given two pairs $`(\mathcal{L}_1, u_1)`$ and $`(\mathcal{L}_2, u_2)`$ in the cost set of an e-class, if $`\mathcal{L}_1 \subset \mathcal{L}_2`$ and $`u_1 \leq u_2`$, then $`\mathcal{L}_2`$ is subsumed by $`\mathcal{L}_1`$ and can be removed from the cost set, intuitively because $`\mathcal{L}_1`$ can compress this e-class even better and with fewer library functions. In practice this optimization prunes libraries with redundant abstraction, where two different abstractions can be used to compress the same subterms.

***Beam Approximation.*** Even with the partial order reduction, calculating the cost set for every e-node and e-class can blow up exponentially. To mitigate this, <span class="smallcaps">babble</span> provides the option to limit both the *size of each library* inside a cost set and the *size of the cost set* stored for each e-class. This results in a *beam-search* style algorithm, where the cost set of each e-class is $`\ensuremath{\textcolor{darkred}{\mathsf{prune}}}`$ed, as shown in <a href="#fig:costset" data-reference-type="ref+label" data-reference="fig:costset">11</a>. This pruning operation first filters out libraries that have more than $`N`$ patterns, then ranks the rest by the total cost (*i.e.* the sum of use cost and the size of the library), and finally returns the top $`K`$ libraries from that set.

# Evaluation

We evaluated <span class="smallcaps">babble</span> and the LLMT algorithm behind it with two quantitative research questions and a third qualitative one:

1.  Can <span class="smallcaps">babble</span> compress programs better than a state-of-the-art library learning tool?<span id="rq:1" data-label="rq:1"></span>

2.  Are the main techniques in LLMT (anti-unification and equational theories) important to the algorithm’s performance?<span id="rq:2" data-label="rq:2"></span>

3.  Do the functions <span class="smallcaps">babble</span> learns make intuitive sense?<span id="rq:3" data-label="rq:3"></span>

***Benchmark Selection.*** We use two suites of benchmarks to evaluate <span class="smallcaps">babble</span>, both shown in <a href="#tab:benchmarks" data-reference-type="ref+label" data-reference="tab:benchmarks">2</a>. The first suite originates from the <span class="smallcaps">DreamCoder</span> work , and is available as a public repository . <span class="smallcaps">DreamCoder</span> is the current state-of-the-art library learning tool, and using these benchmarks allows us to perform a head-to-head comparison. The <span class="smallcaps">DreamCoder</span> benchmarks are split into five domains (each with a different DSL); we selected two of the domains—List and Physics—which we understood best, to add an equational theory.

The second benchmark suite, called <span class="smallcaps">2d cad</span>, comes from . This work collects a large suite of programs in a graphics DSL for the purpose of studying connections between the generated objects and their natural language descriptions. There are 1,000 programs in the “Drawings” portion of this dataset, divided into four subdomains (listed in <a href="#tab:benchmarks" data-reference-type="ref+label" data-reference="tab:benchmarks">2</a>) of 250 programs each.

We ran <span class="smallcaps">babble</span> on all benchmarks on an AMD EPYC 7702P processor at 2.0 GHz. Each benchmark was run on a single core. The <span class="smallcaps">DreamCoder</span> results were taken from the benchmark repository ; <span class="smallcaps">DreamCoder</span> was run on 8 cores of an AMD EPYC 7302 processor at 3.0 GHz.

<table id="tab:benchmarks">
<caption> We selected our benchmark domains from two previous works: <span class="smallcaps">DreamCoder</span> <span class="citation" data-cites="dreamcoder"></span> and <span class="smallcaps">2d cad</span> <span class="citation" data-cites="cogsci-dataset"></span>. Each domain from <span class="smallcaps">DreamCoder</span> has multiple benchmarks; <span class="smallcaps">2d cad</span> has one large benchmark per domain. For some domains, we additionally supplied <span class="smallcaps">babble</span> with an equational theory; we report the number of equations in the final column. </caption>
<tbody>
<tr>
<td colspan="3" style="text-align: center;"><span class="smallcaps">DreamCoder</span> <span class="citation" data-cites="dreamcoder"></span></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Domain</strong></td>
<td style="text-align: right;"><strong># Benchmarks</strong></td>
<td style="text-align: right;"><strong># Eqs</strong></td>
</tr>
<tr>
<td style="text-align: left;">List</td>
<td style="text-align: right;">59</td>
<td style="text-align: right;">14</td>
</tr>
<tr>
<td style="text-align: left;">Physics</td>
<td style="text-align: right;">18</td>
<td style="text-align: right;">8</td>
</tr>
<tr>
<td style="text-align: left;">Text</td>
<td style="text-align: right;">66</td>
<td style="text-align: right;">-</td>
</tr>
<tr>
<td style="text-align: left;">Logo</td>
<td style="text-align: right;">12</td>
<td style="text-align: right;">-</td>
</tr>
<tr>
<td style="text-align: left;">Towers</td>
<td style="text-align: right;">18</td>
<td style="text-align: right;">-</td>
</tr>
</tbody>
</table>

<table id="tab:benchmarks">
<caption> We selected our benchmark domains from two previous works: <span class="smallcaps">DreamCoder</span> <span class="citation" data-cites="dreamcoder"></span> and <span class="smallcaps">2d cad</span> <span class="citation" data-cites="cogsci-dataset"></span>. Each domain from <span class="smallcaps">DreamCoder</span> has multiple benchmarks; <span class="smallcaps">2d cad</span> has one large benchmark per domain. For some domains, we additionally supplied <span class="smallcaps">babble</span> with an equational theory; we report the number of equations in the final column. </caption>
<tbody>
<tr>
<td colspan="3" style="text-align: center;"><span class="smallcaps">2d cad</span> <span class="citation" data-cites="cogsci-dataset"></span></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Domain</strong></td>
<td style="text-align: right;"><strong># Benchmarks</strong></td>
<td style="text-align: right;"><strong># Eqs</strong></td>
</tr>
<tr>
<td style="text-align: left;">Nuts &amp; Bolts</td>
<td style="text-align: right;">1</td>
<td style="text-align: right;">7</td>
</tr>
<tr>
<td style="text-align: left;">Vehicles</td>
<td style="text-align: right;">1</td>
<td style="text-align: right;">9</td>
</tr>
<tr>
<td style="text-align: left;">Gadgets</td>
<td style="text-align: right;">1</td>
<td style="text-align: right;">17</td>
</tr>
<tr>
<td style="text-align: left;">Furniture</td>
<td style="text-align: right;">1</td>
<td style="text-align: right;">9</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: right;"></td>
<td style="text-align: right;"></td>
</tr>
</tbody>
</table>

## Comparison with <span class="smallcaps">DreamCoder</span>

<figure id="fig:dc-domains">
<figure id="fig:dc-domains-list">
<embed src="figures/scatter/list.pdf" />
<figcaption>List domain</figcaption>
</figure>
<figure id="fig:dc-domains-physics">
<embed src="figures/scatter/physics.pdf" />
<figcaption>Physics domain</figcaption>
</figure>
<figure>
<embed src="figures/scatter/text.pdf" />
<figcaption>Text domain</figcaption>
</figure>
<figure>
<embed src="figures/scatter/logo.pdf" />
<figcaption>Logo domain</figcaption>
</figure>
<figure>
<embed src="figures/scatter/towers.pdf" />
<figcaption>Towers domain</figcaption>
</figure>
<figcaption> <span class="smallcaps">babble</span> consistently achieves better compression ratios than <span class="smallcaps">DreamCoder</span> on benchmarks from the <span class="smallcaps">DreamCoder</span> domains, and it does so 1–2 orders of magnitude faster. Each marker shows the compression ratio (x-axis) and run time (y-axis) of a benchmark. Each benchmark is one <span class="smallcaps">DreamCoder</span> input, <em>i.e.</em>, a set of groups of programs as described above. Lower and to the right is better. In the domains where we supplied <span class="smallcaps">babble</span> with an equational theory (List and Physics), additional markers show the performance of <span class="smallcaps">babble</span> using purely syntactic learning (without equations, “BabbleSyn”) or only equality saturation without library learning (“EqSat”). </figcaption>
</figure>

To answer <a href="#rq:1" data-reference-type="ref" data-reference="rq:1">[rq:1]</a>, we compare to the state-of-the-art <span class="smallcaps">DreamCoder</span> tool  on its own benchmarks. The <span class="smallcaps">DreamCoder</span> benchmarks are suited to its workflow; while the input to a library learning task is conceptually a set of programs (or just one big program), each input to <span class="smallcaps">DreamCoder</span> is a set of *groups* of programs. Each group is a set of programs that are all output from the same program synthesis task (from an earlier part of the <span class="smallcaps">DreamCoder</span> pipeline). When compressing a program via library learning, <span class="smallcaps">DreamCoder</span> is minimizing the cost of the program made by concatenating the most compressed program from each group together, in other words:
``` math
\sum_{\textsf{group $g$}}
  \min_{\textsf{program $p \in g$}}
  \textsf{cost}(p)
```
<span class="smallcaps">DreamCoder</span> takes this approach to give its library learning component many variants of the same program, in order to introduce more shared structure between solution programs across different synthesis problems.

To implement <span class="smallcaps">DreamCoder</span>’s benchmarks in <span class="smallcaps">babble</span>, we use the e-graph to capture the notion of program variants in a group. Since every program in a group is the output of the same synthesis task, <span class="smallcaps">babble</span> considers them equivalent and places them in the same e-class.

***Results.*** We ran <span class="smallcaps">babble</span> on five domains from the <span class="smallcaps">DreamCoder</span> benchmark suite. The results are shown in <a href="#fig:dc-domains" data-reference-type="ref+label" data-reference="fig:dc-domains">14</a>. In summary, <span class="smallcaps">babble</span> consistently achieves better compression ratios than <span class="smallcaps">DreamCoder</span> on benchmarks from the <span class="smallcaps">DreamCoder</span> domains, and it does so 1–2 orders of magnitude faster.

***The Role of Equational Theory.*** <span id="sec:ablation" data-label="sec:ablation"></span> To answer <a href="#rq:2" data-reference-type="ref" data-reference="rq:2">[rq:2]</a>, we again turn to the <span class="smallcaps">DreamCoder</span> benchmarks, focusing on the domains where we supplied <span class="smallcaps">babble</span> with an equational theory: List and Physics. In these domains, we ran <span class="smallcaps">babble</span> in two additional configurations:

- “BabbleSyn” ignores the equational theory, just doing syntactic library learning.

- “EqSat” just optimizes the program using Equality Saturation with the rewrites from the equational theory. This configuration *does not* do any library learning.

<a href="#fig:dc-domains-list" data-reference-type="ref+label" data-reference="fig:dc-domains-list">12</a> and <a href="#fig:dc-domains-physics" data-reference-type="ref" data-reference="fig:dc-domains-physics">13</a> show the results for these additional configurations, as well as <span class="smallcaps">DreamCoder</span> and the normal <span class="smallcaps">babble</span> configuration. All <span class="smallcaps">babble</span> configurations rely on targeted subexpression elimination to select the final learned library. The “EqSat” configuration is unsurprisingly very fast but performs relatively little compression, as it does not learn any library abstractions. The “BabbleSyn” configuration does indeed compress the inputs, in fact it is still better than <span class="smallcaps">DreamCoder</span> in both domains. However, the addition of the equational theory (the “<span class="smallcaps">babble</span>” markers in the plots) significantly improves compression and adds relatively little run time, well within an order of magnitude.

## Large-Scale <span class="smallcaps">2d cad</span> Benchmarks

<table id="tab:cogsci">
<tbody>
<tr>
<td colspan="2" style="text-align: center;"></td>
<td colspan="3" style="text-align: center;">Without Eqs</td>
<td colspan="3" style="text-align: center;">With Eqs</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Benchmark</strong></td>
<td style="text-align: right;"><strong>Input Size</strong></td>
<td style="text-align: right;"><strong>Out Size</strong></td>
<td style="text-align: right;"><strong>CR</strong></td>
<td style="text-align: right;"><strong>Time (s)</strong></td>
<td style="text-align: right;"><strong>Out Size</strong></td>
<td style="text-align: right;"><strong>CR</strong></td>
<td style="text-align: right;"><strong>Time (s)</strong></td>
</tr>
<tr>
<td style="text-align: left;">Nuts &amp; Bolts</td>
<td style="text-align: right;">19009</td>
<td style="text-align: right;">2059</td>
<td style="text-align: right;">9.23</td>
<td style="text-align: right;">18.74</td>
<td style="text-align: right;">1744</td>
<td style="text-align: right;">10.90</td>
<td style="text-align: right;">40.75</td>
</tr>
<tr>
<td style="text-align: left;">Vehicles</td>
<td style="text-align: right;">35427</td>
<td style="text-align: right;">6477</td>
<td style="text-align: right;">5.47</td>
<td style="text-align: right;">79.50</td>
<td style="text-align: right;">5505</td>
<td style="text-align: right;">6.44</td>
<td style="text-align: right;">78.03</td>
</tr>
<tr>
<td style="text-align: left;">Gadgets</td>
<td style="text-align: right;">35713</td>
<td style="text-align: right;">6798</td>
<td style="text-align: right;">5.25</td>
<td style="text-align: right;">75.07</td>
<td style="text-align: right;">5037</td>
<td style="text-align: right;">7.09</td>
<td style="text-align: right;">82.29</td>
</tr>
<tr>
<td style="text-align: left;">Furniture</td>
<td style="text-align: right;">42936</td>
<td style="text-align: right;">10539</td>
<td style="text-align: right;">4.07</td>
<td style="text-align: right;">133.25</td>
<td style="text-align: right;">9417</td>
<td style="text-align: right;">4.56</td>
<td style="text-align: right;">110.00</td>
</tr>
<tr>
<td style="text-align: left;">Nuts &amp; Bolts (clean)</td>
<td style="text-align: right;">18259</td>
<td style="text-align: right;">2215</td>
<td style="text-align: right;">8.24</td>
<td style="text-align: right;">18.12</td>
<td style="text-align: right;">1744</td>
<td style="text-align: right;">10.47</td>
<td style="text-align: right;">40.91</td>
</tr>
</tbody>
</table>

<span id="tab:cogsci" data-label="tab:cogsci"></span>

<figure id="fig:cogsci-scatter">
<embed src="figures/scatter/cogsci-scatter.pdf" style="height:5cm" />
<figcaption> Data from <a href="#tab:cogsci" data-reference-type="ref+label" data-reference="tab:cogsci">3</a> in scatter plot. Each line segment shows compression ratio and run time for a domain without (hollow marker) and with (solid marker) an equational theory. Using an equational theory improves compression in all cases, and even improves run time in two cases. </figcaption>
</figure>

The previous section demonstrated that <span class="smallcaps">babble</span>’s performance far surpasses the state of the art. In this section, we present and discuss the results of running <span class="smallcaps">babble</span> on benchmarks from the <span class="smallcaps">2d cad</span> domain. These benchmarks, taken from , are significantly larger (roughly 10x - 100x) than those from the <span class="smallcaps">DreamCoder</span> dataset and out of reach for <span class="smallcaps">DreamCoder</span>.

***Quantitative Results.*** <a href="#tab:cogsci" data-reference-type="ref+label" data-reference="tab:cogsci">3</a> and <a href="#fig:cogsci-scatter" data-reference-type="ref+label" data-reference="fig:cogsci-scatter">15</a> show the results of running <span class="smallcaps">babble</span> on the benchmarks from the <span class="smallcaps">2d cad</span> domain. The plot in <a href="#fig:cogsci-scatter" data-reference-type="ref+label" data-reference="fig:cogsci-scatter">15</a> makes two observations clear. First and relevant for <a href="#rq:2" data-reference-type="ref" data-reference="rq:2">[rq:2]</a>, the addition of an equational theory improved all four benchmarks (the solid marker is always to the right of the hollow marker). Second, and perhaps surprisingly, equational theories can sometimes make <span class="smallcaps">babble</span>*faster*! This is consistent with previous observations about equality saturation : while equality saturation typically makes an e-graph larger, it can sometimes combine two relevant e-classes into one and reduce the amount of work that some operation over an e-graph must do.

We also observed that the Nuts-and-bolts dataset contains several redundant transformations, like the “scale by 1” featured in the running example of <a href="#sec:overview" data-reference-type="ref+label" data-reference="sec:overview">2</a>. These redundancies can be useful for finding abstractions in the absence of an equational theory. However, they should not be required in <span class="smallcaps">babble</span> since LLMT can introduce the redundancies wherever required. We therefore removed all existing redundant transformations from Nuts-and-bolts and ran <span class="smallcaps">babble</span> on the transformed dataset. The results are in the final row of <a href="#tab:cogsci" data-reference-type="ref+label" data-reference="tab:cogsci">3</a>. On the modified dataset, <span class="smallcaps">babble</span> achieves identical compression when using the equational theory, but without the equations it performs worse than on the unmodified dataset.

***Qualitative Evaluation.*** <span id="sec:quali" data-label="sec:quali"></span>

<figure id="fig:qual_cogsci">
<embed src="figures/qual_cogsci.pdf" />
<figcaption>A selection of evaluated programs from each of the domains in the <span class="smallcaps">2d cad</span> dataset, along with a selection of functions that <span class="smallcaps">babble</span> learns within the first ten rounds for each domain. Bolded functions represent learned abstractions. Note this figure uses the concrete syntax from the <span class="smallcaps">2d cad</span> dataset; it is similar to the simplified form shown in the overview. We named the learned functions and their parameters for clarity. </figcaption>
</figure>

<a href="#fig:qual_cogsci" data-reference-type="ref+label" data-reference="fig:qual_cogsci">16</a> highlights a sample of abstractions that <span class="smallcaps">babble</span> discovered from the <span class="smallcaps">2d cad</span> benchmarks. We ran <span class="smallcaps">babble</span> on each of the benchmarks and applied the learned abstractions on a few input programs to visualize their usage. Questions about usability and readability of learned libraries are difficult to answer without rigorous user studies which we leave for future work. Nevertheless, <a href="#fig:qual_cogsci" data-reference-type="ref+label" data-reference="fig:qual_cogsci">16</a> shows that <span class="smallcaps">babble</span> identifies common structures that are similar across different benchmarks, which makes its output easier to reuse and interpret.

First, we revisit the Nuts-and-bolts example from <a href="#sec:intro" data-reference-type="ref+label" data-reference="sec:intro">1</a>: <a href="#fig:qual_cogsci" data-reference-type="ref+label" data-reference="fig:qual_cogsci">16</a> shows that <span class="smallcaps">babble</span> learns the scaled polygon (`ngon`) abstraction which is applicable to several programs in the dataset. We also see that <span class="smallcaps">babble</span> consistently finds a similar abstraction representing a “ring of shapes” for both Nuts-and-bolts and Vehicles. Finally, as the Gadgets example shows, <span class="smallcaps">babble</span> finds abstractions for both the entire model as well as its components. In this case, it learned the function `gadget_body` that abstracts the entire outer shape, and it also learned `dial` that abstracts the handles of the outer shape.

# Related Work

<span class="smallcaps">babble</span> is inspired by work on library learning, specifically the <span class="smallcaps">DreamCoder</span> line of work, as well as equality saturation-based program synthesis and decompilation.

***<span class="smallcaps">DreamCoder</span>.*** <span class="smallcaps">DreamCoder</span>  is a program synthesizer that learns a library of abstractions from solutions to a set of related synthesis tasks. The library is intended to be used for solving other similar synthesis tasks. <span class="smallcaps">DreamCoder</span> uses version spaces  to compactly store a large set of programs and leverages ideas from e-graphs (such as e-matching) but only for exploring the space of refactorings of the original program using the candidate libraries, not for making library learning robust to syntactic variation. Our evaluation shows that <span class="smallcaps">babble</span> can find more optimal abstractions faster than <span class="smallcaps">DreamCoder</span>.

<span class="smallcaps">DreamCoder</span> has sparked several direction of follow-up work that attempt to improve the efficiency of its library learning procedure and the quality of the learned abstractions. One of them is by , which uses natural language annotations and a neural network to guide library learning. Another one is <span class="smallcaps">Stitch</span> , which was developed *concurrently* with this work and is the most closely related to <span class="smallcaps">babble</span>; we discuss <span class="smallcaps">Stitch</span> in some detail below.

***<span class="smallcaps">Stitch</span>.*** The core difference between the two approaches is that <span class="smallcaps">Stitch</span> focuses on improving *efficiency* of purely syntactic library learning, whereas <span class="smallcaps">babble</span> attempts to improve its *expressiveness* by adding equational theories. While <span class="smallcaps">babble</span> separates library learning into two phases—candidate generation via anti-unification and candidate selection via e-graph extraction—the <span class="smallcaps">Stitch</span> algorithm *interleaves* the generation and selection phases in a branch-and-bound top-down search. Starting from the “top” pattern $`X`$, <span class="smallcaps">Stitch</span> gradually refines it until further refinement does not pay off. To quickly prune suboptimal candidate patterns, <span class="smallcaps">Stitch</span> computes an upper bound on their compression by summing up the compression at each match of this pattern in the corpus (this bound is imprecise because it does not take into account that matches might overlap). For candidates that are not pruned this way, <span class="smallcaps">Stitch</span> computes their true compression by searching for the optimal subset of matches to rewrite, a so-called “rewrite strategy”. <span class="smallcaps">babble</span>’s extraction algorithm can be seen as a generalization of <span class="smallcaps">Stitch</span>’s rewrite strategy: while the former searches over both subsets of patterns and how to apply them to the corpus at the same time, the latter considers a single pattern at a time and only searches for the best way to apply it. Since the search space in the former case is much larger, <span class="smallcaps">babble</span> uses a beam search approximation, while in <span class="smallcaps">Stitch</span> the rewrite strategy is precise. To sum up, the main pros and cons of the two approaches are:

- <span class="smallcaps">babble</span> can learn libraries modulo equational theories, while <span class="smallcaps">Stitch</span> cannot;

- <span class="smallcaps">Stitch</span> provides optimality guarantees for learning a single best abstraction at a time, while <span class="smallcaps">babble</span> can learn multiple abstractions at once, but sacrifices theoretical optimality.

***Other Library Learning Techniques.*** <span class="smallcaps">Knorf</span>  is a library learning tool for logic programs, which, like <span class="smallcaps">babble</span>, proceeds in two phases. Their candidate generation phase is similar to the upper bound computation in <span class="smallcaps">Stitch</span>, while their selection phase uses an off-the-shelf constraint solver. It would be interesting to explore whether their constraint-based technique can be generalized beyond logic programs.

Other work develops limited forms of library learning, where only certain kinds of sub-terms can be abstracted. For example, ShapeMod  learns macros for 3D shapes represented in a DSL called ShapeAssembly, and only supports abstracting over numeric parameters, like dimensions of shapes. Our own prior work  extracts common structure from graphical programs, but only supports abstracting over primitive shapes and applying the abstraction at the top level of the program. Such restrictions make the library learning problem more computationally tractable, but limit the expressiveness of the learned abstractions.

There are several neural program synthesis tools  that learn *programming idioms* using statistical techniques. Some of these tools have used “explore-compress” algorithms  to iteratively enumerate a set of programs from a grammar and find a solution that exposes abstractions that make the set of programs maximally compressible. This is similar to common subexpression elimination which <span class="smallcaps">babble</span> uses for guiding extraction.

***Loop rerolling.*** Loop rerolling is related to library learning in that it also aims to discover hidden structure in a program, except that this structure is in the form of loops. A variety of domains have used loop rerolling to infer abstractions from flat input programs. In hardware, loop rerolling is used to optimize programs for code size . In many of these tools, the compiler first unrolls a loop, applies optimizations, then rerolls it — the compiler therefore has structural information about the loop that can be used for rerolling . The graphics domain has used loop-rerolling to discover latent structure from low-level representations. CSGNet  and Shape2Prog  used neural program generators to discover for loops from pixel- and voxel-based input representations. used program synthesis and machine learning to infer loops from hand-drawn images. Szalinski  used equality saturation to automatically learn loops in the form of maps and folds from flat 3D CAD programs that are synthesized by mesh decompilation tools . WebRobot  has used speculative rewriting for inferring loops from traces of web interactions. Similar to <span class="smallcaps">babble</span>(and unlike Szalinski), WebRobot finds abstractions over *multiple* input traces.

***Applications of Anti-Unification.*** Anti-unification is a well-established technique for discovering common structure in programs. It is the core idea behind bottom-up Inductive Logic Programming , and has also been used for software clone detection , programming by example , and learning repetitive code edits . It is possible that these applications could also benefit from <span class="smallcaps">babble</span>’s notion of anti-unification over e-graphs to make them more robust to semantics-preserving transformations.

***Synthesis and Optimization using E-graphs.*** While traditionally e-graphs have been used in SMT solvers for facilatiting communication between different theories, several tools have demonstrated their use for optimization and synthesis. first used e-graphs for equality saturation: a rewrite-driven technique for optimizing Java programs with loops. Since then, several tools have used equality saturation for finding programs equivalent to, but better than, some input program . <span class="smallcaps">babble</span> uses an anti-unification algorithm on e-graphs (together with domain specific rewrites), which prior work has not shown. Additionally, prior work has either used greedy or ILP-based extraction strategies, whereas <span class="smallcaps">babble</span> uses a new targeted common subexpression elimination approach which we believe can be used in many other applications of equality saturation, especially given its amenability to approximation via beam search.

# Conclusion and Future Work

We presented library learning modulo theory (LLMT), a technique for learning abstractions from a corpus of programs modulo a user-provided equational theory. We implemented LLMT in <span class="smallcaps">babble</span>. Our evaluation showed that <span class="smallcaps">babble</span> achieves better compression orders of magnitude faster than the state of the art. On a larger benchmark suite of <span class="smallcaps">2d cad</span> programs, <span class="smallcaps">babble</span> learns sensible functions that compress a dataset that was—until now—too large for library learning techniques.

LLMT and <span class="smallcaps">babble</span> present many avenues for future work. First, our evaluation showed that equational theories are important for achieving high compression, but these must be provided by domain experts. Recent work in automated theory synthesis like Ruler  or <span class="smallcaps">TheSy</span>  could aid the user in this task. Second, LLMT uses e-graph anti-unification to generate promising abstraction candidates, but this approach is incomplete and misses some patterns that could achieve better compression. An exciting direction for future work is to combine LLMT with more efficient top-down search from <span class="smallcaps">Stitch</span> . This is challenging because <span class="smallcaps">Stitch</span> crucially relies on the ability to quickly compute an upper bound on the compression of a given pattern by summing up the local compression at each of its matches in the corpus. This upper bound does not straightforwardly extend to e-graphs because in an e-graph different matches of a pattern may come from different syntactic variants of the corpus, and one needs to trade-off the compression from abstractions against the size difference between different syntactic variants.

<div class="acks">

We are grateful to the anonymous reviewers for their insightful comments. We would like to thank Matthew Bowers for many helpful discussions and especially for publishing the <span class="smallcaps">DreamCoder</span> compression benchmark: we know it was a lot of work to assemble! This work has been supported by the National Science Foundation under Grants No. 1911149 and 1943623.

</div>

# Proofs

<div class="proposition">

The language of compressed terms is strongly normalizing.

</div>

<div class="proof">

*Proof.* Consider evaluating $`\hat{t}`$ in applicative order (leftmost innermost). In this case, any left-hand size of a $`\beta`$-reduction has no inner $`\beta`$-redexes. Since in our language a $`\lambda`$-abstraction can only be on the left-hand side of a $`\beta`$-redex, it means that expression being reduced has no inner $`\lambda`$-abstractions. For that reason, the number of $`\lambda`$-abstractions in an expression strictly decreases with every $`\beta`$-step (the sole one in the reduced redex disappears, and all other $`\lambda`$-abstractions are outside of the reduced redex, and hence unchanged). ◻

</div>

<div class="lemma">

Given a $`\kappa`$-step $`\hat{t}_1 \rightarrow^{\kappa(p')}_1 \hat{t}_2`$ if a pattern $`p`$ has $`N`$ matches in $`\hat{t}_2`$, it also has at least $`N`$ matches in $`\hat{t}_1`$. <span id="lem:pat-match" data-label="lem:pat-match"></span>

</div>

<div class="proof">

*Proof.* There are four cases for what $`p`$ can match in $`\hat{t}_2`$:

- a subterm that does not overlap with the newly introduced $`\beta`$-redex: in this case, the match is unaffected by the $`\kappa`$-step;

- a subterm inside an actual argument of the $`\beta`$-redex: this actual argument becomes a sub-term of $`\hat{t}_1`$;

- a sub-term inside the body of the $`\beta`$-redex: $`\hat{t}_1`$ has a sub-term that is more specific than the body, and hence still matches $`p`$;

- a sub-term that includes the entire $`\beta`$-redex inside: since $`p`$ is first order, it cannot mention the redex, so the redex must be contained entirely inside the substitution; hence again the match is unaffected by the $`\kappa`$-step.

 ◻

</div>

<div class="theorem">

For any term $`t \in \mathcal{T}(\Sigma)`$ and compressed term $`\hat{t} \in \hat{\mathcal{T}}(\Sigma,\mathcal{X})`$:

<div class="description">

If $`t`$ compresses into $`\hat{t}`$, then $`\hat{t}`$ evaluates to $`t`$: $`\forall \mathcal{P}. t \rightarrow^{\kappa(\mathcal{P})} \hat{t} \Longrightarrow \hat{t} \rightarrow^{\beta}t`$.

If $`\hat{t}`$ is a solution to the (global) library learning problem, then $`t`$ compresses into $`\hat{t}`$ using only patterns that have a match in $`t`$: $`\hat{t} \in \mathop{\mathrm{arg\,min}}_{\hat{t}' \rightarrow^{\beta}t} \mathsf{size}(\hat{t}') \Longrightarrow t \rightarrow^{\kappa(\mathcal{P})} \hat{t}`$, where $`\mathcal{P}= \{p \in \mathcal{T}(\Sigma,\mathcal{X}) \mid t' \in \mathsf{subterms}(t) , t' \sqsubseteq p\}`$.

</div>

<span id="thm:pat-lib-learning-app" data-label="thm:pat-lib-learning-app"></span>

</div>

<div class="proof">

*Proof.* The soundness is trivial because inverting any $`\kappa`$-rewrite gives a valid $`\beta`$-reduction.

The other direction (completeness) is more involved. First let us prove that $`\hat{t}`$ can be obtain by any compression, regardless of whether the patterns occur in $`t`$. This is non-trivial because inverting a $`\beta`$-reduction $`(\lambda \overline{X} \ \mathbf{\shortrightarrow}\ \hat{t}_1)\ \overline{\hat{t}_2}  \rightarrow^{\beta}_1\hat{t}'`$ does not always correspond to a well-form $`\kappa`$-step, for two reasons: (a) $`\hat{t}_1`$ itself contains $`\lambda`$-abstractions (and hence does not correspond to a pattern); (b) $`\overline{X} \neq \mathsf{vars}(\hat{t}_1)`$. To overcome point (a), note that in an applicative evaluation, both $`\hat{t}_1`$ and $`\hat{t}_2`$ contain no $`\beta`$-redexes (and hence no $`\lambda`$-abstractions). Hence $`\hat{t}_1`$ is a valid pattern.

For point (b), there are two cases: either (1) $`\mathsf{vars}(\hat{t}_1) \subsetneq \overline{X}`$ or (2) $`\mathsf{vars}(\hat{t}_1) \supsetneq \overline{X}`$. Consider case (1). In this case, the compressed term $`\hat{t}`$ has $`\lambda`$-bindings that are not used in their bodies. Such a term cannot possibly be minimal. Removing unused bindings makes each individual $`\beta`$-redex smaller and cannot remove sharing, so it always makes the overall term smaller as well.

Now consider case (2). This means that $`\lambda \overline{X} \ \mathbf{\shortrightarrow}\ \hat{t}_1`$ has free variables, which must be defined in outer $`\lambda`$-abstractions. However, using such a $`\lambda`$-abstraction contradicts the assumption that we are only interested in global library learning.

Finally, let us prove that all patterns used in the compression have a match in $`t`$. Consider a compression $`t = \hat{t}_0 \rightarrow^{\kappa(p_1)}_1 \hat{t}_1 \dots \rightarrow^{\kappa(p_n)}_1  \hat{t}_n = \hat{t}`$. Clearly, each pattern $`p_i`$ has a match in the (compressed) term $`\hat{t}_{i-1}`$, by definition of the $`\kappa`$-rewrite. Hence, it also occurs in $`t`$, by induction using Lemma <a href="#lem:pat-match" data-reference-type="ref" data-reference="lem:pat-match">[lem:pat-match]</a>. ◻

</div>

# Additional Experiments

<figure id="fig:dc-domains-rounds" data-latex-placement="h">
<figure>
<embed src="figures/scatter/list-rounds.pdf" />
<figcaption>List domain</figcaption>
</figure>
<figure>
<embed src="figures/scatter/physics-rounds.pdf" />
<figcaption>Physics domain</figcaption>
</figure>
<figure>
<embed src="figures/scatter/text-rounds.pdf" />
<figcaption>Text domain</figcaption>
</figure>
<figure>
<embed src="figures/scatter/logo-rounds.pdf" />
<figcaption>Logo domain</figcaption>
</figure>
<figure>
<embed src="figures/scatter/towers-rounds.pdf" />
<figcaption>Towers domain</figcaption>
</figure>
<figcaption> <span class="smallcaps">babble</span>’s default configuration runs for 20 rounds (r=20) to learn additional library functions. This plot shows the data from <a href="#fig:dc-domains" data-reference-type="ref+label" data-reference="fig:dc-domains">14</a>, but with additional <span class="smallcaps">babble</span> configuration running fewer rounds. With fewer rounds, <span class="smallcaps">babble</span> runs faster but compresses worse. </figcaption>
</figure>

[^1]: We suspect that these transformations ended up in the dataset of  because it was generated programmatically from human-designed abstractions, such as “scaled polygon”.

[^2]: As we discuss in <a href="#sec:au" data-reference-type="ref+label" data-reference="sec:au">3</a> this can in theory eliminate optimal patterns, but our evaluation shows that it works well in practice.

[^3]: A careful reader might be wondering if we need to compute infinitely many anti-unifiers because there might be infinitely many equivalent corpora. As we explain shortly, there are only finitely many patterns that are viable abstraction candidates.

[^4]: Hereafter, $`\overline{a}`$ stands for a sequence of elements of syntactic class $`a`$ and $`\epsilon`$ denotes the empty sequence.

[^5]: In a real e-graph implementation, the definitions of e-graphs and the congruence invariant are more involved, because efficient merging of e-classes requires introducing a non-trivial equivalence relation over e-class ids; these details are irrelevant for our purposes. Also, other formalizations of e-graphs do not feature a distinguished root e-class.
