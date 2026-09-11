# 213 kernel-clean theorems, and one that proves the Riemann Hypothesis by naming a variable after it

Author: Jared Wilder. First public timestamp: 2026-09-11.

An audit of the frontier formalizer's cable tree: 939 receipts, gated on
`formal_status = KERNEL_CHECKED` **and** `exitCode = 0` **and** axiom footprint contained in
`{propext, Classical.choice, Quot.sound}` **and** per-declaration clean **and** zero errors **and**
the `.lean` file cross-checked on disk for `sorry`, a declared `axiom`, and `native_decide`.

| | count |
|---|---|
| receipts | 939 |
| exit code 0 | 442 |
| pass the full gate | **213** |
| after removing already-published topics | 161 |
| after deduplicating retry variants | 161 |
| carrying real mathematical content | **~95** |
| distinct clean declaration names across the 213 | **367** |

**In this tree the receipt writer is honest.** Zero receipts print a clean footprint while exiting
nonzero, and every `sorryAx` case is correctly labelled. That is the opposite of what an audit of a
different pool found this morning, and it is worth recording. The traps here are of a different kind.

---

## The trap worth publishing on its own

`cable/theorems/msl_rh-pts-chain-001.lean`, exit code 0, axiom footprint exactly
`{propext, Classical.choice, Quot.sound}`, conclusion `RiemannHyp`:

```lean
import Mathlib
set_option autoImplicit false

theorem msl_rh_pts_chain_001 (L : Real) (RiemannHyp : Prop)
    (hDBN : RiemannHyp <-> L <= 0) (hRodgersTao : 0 <= L) (hPTS : Not (0 < L))
    : RiemannHyp := by rw [hDBN]; exact not_lt.mp hPTS
```

**`RiemannHyp` is a bound variable of type `Prop`.** So is the content. The theorem says: for any
proposition `P` and any real `L`, if `P` is equivalent to `L <= 0`, and `0 <= L`, and `not (0 < L)`,
then `P`. It is `not_lt.mp` with a transfer across the hypothesised equivalence, and it says nothing
about the zeta function.

Every mechanical gate passes it. The kernel is satisfied, the axioms are clean, the exit code is 0,
and the conclusion of the theorem is literally the name of a Millennium problem.

A second file in the same tree has the same shape, with `IsZero`, `IsSimple` and `G` as opaque
binders. Those two are the only instances among all 213.

**This is why an axiom footprint is necessary and not sufficient.** A statement can be kernel-perfect
and contentless, and no amount of receipt discipline detects it. Only reading the binders does.

---

## The real body of work: Erdős 595

**73 unique kernel-clean statements on an open problem.** Throughout,

```lean
Coverable G := ∃ H : ℕ → SimpleGraph V,
  (∀ n, H n ≤ G) ∧ (∀ n, (H n).CliqueFree 3) ∧ G.edgeSet ⊆ ⋃ n, (H n).edgeSet
```

that is, the edge set of `G` is covered by countably many triangle-free subgraphs. `V` is an
arbitrary type. All footprints are exactly `{propext, Classical.choice, Quot.sound}`.

### The reduction

```lean
(∃ H : ℕ → SimpleGraph V, (∀ n, H n ≤ G) ∧ (∀ n, (H n).CliqueFree 3) ∧ G.edgeSet ⊆ ⋃ n, (H n).edgeSet)
  ↔
(∃ c : Sym2 V → ℕ, ∀ x y z : V, G.Adj x y → G.Adj y z → G.Adj x z →
    ¬ (c s(x,y) = c s(y,z) ∧ c s(x,z) = c s(y,z)))
```

Coverability is equivalent to an edge colouring with no monochromatic triangle. An iff, not an
implication.

### The blindness result

```lean
(f : V → ℕ → Bool) (hf : Function.Injective f) : Coverable G
```

**Any graph on at most continuum-many vertices is coverable**, by a first-difference colouring. This
is the negative result that matters: it says the entire approach cannot decide the problem below
`2^ℵ₀`. A smallest witness must live above the continuum.

### A three-step arc

```lean
compactness     (h : ∀ S : Finset V, ∃ f : Sym2 V → Fin k, GoodOn G k ↑S f)
                : ∃ f : Sym2 V → Fin k, GoodOn G k Set.univ f

finite obstruction   ¬ IsCUTF G → ∃ S : Finset V, ∀ f : Sym2 V → Fin k, ¬ GoodOn G k ↑S f

countable core  (hw : ¬ IsCUTF G) : ∃ W : Set V, W.Countable ∧
                  ∀ k : ℕ, ∃ S : Finset V, ↑S ⊆ W ∧ ∀ f : Sym2 V → Fin k, ¬ GoodOn G k ↑S f
```

Compactness for triangle-good `k`-colourings via Tychonoff, then a failure is witnessed on a finite
set, then a Löwenheim-Skolem-style result: a countable core carries the whole obstruction.

### Four more

