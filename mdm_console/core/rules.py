"""Centralized, explainable demo rules for the permission analyzer."""

WEIGHTS = {
    "ACCESS_FINE_LOCATION": 3,
    "READ_CONTACTS": 3,
    "RECORD_AUDIO": 3,
    "READ_SMS": 3,
    "READ_CALL_LOG": 3,
    "CAMERA": 2,
    "READ_EXTERNAL_STORAGE": 2,
}

EXPECTED = {
    "Flashlight": {"CAMERA"},
    "Calculator": set(),
    "Maps": {"ACCESS_FINE_LOCATION", "READ_EXTERNAL_STORAGE"},
    "Messaging": {"READ_CONTACTS", "READ_SMS", "RECORD_AUDIO", "CAMERA"},
    "Camera": {"CAMERA", "RECORD_AUDIO", "READ_EXTERNAL_STORAGE", "ACCESS_FINE_LOCATION"},
    "Game": set(),
}

def level_for_score(score: int) -> tuple[str, str]:
    """Map a demo risk score to a level and action."""
    if score == 0:
        return "Low", "Allow"
    if score <= 3:
        return "Medium", "Review"
    return "High", "Block"
