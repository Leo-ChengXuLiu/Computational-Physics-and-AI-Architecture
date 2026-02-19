"""
Unit tests for the AudioProcessor module.

Microphone hardware is fully mocked so tests can run headlessly.
"""

import sys
import os
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

import speech_recognition as sr
from audio_processor import AudioProcessor


class TestAudioProcessor:
    def test_init_sets_thresholds(self):
        proc = AudioProcessor()
        assert proc.recognizer.dynamic_energy_threshold is True
        assert proc.microphone is None

    @patch("audio_processor.sr.Microphone")
    def test_calibrate_adjusts_noise(self, mock_mic_cls):
        mock_mic = MagicMock()
        mock_mic.__enter__ = MagicMock(return_value=mock_mic)
        mock_mic.__exit__ = MagicMock(return_value=False)
        mock_mic_cls.return_value = mock_mic

        proc = AudioProcessor()
        proc.recognizer.adjust_for_ambient_noise = MagicMock()
        proc.calibrate(duration=0.5)

        proc.recognizer.adjust_for_ambient_noise.assert_called_once()

    def test_recognise_whisper_returns_none_on_unknown(self):
        proc = AudioProcessor()
        proc.recognizer.recognize_whisper = MagicMock(
            side_effect=sr.UnknownValueError()
        )
        audio_data = MagicMock(spec=sr.AudioData)
        result = proc._recognise_whisper(audio_data)
        assert result is None

    def test_recognise_google_returns_none_on_request_error(self):
        proc = AudioProcessor()
        proc.recognizer.recognize_google = MagicMock(
            side_effect=sr.RequestError("unavailable")
        )
        audio_data = MagicMock(spec=sr.AudioData)
        result = proc._recognise_google(audio_data)
        assert result is None

    def test_recognise_whisper_returns_text(self):
        proc = AudioProcessor()
        proc.recognizer.recognize_whisper = MagicMock(return_value="hello world")
        audio_data = MagicMock(spec=sr.AudioData)
        result = proc._recognise_whisper(audio_data)
        assert result == "hello world"

    @pytest.mark.asyncio
    @patch("audio_processor.sr.Microphone")
    async def test_listen_returns_recognised_text(self, mock_mic_cls):
        mock_mic = MagicMock()
        mock_mic.__enter__ = MagicMock(return_value=mock_mic)
        mock_mic.__exit__ = MagicMock(return_value=False)
        mock_mic_cls.return_value = mock_mic

        proc = AudioProcessor()
        proc.microphone = mock_mic

        mock_audio = MagicMock(spec=sr.AudioData)
        proc.recognizer.listen = MagicMock(return_value=mock_audio)
        proc.recognizer.recognize_google = MagicMock(return_value="test phrase")

        result = await proc.listen()
        assert result == "test phrase"