```lean
uncountable subgraph   (h : ¬ G.edgeSet.Countable)
                       : ∃ H, H ≤ G ∧ H.CliqueFree 3 ∧ ¬ H.edgeSet.Countable

countable back         [LinearOrder V] (hcnt : ∀ v, {u | u < v ∧ G.Adj u v}.Countable) : Coverable G

vertex transversal     (hS : S.Countable)
                       (hhit : ∀ x y z, G.Adj x y → G.Adj y z → G.Adj x z → x ∈ S ∨ y ∈ S ∨ z ∈ S)
                       : Coverable G

edge transversal       same, with S : Set (Sym2 V), S ⊆ G.edgeSet

K4-free characterisation   G.CliqueFree 4 ↔ ∀ a b, G.Adj a b →
                             ∀ x ∈ Link G a b, ∀ y ∈ Link G a b, x ≠ y → ¬ G.Adj x y
```

Erdős 595 alone contributes **208 clean declaration instances** across the tree.

---

## Ramsey: kernel-verified, and honestly placed against the literature

All four witnesses below were **recomputed here from the definition**, independent of the Lean files.

| statement | Lean | recomputed | literature |
|---|---|---|---|
| `R(5,5) >= 42` | `not_suffices_41` | confirmed | **published lower bound is 43** (Exoo 1989), so this is one short |
| `R(5,5) <= 62` | `R55_le_62`, unconditional | not recomputed | **published upper bound is 48** (Angeltveit–McKay 2024), so this is far weaker |
| `R(4,5) >= 25` | `msl_r45-global-ramsey-24` | confirmed | `R(4,5) = 25` exactly (McKay–Radziszowski 1995): **matches the record** |
| `R(3,3,3) >= 17` | `msl_erdos595-k16-three-cover` | confirmed | `R(3,3,3) = 17` exactly: **matches the record** |

**None of these improves on the literature.** Their value is that they are kernel-checked, which the
published bounds are not.

The `R(5,5) >= 42` witness is the 41-vertex circulant on `Z_41` with connection set

```
S = {1, 2, 3, 5, 7, 10, 13, 15, 16, 17}  and negatives   (degree 20, inverse-closed)
```

Recomputed: no monochromatic `K5` in the graph and none in the complement, over all
`C(41,5) = 749,398` five-sets.

The `R(4,5) >= 25` witness is the 24-vertex circulant with `S = {1,2,4,8,9,15,16,20,22,23}`: no `K4`
in the graph, no `K5` in the complement.

The `R(3,3,3) >= 17` witness is the GF(16) XOR-coset colouring, which splits `K16` into three
triangle-free graphs. Recomputed: **0 monochromatic triangles among all 560 triples.** Its footprint
is `{propext, Quot.sound}` with no choice.

### The bracket that does not assemble

The two halves above are each verified. **The file that would join them into `42 <= R(5,5) <= 62` is
`KERNEL_FAILED` with `sorryAx` while exiting 0.** Eight more receipts in the same family sit at
`KERNEL_CHECKED_WITH_DECLARED_SORRY`, exit 0, `sorryAx` present.

So the estate holds both halves of a bracket and not the bracket.

---

## Three more things a reader should know before trusting this tree

**A theorem that assumes what it states.** `R45_le_35` takes `(h : Suffices 35 4 5)` as a
hypothesis. `R55_le_70` in the same file is unconditional and fine.

**The `conclusion` field lies about content.** Many receipts headline
`([1,2] : List Nat).length = 2` or `(62 : Nat) < 70` while the real theorem sits in the preamble.
Judging this tree by its `conclusion` field would discard its best work and simultaneously let stubs
look like results.

**`native_decide` exposure is real but quarantined.** 63 receipts use it and every one is
`KERNEL_FAILED`, so none reached this list. The live exposure is in `press/`, which has **no receipts
at all**: `f4_finite.lean` and `m19_kill.lean` carry tournament results such as
`badCount row35 = 2475` and `core19_bad4 = 1653` under compiler trust rather than kernel trust, and
the file's own header says so.

## Corrections this audit forces on the estate's own records

- **`press/` holds no receipts.** An internal note records it as holding roughly 12 sealed theorems
  on tournament combinatorics. There is no exit code and no axiom footprint on record for any of
  them. They read clean and contain no `sorry`, but by this estate's own rule that is not
  verification. Separately, `press/gaga.lean` line 96 is a literal `sorry`.
- **`sealed-library/` holds 5 theorems, all already published.**
- **Four EG411 receipts point at a path that will not survive**: their `root_lean_file` is inside a
  different session's temporary scratchpad rather than the repository. Copies exist under
  `work/EG411-*/artifacts/`, but the receipt's own hash target is a temp path.
- **Three Erdős 595 receipts claim `KERNEL_CHECKED_UNIVERSAL` with `exitCode: null`** — status
  asserted, no kernel result attached. Excluded from the 213.

## Verification

```bash
python verify.py
```

Standard library only. Recomputes the three finite Ramsey witnesses from the definition and
demonstrates the vacuity pattern.

## License

Apache-2.0.
