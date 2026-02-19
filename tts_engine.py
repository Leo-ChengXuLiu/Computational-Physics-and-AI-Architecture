"""
Text-to-Speech engine for spoken response output.

Provides an asynchronous interface to the macOS ``say`` command and
a cross-platform fallback using the ``pyttsx3`` library.
"""

import asyncio
import logging
import platform
import shutil
from typing import Optional

import config

logger = logging.getLogger(__name__)


class TTSEngine:
    """Produce audible speech from text responses.

    On macOS the native ``say`` command is preferred for natural-sounding
    output; on other platforms ``pyttsx3`` is used as a fallback.
    """

    def __init__(self) -> None:
        self._use_native = platform.system() == "Darwin" and bool(shutil.which("say"))
        self._pyttsx_engine: Optional[object] = None

        if self._use_native:
            logger.info("TTS: using macOS native 'say' command")
        else:
            logger.info("TTS: using pyttsx3 fallback engine")

    def _get_pyttsx_engine(self):
        """Lazily initialise the pyttsx3 engine."""
        if self._pyttsx_engine is None:
            import pyttsx3

            engine = pyttsx3.init()
            engine.setProperty("rate", config.TTS_RATE)
            engine.setProperty("volume", config.TTS_VOLUME)
            self._pyttsx_engine = engine
        return self._pyttsx_engine

    async def speak(self, text: str) -> None:
        """Speak the given text aloud, asynchronously."""
        if not text:
            return
        logger.debug("Speaking: %s", text[:80])
        if self._use_native:
            await self._speak_native(text)
        else:
            await asyncio.to_thread(self._speak_pyttsx, text)

    async def _speak_native(self, text: str) -> None:
        """Use macOS ``say`` command via an async subprocess."""
        proc = await asyncio.create_subprocess_exec(
            "say",
            text,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()

    def _speak_pyttsx(self, text: str) -> None:
        """Blocking pyttsx3 speech synthesis."""
        engine = self._get_pyttsx_engine()
        engine.say(text)
        engine.runAndWait()
