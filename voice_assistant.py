"""
Project Amadeus — Voice-Interactive Conversational AI

Main orchestrator that ties together audio capture, speech recognition,
the Gemini language model, and text-to-speech output into a seamless,
hands-free voice interaction loop.

Usage
-----
    export GEMINI_API_KEY="your-key-here"
    python voice_assistant.py
"""

import asyncio
import logging
import signal
import sys

import config
from audio_processor import AudioProcessor
from gemini_client import GeminiClient
from tts_engine import TTSEngine

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


class VoiceAssistant:
    """End-to-end voice interaction loop.

    Pipeline:  Microphone → Speech Recognition → Gemini API → TTS
    """

    def __init__(self) -> None:
        self.audio = AudioProcessor()
        self.gemini = GeminiClient()
        self.tts = TTSEngine()
        self._running = False

    async def run(self) -> None:
        """Start the main interaction loop."""
        self._running = True
        logger.info("Amadeus is starting up…")
        print("\n✨ Amadeus Voice Assistant is ready!")
        print("   Speak naturally — say 'goodbye' to exit.\n")

        # Calibrate microphone for ambient noise
        self.audio.calibrate()

        while self._running:
            await self._interaction_turn()

        logger.info("Amadeus has shut down.")

    async def _interaction_turn(self) -> None:
        """Execute one listen → think → speak cycle."""
        # 1. Listen
        user_text = await self.audio.listen()
        if user_text is None:
            return

        print(f"🎤  You: {user_text}")

        # 2. Check for exit command
        if user_text.strip().lower() in config.EXIT_PHRASES:
            farewell = "Goodbye! It was nice talking to you."
            print(f"🤖  Amadeus: {farewell}")
            await self.tts.speak(farewell)
            self.stop()
            return

        # 3. Optional wake-word gate
        if config.WAKE_WORD and not user_text.lower().startswith(config.WAKE_WORD):
            logger.debug("Wake word not detected; ignoring utterance")
            return

        # 4. Get response from Gemini
        try:
            reply = await self.gemini.send_message(user_text)
        except Exception:
            reply = "I'm sorry, I had trouble processing that. Could you try again?"
            logger.exception("Failed to get Gemini response")

        print(f"🤖  Amadeus: {reply}")

        # 5. Speak the response
        await self.tts.speak(reply)

    def stop(self) -> None:
        """Signal the interaction loop to stop."""
        self._running = False


def main() -> None:
    """Entry point for the voice assistant."""
    assistant = VoiceAssistant()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Graceful shutdown on Ctrl-C
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, assistant.stop)

    try:
        loop.run_until_complete(assistant.run())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        loop.close()


if __name__ == "__main__":
    main()
