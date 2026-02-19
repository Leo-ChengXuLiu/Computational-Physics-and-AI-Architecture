"""
Unit tests for the VoiceAssistant orchestrator.
"""

import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)


class TestVoiceAssistant:
    @patch("voice_assistant.TTSEngine")
    @patch("voice_assistant.GeminiClient")
    @patch("voice_assistant.AudioProcessor")
    def test_stop_sets_running_false(self, mock_audio, mock_gemini, mock_tts):
        from voice_assistant import VoiceAssistant

        assistant = VoiceAssistant()
        assistant._running = True
        assistant.stop()
        assert assistant._running is False

    @pytest.mark.asyncio
    @patch("voice_assistant.TTSEngine")
    @patch("voice_assistant.GeminiClient")
    @patch("voice_assistant.AudioProcessor")
    async def test_interaction_turn_skips_on_none(
        self, mock_audio_cls, mock_gemini_cls, mock_tts_cls
    ):
        from voice_assistant import VoiceAssistant

        assistant = VoiceAssistant()
        assistant.audio.listen = AsyncMock(return_value=None)
        assistant.gemini.send_message = AsyncMock()

        await assistant._interaction_turn()

        # Gemini should NOT have been called
        assistant.gemini.send_message.assert_not_called()

    @pytest.mark.asyncio
    @patch("voice_assistant.TTSEngine")
    @patch("voice_assistant.GeminiClient")
    @patch("voice_assistant.AudioProcessor")
    async def test_interaction_turn_exits_on_goodbye(
        self, mock_audio_cls, mock_gemini_cls, mock_tts_cls
    ):
        from voice_assistant import VoiceAssistant

        assistant = VoiceAssistant()
        assistant.audio.listen = AsyncMock(return_value="goodbye")
        assistant.tts.speak = AsyncMock()

        assistant._running = True
        await assistant._interaction_turn()

        assert assistant._running is False
        assistant.tts.speak.assert_called_once()

    @pytest.mark.asyncio
    @patch("voice_assistant.TTSEngine")
    @patch("voice_assistant.GeminiClient")
    @patch("voice_assistant.AudioProcessor")
    async def test_interaction_turn_sends_to_gemini(
        self, mock_audio_cls, mock_gemini_cls, mock_tts_cls
    ):
        from voice_assistant import VoiceAssistant

        assistant = VoiceAssistant()
        assistant.audio.listen = AsyncMock(return_value="What is the weather?")
        assistant.gemini.send_message = AsyncMock(return_value="It's sunny!")
        assistant.tts.speak = AsyncMock()

        await assistant._interaction_turn()

        assistant.gemini.send_message.assert_called_once_with("What is the weather?")
        assistant.tts.speak.assert_called_once_with("It's sunny!")
