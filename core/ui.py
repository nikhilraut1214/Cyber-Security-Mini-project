"""Centralized UI/UX design system tokens, themes, and presentation components.

Follows the SOC Technical Minimal specification.
Pure presentation layer; no modifications to business logic or session storage.
"""

import streamlit as st

# Theme definitions with exact HEX palettes
THEMES = {
    "dark": {
        "name": "Dark (SOC)",
        "bg_base": "#0B0F17",
        "bg_surface": "#111827",
        "bg_subtle": "#161F30",
        "border": "#1F2937",
        "border_strong": "#374151",
        "text_primary": "#F9FAFB",
        "text_secondary": "#94A3B8",
        "text_muted": "#64748B",
        "accent": "#38BDF8",
        "accent_hover": "#7DD3FC",
        "code_bg": "#0D1117",
        "badge_allow_bg": "#064E3B",
        "badge_allow_text": "#6EE7B7",
        "badge_allow_border": "#047857",
        "badge_review_bg": "#451A03",
        "badge_review_text": "#FCD34D",
        "badge_review_border": "#B45309",
        "badge_block_bg": "#450A0A",
        "badge_block_text": "#FCA5A5",
        "badge_block_border": "#B91C1C",
        "badge_mask_bg": "#2E1065",
        "badge_mask_text": "#C4B5FD",
        "badge_mask_border": "#6D28D9",
        "badge_neutral_bg": "#1E293B",
        "badge_neutral_text": "#94A3B8",
        "badge_neutral_border": "#334155",
    },
    "light": {
        "name": "Light",
        "bg_base": "#F8FAFC",
        "bg_surface": "#FFFFFF",
        "bg_subtle": "#F1F5F9",
        "border": "#E2E8F0",
        "border_strong": "#CBD5E1",
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
        "text_muted": "#94A3B8",
        "accent": "#0284C7",
        "accent_hover": "#0369A1",
        "code_bg": "#F1F5F9",
        "badge_allow_bg": "#F0FDF4",
        "badge_allow_text": "#166534",
        "badge_allow_border": "#BBF7D0",
        "badge_review_bg": "#FFFBEB",
        "badge_review_text": "#92400E",
        "badge_review_border": "#FDE68A",
        "badge_block_bg": "#FEF2F2",
        "badge_block_text": "#991B1B",
        "badge_block_border": "#FECACA",
        "badge_mask_bg": "#F5F3FF",
        "badge_mask_text": "#5B21B6",
        "badge_mask_border": "#DDD6FE",
        "badge_neutral_bg": "#F1F5F9",
        "badge_neutral_text": "#334155",
        "badge_neutral_border": "#CBD5E1",
    },
}


def get_current_theme() -> str:
    """Return the active theme key from session state ('dark' or 'light')."""
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "dark"
    return st.session_state["theme_mode"]


def set_theme(theme_key: str) -> None:
    """Set the active theme mode."""
    if theme_key in THEMES:
        st.session_state["theme_mode"] = theme_key


