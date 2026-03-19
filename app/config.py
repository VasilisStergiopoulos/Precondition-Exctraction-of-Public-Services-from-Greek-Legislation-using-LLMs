from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

CSV_PATH = INPUT_DIR / "process-conditions.csv"
PDF_DIR = OUTPUT_DIR / "pdfs"
TEXT_DIR = OUTPUT_DIR / "texts"
JSON_DIR = OUTPUT_DIR / "json"

MITOS_API_BASE = "https://api.digigov.grnet.gr/v1/services"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

REQUEST_TIMEOUT = 30

for folder in [OUTPUT_DIR, PDF_DIR, TEXT_DIR, JSON_DIR]:
    folder.mkdir(parents=True, exist_ok=True)