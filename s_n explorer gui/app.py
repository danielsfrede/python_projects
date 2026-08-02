"""
app.py

Interactive GUI for the symmetric group explorer, built with Streamlit.
This app does NOT reimplement any group theory logic — it imports and
calls the functions in symmetric_group.py directly, the same module
used by the command-line version (main.py).

Run with:
    streamlit run app.py
"""

import streamlit as st

from symmetric_group import (
    generate_permutations,
    compose,
    inverse,
    is_identity,
    is_self_inverse,
    cycle_notation,
    one_line_notation,
    order,
    sign,
    order_and_sign,
    cayley_table,
    build_dihedral_group,
    draw_dihedral_polygon,
    all_subgroups,
    is_normal_subgroup,
    quotient_group,
    quotient_element_order,
)

st.set_page_config(page_title="Symmetric Group Explorer", layout="wide")

st.title("Symmetric Group Explorer")
st.caption(
    "Interactive GUI over the same `symmetric_group.py` core used by the "
    "command-line version — elements, composition, Cayley tables, dihedral "
    "subgroups, all subgroups, normality, and quotient groups."
)

# ---------------------------------------------------------------------
# Sidebar: choice of n
# ---------------------------------------------------------------------

with st.sidebar:
    st.header("Group settings")
    n = st.number_input("n (for S_n)", min_value=1, max_value=7, value=4, step=1)
    elements = generate_permutations(n)
    st.metric(f"|S_{n}|", f"{len(elements)}")
    if n >= 6:
        st.warning("Large n makes some views (Cayley table, subgroups) slow or wide.")

tabs = st.tabs([
    "Elements", "Compose", "Cayley Table", "Dihedral Group",
    "Subgroups", "Quotient Groups",
])

# ---------------------------------------------------------------------
# Elements tab
# ---------------------------------------------------------------------

