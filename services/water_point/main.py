from fastapi import FastAPI, Request
¢
from fastapi.responses import JSONResponse
from .api import router
from .store import WaterPointStore, WaterPointNotFound

def create_app(store=None):
    app = FastAPIOffline(title="Water Point Service API", version="1.0.0",
                  description="API for registering and monitoring community water points."
                  )
    app.state.store = store or WaterPointStore()
    @app.exception_handler(WaterPointNotFound)
    async def not_found(request: Request, exc: WaterPointNotFound):
        return JSONResponse(status_code=404, content={"detail": f"Water point {exc} not found"})
    app.include_router(router)
    return app

app = create_app()
