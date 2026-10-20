import streamlit as st
from core import rules
from core.analyzer import analyze_app

st.set_page_config(page_title="Permission Analyzer", page_icon="🔎", layout="wide")
st.warning("Simulation: not a real MDM or DLP")
st.title("🔎 Permission Risk Analyzer")
st.write("Compare an app's requested permissions with the permissions expected for its category.")

app_types = sorted(rules.EXPECTED)
st.session_state.setdefault("pa_type", "Flashlight")
st.session_state.setdefault("pa_perms", ["CAMERA", "ACCESS_FINE_LOCATION"])

def load_flashlight_demo():
    """Fill the form with the risky flashlight example."""
    st.session_state["pa_type"] = "Flashlight"
    st.session_state["pa_perms"] = ["CAMERA", "ACCESS_FINE_LOCATION", "READ_CONTACTS"]

st.button("Load flashlight demo", on_click=load_flashlight_demo)
with st.form("analyze_form"):
    app_type = st.selectbox("App type", app_types, key="pa_type")
    permissions = st.multiselect("Requested permissions", sorted(rules.WEIGHTS), key="pa_perms")
    submitted = st.form_submit_button("Analyze permissions", type="primary")
if submitted:
    try:
        result = analyze_app(app_type, permissions)
        if result["action"] == "Allow":
            st.success(f"✅ {result['action']} — {result['level']} risk (score {result['score']})")
        elif result["action"] == "Review":
            st.warning(f"⚠️ {result['action']} — {result['level']} risk (score {result['score']})")
        else:
            st.error(f"🛑 {result['action']} — {result['level']} risk (score {result['score']})")
        st.write("**Unexpected permissions:**", ", ".join(result["unexpected"]) if result["unexpected"] else "None")
        st.write("**Reasons**")
        for reason in result["reasons"]:
            st.write(f"- {reason}")
        st.caption("Permissions alone do not prove data leakage. This score is a teaching heuristic, not a security certification.")
    except ValueError as exc:
        st.error(str(exc))
