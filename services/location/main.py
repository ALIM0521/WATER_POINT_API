from fastapi_offline import FastAPIOffline
from .api import router
from .store import LocationStore

def create_app(store=None):
    app = FastAPIOffline(title="Location Service API", version="1.0.0",
                  description="API for administrative geography and coordinates.")
    app.state.store = store or LocationStore()
    app.include_router(router)
    return app

app = create_app()
