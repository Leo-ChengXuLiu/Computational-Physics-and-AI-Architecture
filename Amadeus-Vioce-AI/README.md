# 🎙️ Project Amadeus — Voice-Interactive Conversational AI

A real-time, multimodal AI assistant that enables hands-free voice interaction
through the Gemini API and macOS native speech recognition.

## Architecture

```
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌────────────┐
│  Microphone │───▶│ AudioProcessor   │───▶│ GeminiClient │───▶│ TTSEngine  │
│  (PyAudio)  │    │ (SpeechRecog.)   │    │ (Gemini API) │    │(say/pyttsx)│
└─────────────┘    └──────────────────┘    └──────────────┘    └────────────┘
                         │                        │
                         ▼                        ▼
                   Speech-to-Text          Context-Aware NLG
```

**Pipeline:**  Microphone → Speech Recognition → Gemini API → Text-to-Speech

## Modules

| Module | Purpose |
|---|---|
| `voice_assistant.py` | Main orchestrator — ties the full pipeline together |
| `gemini_client.py` | Gemini API integration with multi-turn context management |
| `audio_processor.py` | Real-time audio capture and speech-to-text pipeline |
| `tts_engine.py` | Text-to-speech output (macOS native + cross-platform fallback) |
| `config.py` | Centralised configuration via environment variables |

## Prerequisites

- **Python 3.10+**
- **macOS** (recommended) for native speech recognition and TTS
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
- PortAudio system library for microphone access

## Setup

```bash
# 1. Install PortAudio (macOS)
brew install portaudio

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set your Gemini API key
export GEMINI_API_KEY="your-api-key-here"

# 4. Run the assistant
python voice_assistant.py
```

## Configuration

All settings are configurable via environment variables:

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *(required)* | Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model to use |
| `GEMINI_TEMPERATURE` | `0.7` | Response creativity (0.0–1.0) |
| `AUDIO_SAMPLE_RATE` | `16000` | Microphone sample rate (Hz) |
| `TTS_RATE` | `185` | Speech output rate (words/min) |
| `WAKE_WORD` | *(empty)* | Optional wake word to filter utterances |
| `MAX_CONTEXT_TURNS` | `20` | Conversation turns to retain |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

## Running Tests

```bash
cd Project-Amadeus-Voice-AI
pip install -r requirements.txt pytest pytest-asyncio
python -m pytest tests/ -v
```

## Skills Demonstrated

- **API Integration** — Gemini API client with async request handling
- **Audio Stream Processing** — Real-time microphone capture and speech recognition
- **Asynchronous Programming** — Full `asyncio` pipeline keeping the event loop responsive
- **Multimodal AI Engineering** — Voice-in, text-processing, voice-out interaction loop
