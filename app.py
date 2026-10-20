import streamlit as st
from core import store

st.set_page_config(page_title="Mobile DLP Console", page_icon="🛡️", layout="wide")
st.warning("Simulation: not a real MDM or DLP")

st.title("🛡️ Mobile Data Leakage Prevention Console")
st.caption("A student-friendly simulation of mobile app permission checks, outbound text scanning, and audit logging.")
st.info("This demo uses local rules and synthetic examples only. It does not control real devices or send messages.")

device = store.get_device(st.session_state)
counts = store.get_counts(st.session_state)
left, middle, right = st.columns(3)
left.metric("Installed apps", counts["installed_apps"])
middle.metric("Blocked installs", counts["blocked_installs"])
right.metric("Masked / blocked sends", counts["masked_sends"] + counts["blocked_sends"])

st.subheader("Simulated device")
status = "Wiped" if device["wiped"] else "Active"
st.write(f"**Device:** {device['name']}  ·  **Status:** {status}")
if device["installed_apps"]:
    st.dataframe([
        {"App": app["name"], "Type": app["app_type"], "Risk": app.get("risk_level") or "Not recorded",
         "Score": app.get("risk_score") if app.get("risk_score") is not None else "—"}
        for app in device["installed_apps"]
    ], use_container_width=True, hide_index=True)
else:
    st.caption("No apps installed yet. Open **MDM Console** to try installing a demo app.")

st.subheader("Audit log")
logs = store.get_log(st.session_state)
if logs:
    st.dataframe(logs, use_container_width=True, hide_index=True)
    st.download_button("Export audit log as CSV", data=store.log_to_csv(st.session_state),
                       file_name="mdm_audit_log.csv", mime="text/csv")
else:
    st.write("No events yet. Try installing an app.")

with st.expander("How this demo works"):
    st.markdown("""
    - **Permission Analyzer:** compares requested permissions with a small, editable rule table.
    - **DLP-style Scanner:** detects phone, email, card-like and grouped 12-digit ID-like patterns.
    - **MDM Console:** applies Allow / Review / Block and Allow / Mask / Block decisions.
    - **Audit log:** stores event details and finding types/counts, never message contents.

    These are educational heuristics. A permission mismatch or text pattern does not prove malicious activity.
    """)
