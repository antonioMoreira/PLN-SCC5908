import io

import torch
import numpy as np
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio

assert torch.cuda.is_available(), "CUDA is not available. Please check your PyTorch installation."

model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")

def get_transcription(audio_bytes:bytes) -> str:
    """
    Transcribe the audio bytes to text using OpenAI's Whisper API.
    """
    # Assuming you have a function `transcribe_audio` that handles the API call
    audio_np = decode_audio(io.BytesIO(audio_bytes))
    assert isinstance(audio_np, np.ndarray), "Audio data is not in the expected format."
    segments,_ = model.transcribe(audio_np, language='pt')
    transcription = " ".join([segment.text for segment in segments])
    return transcription

