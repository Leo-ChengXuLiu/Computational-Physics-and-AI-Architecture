"""
Audio stream processing and speech recognition module.

Captures microphone input, processes audio data in real time,
and converts speech to text using macOS-compatible recognition
backends via the SpeechRecognition library.
"""

import asyncio
import logging
from typing import Optional

import speech_recognition as sr

import config

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Real-time audio capture and speech-to-text pipeline.

    Audio is captured through the macOS Core Audio framework (via PyAudio)
    and recognised using OpenAI Whisper (local, offline) as the primary
    backend, with Google Web Speech API as a cloud-based fallback.
    """

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = config.RECOGNIZER_ENERGY_THRESHOLD
        self.recognizer.pause_threshold = config.RECOGNIZER_PAUSE_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True
        self.microphone: Optional[sr.Microphone] = None
        self._whisper_available: Optional[bool] = None

    def _ensure_microphone(self) -> sr.Microphone:
        """Lazily initialise the microphone so it can be mocked in tests."""
        if self.microphone is None:
            self.microphone = sr.Microphone(sample_rate=config.AUDIO_SAMPLE_RATE)
        return self.microphone

    def calibrate(self, duration: float = 1.0) -> None:
        """Adjust for ambient noise levels."""
        mic = self._ensure_microphone()
        with mic as source:
            logger.info("Calibrating for ambient noise (%.1f s)…", duration)
            self.recognizer.adjust_for_ambient_noise(source, duration=duration)
            logger.info(
                "Energy threshold set to %.1f", self.recognizer.energy_threshold
            )

    def _listen_blocking(self) -> Optional[str]:
        """Blocking call that captures and recognises one utterance."""
        mic = self._ensure_microphone()
        try:
            with mic as source:
                logger.debug("Listening…")
                audio = self.recognizer.listen(source)
        except OSError:
            logger.exception("Microphone access failed")
            return None

        # Attempt Whisper (local/offline) first, fall back to Google Web Speech
        for recognise, label in [
            (self._recognise_whisper, "Whisper (local)"),
            (self._recognise_google, "Google Web Speech"),
        ]:
            text = recognise(audio)
            if text is not None:
                logger.info("[%s] Recognised: %s", label, text)
                return text

        logger.warning("Speech not recognised by any backend")
        return None

    async def listen(self) -> Optional[str]:
        """Capture a single utterance asynchronously.

        Wraps the blocking microphone capture in an executor so the
        event loop remains responsive during audio I/O.
        """
        return await asyncio.to_thread(self._listen_blocking)

    # ------------------------------------------------------------------
    # Recognition back-ends
    # ------------------------------------------------------------------

    def _recognise_whisper(self, audio: sr.AudioData) -> Optional[str]:
        """Use OpenAI Whisper for local, offline speech recognition.

        Whisper runs entirely on-device, making it suitable for
        low-latency, privacy-preserving voice interaction on macOS.
        """
        if self._whisper_available is False:
            return None
        try:
            text = self.recognizer.recognize_whisper(
                audio, language=config.RECOGNIZER_LANGUAGE.split("-")[0]
            )
            self._whisper_available = True
            return text
        except sr.UnknownValueError:
            return None
        except (sr.RequestError, AttributeError, ImportError):
            logger.debug("Whisper unavailable; will use fallback")
            self._whisper_available = False
            return None

    def _recognise_google(self, audio: sr.AudioData) -> Optional[str]:
        """Fallback: Google Web Speech API (free tier, no key required)."""
        try:
            return self.recognizer.recognize_google(
                audio, language=config.RECOGNIZER_LANGUAGE
            )
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            logger.debug("Google Web Speech unavailable")
            return None
