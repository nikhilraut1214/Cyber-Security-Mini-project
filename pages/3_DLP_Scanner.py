"""Outbound Data Leakage Prevention (DLP) Text Pattern Scanner."""

import streamlit as st
from core import ui
from core.dlp import scan_text, summarize_findings, MAX_TEXT_LENGTH

st.set_page_config(page_title="DLP Text Scanner", layout="wide")

ui.apply_theme()
ui.render_sidebar_nav()
ui.render_simulation_banner()
ui.render_page_header(
    "Outbound DLP Text Scanner",
    "Inspect synthetic outgoing text for payment cards, 12-digit ID patterns, phone numbers, and email addresses.",
)

if "scanner_demo_text" not in st.session_state:
    st.session_state["scanner_demo_text"] = "Call me on 9876543210 or mail test@example.com"


def load_demo():
    """Fill the text area with a synthetic benchmark example containing multiple pattern types."""
    st.session_state["scanner_demo_text"] = "Call me on 9876543210 or mail test@example.com"


input_col, output_col = st.columns([1.15, 0.85], gap="large")

with input_col:
    st.subheader("Payload Inspection Workspace")
    st.button("Load demo example", on_click=load_demo)

    with st.form("scanner_form"):
        text_value = st.text_area(
            "Text to scan (synthetic data only)",
            key="scanner_demo_text",
            max_chars=MAX_TEXT_LENGTH + 1,
            height=140,
        )
        submitted = st.form_submit_button("Scan text", type="primary")

    # Detection Heuristics Reference Card
    st.markdown(
        f"""
        <div class="soc-card">
            <div class="soc-card-header">
                <span>Active Pattern Detection Engines</span>
                {ui.badge_html("Heuristics", "neutral")}
            </div>
            <div style="font-size: 13.5px; line-height: 1.7; color: var(--soc-text-secondary);">
                • <strong>Payment Card:</strong> 13–16 digits with Luhn checksum validation &rarr; {ui.badge_html("Block", "block")}<br>
                • <strong>12-digit ID-like Pattern:</strong> Grouped 4-4-4 digit format &rarr; {ui.badge_html("Block", "block")}<br>
                • <strong>Phone Number:</strong> 10-digit format with optional +91 prefix &rarr; {ui.badge_html("Mask", "mask")}<br>
                • <strong>Email Pattern:</strong> Standard user@domain format &rarr; {ui.badge_html("Mask", "mask")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with output_col:
    st.subheader("Inspection Telemetry & Output")
    if submitted:
        try:
            result = scan_text(text_value)
            action = result["action"]
            findings = result["findings"]
            summary = summarize_findings(findings)

            # Unified single disposition alert
            if action == "Allow":
                st.success(f"Policy Action: Allow — {summary}")
            elif action == "Mask":
                st.warning(f"Policy Action: Mask — {summary}")
                st.markdown("**Sanitized Outbound Payload (Asterisk Masked):**")
                st.code(result["masked_text"])
            else:
                st.error(f"Policy Action: Block — {summary}")

            if findings:
                st.markdown("**Detected Entity Offsets (Zero-Retention):**")
                finding_rows = [
                    {
                        "Pattern Type": item["type"],
                        "Start Offset": item["start"],
                        "End Offset": item["end"],
                        "Span (chars)": item["end"] - item["start"],
                    }
                    for item in findings
                ]
                st.dataframe(
                    finding_rows,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Pattern Type": st.column_config.TextColumn("Pattern Type", width="medium"),
                        "Start Offset": st.column_config.NumberColumn("Start Offset", format="%d", width="small"),
                        "End Offset": st.column_config.NumberColumn("End Offset", format="%d", width="small"),
                        "Span (chars)": st.column_config.NumberColumn("Span (chars)", format="%d", width="small"),
                    },
                )

            st.caption(
                "Privacy constraint: Only pattern categories and counts are recorded in the audit log; "
                "raw payload strings and matched values are discarded immediately to preserve data privacy. "
                "Limitations: Formatted numbers may trigger false positives; obfuscated values may be missed."
            )
        except ValueError as exc:
            st.error(str(exc))
    else:
        st.info("Enter synthetic text or load the benchmark example, then click 'Scan text' to evaluate.")
