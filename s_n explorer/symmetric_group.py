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
    return sigma == list(range(len(sigma)))


def is_self_inverse(sigma: List[int]) -> bool:
    """True if sigma equals its own inverse, i.e. sigma o sigma = identity."""
    return sigma == inverse(sigma)


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
    return _lcm_of_lengths(cycles)


def sign(sigma: List[int]) -> int:
    """
    Sign of the permutation: +1 if even, -1 if odd.
    Product of (-1)^(cycle_length - 1) over all cycles.
    """
    cycles = cycle_decomposition(sigma, exclude_fixed_points=True)
    return _sign_of_cycles(cycles)


def order_and_sign(sigma: List[int]):
    """
    Computes order and sign together from a single cycle
    decomposition, for callers that need both (avoids decomposing
    sigma twice).
    """
    cycles = cycle_decomposition(sigma, exclude_fixed_points=True)
    return _lcm_of_lengths(cycles), _sign_of_cycles(cycles)


def _lcm_of_lengths(cycles) -> int:
    result = 1
    for c in cycles:
        result = result * len(c) // gcd(result, len(c))
    return result


def _sign_of_cycles(cycles) -> int:
    s = 1
    for c in cycles:
        if (len(c) - 1) % 2 != 0:
            s = -s
    return s


def describe(sigma: List[int]) -> str:
    """Convenience: 'one-line = cycle-notation' summary of sigma."""
    return f"{one_line_notation(sigma)} = {cycle_notation(sigma)}"


# ---------------------------------------------------------------------
# Listing elements and their inverses
# ---------------------------------------------------------------------

def _print_row_table(headers: List[str], widths: List[int], rows: List[List[str]]) -> None:
    """
    Shared helper for printing a simple left-aligned column table
    (used by the various "list elements ..." printers so column
    formatting logic lives in one place).
    """
    header_line = "  ".join(f"{h:<{w}}" for h, w in zip(headers, widths))
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print("  ".join(f"{cell:<{w}}" for cell, w in zip(row, widths)))


def list_elements_with_inverses(elements: List[List[int]]) -> None:
    """
    Prints every element of the group alongside its inverse, in both
    one-line and cycle notation, with an index for reference.
    """
    headers = ["#", "Element", "Cycles", "Inverse", "Inv. cycles"]
    widths = [4, 20, 15, 20, 15]
    rows = []
    for i, sigma in enumerate(elements):
        inv = inverse(sigma)
        rows.append([
            str(i + 1), one_line_notation(sigma), cycle_notation(sigma),
            one_line_notation(inv), cycle_notation(inv),
        ])
    _print_row_table(headers, widths, rows)


def list_self_inverse_elements(elements: List[List[int]]) -> None:
    """
    Prints only the elements that are their own inverse, i.e. sigma
    such that sigma o sigma = identity (sigma^2 = id). These are
    exactly the identity itself and the involutions (permutations
    consisting only of fixed points and 2-cycles).
    """
    headers = ["#", "Element", "Cycles"]
    widths = [4, 20, 15]
    rows = [
        [str(i + 1), one_line_notation(sigma), cycle_notation(sigma)]
        for i, sigma in enumerate(elements)
        if is_self_inverse(sigma)
    ]
    _print_row_table(headers, widths, rows)
    print(f"\nTotal self-inverse elements: {len(rows)} out of {len(elements)}")


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


# ---------------------------------------------------------------------
# Dihedral group D_n as a subgroup of S_n
# ---------------------------------------------------------------------

