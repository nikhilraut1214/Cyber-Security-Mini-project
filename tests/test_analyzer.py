import pytest
from core.analyzer import analyze_app

def test_calculator_no_permissions_is_low_allow():
    result = analyze_app("Calculator", [])
    assert (result["level"], result["action"], result["score"]) == ("Low", "Allow", 0)

def test_flashlight_camera_is_expected():
    result = analyze_app("Flashlight", ["CAMERA"])
    assert (result["level"], result["action"], result["score"]) == ("Low", "Allow", 0)

def test_flashlight_location_needs_review():
    result = analyze_app("Flashlight", ["CAMERA", "ACCESS_FINE_LOCATION"])
    assert (result["level"], result["action"], result["score"]) == ("Medium", "Review", 3)
    assert result["unexpected"] == ["ACCESS_FINE_LOCATION"]

def test_flashlight_location_and_contacts_is_blocked():
    result = analyze_app("Flashlight", ["CAMERA", "ACCESS_FINE_LOCATION", "READ_CONTACTS"])
    assert (result["level"], result["action"], result["score"]) == ("High", "Block", 6)

def test_maps_location_is_expected():
    result = analyze_app("Maps", ["ACCESS_FINE_LOCATION"])
    assert (result["level"], result["action"], result["score"]) == ("Low", "Allow", 0)

def test_messaging_unexpected_call_log_needs_review():
    result = analyze_app("Messaging", ["READ_CONTACTS", "READ_SMS", "READ_CALL_LOG"])
    assert (result["level"], result["action"], result["score"]) == ("Medium", "Review", 3)

def test_unknown_app_type_raises():
    with pytest.raises(ValueError, match="Unknown app type"):
        analyze_app("Unknown", [])

def test_unknown_permission_raises():
    with pytest.raises(ValueError, match="Unknown permission"):
        analyze_app("Calculator", ["BLUETOOTH"])
