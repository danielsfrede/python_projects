"""
symmetric_group.py

Models the symmetric group S_n: generates all permutations of
{0, 1, ..., n-1} and defines composition as the group operation.

A permutation sigma is represented as a list p such that
sigma(i) = p[i]  (one-line notation).

Composition convention (the standard one in group theory):
    (sigma o tau)(i) = sigma(tau(i))
i.e. tau is applied first, then sigma. With this convention, the set
of n! permutations under composition forms the group S_n: the
operation is associative, there is an identity element, and every
element has an inverse.
"""

from math import gcd
from itertools import permutations
from typing import List


# ---------------------------------------------------------------------
# Generation of elements of S_n
# ---------------------------------------------------------------------

def generate_permutations(n: int) -> List[List[int]]:
    """
    Returns the list of all n! permutations of {0, ..., n-1}.
    Uses itertools.permutations (equivalent in result to a Heap-style
    algorithm, but more idiomatic in Python).
    """
    return [list(p) for p in permutations(range(n))]


# ---------------------------------------------------------------------
# Group operation: composition
# ---------------------------------------------------------------------

def compose(sigma: List[int], tau: List[int]) -> List[int]:
    """
    Computes sigma o tau, defined by (sigma o tau)(i) = sigma(tau(i)).
    """
    if len(sigma) != len(tau):
        raise ValueError("Permutations must act on the same n")
    return [sigma[tau[i]] for i in range(len(sigma))]


def identity(n: int) -> List[int]:
    """Returns the identity permutation of S_n."""
    return list(range(n))


def inverse(sigma: List[int]) -> List[int]:
    """
    Computes the inverse permutation: sigma^{-1}(sigma(i)) = i.
    """
    inv = [0] * len(sigma)
    for i, v in enumerate(sigma):
        inv[v] = i
    return inv


def is_identity(sigma: List[int]) -> bool:
    return all(sigma[i] == i for i in range(len(sigma)))


# ---------------------------------------------------------------------
# Cycle structure
# ---------------------------------------------------------------------

def cycle_decomposition(sigma: List[int], exclude_fixed_points: bool = True):
    """
    Decomposes sigma into disjoint cycles. Returns a list of lists of
    indices (internally 0-indexed).
    """
    n = len(sigma)
    visited = [False] * n
    cycles = []
    for start in range(n):
        if visited[start]:
            continue
        cycle = []
        current = start
        while not visited[current]:
            visited[current] = True
            cycle.append(current)
            current = sigma[current]
        if not (exclude_fixed_points and len(cycle) == 1):
            cycles.append(cycle)
    return cycles


def cycle_notation(sigma: List[int]) -> str:
    """Represents sigma in standard cycle notation, 1-indexed."""
    cycles = cycle_decomposition(sigma, exclude_fixed_points=True)
    if not cycles:
        return "id"
    parts = []
    for c in cycles:
        parts.append("(" + " ".join(str(i + 1) for i in c) + ")")
    return "".join(parts)


def one_line_notation(sigma: List[int]) -> str:
    return "(" + " ".join(str(x + 1) for x in sigma) + ")"


def order(sigma: List[int]) -> int:
    """Order of the permutation: lcm of its cycle lengths."""
    cycles = cycle_decomposition(sigma, exclude_fixed_points=True)
    result = 1
    for c in cycles:
        result = result * len(c) // gcd(result, len(c))
    return result


def sign(sigma: List[int]) -> int:
    """
    Sign of the permutation: +1 if even, -1 if odd.
    Product of (-1)^(cycle_length - 1) over all cycles.
    """
    cycles = cycle_decomposition(sigma, exclude_fixed_points=True)
    s = 1
    for c in cycles:
        if (len(c) - 1) % 2 != 0:
            s = -s
    return s


# ---------------------------------------------------------------------
# Listing elements and their inverses
# ---------------------------------------------------------------------

def list_elements_with_inverses(elements: List[List[int]]) -> None:
    """
    Prints every element of the group alongside its inverse, in both
    one-line and cycle notation, with an index for reference.
    """
    print(f"{'#':>4}  {'Element':<20} {'Cycles':<15} {'Inverse':<20} {'Inv. cycles':<15}")
    print("-" * 78)
    for i, sigma in enumerate(elements):
        inv = inverse(sigma)
        print(
            f"{i + 1:>4}  "
            f"{one_line_notation(sigma):<20} "
            f"{cycle_notation(sigma):<15} "
            f"{one_line_notation(inv):<20} "
            f"{cycle_notation(inv):<15}"
        )


def list_self_inverse_elements(elements: List[List[int]]) -> None:
    """
    Prints only the elements that are their own inverse, i.e. sigma
    such that sigma o sigma = identity (sigma^2 = id). These are
    exactly the identity itself and the involutions (permutations
    consisting only of fixed points and 2-cycles).
    """
    print(f"{'#':>4}  {'Element':<20} {'Cycles':<15}")
    print("-" * 45)
    count = 0
    for i, sigma in enumerate(elements):
        if sigma == inverse(sigma):
            count += 1
            print(f"{i + 1:>4}  {one_line_notation(sigma):<20} {cycle_notation(sigma):<15}")
    print(f"\nTotal self-inverse elements: {count} out of {len(elements)}")


# ---------------------------------------------------------------------
# Cayley table (group multiplication / composition table)
# ---------------------------------------------------------------------

def cayley_table(elements: List[List[int]]) -> List[List[int]]:
    """
    Builds the Cayley table of the group: an m x m matrix (m = n!)
    where entry [i][j] is the index (into `elements`) of
    elements[i] o elements[j].
    """
    m = len(elements)
    index_of = {tuple(p): k for k, p in enumerate(elements)}
    table = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            result = compose(elements[i], elements[j])
            table[i][j] = index_of[tuple(result)]
    return table


def print_cayley_table(elements: List[List[int]]) -> None:
    """
    Prints the Cayley table of the group using the 1-based indices
    from `elements` as row/column labels. Entry (i, j) is the index
    of elements[i] o elements[j] (row applied to column, i.e. row is
    sigma and column is tau in sigma o tau).
    """
    m = len(elements)
    table = cayley_table(elements)

    width = len(str(m)) + 1
    header = " " * (width + 1) + " ".join(f"{j + 1:>{width}}" for j in range(m))
    print(header)
    print(" " * (width + 1) + "-" * (len(header) - (width + 1)))
    for i in range(m):
        row = " ".join(f"{table[i][j] + 1:>{width}}" for j in range(m))
        print(f"{i + 1:>{width}} |{row}")
