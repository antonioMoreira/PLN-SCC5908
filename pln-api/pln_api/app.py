import base64

import uvicorn
from rich import print
from starlette.routing import Route
from starlette.requests import Request
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from .text_processing import get_pos_tags
from .audio_processing import get_transcription


async def homepage(request) -> JSONResponse:
    return JSONResponse({
        "message": "Welcome to the API!"
    })


async def health_check(request) -> JSONResponse:
    return JSONResponse({
        "status": "healthy"
    })


async def handle_tagger(request:Request) -> JSONResponse:
    assert isinstance(request, Request)
    try:
        data = await request.json()
        assert isinstance(data, dict) and "sentence" in data
        tags = get_pos_tags(data["sentence"])
        return JSONResponse({'data':tags}, status_code=201)
    except Exception as e:
        return JSONResponse({
            "Error while tagging.": str(e)
        }, status_code=400)


async def handle_transcribe(request:Request) -> JSONResponse:
    assert isinstance(request, Request)
    try:
        data = await request.json()
        assert isinstance(data, dict) and "audio_base64" in data
        audio_bytes = base64.b64decode(request['audio_base64'])
        transcription = get_transcription(audio_bytes)
        return JSONResponse({"transcription": transcription}, status_code=201)
    except Exception as e:
        return JSONResponse({
            "Error while transcribing.": str(e)
        }, status_code=400)


routes = [
    Route("/", endpoint=homepage),
    Route("/health", endpoint=health_check),
    Route("/pln/tagger", endpoint=handle_tagger, methods=["POST"]),
    Route("/pln/transcribe", endpoint=handle_transcribe, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)