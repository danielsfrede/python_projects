# Symmetric Group Explorer GUI

An interactive Python program for exploring the symmetric group S_n and permutation group theory: elements, composition, cycle structure, Cayley tables, dihedral subgroups D_m, all subgroups with normality checks, and quotient groups G/H.

Run the CLI: `python3 main.py`
Run the GUI: `pip install -r requirements.txt && streamlit run app.py`

## Files
- `symmetric_group.py` — core group-theory logic (shared by both interfaces)
- `main.py` — command-line menu · `app.py` — Streamlit GUI · `requirements.txt` — GUI dependency
