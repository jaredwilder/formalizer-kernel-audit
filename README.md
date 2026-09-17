# Formalizer kernel audit

An audit of 939 Lean proof receipts, checking not only compilation and axiom footprints but also whether the theorem statements carry substantive mathematical content.

## Audit totals

| | count |
|---|---:|
| receipts | 939 |
| exit code 0 | 442 |
| pass the full kernel/receipt gate | **213** |
| distinct clean declaration names | **367** |
| deduplicated, not already published elsewhere | 161 |
| estimated substantive mathematical statements | about 95 |

The full gate requires:

- `formal_status = KERNEL_CHECKED`;
- exit code 0;
- per-declaration axiom footprint contained in `{propext, Classical.choice, Quot.sound}`;
- zero recorded Lean errors;
- source cross-check with no `sorry`, declared project axiom, or `native_decide`.

## Kernel validity is not semantic validity

One audited theorem has conclusion named `RiemannHyp`, but `RiemannHyp` is merely a bound variable of type `Prop`:

```lean
theorem msl_rh_pts_chain_001 (L : Real) (RiemannHyp : Prop)
    (hDBN : RiemannHyp <-> L <= 0)
    (hRodgersTao : 0 <= L)
    (hPTS : Not (0 < L)) : RiemannHyp := by
  rw [hDBN]
  exact not_lt.mp hPTS
```

The theorem is logically correct and kernel-clean. Its content is simply: if an arbitrary proposition is equivalent to `L<=0`, and `L=0` follows from the hypotheses, then the proposition holds. It does not state anything about the zeta function.

This example is the central lesson of the audit: a clean kernel receipt certifies a proof of the formal statement, not that the formal statement means what its name suggests.

## Erdős #595 formal core

The strongest substantive cluster is a family of kernel-clean results around countable covers of a graph by triangle-free subgraphs.

Define `Coverable G` to mean that the edge set of `G` is covered by countably many triangle-free subgraphs.

Among the formal results are:

- an exact equivalence between such a cover and an edge-coloring with no monochromatic triangle;
- a first-difference coloring showing that **every graph on at most continuum-many vertices is coverable**;
- compactness for finite good colorings;
- finite obstruction extraction;
- a countable core carrying every finite obstruction;
- countable vertex- and edge-transversal criteria;
- a `K4`-free common-link characterization.

The first-difference theorem is especially useful: any counterexample to the countable triangle-free-cover property must have more than continuum-many vertices.

Focused subject work on this problem is published in [`erdos595-barrier-tower`](https://github.com/jaredwilder/erdos595-barrier-tower) and [`fiber-coherence-cycle-rank`](https://github.com/jaredwilder/fiber-coherence-cycle-rank).

## Ramsey statements in the audit

Several kernel-checked Ramsey statements were independently recomputed from their finite witnesses:

| statement | finite check | literature relation |
|---|---|---|
| `R(5,5)>=42` | confirmed on the 41-vertex circulant | weaker than the best published lower bound |
| `R(4,5)>=25` | confirmed | matches the exact known value |
| `R(3,3,3)>=17` | confirmed | matches the exact known value |

The audit also found that the file intended to assemble one two-sided `R(5,5)` bracket carries `sorryAx`; the independently verified halves should therefore be cited separately.

## Receipt failure modes

The audit records several recurring problems that a reliable formal pipeline must distinguish:

- a theorem can be kernel-clean but semantically vacuous;
- a theorem can assume essentially its own conclusion;
- a receipt summary can describe a trivial side theorem while the substantive theorem sits elsewhere in the file;
- `native_decide` and `sorryAx` can be present even when a high-level status label looks strong;
- source paths in receipts can point to temporary files rather than durable repository artifacts.

## Verification

```bash
python verify.py
```

The verifier recomputes selected finite Ramsey witnesses and demonstrates the semantic-vacuity pattern described above.

This repository is an audit of proof artifacts, not a theorem bank. The cleaned mathematical results should be cited from their subject repositories where available.

Author: Jared Wilder. License: Apache-2.0.
