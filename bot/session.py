from pathlib import Path

SESSION_FILE = Path("session.json")


def session_exists():

    return SESSION_FILE.exists()