import streamlit as st
from core.dlp import scan_text, summarize_findings, MAX_TEXT_LENGTH

st.set_page_config(page_title="DLP-style Scanner", page_icon="🧪", layout="wide")
st.warning("Simulation: not a real MDM or DLP")
st.title("🧪 DLP-style Text Scanner")
st.write("Scan synthetic outgoing text for phone, email, card-like and grouped 12-digit ID-like patterns.")

if "scanner_demo_text" not in st.session_state:
    st.session_state["scanner_demo_text"] = "Call me on 9876543210 or mail test@example.com"
def load_demo():
    st.session_state["scanner_demo_text"] = "Call me on 9876543210 or mail test@example.com"

st.button("Load demo example", on_click=load_demo)
with st.form("scanner_form"):
    text_value = st.text_area("Text to scan (synthetic data only)", key="scanner_demo_text", max_chars=MAX_TEXT_LENGTH + 1, height=140)
    submitted = st.form_submit_button("Scan text", type="primary")
if submitted:
    try:
        result = scan_text(text_value)
        if result["action"] == "Allow":
            st.success("✅ Allow — no supported sensitive patterns found")
        elif result["action"] == "Mask":
            st.warning("🛡️ Mask — sensitive-looking text would be masked before sending")
            st.code(result["masked_text"])
        else:
            st.error("🛑 Block — high-risk sensitive-looking pattern found")
        st.write("**Finding summary:**", summarize_findings(result["findings"]))
        if result["findings"]:
            st.dataframe([{"Type": item["type"], "Start": item["start"], "End": item["end"]} for item in result["findings"]],
                         use_container_width=True, hide_index=True)
        st.caption("Limitations: harmless numbers can be flagged, obfuscated values can be missed, and only four pattern types are checked.")
    except ValueError as exc:
        st.error(str(exc))
