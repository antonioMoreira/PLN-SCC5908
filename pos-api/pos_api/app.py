import uvicorn
from rich import print
from starlette.routing import Route
from starlette.requests import Request
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from .text_processing import get_pos_tags

async def homepage(request) -> JSONResponse:
    return JSONResponse({
        "message": "Welcome to the API!"
    })

async def handle_tagger(request:Request) -> JSONResponse:
    assert isinstance(request, Request)
    print(request)
    print(type(request))
    try:
        data = await request.json()
        assert isinstance(data, dict) and "sentence" in data
        tags = get_pos_tags(data["sentence"])
        return JSONResponse(tags, status_code=201)
    except Exception as e:
        return JSONResponse({
            "error": str(e)
        }, status_code=400)


async def health_check(request) -> JSONResponse:
    return JSONResponse({
        "status": "healthy"
    })


routes = [
    Route("/", endpoint=homepage),
    Route("/health", endpoint=health_check),
    Route("/tagger", endpoint=handle_tagger, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)