def build_dihedral_group(n: int):
    """
    Constructs the dihedral group D_n (symmetries of a regular n-gon,
    with vertices labeled 0..n-1) as a subgroup of S_n.

    The rotation r is the n-cycle (0 1 2 ... n-1): r(i) = (i+1) mod n.
    The reflection s fixes vertex 0 (for odd n) or swaps pairs of
    vertices around an axis (for even n): s(i) = (-i) mod n, i.e. the
    reflection through vertex 0 / edge midpoint. Every element of D_n
    can be written uniquely as r^k or s o r^k for k = 0, ..., n-1,
    giving |D_n| = 2n elements.

    Returns a list of dicts, each with:
        'permutation' : the element as one-line notation (List[int])
        'name'        : 'e', 'r', 'r^2', ..., 's', 's r', 's r^2', ...
        'type'        : 'rotation' or 'reflection'
        'angle_deg'   : rotation angle in degrees (for rotations)
    """
    if n < 3:
        raise ValueError("A dihedral group of a polygon needs n >= 3")

    def rotation_power(k: int) -> List[int]:
        # r^k : i -> (i + k) mod n
        return [(i + k) % n for i in range(n)]

    def reflection() -> List[int]:
        # s : i -> (-i) mod n  (reflection fixing vertex 0)
        return [(-i) % n for i in range(n)]

    s = reflection()
    elements = []

    for k in range(n):
        r_k = rotation_power(k)
        name = "e" if k == 0 else ("r" if k == 1 else f"r^{k}")
        elements.append({
            "permutation": r_k,
            "name": name,
            "type": "rotation",
            "angle_deg": (360 * k) // n,
        })

    for k in range(n):
        r_k = rotation_power(k)
        s_r_k = compose(s, r_k)  # apply r^k first, then reflect
        name = "s" if k == 0 else ("s r" if k == 1 else f"s r^{k}")
        elements.append({
            "permutation": s_r_k,
            "name": name,
            "type": "reflection",
            "angle_deg": None,
        })

    return elements


def print_dihedral_group(n: int) -> None:
    """
    Prints all 2n elements of D_n (as a subgroup of S_n): the n
    rotations and n reflections, each with its name, permutation
    (one-line and cycle notation), and geometric meaning.
    """
    elements = build_dihedral_group(n)

    print(f"Dihedral group D_{n} (symmetries of a regular {n}-gon), as a subgroup of S_{n}.")
    print(f"Vertices are labeled 0..{n - 1}. |D_{n}| = {len(elements)} elements.\n")

    print("Rotations (about the center):")
    rows = [
        [el["name"], f"{el['angle_deg']}deg", one_line_notation(el["permutation"]), cycle_notation(el["permutation"])]
        for el in elements if el["type"] == "rotation"
    ]
    _print_row_table(["Name", "Angle", "One-line", "Cycles"], [8, 8, 20, 15], rows)

    print("\nReflections (about an axis through the center):")
    rows = [
        [el["name"], one_line_notation(el["permutation"]), cycle_notation(el["permutation"])]
        for el in elements if el["type"] == "reflection"
    ]
    _print_row_table(["Name", "One-line", "Cycles"], [8, 20, 15], rows)


def draw_dihedral_polygon(n: int) -> str:
    """
    Draws the regular n-gon that D_n acts on, as an ASCII-art picture
    with vertices labeled 0..n-1 placed on a circle. This is only a
    schematic (rough) drawing meant to show which object the group
    acts on, not a precise geometric plot.
    """
    import math

    radius = 10
    width = 2 * radius + 4
    cy_offset = radius + 2
    height = cy_offset + radius + 2

    grid = [[" " for _ in range(width)] for _ in range(height)]
    cx, cy = width // 2, cy_offset

    coords = []
    for i in range(n):
        # vertex 0 at the top, going clockwise, matching angle_deg above
        theta = math.pi / 2 - 2 * math.pi * i / n
        x = cx + round(radius * math.cos(theta))
        y = cy - round(radius * math.sin(theta) * 0.5)  # squash vertically for terminal aspect ratio
        coords.append((x, y))

    # draw edges of the polygon by connecting consecutive vertices
    for i in range(n):
        x0, y0 = coords[i]
        x1, y1 = coords[(i + 1) % n]
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for t in range(steps + 1):
            x = round(x0 + (x1 - x0) * t / steps)
            y = round(y0 + (y1 - y0) * t / steps)
            if 0 <= y < len(grid) and 0 <= x < width:
                if grid[y][x] == " ":
                    grid[y][x] = "."

    # place vertex labels on top of the edges
    for i, (x, y) in enumerate(coords):
        label = str(i)
        for j, ch in enumerate(label):
            xx = x + j - (len(label) - 1) // 2
            if 0 <= y < len(grid) and 0 <= xx < width:
                grid[y][xx] = ch

    # center mark
    if 0 <= cy < len(grid) and 0 <= cx < width:
        grid[cy][cx] = "+"

    lines = ["".join(row).rstrip() for row in grid]
    # trim fully blank leading/trailing rows for a tighter picture
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    return "\n".join(lines)


