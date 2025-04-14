import base64
import io
import logging
import os
import tempfile

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

import torchaudio
from faster_whisper import WhisperModel

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

log = logging.getLogger(__name__)

log.info("Loading Faster-Whisper model...")
model = WhisperModel("tiny", device="cuda", compute_type="float16")
log.info("Model loaded.")

# === FastAPI setup ===
app = FastAPI()

class AudioRequest(BaseModel):
    audio_base64: str

@app.post("/transcribe")
async def transcribe_audio(request: AudioRequest):
    try:
        log.info("Received transcription request")

        # Decode base64 into audio bytes and save temporarily
        audio_bytes = base64.b64decode(request.audio_base64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        # Load audio and resample to 16kHz
        waveform, sr = torchaudio.load(tmp_path)
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
            waveform = resampler(waveform)
        # Convert to mono if stereo
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        # Save the processed audio to a temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_tmp:
            torchaudio.save(wav_tmp.name, waveform, 16000)
            wav_path = wav_tmp.name

        # Transcribe using Faster-Whisper
        segments, _ = model.transcribe(wav_path, language="pt")
        transcription = " ".join([segment.text for segment in segments])

        log.info(f"Transcription successful: {transcription}")
        return JSONResponse(content={"transcription": transcription})

    except Exception as e:
        log.exception("Transcription failed")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
