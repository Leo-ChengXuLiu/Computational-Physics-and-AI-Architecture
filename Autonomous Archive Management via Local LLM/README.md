# 🤖 Autonomous Archive Management via Local LLM

An intelligent, autonomous workflow tool designed to dynamically categorize, manage, and version-control graduate-level theoretical physics manuscripts using a localized Large Language Model.

## Architecture

```text
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌────────────┐
│   _Inbox/   │───▶│ auto_organize.py │───▶│  Ollama API  │───▶│ Git CI/CD  │
│ (Raw Files) │    │ (Python Script)  │    │   (llama3)   │    │ (Push/Sync)│
└─────────────┘    └──────────────────┘    └──────────────┘    └────────────┘
                             │                     │                 ▲
                             ▼                     ▼                 │
                       Dir Monitoring    Semantic Categorization ────┘
```

**Pipeline:** File Detection (`_Inbox`) → LLM Semantic Routing → System File Move → Automated Git Sync

## Modules

| File / Directory | Purpose |
|---|---|
| `auto_organize.py` | Main orchestrator — integrates LLM requests, file I/O operations, and Git subprocesses |
| `_Inbox/` | Designated drop-zone for unorganized, raw physics manuscripts and notes |
| `requirements.txt` | Python dependencies (HTTP requests for local API) |

## Prerequisites

- **Python 3.8+**
- **Ollama** installed locally for privacy-first, zero-latency inference
- Git CLI configured for your local repository

## Setup

```bash
# 1. Start Ollama and pull the target model (if not already installed)
ollama pull llama3
ollama serve

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Drop raw note files (e.g., 'triso fuel.pdf') into the _Inbox folder

# 4. Execute the autonomous agent
python auto_organize.py
```

## Configuration

Core variables are currently configured directly within the script's configuration zone:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Local Ollama API endpoint |
| `MODEL_NAME` | `llama3` | The target LLM engine used for categorisation |
| `INBOX_DIR` | `_Inbox` | Target directory for monitoring new files |
| `DEFAULT_FOLDER` | `Uncategorized` | Fallback routing directory if LLM inference fails |

## Running the Agent

The script is designed for single-execution or cron-job scheduling. Run it directly from the terminal to process the inbox and trigger the sync:

```bash
cd LLM_Workflow_Automation
python auto_organize.py
```
*(The terminal will output the AI's decision process, the physical file movement, and the Git commit status).*

## Skills Demonstrated

- **Local LLM Deployment** — Interfacing directly with locally hosted AI models (Ollama) without relying on external APIs.
- **Prompt Engineering** — Designing strictly bounded, deterministic prompts for accurate taxonomy and JSON/text routing.
- **Git CI/CD Automation** — Scripting automated staging, timestamped commits, and remote repository synchronization via `subprocess`.
- **System I/O Operations** — Dynamic directory creation and file stream handling (`os`, `shutil`).