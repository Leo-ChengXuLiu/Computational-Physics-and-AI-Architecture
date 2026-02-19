"""
Configuration module for Project Amadeus Voice-Interactive AI.

Manages API keys, audio parameters, and application settings
through environment variables and sensible defaults.
"""

import os


# Gemini API Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_MAX_OUTPUT_TOKENS = int(os.environ.get("GEMINI_MAX_OUTPUT_TOKENS", "1024"))
GEMINI_TEMPERATURE = float(os.environ.get("GEMINI_TEMPERATURE", "0.7"))

# Audio Configuration
AUDIO_SAMPLE_RATE = int(os.environ.get("AUDIO_SAMPLE_RATE", "16000"))
AUDIO_CHANNELS = 1
AUDIO_CHUNK_DURATION_SEC = float(os.environ.get("AUDIO_CHUNK_DURATION_SEC", "0.5"))
SILENCE_THRESHOLD = float(os.environ.get("SILENCE_THRESHOLD", "500"))
SILENCE_TIMEOUT_SEC = float(os.environ.get("SILENCE_TIMEOUT_SEC", "2.0"))

# Speech Recognition Configuration
RECOGNIZER_ENERGY_THRESHOLD = int(
    os.environ.get("RECOGNIZER_ENERGY_THRESHOLD", "300")
)
RECOGNIZER_PAUSE_THRESHOLD = float(
    os.environ.get("RECOGNIZER_PAUSE_THRESHOLD", "1.0")
)
RECOGNIZER_LANGUAGE = os.environ.get("RECOGNIZER_LANGUAGE", "en-US")

# TTS Configuration
TTS_RATE = int(os.environ.get("TTS_RATE", "185"))
TTS_VOLUME = float(os.environ.get("TTS_VOLUME", "0.9"))

# Conversation Context
MAX_CONTEXT_TURNS = int(os.environ.get("MAX_CONTEXT_TURNS", "20"))
SYSTEM_PROMPT = os.environ.get(
    "SYSTEM_PROMPT",
    (
        "You are Amadeus, a friendly and knowledgeable voice assistant. "
        "Keep responses concise and conversational since they will be spoken aloud. "
        "Aim for 2-3 sentences unless the user asks for detailed information."
    ),
)

# Application Settings
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
WAKE_WORD = os.environ.get("WAKE_WORD", "").lower()
EXIT_PHRASES = {"goodbye", "exit", "quit", "stop", "bye"}
