from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_web_dashboard_assets_exist() -> None:
    web_root = ROOT / "dashboard" / "web"

    assert (web_root / "index.html").exists()
    assert (web_root / "styles.css").exists()
    assert (web_root / "app.js").exists()


def test_web_dashboard_contains_interactive_controls() -> None:
    html = (ROOT / "dashboard" / "web" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "dashboard" / "web" / "app.js").read_text(encoding="utf-8")

    assert 'id="refreshButton"' in html
    assert 'id="mockButton"' in html
    assert "renderSnapshot" in script
    assert "refreshBackendHealth" in script

