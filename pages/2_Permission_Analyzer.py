"""Android Permission Least-Privilege Risk Analyzer."""

import streamlit as st
from core import rules, ui
from core.analyzer import analyze_app

st.set_page_config(page_title="Permission Risk Analyzer", layout="wide")

ui.apply_theme()
ui.render_sidebar_nav()
ui.render_simulation_banner()
ui.render_page_header(
    "Permission Risk Analyzer",
    "Evaluate Android package permissions against category least-privilege baselines using weighted heuristics.",
)

app_types = sorted(rules.EXPECTED)
st.session_state.setdefault("pa_type", "Flashlight")
st.session_state.setdefault("pa_perms", ["CAMERA", "ACCESS_FINE_LOCATION"])


def load_flashlight_demo():
    """Fill the form with the risky flashlight benchmark example."""
    st.session_state["pa_type"] = "Flashlight"
    st.session_state["pa_perms"] = ["CAMERA", "ACCESS_FINE_LOCATION", "READ_CONTACTS"]


input_col, result_col = st.columns([1.15, 0.85], gap="large")

with input_col:
    st.subheader("Package Configuration")
    st.button("Load flashlight demo", on_click=load_flashlight_demo)

    with st.form("analyze_form"):
        app_type = st.selectbox("App type", app_types, key="pa_type")
        permissions = st.multiselect(
            "Requested permissions", sorted(rules.WEIGHTS), key="pa_perms"
        )
        submitted = st.form_submit_button("Analyze permissions", type="primary")

    # Dynamic baseline reference
    expected_for_type = rules.EXPECTED.get(app_type, set())
    expected_str = ", ".join(sorted(expected_for_type)) if expected_for_type else "None (Zero permissions expected)"
    st.markdown(
        f"""
        <div class="soc-card">
            <div class="soc-card-header">
                <span>Category Baseline: {app_type}</span>
                {ui.badge_html("Least Privilege", "neutral")}
            </div>
            <div style="font-size: 14px; color: var(--soc-text-secondary);">
                Expected permissions: <code style="color: var(--soc-text-primary);">{expected_str}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with result_col:
    st.subheader("Policy Evaluation & Score")
    if submitted:
        try:
            result = analyze_app(app_type, permissions)
            action = result["action"]
            level = result["level"]
            score = result["score"]

            # Unified single verdict callout
            if action == "Allow":
                st.success(f"Policy Decision: {action} — {level} Risk (Calculated Score: {score})")
            elif action == "Review":
                st.warning(f"Policy Decision: {action} — {level} Risk (Calculated Score: {score})")
            else:
                st.error(f"Policy Decision: {action} — {level} Risk (Calculated Score: {score})")

            st.markdown("**Unexpected Permissions Identified:**")
            if result["unexpected"]:
                badges = " ".join([ui.badge_html(p, "block") for p in result["unexpected"]])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.markdown(ui.badge_html("None (All permissions expected)", "allow"), unsafe_allow_html=True)

            st.markdown("**Policy Heuristic Evaluation:**")
            for reason in result["reasons"]:
                st.markdown(f"- `{reason}`")

            st.caption(
                "Policy note: Permissions alone do not prove data leakage. "
                "This score is an explainable heuristic based on least-privilege principles, not a formal security certification."
            )
        except ValueError as exc:
            st.error(str(exc))
    else:
        st.info("Select an app category and permissions, then click 'Analyze permissions' to evaluate risk.")