def generate_css(theme_key: str) -> str:
    """Generate scoped CSS variables and base styles matching the theme."""
    t = THEMES[theme_key]
    return f"""
    <style>
    :root {{
        --soc-bg-base: {t['bg_base']};
        --soc-bg-surface: {t['bg_surface']};
        --soc-bg-subtle: {t['bg_subtle']};
        --soc-border: {t['border']};
        --soc-border-strong: {t['border_strong']};
        --soc-text-primary: {t['text_primary']};
        --soc-text-secondary: {t['text_secondary']};
        --soc-text-muted: {t['text_muted']};
        --soc-accent: {t['accent']};
        --soc-accent-hover: {t['accent_hover']};
        --soc-code-bg: {t['code_bg']};
    }}

    /* Base application surface styling */
    .stApp {{
        background-color: {t['bg_base']} !important;
        color: {t['text_primary']} !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }}

    /* Global typography overrides */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
        color: {t['text_primary']} !important;
        font-weight: 600 !important;
        letter-spacing: -0.015em !important;
    }}
    .stApp p, .stApp label, .stApp span, .stApp div {{
        color: {t['text_primary']};
    }}

    /* Sidebar surface */
    [data-testid="stSidebar"] {{
        background-color: {t['bg_surface']} !important;
        border-right: 1px solid {t['border']} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {t['text_primary']};
    }}

    /* Simulation Compliance Banner */
    .soc-env-banner {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 14px;
        background-color: {t['bg_subtle']};
        border: 1px solid {t['border']};
        border-radius: 4px;
        margin-bottom: 16px;
        font-size: 12px;
    }}
    .soc-env-badge {{
        display: inline-block;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 3px;
        background-color: {t['badge_neutral_bg']};
        color: {t['badge_neutral_text']};
        border: 1px solid {t['badge_neutral_border']};
        letter-spacing: 0.05em;
    }}
    .soc-env-meta {{
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 11px;
        color: {t['text_secondary']};
        letter-spacing: 0.02em;
    }}

    /* Technical Card Containers */
    .soc-card {{
        background-color: {t['bg_surface']};
        border: 1px solid {t['border']};
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 14px;
    }}
    .soc-card-header {{
        font-size: 11.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {t['text_secondary']};
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    /* KPI / Metric Card */
    .soc-kpi-card {{
        background-color: {t['bg_surface']};
        border: 1px solid {t['border']};
        border-radius: 6px;
        padding: 12px 14px;
        height: 100%;
    }}
    .soc-kpi-label {{
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {t['text_secondary']};
        margin-bottom: 4px;
    }}
    .soc-kpi-val {{
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 24px;
        font-weight: 700;
        color: {t['text_primary']};
        line-height: 1.2;
    }}
    .soc-kpi-sub {{
        font-size: 11.5px;
        color: {t['text_muted']};
        margin-top: 4px;
    }}

    /* Status Pill Badges (Text-only, no emojis) */
    .soc-badge {{
        display: inline-block;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 3px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        line-height: 1.4;
    }}
    .soc-badge-allow {{
        background-color: {t['badge_allow_bg']};
        color: {t['badge_allow_text']};
        border: 1px solid {t['badge_allow_border']};
    }}
    .soc-badge-review {{
        background-color: {t['badge_review_bg']};
        color: {t['badge_review_text']};
        border: 1px solid {t['badge_review_border']};
    }}
    .soc-badge-block {{
        background-color: {t['badge_block_bg']};
        color: {t['badge_block_text']};
        border: 1px solid {t['badge_block_border']};
    }}
    .soc-badge-mask {{
        background-color: {t['badge_mask_bg']};
        color: {t['badge_mask_text']};
        border: 1px solid {t['badge_mask_border']};
    }}
    .soc-badge-neutral {{
        background-color: {t['badge_neutral_bg']};
        color: {t['badge_neutral_text']};
        border: 1px solid {t['badge_neutral_border']};
    }}

    /* Verdict Card */
    .soc-verdict-card {{
        background-color: {t['bg_subtle']};
        border: 1px solid {t['border']};
        border-radius: 6px;
        padding: 14px 16px;
        margin-top: 10px;
        margin-bottom: 12px;
    }}
    .soc-verdict-title {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 6px;
    }}

    /* Streamlit Metric Box styling */
    [data-testid="stMetric"] {{
        background-color: {t['bg_surface']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {t['text_secondary']} !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}
    [data-testid="stMetricValue"] {{
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace !important;
        color: {t['text_primary']} !important;
        font-size: 22px !important;
    }}

    /* Form and Input styling */
    .stTextInput input, .stTextArea textarea, [data-baseweb="select"] {{
        background-color: {t['bg_surface']} !important;
        color: {t['text_primary']} !important;
        border-color: {t['border_strong']} !important;
        border-radius: 4px !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {t['accent']} !important;
    }}

    /* Dataframe table border and rounding */
    [data-testid="stDataFrame"], [data-testid="stTable"] {{
        border: 1px solid {t['border']} !important;
        border-radius: 4px !important;
        background-color: {t['bg_surface']} !important;
    }}

    /* Primary and Secondary buttons */
    .stButton button[kind="primary"] {{
        background-color: {t['accent']} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
    }}
    .stButton button[kind="primary"]:hover {{
        background-color: {t['accent_hover']} !important;
    }}
    .stButton button[kind="secondary"] {{
        background-color: {t['bg_surface']} !important;
        color: {t['text_primary']} !important;
        border: 1px solid {t['border_strong']} !important;
        border-radius: 4px !important;
    }}
    .stButton button[kind="secondary"]:hover {{
        background-color: {t['bg_subtle']} !important;
    }}

    /* Inline code blocks */
    code {{
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace !important;
        font-size: 12px !important;
        background-color: {t['code_bg']} !important;
        color: {t['text_primary']} !important;
        padding: 2px 5px !important;
        border-radius: 3px !important;
        border: 1px solid {t['border']} !important;
    }}
    pre code {{
        border: none !important;
    }}
    </style>
    """


