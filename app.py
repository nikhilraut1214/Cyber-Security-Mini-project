"""Operational Overview & Telemetry Dashboard for Mobile Endpoint Security Simulation."""

import streamlit as st
from core import store, rules, ui

st.set_page_config(
    page_title="Endpoint Security Console",
    layout="wide",
)

ui.apply_theme()
ui.render_sidebar_nav()
ui.render_simulation_banner()
ui.render_page_header(
    "ENDPOINT SECURITY & DLP CONSOLE",
    "Operational overview of simulated endpoint permissions, outbound data checks, and audit telemetry.",
)

device = store.get_device(st.session_state)
counts = store.get_counts(st.session_state)

# KPI row using actual data only
col1, col2, col3, col4 = st.columns(4)
status_str = "WIPED" if device["wiped"] else "ACTIVE"
col1.metric("Simulated Device", device["name"], delta=status_str, delta_color="normal" if not device["wiped"] else "inverse")
col2.metric("Installed Apps", counts["installed_apps"])
col3.metric("Blocked Installs", counts["blocked_installs"])
col4.metric("DLP Blocked/Masked Events", counts["masked_sends"] + counts["blocked_sends"])

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Two-column operational ledger and rules reference
left_col, right_col = st.columns([1.2, 0.8], gap="large")

with left_col:
    st.subheader("Simulated Device Ledger")
    status_badge = (
        ui.badge_html("WIPED", "block")
        if device["wiped"]
        else ui.badge_html("ACTIVE", "allow")
    )
    st.markdown(
        f"""
        <div style="font-size: 13px; color: var(--soc-text-secondary); margin-bottom: 8px;">
            Endpoint: <strong style="color: var(--soc-text-primary);">{device['name']}</strong>
            &nbsp;·&nbsp; Operational Status: {status_badge}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if device["installed_apps"]:
        app_rows = [
            {
                "Package Name": app["name"],
                "Category": app["app_type"],
                "Risk Level": app.get("risk_level") or "Not recorded",
                "Risk Score": app.get("risk_score") if app.get("risk_score") is not None else "—",
            }
            for app in device["installed_apps"]
        ]
        st.dataframe(app_rows, width="stretch", hide_index=True)
    else:
        st.caption("No apps installed yet. Open **MDM Console** to try installing a demo app.")

with right_col:
    st.subheader("Heuristic Policy Reference")
    st.caption("Static permission weights and category baselines applied by the policy engine.")
    with st.expander("Permission Risk Weights", expanded=True):
        weight_rows = [{"Permission": perm, "Weight": weight} for perm, weight in sorted(rules.WEIGHTS.items())]
        st.dataframe(weight_rows, width="stretch", hide_index=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

st.subheader("Audit Trail")
logs = store.get_log(st.session_state)
if logs:
    st.dataframe(logs, width="stretch", hide_index=True)
    st.download_button(
        "Export audit log as CSV",
        data=store.log_to_csv(st.session_state),
        file_name="mdm_audit_log.csv",
        mime="text/csv",
    )
else:
    st.write("No events yet. Try installing an app.")

with st.expander("Security Engine Details & Scope"):
    st.markdown(
        """
        - **Permission Risk Analyzer:** Evaluates requested Android permissions against category expectations. Score: `0` (Allow), `1–3` (Review), `>3` (Block).
        - **DLP-style Text Scanner:** Evaluates outbound text for Payment Card numbers (Luhn-validated), Grouped 12-digit ID patterns, Indian phone formats, and RFC-like email addresses.
        - **MDM Policy Enforcement:** Intercepts untrusted installs and high-risk outgoing text. Provides simulated device remote wipe capability.
        - **Audit Logging:** Records decision metadata, event type, and finding counts. Raw message content and matched card/ID values are never written to disk or logs.
        """
    )
