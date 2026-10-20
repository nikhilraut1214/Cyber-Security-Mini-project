import streamlit as st
from core.analyzer import analyze_app
from core.dlp import scan_text, summarize_findings, MAX_TEXT_LENGTH
from core import rules, store

st.set_page_config(page_title="MDM Console", page_icon="📱", layout="wide")
st.warning("Simulation: not a real MDM or DLP")
st.title("📱 MDM Console")
st.caption("Simulate app installation, outgoing message checks, and a lost-device wipe.")

DEMO_NAME, DEMO_TYPE = "Flashlight", "Flashlight"
DEMO_PERMS = ["CAMERA", "ACCESS_FINE_LOCATION", "READ_CONTACTS"]

def load_install_demo():
    """Fill the install form with the risky flashlight example."""
    st.session_state["install_name"] = DEMO_NAME
    st.session_state["install_type"] = DEMO_TYPE
    st.session_state["install_perms"] = list(DEMO_PERMS)

# On first visit the form starts with the risky flashlight example already filled in.
if "install_name" not in st.session_state:
    load_install_demo()

device = store.get_device(st.session_state)
with st.sidebar:
    st.subheader(device["name"])
    st.write("Status:", "🟥 Wiped" if device["wiped"] else "🟢 Active")
    st.write(f"Installed apps: **{len(device['installed_apps'])}**")
    if device["wiped"]:
        if st.button("Re-enrol device", use_container_width=True):
            store.reenrol_device(st.session_state)
            st.rerun()
    else:
        if st.button("Lost phone — wipe", type="secondary", use_container_width=True):
            store.wipe_device(st.session_state)
            st.rerun()
    st.caption("Wipe only clears this demo's simulated app list.")

if device["wiped"]:
    st.error("This device was wiped. Re-enrol it to continue.")
    st.stop()

install_col, device_col = st.columns([1.2, 0.8], gap="large")
with install_col:
    st.subheader("Install an app")
    st.button("Load demo example: risky flashlight", on_click=load_install_demo)
    with st.form("install_form"):
        app_name = st.text_input("App name", key="install_name", max_chars=60)
        app_type = st.selectbox("App type", sorted(rules.EXPECTED), key="install_type")
        permissions = st.multiselect("Requested permissions", sorted(rules.WEIGHTS), key="install_perms")
        check_install = st.form_submit_button("Check and install", type="primary")
    if check_install:
        try:
            clean_name = store.validate_app_name(app_name)
            analysis = analyze_app(app_type, permissions)
            pending = {"name": clean_name, "type": app_type, "permissions": list(permissions), "analysis": analysis}
            if analysis["action"] == "Allow":
                store.install_app(st.session_state, clean_name, app_type, permissions, analysis)
                store.clear_pending_install(st.session_state)
                st.success(f"{clean_name} installed. Risk: {analysis['level']} (score {analysis['score']}).")
            elif analysis["action"] == "Block":
                store.log_decision(st.session_state, "Install", f"{clean_name} ({app_type}), score {analysis['score']}", "Blocked")
                store.clear_pending_install(st.session_state)
                st.error(f"Installation blocked. Risk: {analysis['level']} (score {analysis['score']}).")
            else:
                store.set_pending_install(st.session_state, pending)
                st.warning(f"Needs administrator review. Risk: {analysis['level']} (score {analysis['score']}).")
        except ValueError as exc:
            st.error(str(exc))

    pending = store.get_pending_install(st.session_state)
    if pending:
        analysis = pending["analysis"]
        st.warning(f"Pending review: **{pending['name']}** ({pending['type']}) — score {analysis['score']}")
        for reason in analysis["reasons"]:
            st.write(f"• {reason}")
        approve_col, reject_col = st.columns(2)
        if approve_col.button("Approve install", type="primary", use_container_width=True):
            store.install_app(st.session_state, pending["name"], pending["type"], pending["permissions"], analysis)
            store.log_decision(st.session_state, "Approve", f"{pending['name']} ({pending['type']})", "Approved by admin")
            store.clear_pending_install(st.session_state)
            st.rerun()
        if reject_col.button("Reject install", use_container_width=True):
            store.log_decision(st.session_state, "Reject", f"{pending['name']} ({pending['type']})", "Rejected by admin")
            store.clear_pending_install(st.session_state)
            st.rerun()

with device_col:
    st.subheader("Installed apps")
    current = store.get_device(st.session_state)["installed_apps"]
    if current:
        for app in current:
            st.markdown(f"**{app['name']}** · {app['app_type']}  \nRisk: {app.get('risk_level') or '—'}")
    else:
        st.caption("No apps installed.")

st.divider()
st.subheader("Send a message")
st.caption("Use synthetic examples only. Messages are not sent to any real service.")
with st.form("send_form"):
    message = st.text_area("Message to check", placeholder="Example: Call me on 9876543210", max_chars=MAX_TEXT_LENGTH + 1, height=110)
    send = st.form_submit_button("Check and send", type="primary")
if send:
    try:
        result = scan_text(message)
        summary = summarize_findings(result["findings"])
        if result["action"] == "Allow":
            store.log_decision(st.session_state, "Send", summary, "Sent unchanged")
            st.success("Allowed. Message would be sent unchanged in this simulation.")
        elif result["action"] == "Mask":
            store.log_decision(st.session_state, "Send", summary, "Masked and sent")
            st.warning("Sensitive-looking text found. The masked version would be sent:")
            st.code(result["masked_text"])
        else:
            store.log_decision(st.session_state, "Send", summary, "Blocked")
            st.error("Blocked. The message would not be sent.")
            st.write("Finding types:", ", ".join(sorted({f["type"] for f in result["findings"]})))
        if result["findings"]:
            st.caption(f"Detected {len(result['findings'])} finding(s). Raw values are not written to the audit log.")
    except ValueError as exc:
        st.error(str(exc))

st.divider()
st.subheader("Audit log")
logs = store.get_log(st.session_state)
if logs:
    st.dataframe(logs, use_container_width=True, hide_index=True)
else:
    st.write("No events yet. Try installing an app.")