def apply_theme() -> str:
    """Inject the active theme CSS and return the theme key."""
    theme_key = get_current_theme()
    st.markdown(generate_css(theme_key), unsafe_allow_html=True)
    return theme_key


def render_sidebar_nav() -> None:
    """Render centralized sidebar controls: theme switcher and environment info."""
    with st.sidebar:
        st.markdown(
            """
            <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--soc-text-secondary); margin-bottom: 8px;">
                DISPLAY THEME
            </div>
            """,
            unsafe_allow_html=True,
        )
        current_theme = get_current_theme()
        theme_index = 0 if current_theme == "dark" else 1
        selected = st.radio(
            "Select theme",
            options=["Dark (SOC)", "Light"],
            index=theme_index,
            label_visibility="collapsed",
            key="theme_radio_selector",
        )
        new_theme = "dark" if selected == "Dark (SOC)" else "light"
        if new_theme != current_theme:
            set_theme(new_theme)
            st.rerun()

        st.divider()
        st.markdown(
            """
            <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--soc-text-secondary); margin-bottom: 8px;">
                SYSTEM TELEMETRY
            </div>
            <div style="font-family: ui-monospace, monospace; font-size: 11.5px; line-height: 1.6; color: var(--soc-text-muted);">
                ENGINE: Heuristic v1.2<br>
                PROFILE: Android Sandbox<br>
                STORAGE: In-Memory Session<br>
                PRIVACY: Non-Attributed Log
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_simulation_banner() -> None:
    """Render a clean, professional SOC environment banner (replaces raw st.warning)."""
    st.markdown(
        """
        <div class="soc-env-banner">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="soc-env-badge">SIMULATION ENVIRONMENT</span>
                <span class="soc-env-meta">STATIC HEURISTIC RULE ENGINE · LOCAL DEMO DATA ONLY</span>
            </div>
            <span class="soc-badge soc-badge-neutral">LOCAL SIMULATION</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str) -> None:
    """Render consistent technical header."""
    st.markdown(
        f"""
        <div style="margin-bottom: 14px;">
            <h1 style="font-size: 22px; font-weight: 600; margin: 0; padding: 0; letter-spacing: -0.02em;">
                {title}
            </h1>
            <div style="font-size: 13px; color: var(--soc-text-secondary); margin-top: 3px;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge_html(text: str, kind: str = "neutral") -> str:
    """Return inline HTML for a text-based status pill badge."""
    kind_class = {
        "allow": "soc-badge-allow",
        "review": "soc-badge-review",
        "block": "soc-badge-block",
        "mask": "soc-badge-mask",
        "neutral": "soc-badge-neutral",
    }.get(kind.lower(), "soc-badge-neutral")
    return f'<span class="soc-badge {kind_class}">{text}</span>'