with tabs[0]:
    st.subheader(f"All {len(elements)} elements of S_{n}, with inverses")
    rows = []
    for sigma in elements:
        inv = inverse(sigma)
        o, s = order_and_sign(sigma)
        rows.append({
            "Element": one_line_notation(sigma),
            "Cycles": cycle_notation(sigma),
            "Order": o,
            "Sign": "+1" if s == 1 else "-1",
            "Self-inverse": "yes" if is_self_inverse(sigma) else "",
            "Inverse": cycle_notation(inv),
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------
# Compose tab
# ---------------------------------------------------------------------

with tabs[1]:
    st.subheader("Compose two permutations: sigma o tau")
    labels = [f"{i + 1}: {cycle_notation(p)}" for i, p in enumerate(elements)]

    col1, col2 = st.columns(2)
    with col1:
        sigma_choice = st.selectbox("sigma", labels, index=0, key="sigma_choice")
    with col2:
        default_tau = 1 if len(labels) > 1 else 0
        tau_choice = st.selectbox("tau", labels, index=default_tau, key="tau_choice")

    sigma = elements[labels.index(sigma_choice)]
    tau = elements[labels.index(tau_choice)]
    result = compose(sigma, tau)

    st.markdown("**Result — tau is applied first, then sigma:**")
    st.code(
        f"sigma       = {one_line_notation(sigma)} = {cycle_notation(sigma)}\n"
        f"tau         = {one_line_notation(tau)} = {cycle_notation(tau)}\n"
        f"sigma o tau = {one_line_notation(result)} = {cycle_notation(result)}",
        language=None,
    )
    r_order, r_sign = order_and_sign(result)
    st.write(f"Order of the result: **{r_order}** &nbsp;&nbsp; Sign: **{'+1 (even)' if r_sign == 1 else '-1 (odd)'}**")

# ---------------------------------------------------------------------
# Cayley Table tab
# ---------------------------------------------------------------------

with tabs[2]:
    st.subheader(f"Cayley table of S_{n}")
    if len(elements) > 24:
        st.info(
            f"S_{n} has {len(elements)} elements — the table would be "
            f"{len(elements)}x{len(elements)}. Choose a smaller n to view it."
        )
    else:
        table = cayley_table(elements)
        m = len(elements)
        header = [""] + [str(j + 1) for j in range(m)]
        display_rows = []
        for i in range(m):
            display_rows.append([str(i + 1)] + [str(table[i][j] + 1) for j in range(m)])
        st.dataframe(
            {header[c]: [row[c] for row in display_rows] for c in range(len(header))},
            use_container_width=True, hide_index=True,
        )
        st.caption("Entry (row i, column j) = index of element_i o element_j (1-indexed).")

# ---------------------------------------------------------------------
# Dihedral Group tab
# ---------------------------------------------------------------------

with tabs[3]:
    st.subheader("Dihedral group D_m — symmetries of a regular m-gon")
    m = st.number_input("m (D_m, m >= 3)", min_value=3, max_value=12, value=5, step=1, key="dihedral_m")

    dihedral_elements = build_dihedral_group(m)
    st.metric(f"|D_{m}|", f"{len(dihedral_elements)}")

    col_pic, col_list = st.columns([1, 1.4])

    with col_pic:
        st.text(draw_dihedral_polygon(m))
        st.caption(
            f"Rotation r sends vertex i to i+1 (mod {m}). "
            f"Reflection s fixes vertex 0 and sends i to -i (mod {m})."
        )

    with col_list:
        st.markdown("**Rotations**")
        rot_rows = [
            {"Name": e["name"], "Angle": f"{e['angle_deg']}°",
             "One-line": one_line_notation(e["permutation"]),
             "Cycles": cycle_notation(e["permutation"])}
            for e in dihedral_elements if e["type"] == "rotation"
        ]
        st.dataframe(rot_rows, use_container_width=True, hide_index=True)

        st.markdown("**Reflections**")
        refl_rows = [
            {"Name": e["name"],
             "One-line": one_line_notation(e["permutation"]),
             "Cycles": cycle_notation(e["permutation"])}
            for e in dihedral_elements if e["type"] == "reflection"
        ]
        st.dataframe(refl_rows, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------
# Subgroups tab
# ---------------------------------------------------------------------

with tabs[4]:
    st.subheader("All subgroups, and whether they are normal")

    source = st.radio("Ambient group", [f"S_{n}", f"D_{st.session_state.get('dihedral_m', 5)}"], horizontal=True)
    if source.startswith("S_"):
        group_elements = elements
        group_label = f"S_{n}"
    else:
        m_for_sub = st.session_state.get("dihedral_m", 5)
        group_elements = [e["permutation"] for e in build_dihedral_group(m_for_sub)]
        group_label = f"D_{m_for_sub}"

    st.write(f"|{group_label}| = {len(group_elements)}")

    proceed = True
    if len(group_elements) > 24:
        proceed = st.checkbox(
            f"{group_label} has {len(group_elements)} elements — enumerating all subgroups "
            "can be slow. Continue anyway?"
        )

    if proceed and st.button("Find all subgroups", key="find_subgroups_btn"):
        with st.spinner("Enumerating subgroups..."):
            subgroups = all_subgroups(group_elements)
            results = [(h, is_normal_subgroup(h, group_elements)) for h in subgroups]
        st.session_state["subgroups_result"] = results
        st.session_state["subgroups_group_elements"] = group_elements
        st.session_state["subgroups_group_label"] = group_label

    if "subgroups_result" in st.session_state and st.session_state.get("subgroups_group_label") == group_label:
        results = st.session_state["subgroups_result"]
        st.success(f"Found {len(results)} subgroup(s) of {group_label}.")
        for idx, (h, normal) in enumerate(results, start=1):
            tag = "🟡 NORMAL" if normal else "not normal"
            note = ""
            if len(h) == 1:
                note = " (trivial)"
            elif len(h) == len(group_elements):
                note = " (whole group)"
            members = ", ".join(cycle_notation(x) for x in h)
            st.markdown(f"**Subgroup {idx}: order {len(h)}{note} — {tag}**")
            st.code("{ " + members + " }", language=None)

# ---------------------------------------------------------------------
# Quotient Groups tab
# ---------------------------------------------------------------------

with tabs[5]:
    st.subheader("Quotient group G / H (requires H normal in G)")

    if "subgroups_result" not in st.session_state:
        st.info("Compute subgroups first on the **Subgroups** tab to select a normal subgroup H.")
    else:
        results = st.session_state["subgroups_result"]
        group_elements = st.session_state["subgroups_group_elements"]
        group_label = st.session_state["subgroups_group_label"]
        normal_subs = [h for h, normal in results if normal]

        if not normal_subs:
            st.warning("No normal subgroups found for this group.")
        else:
            options = [f"order {len(h)}" for h in normal_subs]
            choice = st.selectbox("Choose H", options, key="quotient_h_choice")
            h = normal_subs[options.index(choice)]

            q = quotient_group(h, group_elements)
            cosets, table, id_idx = q["cosets"], q["table"], q["identity_idx"]

            st.write(
                f"|{group_label}/H| = {len(group_elements)} / {len(h)} = **{q['order']}**"
            )

            st.markdown("**Cosets**")
            for i, c in enumerate(cosets):
                tag = " ← identity (this coset is H itself)" if i == id_idx else ""
                members = ", ".join(cycle_notation(g) for g in c)
                st.code(f"coset {i + 1}{tag}: {{ {members} }}", language=None)

            st.markdown("**Cayley table of the quotient group**")
            m = q["order"]
            header = [""] + [str(j + 1) for j in range(m)]
            display_rows = []
            for i in range(m):
                display_rows.append([str(i + 1)] + [str(table[i][j] + 1) for j in range(m)])
            st.dataframe(
                {header[c]: [row[c] for row in display_rows] for c in range(len(header))},
                use_container_width=True, hide_index=True,
            )

            st.markdown("**Element orders within the quotient**")
            order_rows = [
                {"Coset": i + 1, "Order": quotient_element_order(table, id_idx, i)}
                for i in range(m)
            ]
            st.dataframe(order_rows, use_container_width=True, hide_index=True)
