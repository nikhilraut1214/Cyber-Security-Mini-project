"""Session-state helpers. All device and audit state mutations live here."""
from datetime import datetime
import csv
import io
import re
from core.dlp import scan_text

def _ensure_state(state):
    state.setdefault("device", {"name": "Student Phone", "installed_apps": [], "wiped": False})
    state.setdefault("audit_log", [])
    state.setdefault("pending_install", None)

def get_device(state) -> dict:
    _ensure_state(state)
    return state["device"]

def validate_app_name(name) -> str:
    """Return the cleaned app name, or raise ValueError. Used by the page and the store."""
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 60:
        raise ValueError("Enter an app name between 1 and 60 characters.")
    clean = name.strip()
    # Avoid placing sensitive-looking user input into app state or the audit log.
    if scan_text(clean)["findings"]:
        raise ValueError("App name contains a sensitive-looking pattern. Use a simple demo label.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 _().-]*", clean):
        raise ValueError("Use letters, numbers, spaces, parentheses, periods, underscores, or hyphens in the app name.")
    return clean

def install_app(state, name, app_type, permissions, analysis=None) -> None:
    _ensure_state(state)
    name = validate_app_name(name)
    device = state["device"]
    if device["wiped"]:
        raise ValueError("This device was wiped. Re-enrol it before installing apps.")
    record = {
        "name": name.strip(),
        "app_type": app_type,
        "permissions": list(permissions),
        "risk_level": analysis.get("level") if analysis else None,
        "risk_score": analysis.get("score") if analysis else None,
    }
    device["installed_apps"] = [
        app for app in device["installed_apps"]
        if not (app["name"].casefold() == record["name"].casefold() and app["app_type"] == app_type)
    ]
    device["installed_apps"].append(record)
    add_log(state, "Install", f"{record['name']} ({app_type})", "Installed")

def wipe_device(state) -> None:
    _ensure_state(state)
    state["device"]["installed_apps"] = []
    state["device"]["wiped"] = True
    state["pending_install"] = None
    add_log(state, "Wipe", "Installed app list cleared", "Device wiped")

def reenrol_device(state) -> None:
    _ensure_state(state)
    state["device"]["wiped"] = False
    add_log(state, "Re-enrol", "Device re-enrolled", "Active")

def add_log(state, event, detail, result) -> None:
    _ensure_state(state)
    # Detail is supplied by callers and must never contain message text or matched values.
    row = {
        "time": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "event": str(event),
        "detail": str(detail),
        "result": str(result),
    }
    state["audit_log"].insert(0, row)

def get_log(state) -> list[dict]:
    _ensure_state(state)
    return list(state["audit_log"])

def log_to_csv(state) -> str:
    _ensure_state(state)
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=["time", "event", "detail", "result"])
    writer.writeheader()
    writer.writerows(state["audit_log"])
    return output.getvalue()

def get_counts(state) -> dict:
    _ensure_state(state)
    rows = state["audit_log"]
    return {
        "installed_apps": len(state["device"]["installed_apps"]),
        "blocked_installs": sum(row["event"] == "Install" and row["result"] == "Blocked" for row in rows),
        "masked_sends": sum(row["event"] == "Send" and row["result"] == "Masked and sent" for row in rows),
        "blocked_sends": sum(row["event"] == "Send" and row["result"] == "Blocked" for row in rows),
        "total_events": len(rows),
    }

def set_pending_install(state, pending) -> None:
    _ensure_state(state)
    state["pending_install"] = pending

def get_pending_install(state):
    _ensure_state(state)
    return state["pending_install"]

def clear_pending_install(state) -> None:
    _ensure_state(state)
    state["pending_install"] = None

def log_decision(state, event, detail, result) -> None:
    """Public helper for safe decision logging from UI flows."""
    add_log(state, event, detail, result)
