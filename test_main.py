import pytest
from main import AUDIO_FORMATS, INPUT_FORMATS

# Only import AudioSegment for the conversion test
from pydub import AudioSegment
import os

def test_audio_formats():
    assert set(AUDIO_FORMATS) == {'mp3', 'wav', 'ogg', 'flac'}

def test_input_formats():
    assert INPUT_FORMATS[0] == 'All'
    for fmt in AUDIO_FORMATS:
        assert fmt in INPUT_FORMATS

def test_audio_conversion(tmp_path):
    # Create a short silent wav file and convert to mp3
    wav_path = tmp_path / 'test.wav'
    mp3_path = tmp_path / 'test.mp3'
    seg = AudioSegment.silent(duration=1000)  # 1 second
    seg.export(wav_path, format='wav')
    # Now read and convert to mp3
    audio = AudioSegment.from_file(wav_path)
    audio.export(mp3_path, format='mp3')
    assert mp3_path.exists() and mp3_path.stat().st_size > 0 