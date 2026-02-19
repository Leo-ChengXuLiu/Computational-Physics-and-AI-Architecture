"""
Unit tests for the TTSEngine module.
"""

import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

from tts_engine import TTSEngine


class TestTTSEngine:
    @patch("tts_engine.shutil.which", return_value=None)
    @patch("tts_engine.platform.system", return_value="Linux")
    def test_falls_back_to_pyttsx_on_linux(self, mock_sys, mock_which):
        engine = TTSEngine()
        assert engine._use_native is False

    @patch("tts_engine.shutil.which", return_value="/usr/bin/say")
    @patch("tts_engine.platform.system", return_value="Darwin")
    def test_uses_native_on_macos(self, mock_sys, mock_which):
        engine = TTSEngine()
        assert engine._use_native is True

    @pytest.mark.asyncio
    @patch("tts_engine.shutil.which", return_value=None)
    @patch("tts_engine.platform.system", return_value="Linux")
    async def test_speak_empty_text_is_noop(self, mock_sys, mock_which):
        engine = TTSEngine()
        # Should return immediately without error
        await engine.speak("")

    @pytest.mark.asyncio
    @patch("tts_engine.shutil.which", return_value="/usr/bin/say")
    @patch("tts_engine.platform.system", return_value="Darwin")
    @patch("tts_engine.asyncio.create_subprocess_exec")
    async def test_speak_native_calls_say(self, mock_exec, mock_sys, mock_which):
        mock_proc = MagicMock()
        mock_proc.wait = AsyncMock()
        mock_exec.return_value = mock_proc

        engine = TTSEngine()
        await engine.speak("Hello world")

        mock_exec.assert_called_once()
        args = mock_exec.call_args[0]
        assert args[0] == "say"
        assert args[1] == "Hello world"
