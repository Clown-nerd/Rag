
import os
from pathlib import Path

# Load environment variables from backend/.env when the package is imported.
# This makes OLLAMA_BASE_URL and model names available to modules that read
# them at import time.
def _load_dotenv():
	env_path = Path(__file__).resolve().parents[1] / ".env"
	if not env_path.exists():
		return
	try:
		text = env_path.read_text(encoding="utf-8")
	except Exception:
		return
	for line in text.splitlines():
		line = line.strip()
		if not line or line.startswith("#"):
			continue
		if "=" not in line:
			continue
		key, val = line.split("=", 1)
		key = key.strip()
		val = val.strip().strip('"').strip("'")
		if key and key not in os.environ:
			os.environ[key] = val


_load_dotenv()
