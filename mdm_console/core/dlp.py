"""Rule-based DLP-style scanner for synthetic demo text only."""
import re
from collections import Counter

MAX_TEXT_LENGTH = 5000

# Card candidates accept spaces/hyphens; validity is checked with Luhn.
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){12,15}\d(?!\d)")
AADHAAR_RE = re.compile(r"(?<!\d)\d{4}[ -]\d{4}[ -]\d{4}(?!\d)")
PHONE_RE = re.compile(r"(?<!\d)(?:(?:\+?91)[ -]?)?[6-9]\d{4}[ -]?\d{5}(?!\d)")
EMAIL_RE = re.compile(r"(?i)(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])")

def _luhn_valid(number: str) -> bool:
    """Return whether a digit string passes the Luhn checksum."""
    digits = [int(char) for char in number if char.isdigit()]
    total = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return bool(digits) and total % 10 == 0

def _candidates(pattern, text, kind, validator=None):
    """Collect position-only findings that pass an optional candidate check."""
    matches = []
    for match in pattern.finditer(text):
        value = match.group()
        if validator is None or validator(value):
            matches.append({"type": kind, "start": match.start(), "end": match.end()})
    return matches

def scan_text(text: str) -> dict:
    """Detect, mask, or block sensitive-looking text without returning matched values."""
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError("Text is too long for this demo. Use under 5,000 characters.")

    candidates = []
    candidates += _candidates(CARD_RE, text, "card", lambda value: _luhn_valid(value))
    candidates += _candidates(AADHAAR_RE, text, "aadhaar_like")
    candidates += _candidates(PHONE_RE, text, "phone")
    candidates += _candidates(EMAIL_RE, text, "email")

    # Detection priority is card, ID-like, phone, email. Ignore overlapping later matches.
    priority = {"card": 0, "aadhaar_like": 1, "phone": 2, "email": 3}
    candidates.sort(key=lambda item: (item["start"], priority[item["type"]], -(item["end"] - item["start"])))
    findings = []
    for candidate in candidates:
        if any(candidate["start"] < item["end"] and candidate["end"] > item["start"] for item in findings):
            continue
        findings.append(candidate)
    findings.sort(key=lambda item: item["start"])

    masked = list(text)
    for finding in findings:
        for position in range(finding["start"], finding["end"]):
            masked[position] = "*"

    kinds = {finding["type"] for finding in findings}
    if kinds.intersection({"card", "aadhaar_like"}):
        action = "Block"
    elif findings:
        action = "Mask"
    else:
        action = "Allow"
    return {"findings": findings, "masked_text": "".join(masked), "action": action}

def summarize_findings(findings: list[dict]) -> str:
    """Format only finding types and counts for a privacy-safe audit detail."""
    counts = Counter(item["type"] for item in findings)
    if not counts:
        return "No sensitive patterns found"
    labels = [f"{count} {kind}" for kind, count in sorted(counts.items())]
    return ", ".join(labels)
