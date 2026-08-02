# python_projects
Most of this code had been generated with AI. Handle with care.


### Symmetric Group Explorer
An interactive Python program for exploring the symmetric group S_n and permutation group theory.
 
It generates all n! permutations of {1, ..., n}, computes compositions, inverses, cycle decomposition, order, and sign, and prints the group's Cayley (multiplication) table. It also builds dihedral groups D_m as subgroups of S_m, showing all rotations and reflections with an ASCII drawing of the regular m-gon. Finally, it enumerates all subgroups of a given group and identifies which ones are normal.
 
Run with: `python3 main.py`
 
Files
- `symmetric_group.py` — core group-theory logic
- `main.py` — interactive command-line menu


### Symmetric Group Explorer GUI
An interactive Python program for exploring the symmetric group S_n and permutation group theory: elements, composition, cycle structure, Cayley tables, dihedral subgroups D_m, all subgroups with normality checks, and quotient groups G/H.

Run the CLI: `python3 main.py` Run the GUI: `pip install -r requirements.txt && streamlit run app.py`

Files
- `symmetric_group.py` — core group-theory logic (shared by both interfaces)
- `main.py` — command-line menu
- `app.py` — Streamlit GUI · requirements.txt — GUI dependency

