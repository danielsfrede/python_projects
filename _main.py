"""
main.py

Interactive program for exploring S_n:
  - asks the user for n
  - generates all n! permutations of {1, ..., n}
  - lets the user pick two permutations (by index) and computes their
    composition, cycle structure, order, sign, and inverse.
"""

from math import factorial

from symmetric_group import (
    generate_permutations,
    compose,
    inverse,
    is_identity,
    cycle_notation,
    one_line_notation,
    order,
    sign,
    list_elements_with_inverses,
    print_cayley_table,
)


def read_n() -> int:
    while True:
        entry = input("Enter the number of elements n (S_n, n <= 8 recommended): ").strip()
        try:
            n = int(entry)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        if n < 1:
            print("n must be at least 1.")
            continue
        if n > 10:
            print("n! grows very fast (n=10 -> 3,628,800). Choose a smaller n.")
            continue
        return n


def read_index(message: str, maximum: int) -> int:
    while True:
        entry = input(message).strip()
        try:
            idx = int(entry)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        if idx < 1 or idx > maximum:
            print(f"Index must be between 1 and {maximum}.")
            continue
        return idx


def print_elements(elements, n):
    print()
    print(f"Elements of S_{n} (one-line notation, cycle notation):")
    for i, p in enumerate(elements):
        print(f"  {i + 1:>3}: {one_line_notation(p):<20} {cycle_notation(p)}")


def main():
    n = read_n()
    elements = generate_permutations(n)

    print()
    print(f"S_{n} has {len(elements)} elements (n! = {factorial(n)}).")
    print_elements(elements, n)

    running = True
    while running:
        print()
        print("Options:")
        print("  1) Compose two permutations (sigma o tau)")
        print("  2) Inspect a single permutation (cycles, order, sign, inverse)")
        print("  3) List all elements again")
        print("  4) List all elements with their inverses")
        print("  5) Print Cayley table (all compositions)")
        print("  6) Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            i = read_index(f"Index of sigma (1..{len(elements)}): ", len(elements))
            j = read_index(f"Index of tau   (1..{len(elements)}): ", len(elements))
            sigma = elements[i - 1]
            tau = elements[j - 1]
            result = compose(sigma, tau)

            print()
            print(f"sigma = {one_line_notation(sigma)} = {cycle_notation(sigma)}")
            print(f"tau   = {one_line_notation(tau)} = {cycle_notation(tau)}")
            print(f"sigma o tau = {one_line_notation(result)} = {cycle_notation(result)}")
            print("(read as: apply tau first, then sigma)")

        elif choice == "2":
            i = read_index(f"Index (1..{len(elements)}): ", len(elements))
            p = elements[i - 1]
            print()
            print(f"Permutation     : {one_line_notation(p)}")
            print(f"Cycle notation  : {cycle_notation(p)}")
            print(f"Order           : {order(p)}")
            print(f"Sign (parity)   : {'+1 (even)' if sign(p) == 1 else '-1 (odd)'}")
            inv = inverse(p)
            print(f"Inverse         : {one_line_notation(inv)} = {cycle_notation(inv)}")
            print(f"Is identity?    : {is_identity(p)}")

        elif choice == "3":
            print_elements(elements, n)

        elif choice == "4":
            print()
            list_elements_with_inverses(elements)

        elif choice == "5":
            print()
            if len(elements) > 24:
                confirm = input(
                    f"S_{n} has {len(elements)} elements, so the table is "
                    f"{len(elements)}x{len(elements)} and will be wide. Continue? (y/n): "
                ).strip().lower()
                if confirm != "y":
                    continue
            print(f"Cayley table of S_{n} (entry = index of row o column):")
            print_cayley_table(elements)

        elif choice == "6":
            running = False

        else:
            print("Invalid option, try again.")

    print("Goodbye.")


if __name__ == "__main__":
    main()
