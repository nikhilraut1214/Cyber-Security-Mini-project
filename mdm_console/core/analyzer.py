"""Pure permission-risk analysis; no UI, storage, or network calls."""
from core import rules

def analyze_app(app_type: str, permissions: list[str]) -> dict:
    """Score permissions that are not expected for the selected app type."""
    if app_type not in rules.EXPECTED:
        choices = ", ".join(sorted(rules.EXPECTED))
        raise ValueError(f"Unknown app type '{app_type}'. Choose one of: {choices}.")

    if not isinstance(permissions, (list, tuple, set)):
        raise ValueError("Permissions must be provided as a list.")
    requested = list(dict.fromkeys(permissions))
    for permission in requested:
        if permission not in rules.WEIGHTS:
            raise ValueError(f"Unknown permission '{permission}'.")

    expected = rules.EXPECTED[app_type]
    unexpected = [permission for permission in requested if permission not in expected]
    score = sum(rules.WEIGHTS[permission] for permission in unexpected)
    level, action = rules.level_for_score(score)
    reasons = [
        f"{permission} is not needed by a {app_type} app (weight {rules.WEIGHTS[permission]})"
        for permission in unexpected
    ]
    if not reasons:
        reasons = [f"All requested permissions are expected for a {app_type} app."]
    return {
        "app_type": app_type,
        "requested": requested,
        "unexpected": unexpected,
        "score": score,
        "level": level,
        "reasons": reasons,
        "action": action,
    }
