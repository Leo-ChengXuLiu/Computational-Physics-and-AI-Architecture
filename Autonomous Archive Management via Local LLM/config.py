import os

# API Configurations
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_ENDPOINT = f"{OLLAMA_HOST}/api/generate"
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")

# Directory Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INBOX_DIR = os.path.join(BASE_DIR, "_Inbox")
DEFAULT_FALLBACK_FOLDER = "Uncategorized"