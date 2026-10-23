"""Tests for core/ui.py design tokens, theme switching, and presentation helpers."""

from core import ui


def test_themes_definition_contains_required_keys():
    assert "dark" in ui.THEMES
    assert "light" in ui.THEMES
    for theme_key in ("dark", "light"):
        t = ui.THEMES[theme_key]
        assert "bg_base" in t
        assert "bg_surface" in t
        assert "border" in t
        assert "text_primary" in t
        assert "accent" in t


def test_theme_state_default_and_setter():
    state = {}
    import streamlit as st

    original_state = getattr(st, "session_state", {})
    # Verify setter logic
    ui.set_theme("light")
    assert ui.get_current_theme() == "light"
    ui.set_theme("dark")
    assert ui.get_current_theme() == "dark"


def test_generate_css_returns_non_empty_css():
    css_dark = ui.generate_css("dark")
    assert "--soc-bg-base" in css_dark
    assert ui.THEMES["dark"]["bg_base"] in css_dark

    css_light = ui.generate_css("light")
    assert "--soc-bg-base" in css_light
    assert ui.THEMES["light"]["bg_base"] in css_light


def test_badge_html_generates_valid_span():
    badge = ui.badge_html("ALLOW", "allow")
    assert "soc-badge" in badge
    assert "soc-badge-allow" in badge
    assert "ALLOW" in badge

    badge_block = ui.badge_html("BLOCK", "block")
    assert "soc-badge-block" in badge_block
