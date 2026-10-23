"""Headless checks of the Streamlit pages using Streamlit's AppTest."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
HOME = str(ROOT / "app.py")
CONSOLE = str(ROOT / "pages" / "1_MDM_Console.py")
ANALYZER = str(ROOT / "pages" / "2_Permission_Analyzer.py")
SCANNER = str(ROOT / "pages" / "3_DLP_Scanner.py")
RISKY = ["ACCESS_FINE_LOCATION", "CAMERA", "READ_CONTACTS"]

def start(path):
    return AppTest.from_file(path, default_timeout=30).run()

def click(at, text):
    [b for b in at.button if text in b.label][0].click().run()

def test_all_pages_load_without_errors():
    for path in (HOME, CONSOLE, ANALYZER, SCANNER):
        assert not start(path).exception

def test_console_starts_with_risky_flashlight_filled_in():
    at = start(CONSOLE)
    assert at.selectbox(key="install_type").value == "Flashlight"
    assert sorted(at.multiselect(key="install_perms").value) == RISKY

def test_console_demo_button_restores_the_example():
    at = start(CONSOLE)
    at.selectbox(key="install_type").select("Calculator").run()
    at.multiselect(key="install_perms").set_value([]).run()
    assert at.selectbox(key="install_type").value == "Calculator"
    click(at, "Load demo example")
    assert at.selectbox(key="install_type").value == "Flashlight"
    assert sorted(at.multiselect(key="install_perms").value) == RISKY

def test_risky_flashlight_is_blocked_and_not_installed():
    at = start(CONSOLE)
    click(at, "Check and install")
    assert any("blocked" in e.value.lower() for e in at.error)
    assert at.session_state["device"]["installed_apps"] == []

def test_review_then_approve_installs_the_app():
    at = start(CONSOLE)
    at.multiselect(key="install_perms").set_value(["CAMERA", "ACCESS_FINE_LOCATION"]).run()
    click(at, "Check and install")
    assert any("review" in w.value.lower() for w in at.warning)
    click(at, "Approve")
    assert [a["name"] for a in at.session_state["device"]["installed_apps"]] == ["Flashlight"]

def test_hyphenated_app_name_is_accepted_on_the_page():
    at = start(CONSOLE)
    at.text_input(key="install_name").set_value("Torch-Pro").run()
    at.selectbox(key="install_type").select("Calculator").run()
    at.multiselect(key="install_perms").set_value([]).run()
    click(at, "Check and install")
    assert [a["name"] for a in at.session_state["device"]["installed_apps"]] == ["Torch-Pro"]

def test_sensitive_looking_app_name_is_rejected():
    at = start(CONSOLE)
    at.text_input(key="install_name").set_value("9876543210").run()
    click(at, "Check and install")
    assert at.error
    assert at.session_state["device"]["installed_apps"] == []

def test_audit_log_never_holds_raw_values():
    at = start(CONSOLE)
    for text in ("Call me on 9876543210", "card 4111 1111 1111 1111"):
        at.text_area[0].set_value(text).run()
        click(at, "Check and send")
    log_text = str(at.session_state["audit_log"])
    assert "9876543210" not in log_text and "4111" not in log_text
    assert len(at.session_state["audit_log"]) == 2

def test_analyzer_demo_button_fills_the_risky_example():
    at = start(ANALYZER)
    at.selectbox(key="pa_type").select("Calculator").run()
    click(at, "Load flashlight demo")
    assert at.selectbox(key="pa_type").value == "Flashlight"
    assert sorted(at.multiselect(key="pa_perms").value) == RISKY


def test_theme_switcher_toggles_mode_without_error():
    at = start(HOME)
    assert not at.exception
    assert at.radio(key="theme_radio_selector").value == "Dark (SOC)"
    at.radio(key="theme_radio_selector").set_value("Light").run()
    assert not at.exception
    assert at.session_state["theme_mode"] == "light"


