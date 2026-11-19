from fastapi_offline import FastAPIOffline
from .api import router

def create_app(store=None):
    app = FastAPIOffline(title="Community Payment Service API", version="1.0.0",
                  description="API for recording household water-point contributions.")
    if store is None:
        from .store import PaymentStore
        store = PaymentStore()
    app.state.store = store
    app.include_router(router)
    return app

app = create_app()
