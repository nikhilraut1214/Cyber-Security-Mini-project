"""Android Permission Least-Privilege Risk Analyzer."""

import streamlit as st
from core import rules, ui
from core.analyzer import analyze_app

st.set_page_config(page_title="Permission Risk Analyzer", layout="wide")

ui.apply_theme()
ui.render_sidebar_nav()
ui.render_simulation_banner()
ui.render_page_header(
    "PERMISSION RISK ANALYZER",
    "Evaluate Android package permissions against category least-privilege baselines using weighted heuristics.",
)

app_types = sorted(rules.EXPECTED)
st.session_state.setdefault("pa_type", "Flashlight")
st.session_state.setdefault("pa_perms", ["CAMERA", "ACCESS_FINE_LOCATION"])


def load_flashlight_demo():
    """Fill the form with the risky flashlight benchmark example."""
    st.session_state["pa_type"] = "Flashlight"
    st.session_state["pa_perms"] = ["CAMERA", "ACCESS_FINE_LOCATION", "READ_CONTACTS"]


input_col, result_col = st.columns([1.1, 0.9], gap="large")

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
                <span>CATEGORY BASELINE FOR {app_type.upper()}</span>
                {ui.badge_html("LEAST PRIVILEGE", "neutral")}
            </div>
            <div style="font-size: 13px; color: var(--soc-text-secondary);">
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

            badge_kind = {
                "Allow": "allow",
                "Review": "review",
                "Block": "block",
            }.get(action, "neutral")

            st.markdown(
                f"""
                <div class="soc-card" style="border-left: 3px solid var(--soc-accent);">
                    <div class="soc-card-header">
                        <span>POLICY DECISION</span>
                        {ui.badge_html(f"{action.upper()}", badge_kind)}
                    </div>
                    <div style="display: flex; gap: 20px; align-items: baseline; margin: 8px 0;">
                        <div>
                            <span style="font-size: 11px; color: var(--soc-text-secondary); text-transform: uppercase;">Heuristic Score</span>
                            <div style="font-family: ui-monospace, monospace; font-size: 26px; font-weight: 700; color: var(--soc-text-primary);">
                                {score}
                            </div>
                        </div>
                        <div>
                            <span style="font-size: 11px; color: var(--soc-text-secondary); text-transform: uppercase;">Assigned Risk</span>
                            <div style="font-size: 16px; font-weight: 600; color: var(--soc-text-primary);">
                                {level} Risk
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Preserve standard Streamlit message elements for accessibility and tests
            if action == "Allow":
                st.success(f"Action: {action} — {level} risk (Calculated score: {score})")
            elif action == "Review":
                st.warning(f"Action: {action} — {level} risk (Calculated score: {score})")
            else:
                st.error(f"Action: {action} — {level} risk (Calculated score: {score})")

            st.markdown("**Unexpected Permissions Identified:**")
            if result["unexpected"]:
                badges = " ".join([ui.badge_html(p, "block") for p in result["unexpected"]])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.markdown(ui.badge_html("NONE", "allow"), unsafe_allow_html=True)

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            st.markdown("**Heuristic Policy Violations:**")
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
