"""
Gemini API client with context-aware conversation management.

Handles API integration, request/response lifecycle, conversation
history tracking, and context-window management for multi-turn dialogue.
"""

import asyncio
import logging
import time
from typing import Optional

import google.generativeai as genai

import config

logger = logging.getLogger(__name__)


class ConversationContext:
    """Manages multi-turn conversation history with a sliding window."""

    def __init__(self, system_prompt: str, max_turns: int):
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.history: list[dict[str, str]] = []

    def add_user_message(self, text: str) -> None:
        """Record a user utterance in the conversation history."""
        self.history.append({"role": "user", "parts": [text]})
        self._trim()

    def add_assistant_message(self, text: str) -> None:
        """Record an assistant response in the conversation history."""
        self.history.append({"role": "model", "parts": [text]})
        self._trim()

    def get_history(self) -> list[dict[str, str]]:
        """Return the current conversation history."""
        return list(self.history)

    def clear(self) -> None:
        """Reset the conversation history."""
        self.history.clear()

    def _trim(self) -> None:
        """Keep only the most recent turns within the configured window."""
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2) :]


class GeminiClient:
    """Async wrapper around the Gemini generative AI API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model_name = model_name or config.GEMINI_MODEL

        if not self.api_key:
            raise ValueError(
                "Gemini API key is required. Set the GEMINI_API_KEY "
                "environment variable or pass it directly."
            )

        genai.configure(api_key=self.api_key)

        generation_config = genai.types.GenerationConfig(
            max_output_tokens=config.GEMINI_MAX_OUTPUT_TOKENS,
            temperature=config.GEMINI_TEMPERATURE,
        )

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            system_instruction=config.SYSTEM_PROMPT,
        )

        self.context = ConversationContext(
            system_prompt=config.SYSTEM_PROMPT,
            max_turns=config.MAX_CONTEXT_TURNS,
        )

        logger.info("GeminiClient initialised with model: %s", self.model_name)

    async def send_message(self, user_text: str) -> str:
        """Send a user message and return the model's response.

        Manages conversation context and handles API latency by running
        the blocking API call in a thread-pool executor.
        """
        self.context.add_user_message(user_text)

        start = time.monotonic()
        try:
            chat = self.model.start_chat(history=self.context.get_history()[:-1])
            response = await asyncio.to_thread(chat.send_message, user_text)
            reply = response.text.strip()
        except Exception:
            logger.exception("Gemini API request failed")
            self.context.history.pop()  # remove the failed user message
            raise

        elapsed = time.monotonic() - start
        logger.info("Gemini responded in %.2f s", elapsed)

        self.context.add_assistant_message(reply)
        return reply

    def reset_conversation(self) -> None:
        """Clear conversation context to start fresh."""
        self.context.clear()
        logger.info("Conversation context cleared")
