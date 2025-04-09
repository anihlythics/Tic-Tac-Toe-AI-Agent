import streamlit.web.cli as stcli
import sys

def test_app_runs(monkeypatch):
    """This is a smoke test to ensure the app launches."""
    monkeypatch.setattr(sys, "argv", ["streamlit", "run", "app.py"])
    try:
        stcli.main()
    except SystemExit:
        # Streamlit exits with sys.exit, which raises SystemExit
        pass