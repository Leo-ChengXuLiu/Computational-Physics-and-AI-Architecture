"""
Unit tests for the ConversationContext and GeminiClient modules.

All external API calls are mocked so tests run without credentials.
"""

import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Ensure the project root is on sys.path
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

from gemini_client import ConversationContext, GeminiClient


# ── ConversationContext tests ───────────────────────────────────────────


class TestConversationContext:
    def test_add_user_message(self):
        ctx = ConversationContext(system_prompt="test", max_turns=5)
        ctx.add_user_message("hello")
        assert len(ctx.history) == 1
        assert ctx.history[0]["role"] == "user"
        assert ctx.history[0]["parts"] == ["hello"]

    def test_add_assistant_message(self):
        ctx = ConversationContext(system_prompt="test", max_turns=5)
        ctx.add_assistant_message("hi there")
        assert len(ctx.history) == 1
        assert ctx.history[0]["role"] == "model"

    def test_trim_keeps_recent_turns(self):
        ctx = ConversationContext(system_prompt="test", max_turns=2)
        for i in range(10):
            ctx.add_user_message(f"user-{i}")
            ctx.add_assistant_message(f"bot-{i}")
        # max_turns=2 → keep last 4 entries (2 turns × 2 messages each)
        assert len(ctx.history) == 4
        assert ctx.history[0]["parts"] == ["user-8"]

    def test_clear(self):
        ctx = ConversationContext(system_prompt="test", max_turns=5)
        ctx.add_user_message("hello")
        ctx.clear()
        assert len(ctx.history) == 0

    def test_get_history_returns_copy(self):
        ctx = ConversationContext(system_prompt="test", max_turns=5)
        ctx.add_user_message("hello")
        history = ctx.get_history()
        history.clear()
        assert len(ctx.history) == 1  # original unchanged


# ── GeminiClient tests ─────────────────────────────────────────────────


class TestGeminiClient:
    @patch("gemini_client.genai")
    def test_init_requires_api_key(self, mock_genai):
        with pytest.raises(ValueError, match="API key is required"):
            GeminiClient(api_key="")

    @patch("gemini_client.genai")
    def test_init_configures_model(self, mock_genai):
        client = GeminiClient(api_key="test-key", model_name="gemini-test")
        mock_genai.configure.assert_called_once_with(api_key="test-key")
        assert client.model_name == "gemini-test"

    @patch("gemini_client.genai")
    def test_reset_conversation_clears_context(self, mock_genai):
        client = GeminiClient(api_key="test-key")
        client.context.add_user_message("hi")
        client.reset_conversation()
        assert len(client.context.history) == 0

    @pytest.mark.asyncio
    @patch("gemini_client.genai")
    async def test_send_message_updates_context(self, mock_genai):
        client = GeminiClient(api_key="test-key")

        # Mock the chat response
        mock_response = MagicMock()
        mock_response.text = "Hello from Amadeus!"
        mock_chat = MagicMock()
        mock_chat.send_message.return_value = mock_response
        client.model.start_chat = MagicMock(return_value=mock_chat)

        reply = await client.send_message("Hi there")

        assert reply == "Hello from Amadeus!"
        assert len(client.context.history) == 2
        assert client.context.history[0]["role"] == "user"
        assert client.context.history[1]["role"] == "model"

    @pytest.mark.asyncio
    @patch("gemini_client.genai")
    async def test_send_message_rolls_back_on_error(self, mock_genai):
        client = GeminiClient(api_key="test-key")

        mock_chat = MagicMock()
        mock_chat.send_message.side_effect = RuntimeError("API error")
        client.model.start_chat = MagicMock(return_value=mock_chat)

        with pytest.raises(RuntimeError):
            await client.send_message("Hi")

        # Context should be empty — failed user message was rolled back
        assert len(client.context.history) == 0
