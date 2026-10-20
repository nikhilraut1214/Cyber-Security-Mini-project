import pytest
from core.dlp import scan_text

def test_phone_is_masked():
    result = scan_text("Call me on 9876543210")
    assert result["action"] == "Mask"
    assert [f["type"] for f in result["findings"]] == ["phone"]
    assert result["masked_text"] == "Call me on **********"

def test_email_is_masked():
    result = scan_text("mail test@example.com")
    assert result["action"] == "Mask"
    assert [f["type"] for f in result["findings"]] == ["email"]
    assert "*" in result["masked_text"]
    assert "test@example.com" not in result["masked_text"]

def test_fake_luhn_card_is_blocked():
    result = scan_text("card 4111 1111 1111 1111")
    assert result["action"] == "Block"
    assert [f["type"] for f in result["findings"]] == ["card"]

def test_grouped_id_like_number_is_blocked():
    result = scan_text("ref 1234 5678 9012")
    assert result["action"] == "Block"
    assert [f["type"] for f in result["findings"]] == ["aadhaar_like"]

def test_non_luhn_16_digit_number_is_not_card():
    result = scan_text("order 1234567890123456")
    assert result["action"] == "Allow"
    assert result["findings"] == []

def test_plain_text_is_allowed():
    result = scan_text("see you at 5 pm")
    assert result["action"] == "Allow"
    assert result["findings"] == []

def test_empty_text_is_allowed():
    assert scan_text("") == {"findings": [], "masked_text": "", "action": "Allow"}

def test_text_over_limit_is_rejected():
    with pytest.raises(ValueError, match="under 5,000"):
        scan_text("x" * 5001)

def test_findings_do_not_include_matched_values():
    result = scan_text("Call 9876543210")
    assert set(result["findings"][0]) == {"type", "start", "end"}

def test_phone_with_country_prefix_is_masked():
    result = scan_text("Call +91 9876543210")
    assert result["action"] == "Mask"
    assert len(result["findings"]) == 1

def test_phone_written_with_spaces_is_masked():
    result = scan_text("Call +91 98765 43210")
    assert result["action"] == "Mask"
    assert [f["type"] for f in result["findings"]] == ["phone"]
    assert "98765" not in result["masked_text"]

def test_hyphenated_id_like_number_is_blocked():
    result = scan_text("ref 1234-5678-9012")
    assert result["action"] == "Block"
    assert [f["type"] for f in result["findings"]] == ["aadhaar_like"]

def test_spaced_card_is_still_a_card_not_a_phone():
    result = scan_text("card 6011 1111 1111 1117")
    assert [f["type"] for f in result["findings"]] == ["card"]
    assert result["action"] == "Block"

def test_unspaced_12_digit_number_is_a_documented_miss():
    # Known limit: 12 digits with no separators are not treated as ID-like.
    assert scan_text("ref 123456789012")["action"] == "Allow"
