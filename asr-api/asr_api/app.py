import io
import os
import base64
import logging
import tempfile

import torch
import torchaudio
import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from fastapi.middleware.cors import CORSMiddleware


assert torch.cuda.is_available(), "CUDA is not available. Please check your PyTorch installation."

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

log = logging.getLogger(__name__)

log.info("Loading Faster-Whisper model...")
model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
log.info("Model loaded.")

# === FastAPI setup ===
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AudioRequest(BaseModel):
    audio_base64: str

@app.post("/transcribe")
async def transcribe_audio(request: AudioRequest) -> JSONResponse:
    try:
        log.info("Received transcription request")
        # Decode base64 into audio bytes and save temporarily
        audio_bytes = base64.b64decode(request.audio_base64)
        audio_np = decode_audio(io.BytesIO(audio_bytes))

        assert isinstance(audio_np, np.ndarray)
        segments, _ = model.transcribe(audio_np, language="pt")
        transcription = " ".join([segment.text for segment in segments])

        log.info(f"Transcription successful: {transcription}")
        return JSONResponse(content={"transcription": transcription})

    except Exception as e:
        log.exception("Transcription failed")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
