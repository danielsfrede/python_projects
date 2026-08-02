# python_projects


### Symmetric Group Explorer
An interactive Python program for exploring the symmetric group S_n and permutation group theory.
 
It generates all n! permutations of {1, ..., n}, computes compositions, inverses, cycle decomposition, order, and sign, and prints the group's Cayley (multiplication) table. It also builds dihedral groups D_m as subgroups of S_m, showing all rotations and reflections with an ASCII drawing of the regular m-gon. Finally, it enumerates all subgroups of a given group and identifies which ones are normal.
 
Run with: `python3 main.py`
 
Files
- `symmetric_group.py` — core group-theory logic
- `main.py` — interactive command-line menu