def print_dihedral_drawing(n: int) -> None:
    """
    Prints an ASCII drawing of the regular n-gon acted on by D_n,
    with vertices labeled 0..n-1 (vertex 0 at the top, going clockwise
    to match the rotation r: i -> i+1).
    """
    print(f"Regular {n}-gon acted on by D_{n} (vertex 0 at top, clockwise):\n")
    print(draw_dihedral_polygon(n))
    print(
        f"\nRotation r sends vertex i to vertex i+1 (mod {n}), i.e. one step clockwise."
        f"\nReflection s fixes vertex 0 and sends vertex i to vertex -i (mod {n})."
    )


# ---------------------------------------------------------------------
# Subgroups and normality
# ---------------------------------------------------------------------

def generate_subgroup(generators: List[List[int]], n: int) -> List[List[int]]:
    """
    Generates the subgroup of S_n generated by the given list of
    permutations (closure under composition and inverse), starting
    from the identity. Returns the elements as a sorted list (sorted
    by tuple order) for a canonical representation.
    """
    id_perm = identity(n)
    closure = {tuple(id_perm)}
    frontier = [id_perm] + [list(g) for g in generators]
    frontier_set = set(tuple(g) for g in frontier)
    closure |= frontier_set

    to_process = list(frontier_set)
    while to_process:
        a = list(to_process.pop())
        for b_tuple in list(closure):
            b = list(b_tuple)
            for product in (compose(a, b), compose(b, a)):
                t = tuple(product)
                if t not in closure:
                    closure.add(t)
                    to_process.append(t)

    return [list(t) for t in sorted(closure)]


def all_subgroups(elements: List[List[int]]) -> List[List[List[int]]]:
    """
    Finds all subgroups of the group formed by `elements` (assumed to
    already be closed under composition, e.g. all of S_n or a
    dihedral group built by build_dihedral_group). Every subgroup is
    generated by some subset of its elements, so this grows subgroups
    incrementally: start from the trivial subgroup, and repeatedly
    try adding one more generator, keeping only subgroups not already
    found. Exponential in the worst case, so only practical for small
    groups (|G| up to a few dozen, e.g. S_4 or D_n for modest n).
    """
    if not elements:
        return []
    n = len(elements[0])
    elem_set = set(tuple(e) for e in elements)

    trivial = frozenset([tuple(identity(n))])
    found = {trivial: sorted(trivial)}
    frontier = [trivial]

    while frontier:
        next_frontier = []
        for h_key in frontier:
            for g in elem_set:
                if g in h_key:
                    continue
                candidate = generate_subgroup([list(g)] + [list(x) for x in h_key], n)
                key = frozenset(tuple(c) for c in candidate)
                if key not in found:
                    found[key] = sorted(key)
                    next_frontier.append(key)
        frontier = next_frontier

    result = list(found.values())
    result.sort(key=lambda subgrp: (len(subgrp), subgrp))
    return [[list(t) for t in subgrp] for subgrp in result]


def is_normal_subgroup(subgroup: List[List[int]], elements: List[List[int]]) -> bool:
    """
    Checks whether `subgroup` is a normal subgroup of the group formed
    by `elements`: for every g in elements and every h in subgroup,
    g o h o g^{-1} must also be in subgroup (i.e. gHg^{-1} = H).
    """
    subgroup_set = set(tuple(h) for h in subgroup)
    for g in elements:
        g_inv = inverse(g)
        for h in subgroup:
            conjugate = compose(compose(g, h), g_inv)
            if tuple(conjugate) not in subgroup_set:
                return False
    return True


def print_all_subgroups(elements: List[List[int]], group_label: str = "G") -> None:
    """
    Lists every subgroup of the group formed by `elements`, its order,
    its elements (in cycle notation), and whether it is normal.
    Warning: this is computationally expensive and only intended for
    small groups (|G| roughly <= 24, e.g. S_4 or D_n for n <= 8).
    """
    subgroups = all_subgroups(elements)
    print(f"Subgroups of {group_label} (|{group_label}| = {len(elements)}):")
    print(f"Found {len(subgroups)} subgroup(s) in total.\n")

    for idx, h in enumerate(subgroups, start=1):
        normal = is_normal_subgroup(h, elements)
        members = ", ".join(cycle_notation(x) for x in h)
        tag = "NORMAL" if normal else "not normal"
        trivial_note = ""
        if len(h) == 1:
            trivial_note = " (trivial subgroup)"
        elif len(h) == len(elements):
            trivial_note = f" (the whole group {group_label})"
        print(f"  Subgroup {idx}: order {len(h)}{trivial_note} -- {tag}")
        print(f"    Elements: {{ {members} }}")
        print()
