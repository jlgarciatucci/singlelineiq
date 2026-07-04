from pathlib import Path
import os

APP_NAME = os.getenv("APP_NAME", "SingleLineIQ")
USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"
USE_DEMO_SLD_EXTRACT = os.getenv("USE_DEMO_SLD_EXTRACT", "true").lower() == "true"
GEMINI_STRICT_MODE = os.getenv("GEMINI_STRICT_MODE", "false").lower() == "true"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
GEMINI_TIMEOUT_SECONDS = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "180"))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent
DATA_DIR = Path(os.getenv("DATA_DIR", str(REPO_ROOT / "data" / "synthetic"))).resolve()

CONSUMER_LIST_FILE = DATA_DIR / "SingleLineIQ_Consumer_List_v15_full_hierarchy.csv"
DESIGN_CRITERIA_FILE = DATA_DIR / "SingleLineIQ_Design_Criteria_v15_full_hierarchy.csv"
EXPECTED_TOPOLOGY_FILE = DATA_DIR / "SingleLineIQ_Expected_Inferred_Topology_v15_full_hierarchy.csv"
INJECTED_ISSUES_FILE = DATA_DIR / "SingleLineIQ_Injected_Issues_v15_full_hierarchy.csv"
SLD_EXTRACT_FILE = DATA_DIR / "SingleLineIQ_SLD_Expected_Visual_Extract_v15_full_hierarchy.csv"
SLD_PDF_FILE = DATA_DIR / "SingleLineDiagram.pdf"
