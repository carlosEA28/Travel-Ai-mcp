import contextlib
from fastapi import FastAPI

from flight_server import flight_mcp
from weather_server import weather_mcp

from fastapi.middleware.cors import CORSMiddleware


# lifespan significa eventos que rodam durate a ainicialização e encerramento do app
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(weather_mcp.session_manager.run())
        await stack.enter_async_context(flight_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/weather", weather_mcp.streamable_http_app())
app.mount("/flight", flight_mcp.streamable_http_app())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:4321"] se quiser limitar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
