import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_official_color_palette_tokens():
    """Verify all 11 official Peacock brand colors from Section 8.2 exist in CSS."""
    with open("app/static/css/peacock.css", "r", encoding="utf-8") as f:
        css = f.read().upper()
    
    official_colors = {
        "ROYAL_PEACOCK_BLUE": "#063B78",
        "TURQUOISE_BLUE": "#1688C1",
        "EMERALD_GREEN": "#006B45",
        "DEEP_PEACOCK_GREEN": "#1B4A35",
        "LEAF_GREEN": "#4A7640",
        "PEACOCK_FEATHER_GOLD": "#C5A76B",
        "DARK_EMERALD": "#003B36",
        "CHAMPAGNE_GOLD": "#D6B875",
        "IVORY_CREAM": "#F1E4C8",
        "WARM_CHARCOAL": "#49443F",
        "WARM_TAUPE": "#B8B0A0",
    }
    
    for name, hex_code in official_colors.items():
        assert hex_code in css, f"Official color {name} ({hex_code}) missing from peacock.css"

def test_light_mode_black_text_contrast():
    """Verify Light Mode mandates black text (#000000) for high readability."""
    with open("app/static/css/peacock.css", "r", encoding="utf-8") as f:
        css = f.read()
    
    assert "--color-text-main: #000000;" in css
    assert "#000000 !important" in css

def test_dark_mode_white_text_contrast():
    """Verify Dark Mode mandates white text (#ffffff) for high readability."""
    with open("app/static/css/peacock.css", "r", encoding="utf-8") as f:
        css = f.read()
    
    assert "--color-text-main: #ffffff;" in css
    assert "#ffffff !important" in css

def test_dark_mode_avoids_pure_black_backgrounds():
    """Verify Dark Mode utilizes Deep Peacock Green (#1B4A35) and Dark Emerald (#003B36) instead of pure black."""
    with open("app/static/css/peacock.css", "r", encoding="utf-8") as f:
        css = f.read()
    
    assert "--color-surface: #003B36;" in css
    assert "var(--color-dark-emerald)" in css

def test_theme_switcher_script_and_persistence():
    """Verify theme switcher functions and localStorage persistence in JS."""
    with open("app/static/js/peacock.js", "r", encoding="utf-8") as f:
        js = f.read()
    
    assert "togglePeacockTheme" in js
    assert "setPeacockTheme" in js
    assert "applyPeacockTheme" in js
    assert "peacock-theme" in js
    assert "data-bs-theme" in js

def test_navbar_theme_toggle_button_rendered():
    """Verify visible theme switcher button is present in rendered navigation."""
    response = client.get("/")
    assert response.status_code == 200
    assert "theme-toggle-btn" in response.text
    assert "togglePeacockTheme()" in response.text
    assert "theme-toggle-icon" in response.text
