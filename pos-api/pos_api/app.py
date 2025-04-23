import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request) -> JSONResponse:
    return JSONResponse({
        "message": "Welcome to the API!"
    })


async def handle_post(request) -> JSONResponse:
    try:
        data = await request.json()
        # Process the data as needed
        return JSONResponse({
            "message": "Data received successfully",
            "data": data
        }, status_code=201)
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
]


app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)