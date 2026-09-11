#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recomputes the finite Ramsey witnesses from the definition, and demonstrates
the vacuity pattern that passes every mechanical gate.

    python verify.py

Standard library only. Exit 0 means everything reproduced.
"""
from __future__ import annotations

import sys
from itertools import combinations

FAILURES = []


def check(label, got, want):
    ok = got == want
    print("  %-56s %s" % (label, "PASS" if ok else "FAIL got=%r want=%r" % (got, want)))
    if not ok:
        FAILURES.append(label)


def circulant(n, S):
    Sset = set(x % n for x in S)
    return [[(u != v and (v - u) % n in Sset) for v in range(n)] for u in range(n)]


def find_mono(adj, n, k, want):
    """A k-set all of whose pairs have adjacency == want, or None."""
    for K in combinations(range(n), k):
        if all(adj[a][b] == want for a, b in combinations(K, 2)):
            return K
    return None


def test_r55_lower():
    print("R(5,5) >= 42 : the 41-vertex circulant")
    S = [1, 2, 3, 5, 7, 10, 13, 15, 16, 17]
    S = S + [41 - s for s in S]
    adj = circulant(41, S)
    check("connection set is inverse-closed",
          all((41 - s) % 41 in set(S) for s in S), True)
    check("degree", sum(1 for v in range(41) if adj[0][v]), 20)
    check("no mono K5 in the graph", find_mono(adj, 41, 5, True), None)
    check("no mono K5 in the complement", find_mono(adj, 41, 5, False), None)
    print("     => a 41-vertex 2-colouring with no mono K5, so R(5,5) >= 42")
    print("     the published lower bound is 43 (Exoo 1989): this is one short")


def test_r45_lower():
    print("R(4,5) >= 25 : the 24-vertex circulant")
    S = [1, 2, 4, 8, 9, 15, 16, 20, 22, 23]
    adj = circulant(24, S)
    check("connection set is inverse-closed",
          all((24 - s) % 24 in set(S) for s in S), True)
    check("no K4 in the graph", find_mono(adj, 24, 4, True), None)
    check("no K5 in the complement", find_mono(adj, 24, 5, False), None)
    print("     => R(4,5) >= 25, which MATCHES the known exact value 25")


def gf16_mul(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        hi = a & 8
        a = (a << 1) & 15
        if hi:
            a ^= 3          # x^4 = x + 1
        b >>= 1
    return p


def test_r333_lower():
    print("R(3,3,3) >= 17 : K16 as a union of three triangle-free graphs")
    powers, x = [], 1
    for _ in range(15):
        powers.append(x)
        x = gf16_mul(x, 2)
    check("2 generates GF(16)*", len(set(powers)), 15)
    cls = {v: i % 3 for i, v in enumerate(powers)}
    bad = sum(1 for a, b, c in combinations(range(16), 3)
              if cls[a ^ b] == cls[a ^ c] == cls[b ^ c])
    check("triples examined", len(list(combinations(range(16), 3))), 560)
    check("monochromatic triangles", bad, 0)
    print("     => R(3,3,3) >= 17, which MATCHES the known exact value 17")


def test_vacuity_pattern():
    print("The vacuity pattern, in Python")
    print("     the Lean file is:")
    print("       theorem ... (L : Real) (RiemannHyp : Prop)")
    print("           (hDBN : RiemannHyp <-> L <= 0) (hRodgersTao : 0 <= L)")
    print("           (hPTS : Not (0 < L)) : RiemannHyp")
    print("     RiemannHyp is a BOUND VARIABLE of type Prop.")
    print()

    def theorem(L, P, hDBN_holds):
        # hRodgersTao: 0 <= L, hPTS: not (0 < L)  =>  L == 0  =>  L <= 0
        assert 0 <= L and not (0 < L)
        return P if hDBN_holds else None

    # it concludes P for ANY proposition P, because P is universally quantified
    for P in (True, False, "the moon is a balloon"):
        check("concludes P = %r regardless of content" % (P,),
              theorem(0, P, True), P)
    print("     => the conclusion is whatever proposition is substituted.")
    print("     Exit 0, clean axioms, and no content. Only reading the binders catches it.")


def main():
    for fn in (test_r55_lower, test_r45_lower, test_r333_lower, test_vacuity_pattern):
        fn()
        print()
    if FAILURES:
        print("FAILED: %d check(s)" % len(FAILURES))
        for f in FAILURES:
            print("   " + f)
        return 1
    print("ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
