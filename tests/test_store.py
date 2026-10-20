import csv
import io
from core import store

def fresh_state():
    return {}

def test_get_device_initializes_default():
    device = store.get_device(fresh_state())
    assert device == {"name": "Student Phone", "installed_apps": [], "wiped": False}

def test_install_app_adds_app_and_log():
    state = fresh_state()
    store.install_app(state, "Calculator", "Calculator", [], {"level": "Low", "score": 0})
    assert len(store.get_device(state)["installed_apps"]) == 1
    assert store.get_log(state)[0]["event"] == "Install"

def test_wipe_clears_apps_and_marks_wiped():
    state = fresh_state()
    store.install_app(state, "Calculator", "Calculator", [])
    store.wipe_device(state)
    assert store.get_device(state)["installed_apps"] == []
    assert store.get_device(state)["wiped"] is True
    assert store.get_log(state)[0]["event"] == "Wipe"

def test_reenrol_allows_device_to_be_active():
    state = fresh_state()
    store.wipe_device(state)
    store.reenrol_device(state)
    assert store.get_device(state)["wiped"] is False
    assert store.get_log(state)[0]["event"] == "Re-enrol"

def test_newest_log_row_is_first():
    state = fresh_state()
    store.add_log(state, "Install", "A", "Installed")
    store.add_log(state, "Send", "No sensitive patterns found", "Sent")
    assert store.get_log(state)[0]["event"] == "Send"

def test_csv_has_header_and_rows():
    state = fresh_state()
    store.add_log(state, "Send", "1 phone", "Masked and sent")
    rows = list(csv.DictReader(io.StringIO(store.log_to_csv(state))))
    assert len(rows) == 1
    assert list(rows[0]) == ["time", "event", "detail", "result"]

def test_counts_include_blocked_installs_and_sends():
    state = fresh_state()
    store.log_decision(state, "Install", "Flashlight", "Blocked")
    store.log_decision(state, "Send", "1 card", "Blocked")
    store.log_decision(state, "Send", "1 phone", "Masked and sent")
    counts = store.get_counts(state)
    assert counts["blocked_installs"] == 1
    assert counts["blocked_sends"] == 1
    assert counts["masked_sends"] == 1

def test_install_is_rejected_after_wipe():
    state = fresh_state()
    store.wipe_device(state)
    try:
        store.install_app(state, "Calculator", "Calculator", [])
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Re-enrol" in str(exc)


def test_sensitive_looking_app_name_is_rejected():
    state = fresh_state()
    try:
        store.install_app(state, "App 9876543210", "Calculator", [])
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "sensitive-looking" in str(exc)

import pytest

def test_validate_app_name_accepts_simple_labels():
    assert store.validate_app_name("  Torch-Pro  ") == "Torch-Pro"
    assert store.validate_app_name("My_App (v2).1") == "My_App (v2).1"

@pytest.mark.parametrize("bad", ["", "   ", "x" * 61, "9876543210", "<script>", "-start"])
def test_validate_app_name_rejects_bad_labels(bad):
    with pytest.raises(ValueError):
        store.validate_app_name(bad)

def test_install_app_uses_same_name_rule_as_the_page():
    state = {}
    store.install_app(state, "Torch-Pro", "Flashlight", ["CAMERA"])
    assert store.get_device(state)["installed_apps"][0]["name"] == "Torch-Pro"
