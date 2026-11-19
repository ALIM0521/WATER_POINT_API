from fastapi_offline import FastAPIOffline
from .api import router

def create_app(store=None):
    app = FastAPIOffline(title="Maintenance Ticket Service API", version="1.0.0",
                  description="API for reporting water-point faults and tracking repairs.")
    if store is None:
        from .store import TicketStore
        store = TicketStore()
    app.state.store = store
    app.include_router(router)
    return app

app = create_app()
