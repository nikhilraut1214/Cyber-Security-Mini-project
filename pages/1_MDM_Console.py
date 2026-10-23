"""Mobile Device Management (MDM) Console & Policy Enforcement Simulator."""

import streamlit as st
from core.analyzer import analyze_app
from core.dlp import scan_text, summarize_findings, MAX_TEXT_LENGTH
from core import rules, store, ui

st.set_page_config(page_title="MDM Console", layout="wide")

ui.apply_theme()
ui.render_sidebar_nav()
ui.render_simulation_banner()
ui.render_page_header(
    "MOBILE DEVICE MANAGEMENT CONSOLE",
    "Simulate endpoint policy enforcement, application installations, and outbound DLP inspection.",
)

DEMO_NAME, DEMO_TYPE = "Flashlight", "Flashlight"
DEMO_PERMS = ["CAMERA", "ACCESS_FINE_LOCATION", "READ_CONTACTS"]


def load_install_demo():
    """Fill the install form with the risky flashlight benchmark example."""
    st.session_state["install_name"] = DEMO_NAME
    st.session_state["install_type"] = DEMO_TYPE
    st.session_state["install_perms"] = list(DEMO_PERMS)


# On first visit the form starts with the risky flashlight example already filled in.
if "install_name" not in st.session_state:
    load_install_demo()

device = store.get_device(st.session_state)

