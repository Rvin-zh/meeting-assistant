import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

DATA_DIR = ROOT_DIR / "data"
MEETINGS_DIR = DATA_DIR / "meetings"
VECTORS_DIR = DATA_DIR / "vectors"
SYNTHETIC_DIR = DATA_DIR / "synthetic"

MEETINGS_DIR.mkdir(parents=True, exist_ok=True)
VECTORS_DIR.mkdir(parents=True, exist_ok=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
JIRA_SITE_URL = os.getenv("JIRA_SITE_URL", "https://arvinzaheri17.atlassian.net")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "KAN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "google:gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
