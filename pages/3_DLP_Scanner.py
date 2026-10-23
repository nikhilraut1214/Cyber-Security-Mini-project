"""Outbound Data Leakage Prevention (DLP) Text Pattern Scanner."""

import streamlit as st
from core import ui
from core.dlp import scan_text, summarize_findings, MAX_TEXT_LENGTH

st.set_page_config(page_title="DLP Text Scanner", layout="wide")

ui.apply_theme()
ui.render_sidebar_nav()
ui.render_simulation_banner()
ui.render_page_header(
    "OUTBOUND DLP TEXT SCANNER",
    "Inspect synthetic outgoing text for payment cards, 12-digit ID patterns, phone numbers, and email addresses.",
)

if "scanner_demo_text" not in st.session_state:
    st.session_state["scanner_demo_text"] = "Call me on 9876543210 or mail test@example.com"


def load_demo():
    """Fill the text area with a synthetic benchmark example containing multiple pattern types."""
    st.session_state["scanner_demo_text"] = "Call me on 9876543210 or mail test@example.com"


input_col, output_col = st.columns([1.1, 0.9], gap="large")

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
                <span>ACTIVE PATTERN DETECTION ENGINES</span>
                {ui.badge_html("HEURISTICS", "neutral")}
            </div>
            <div style="font-size: 12px; line-height: 1.6; color: var(--soc-text-secondary);">
                • <strong>Payment Card:</strong> 13–16 digits with Luhn checksum validation &rarr; {ui.badge_html("BLOCK", "block")}<br>
                • <strong>12-digit ID-like Pattern:</strong> Grouped 4-4-4 digit format &rarr; {ui.badge_html("BLOCK", "block")}<br>
                • <strong>Phone Number:</strong> 10-digit format with optional +91 prefix &rarr; {ui.badge_html("MASK", "mask")}<br>
                • <strong>Email Pattern:</strong> Standard user@domain format &rarr; {ui.badge_html("MASK", "mask")}
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

            badge_kind = {
                "Allow": "allow",
                "Mask": "mask",
                "Block": "block",
            }.get(action, "neutral")

            st.markdown(
                f"""
                <div class="soc-card" style="border-left: 3px solid var(--soc-accent);">
                    <div class="soc-card-header">
                        <span>POLICY DISPOSITION</span>
                        {ui.badge_html(f"{action.upper()}", badge_kind)}
                    </div>
                    <div style="font-size: 14px; font-weight: 600; color: var(--soc-text-primary); margin: 6px 0;">
                        {summary}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Standard messages for accessibility and test consistency
            if action == "Allow":
                st.success("Action: Allow — No supported sensitive patterns detected.")
            elif action == "Mask":
                st.warning("Action: Mask — Sensitive pattern detected. Payload masked before dispatch:")
                st.code(result["masked_text"])
            else:
                st.error("Action: Block — High-risk pattern detected. Outbound dispatch blocked.")

            if findings:
                st.markdown("**Detected Entity Offsets (Zero-Retention):**")
                finding_rows = [
                    {
                        "Pattern Type": item["type"],
                        "Start Index": item["start"],
                        "End Index": item["end"],
                        "Span (chars)": item["end"] - item["start"],
                    }
                    for item in findings
                ]
                st.dataframe(finding_rows, width="stretch", hide_index=True)

            st.caption(
                "Privacy constraint: Only pattern categories and counts are recorded in the audit log; "
                "raw payload strings and matched values are discarded immediately to preserve data privacy. "
                "Limitations: Formatted numbers may trigger false positives; obfuscated values may be missed."
            )
        except ValueError as exc:
            st.error(str(exc))
    else:
        st.info("Enter synthetic text or load the benchmark example, then click 'Scan text' to evaluate.")