with st.sidebar:
    st.markdown(
        """
        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--soc-text-secondary); margin-bottom: 6px;">
            SIMULATED ENDPOINT PROFILE
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"**Endpoint:** `{device['name']}`")
    status_badge = (
        ui.badge_html("WIPED", "block")
        if device["wiped"]
        else ui.badge_html("ACTIVE", "allow")
    )
    st.markdown(f"Operational State: {status_badge}", unsafe_allow_html=True)
    st.markdown(f"Installed Packages: **`{len(device['installed_apps'])}`**")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if device["wiped"]:
        if st.button("Re-enrol device", use_container_width=True):
            store.reenrol_device(st.session_state)
            st.rerun()
    else:
        if st.button("Lost phone — wipe", type="secondary", use_container_width=True):
            store.wipe_device(st.session_state)
            st.rerun()
    st.caption("Device wipe clears simulated packages and revokes active state.")

if device["wiped"]:
    st.error("This device was wiped. Re-enrol it to continue.")
    st.stop()

install_col, device_col = st.columns([1.2, 0.8], gap="large")

with install_col:
    st.subheader("Install an Application")
    st.button("Load demo example: risky flashlight", on_click=load_install_demo)

    with st.form("install_form"):
        app_name = st.text_input("App name", key="install_name", max_chars=60)
        app_type = st.selectbox("App type", sorted(rules.EXPECTED), key="install_type")
        permissions = st.multiselect(
            "Requested permissions", sorted(rules.WEIGHTS), key="install_perms"
        )
        check_install = st.form_submit_button("Check and install", type="primary")

    if check_install:
        try:
            clean_name = store.validate_app_name(app_name)
            analysis = analyze_app(app_type, permissions)
            pending = {
                "name": clean_name,
                "type": app_type,
                "permissions": list(permissions),
                "analysis": analysis,
            }
            if analysis["action"] == "Allow":
                store.install_app(
                    st.session_state, clean_name, app_type, permissions, analysis
                )
                store.clear_pending_install(st.session_state)
                st.success(
                    f"[ALLOW] {clean_name} installed successfully. Policy Risk: {analysis['level']} (Score: {analysis['score']})."
                )
            elif analysis["action"] == "Block":
                store.log_decision(
                    st.session_state,
                    "Install",
                    f"{clean_name} ({app_type}), score {analysis['score']}",
                    "Blocked",
                )
                store.clear_pending_install(st.session_state)
                st.error(
                    f"[BLOCK] Installation blocked by policy. Risk level: {analysis['level']} (Score: {analysis['score']})."
                )
            else:
                store.set_pending_install(st.session_state, pending)
                st.warning(
                    f"[REVIEW] Needs administrator review. Risk level: {analysis['level']} (Score: {analysis['score']})."
                )
        except ValueError as exc:
            st.error(str(exc))

    pending = store.get_pending_install(st.session_state)
    if pending:
        analysis = pending["analysis"]
        st.markdown(
            f"""
            <div class="soc-card" style="border-left: 3px solid var(--soc-accent);">
                <div class="soc-card-header">
                    <span>ADMINISTRATIVE APPROVAL QUEUE</span>
                    {ui.badge_html("NEEDS REVIEW", "review")}
                </div>
                <div style="font-size: 14px; font-weight: 600; margin-bottom: 6px;">
                    {pending['name']} <span style="font-size: 12px; color: var(--soc-text-secondary);">({pending['type']})</span>
                    &nbsp;·&nbsp; Calculated Risk Score: <code>{analysis['score']}</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.warning(
            f"Pending review: **{pending['name']}** ({pending['type']}) — score {analysis['score']}"
        )
        for reason in analysis["reasons"]:
            st.write(f"• {reason}")

        approve_col, reject_col = st.columns(2)
        if approve_col.button(
            "Approve install", type="primary", use_container_width=True
        ):
            store.install_app(
                st.session_state,
                pending["name"],
                pending["type"],
                pending["permissions"],
                analysis,
            )
            store.log_decision(
                st.session_state,
                "Approve",
                f"{pending['name']} ({pending['type']})",
                "Approved by admin",
            )
            store.clear_pending_install(st.session_state)
            st.rerun()
        if reject_col.button("Reject install", use_container_width=True):
            store.log_decision(
                st.session_state,
                "Reject",
                f"{pending['name']} ({pending['type']})",
                "Rejected by admin",
            )
            store.clear_pending_install(st.session_state)
            st.rerun()

with device_col:
    st.subheader("Installed Packages")
    current = store.get_device(st.session_state)["installed_apps"]
    if current:
        app_rows = [
            {
                "Package": app["name"],
                "Category": app["app_type"],
                "Risk Level": app.get("risk_level") or "—",
                "Score": app.get("risk_score") if app.get("risk_score") is not None else "—",
            }
            for app in current
        ]
        st.dataframe(app_rows, width="stretch", hide_index=True)
    else:
        st.caption("No packages currently installed on simulated endpoint.")

st.divider()

# Outbound Data Channel / DLP Inspection
st.subheader("Outbound Message Transmission Check")
st.caption("Scan outgoing simulated communication payload for sensitive patterns before dispatch.")

with st.form("send_form"):
    message = st.text_area(
        "Message to check",
        placeholder="Example: Call me on 9876543210",
        max_chars=MAX_TEXT_LENGTH + 1,
        height=110,
    )
    send = st.form_submit_button("Check and send", type="primary")

if send:
    try:
        result = scan_text(message)
        summary = summarize_findings(result["findings"])
        if result["action"] == "Allow":
            store.log_decision(st.session_state, "Send", summary, "Sent unchanged")
            st.success("[ALLOW] Clean payload. Outbound transmission permitted without modification.")
        elif result["action"] == "Mask":
            store.log_decision(st.session_state, "Send", summary, "Masked and sent")
            st.warning("[MASK] Sensitive pattern detected. Payload masked prior to transmission:")
            st.code(result["masked_text"])
        else:
            store.log_decision(st.session_state, "Send", summary, "Blocked")
            st.error("[BLOCK] High-risk pattern detected. Outbound message blocked.")
            findings_types = ", ".join(sorted({f["type"] for f in result["findings"]}))
            st.write(f"Detected Pattern Types: `{findings_types}`")

        if result["findings"]:
            st.caption(
                f"Evaluation: {len(result['findings'])} finding(s) identified. Raw payload values are excluded from audit records."
            )
    except ValueError as exc:
        st.error(str(exc))

st.divider()
st.subheader("Session Audit Trail")
logs = store.get_log(st.session_state)
if logs:
    st.dataframe(logs, width="stretch", hide_index=True)
else:
    st.write("No events yet. Try installing an app.")
