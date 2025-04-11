import base64
import io
import logging
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from openai import OpenAI

client = OpenAI(api_key="KEY")

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

log = logging.getLogger(__name__)

app = FastAPI()

class AudioRequest(BaseModel):
    audio_base64: str

@app.post("/transcribe")
async def transcribe_audio(request: AudioRequest):
    try:
        log.info("Received transcription request")

         # Decode base64 string into binary audio data
        audio_data = base64.b64decode(request.audio_base64)

        # Write to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name

        # Send to Whisper
        with open(temp_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )

        log.info(f"Transcription successful: {transcript.text}")
        return JSONResponse(content={"transcription": transcript.text})

    except Exception as e:
        log.exception("Transcription failed")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

